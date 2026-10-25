#!/bin/bash
# Compile/link an unsigned arm64 iOS app; no signing, deployment or restart.
set -euo pipefail
test "$(id -u)" != 0
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
export LANG=en_US.UTF-8
mkdir -p "$HOME/Developer"
run=$(mktemp -d "$HOME/Developer/IOSDevSmoke.XXXXXXXX")
exec > >(tee "$run/verification.log") 2>&1
echo "IOS_SMOKE_DIRECTORY $run"
xcodebuild -version
xcodebuild -showsdks
xcrun --sdk iphoneos --show-sdk-version
mkdir "$run/DevSmoke.xcodeproj"
cat > "$run/DevSmokeApp.swift" <<'SWIFT'
import SwiftUI

@main
struct DevSmokeApp: App {
    var body: some Scene {
        WindowGroup {
            Text("Developer environment ready")
                .padding()
        }
    }
}
SWIFT
cat > "$run/DevSmoke.xcodeproj/project.pbxproj" <<'PROJECT'
// !$*UTF8*$!
{
 archiveVersion = 1;
 classes = {};
 objectVersion = 56;
 objects = {
  A00000000000000000000001 = {isa = PBXProject; buildConfigurationList = A00000000000000000000002; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; knownRegions = (en, Base); mainGroup = A00000000000000000000003; productRefGroup = A00000000000000000000004; projectDirPath = ""; projectRoot = ""; targets = (A00000000000000000000005); };
  A00000000000000000000002 = {isa = XCConfigurationList; buildConfigurations = (A00000000000000000000006); defaultConfigurationIsVisible = 0; defaultConfigurationName = Debug; };
  A00000000000000000000003 = {isa = PBXGroup; children = (A00000000000000000000007, A00000000000000000000004); sourceTree = "<group>"; };
  A00000000000000000000004 = {isa = PBXGroup; children = (A00000000000000000000008); name = Products; sourceTree = "<group>"; };
  A00000000000000000000005 = {isa = PBXNativeTarget; buildConfigurationList = A00000000000000000000009; buildPhases = (A0000000000000000000000A, A0000000000000000000000B, A0000000000000000000000C); buildRules = (); dependencies = (); name = DevSmoke; productName = DevSmoke; productReference = A00000000000000000000008; productType = "com.apple.product-type.application"; };
  A00000000000000000000006 = {isa = XCBuildConfiguration; buildSettings = {CLANG_ENABLE_MODULES = YES; SDKROOT = iphoneos; }; name = Debug; };
  A00000000000000000000007 = {isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = DevSmokeApp.swift; sourceTree = "<group>"; };
  A00000000000000000000008 = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = DevSmoke.app; sourceTree = BUILT_PRODUCTS_DIR; };
  A00000000000000000000009 = {isa = XCConfigurationList; buildConfigurations = (A0000000000000000000000D); defaultConfigurationIsVisible = 0; defaultConfigurationName = Debug; };
  A0000000000000000000000A = {isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = (A0000000000000000000000E); runOnlyForDeploymentPostprocessing = 0; };
  A0000000000000000000000B = {isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A0000000000000000000000C = {isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0; };
  A0000000000000000000000D = {isa = XCBuildConfiguration; buildSettings = {CODE_SIGNING_ALLOWED = NO; GENERATE_INFOPLIST_FILE = YES; INFOPLIST_KEY_UILaunchScreen_Generation = YES; INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES; IPHONEOS_DEPLOYMENT_TARGET = 15.0; PRODUCT_BUNDLE_IDENTIFIER = org.example.HVDevSmoke; PRODUCT_NAME = "$(TARGET_NAME)"; SDKROOT = iphoneos; SUPPORTED_PLATFORMS = "iphoneos iphonesimulator"; SWIFT_VERSION = 5.0; TARGETED_DEVICE_FAMILY = "1,2"; }; name = Debug; };
  A0000000000000000000000E = {isa = PBXBuildFile; fileRef = A00000000000000000000007; };
 };
 rootObject = A00000000000000000000001;
}
PROJECT
if ! xcodebuild -project "$run/DevSmoke.xcodeproj" -target DevSmoke \
  -configuration Debug -sdk iphoneos -arch arm64 \
  SYMROOT="$run/build" OBJROOT="$run/obj" CODE_SIGNING_ALLOWED=NO build \
  > "$run/build.log" 2>&1; then
  tail -n 45 "$run/build.log"
  echo 'IOS_SMOKE_BUILD_FAILED; preserve this directory for diagnosis.'
  exit 1
fi
app="$run/build/Debug-iphoneos/DevSmoke.app"
test -f "$app/DevSmoke"
file "$app/DevSmoke"
test "$(xcrun lipo -archs "$app/DevSmoke")" = arm64
/usr/libexec/PlistBuddy -c 'Print :MinimumOSVersion' "$app/Info.plist"
shasum -a 256 "$app/DevSmoke"
tail -n 5 "$run/build.log"
echo 'IOS_ARM64_BUILD_VERIFIED_UNSIGNED'
echo 'Device execution, signing and Simulator runtime are separate tests.'
