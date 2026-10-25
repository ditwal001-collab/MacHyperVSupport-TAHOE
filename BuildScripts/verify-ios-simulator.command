#!/bin/bash
# Run the existing smoke project on one already booted local iOS Simulator.
set -euo pipefail
project=${1:?Pass the existing IOSDevSmoke project directory}
case "$project" in "$HOME"/Developer/IOSDevSmoke.*) ;; *) exit 2 ;; esac
test -f "$project/DevSmoke.xcodeproj/project.pbxproj"
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
export LANG=en_US.UTF-8
run=$(mktemp -d "$project/SimulatorCheck.XXXXXXXX")
exec > >(tee "$run/verification.log") 2>&1
echo "SIMULATOR_CHECK_DIRECTORY $run"
xcodebuild -version
xcrun simctl list runtimes
xcrun simctl list devices booted
if ! xcodebuild -project "$project/DevSmoke.xcodeproj" -target DevSmoke \
  -configuration Debug -sdk iphonesimulator -arch x86_64 \
  SYMROOT="$run/build" OBJROOT="$run/obj" CODE_SIGNING_ALLOWED=NO build \
  > "$run/build.log" 2>&1; then
  tail -n 40 "$run/build.log"
  exit 1
fi
app="$run/build/Debug-iphonesimulator/DevSmoke.app"
file "$app/DevSmoke"
test "$(xcrun lipo -archs "$app/DevSmoke")" = x86_64
xcrun simctl install booted "$app"
xcrun simctl launch booted org.example.HVDevSmoke
sleep 3
xcrun simctl io booted screenshot "$run/simulator.png"
shasum -a 256 "$app/DevSmoke" "$run/simulator.png"
tail -n 5 "$run/build.log"
echo 'IOS_SIMULATOR_APP_LAUNCHED; inspect the screenshot to verify UI rendering.'
