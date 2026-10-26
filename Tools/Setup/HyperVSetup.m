// Integrated first-login setup. No credential collection or security-policy edits.
#import <Cocoa/Cocoa.h>
#import <CoreGraphics/CoreGraphics.h>
#include <unistd.h>

static NSString *const Support = @"/Library/Application Support/MacHyperVSetup";
static NSString *const FramebufferUUID = @"3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6";

static BOOL FramebufferLoaded(void) {
  NSTask *task = [[NSTask alloc] init];
  task.launchPath = @"/usr/sbin/kextstat";
  task.arguments = @[@"-b", @"fish.goldfish64.MacHyperVFramebuffer"];
  NSPipe *pipe = [NSPipe pipe];
  task.standardOutput = pipe;
  task.standardError = [NSFileHandle fileHandleWithNullDevice];
  @try { [task launch]; } @catch (NSException *e) { return NO; }
  NSData *data = [[pipe fileHandleForReading] readDataToEndOfFile];
  [task waitUntilExit];
  NSString *text = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
  return task.terminationStatus == 0 && [text containsString:FramebufferUUID];
}

static BOOL ApplyDisplay(void) {
  CGDirectDisplayID display = CGMainDisplayID();
  if (!display) return NO;
  if (CGDisplayPixelsWide(display) == 1920 && CGDisplayPixelsHigh(display) == 1080) return YES;
  NSDictionary *options = @{(__bridge NSString *)kCGDisplayShowDuplicateLowResolutionModes: @YES};
  CFArrayRef modes = CGDisplayCopyAllDisplayModes(display, (__bridge CFDictionaryRef)options);
  if (!modes) return NO;
  BOOL applied = NO;
  for (CFIndex i = 0; i < CFArrayGetCount(modes); ++i) {
    CGDisplayModeRef mode = (CGDisplayModeRef)CFArrayGetValueAtIndex(modes, i);
    if (CGDisplayModeGetWidth(mode) == 1920 && CGDisplayModeGetHeight(mode) == 1080 &&
        CGDisplayModeGetPixelWidth(mode) == 1920 && CGDisplayModeGetPixelHeight(mode) == 1080) {
      applied = CGDisplaySetDisplayMode(display, mode, NULL) == kCGErrorSuccess;
      break;
    }
  }
  CFRelease(modes);
  return applied && CGDisplayPixelsWide(display) == 1920 && CGDisplayPixelsHigh(display) == 1080;
}

@interface SetupDelegate : NSObject <NSApplicationDelegate>
@property(nonatomic, strong) NSWindow *window;
@property(nonatomic, strong) NSTextField *message;
@property(nonatomic, strong) NSButton *approve;
@property(nonatomic, strong) NSProgressIndicator *progress;
@property(nonatomic, strong) NSTimer *timer;
@property NSInteger attempts;
@property BOOL finished;
@end

