#!/bin/bash
# Root first-boot stage; no credentials, security-policy changes or automatic reboot.
set -euo pipefail
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
umask 022
test "$(id -u)" = 0
support='/Library/Application Support/MacHyperVSetup'
state="$support/state"
mkdir -p "$state"
chmod 700 "$state"
status() {
  printf '%s\n' "$1" > "$support/status.new"
  chmod 644 "$support/status.new"
  mv "$support/status.new" "$support/status.txt"
}
test ! -f "$state/failed" || exit 0
if kextstat -b fish.goldfish64.MacHyperVFramebuffer 2>/dev/null | grep -q '3C6D0CDD-D9E7-39C8-94FB-D97A47BE3CF6'; then
  status driver-ready
  exit 0
fi
test ! -f "$state/installed" || { status awaiting-approval; exit 0; }
if [ -f "$state/active" ]; then
  previous=$(cat "$state/active")
  if [[ "$previous" =~ ^[0-9]+$ ]] && kill -0 "$previous" 2>/dev/null &&
      ps -p "$previous" -o command= | grep -Fq "$support/bootstrap.command"; then exit 0; fi
  mv "$state/active" "$state/interrupted-$(date -u +%Y%m%dT%H%M%SZ)-$$"
fi
test "$(sw_vers -buildVersion)" = 25G241 || { status failed; touch "$state/failed"; exit 1; }
test "$(uname -m)" = x86_64 || { status failed; touch "$state/failed"; exit 1; }
# Apple's stock Aux may not exist in the first moments of a new system startup.
test -f /Library/KernelCollections/AuxiliaryKernelExtensions.kc || { status waiting-os; exit 0; }
kextstat -b fish.goldfish64.MacHyperVSupport 2>/dev/null | grep -q '7CAF03F1-3631-33A9-AAAF-581270B665B0' || { status waiting-os; exit 0; }
printf '%s\n' $$ > "$state/active"
trap 'rm -f "$state/active"' EXIT
exec >> "$support/setup.log" 2>&1
failed() { status failed; touch "$state/failed"; echo 'SETUP_FAILED: original collection backups retained; no automatic reboot'; }
trap failed ERR
echo "SETUP_BEGIN $(date -u +%FT%TZ)"
if [ ! -d /Library/Developer/KDKs/KDK_26.7.1_25G241.kdk ]; then
  status installing-kdk
  dmg="$state/Kernel_Debug_Kit_26.7.1_build_25G241.dmg"
  if [ ! -f "$dmg" ]; then
    curl --fail --location --retry 3 --proto '=https' --tlsv1.2 \
      'https://github.com/dortania/KdkSupportPkg/releases/download/25G241/Kernel_Debug_Kit_26.7.1_build_25G241.dmg' \
      -o "$dmg.partial"
    mv "$dmg.partial" "$dmg"
  fi
  echo "9045a521c8ae362d4cb2cc54701b03462686e0069518a0b66cfe2028f87dfe9b  $dmg" | shasum -a 256 -c -
  mount="$state/kdk-mount"
  mkdir -p "$mount"
  hdiutil attach -readonly -nobrowse -mountpoint "$mount" "$dmg"
  pkgutil --check-signature "$mount/KernelDebugKit.pkg" > "$state/kdk-signature.txt"
  grep -q 'signed Apple Software' "$state/kdk-signature.txt"
  grep -q 'Apple Root CA' "$state/kdk-signature.txt"
  installer -pkg "$mount/KernelDebugKit.pkg" -target /
  hdiutil detach "$mount"
fi
status installing-framebuffer
bash "$support/Payload/Install.command"
touch "$state/installed"
status awaiting-approval
echo "SETUP_INSTALLED $(date -u +%FT%TZ); native macOS approval/restart remains part of setup"