@implementation SetupDelegate
- (void)applicationDidFinishLaunching:(NSNotification *)notification {
  self.window = [[NSWindow alloc] initWithContentRect:NSMakeRect(0, 0, 560, 260)
      styleMask:NSWindowStyleMaskTitled backing:NSBackingStoreBuffered defer:NO];
  self.window.title = @"Hyper-V setup";
  [self.window center];
  NSTextField *title = [NSTextField labelWithString:@"Finishing your Mac setup"];
  title.font = [NSFont boldSystemFontOfSize:23];
  title.frame = NSMakeRect(28, 194, 510, 35);
  [self.window.contentView addSubview:title];
  self.message = [NSTextField wrappingLabelWithString:@"Preparing Hyper-V support…"];
  self.message.frame = NSMakeRect(28, 86, 500, 95);
  [self.window.contentView addSubview:self.message];
  self.progress = [[NSProgressIndicator alloc] initWithFrame:NSMakeRect(28, 57, 500, 18)];
  self.progress.indeterminate = YES;
  [self.progress startAnimation:nil];
  [self.window.contentView addSubview:self.progress];
  self.approve = [NSButton buttonWithTitle:@"Open macOS approval" target:self action:@selector(openApproval:)];
  self.approve.frame = NSMakeRect(306, 15, 225, 32);
  self.approve.hidden = YES;
  [self.window.contentView addSubview:self.approve];
  self.timer = [NSTimer scheduledTimerWithTimeInterval:2 target:self selector:@selector(update:)
      userInfo:nil repeats:YES];
  [self update:nil];
}
- (void)openApproval:(id)sender {
  [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:
      @"x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension"]];
}
- (void)update:(NSTimer *)timer {
  if (self.finished) return;
  // Never interrupt the user's Apple account / initial Setup Assistant session.
  if ([[NSRunningApplication runningApplicationsWithBundleIdentifier:@"com.apple.SetupAssistant"] count]) {
    [self.window orderOut:nil];
    return;
  }
  if (!self.window.visible) [self.window makeKeyAndOrderFront:nil];
  if (FramebufferLoaded()) {
    if (ApplyDisplay()) {
      self.finished = YES;
      [[NSUserDefaults standardUserDefaults] setBool:YES forKey:@"SetupComplete"];
      [self.progress stopAnimation:nil];
      self.approve.hidden = YES;
      self.message.stringValue = @"Setup complete. Your display is ready at 1920 × 1080.";
      [self.timer invalidate];
      [NSTimer scheduledTimerWithTimeInterval:8 repeats:NO block:^(NSTimer *t) { [NSApp terminate:nil]; }];
      return;
    }
    if (++self.attempts > 60) {
      self.message.stringValue = @"The display could not switch to 1920 × 1080. The setup log is available in /Library/Application Support/MacHyperVSetup.";
      [self.progress stopAnimation:nil];
    } else self.message.stringValue = @"Configuring your display…";
    return;
  }
  NSString *state = [NSString stringWithContentsOfFile:[Support stringByAppendingPathComponent:@"status.txt"]
      encoding:NSUTF8StringEncoding error:nil];
  state = [state stringByTrimmingCharactersInSet:NSCharacterSet.whitespaceAndNewlineCharacterSet];
  self.approve.hidden = ![state isEqualToString:@"awaiting-approval"];
  if ([state isEqualToString:@"awaiting-approval"]) {
    self.message.stringValue = @"macOS needs to approve the display extension. Click Allow in Privacy & Security, then use the Restart button there. Setup continues automatically after sign-in.";
    [self.progress stopAnimation:nil];
  } else if ([state isEqualToString:@"failed"]) {
    self.message.stringValue = @"Setup needs attention. The diagnostic log is in /Library/Application Support/MacHyperVSetup/setup.log.";
    [self.progress stopAnimation:nil];
  } else if ([state isEqualToString:@"installing-kdk"]) {
    self.message.stringValue = @"Preparing the Apple components needed for your display driver…";
  } else if ([state isEqualToString:@"installing-framebuffer"]) {
    self.message.stringValue = @"Installing Hyper-V display support…";
  } else self.message.stringValue = @"Waiting for macOS to finish preparing the system…";
}
@end

int main(int argc, const char **argv) {
  @autoreleasepool {
    if (argc == 2 && !strcmp(argv[1], "--help")) {
      puts("MacHyperVSetup: integrated first-login display setup; --set-display, --verify-display");
      return 0;
    }
    if (argc == 2 && !strcmp(argv[1], "--verify-display")) {
      CGDirectDisplayID d = CGMainDisplayID();
      printf("{\"width\":%zu,\"height\":%zu}\n", CGDisplayPixelsWide(d), CGDisplayPixelsHigh(d));
      return CGDisplayPixelsWide(d) == 1920 && CGDisplayPixelsHigh(d) == 1080 ? 0 : 1;
    }
    if (argc == 2 && !strcmp(argv[1], "--set-display")) return FramebufferLoaded() && ApplyDisplay() ? 0 : 1;
    if (getuid() < 501 || [[NSUserDefaults standardUserDefaults] boolForKey:@"SetupComplete"]) return 0;
    NSApplication *application = NSApplication.sharedApplication;
    static SetupDelegate *delegate;
    delegate = [[SetupDelegate alloc] init];
    application.delegate = delegate;
    [application run];
  }
  return 0;
}
