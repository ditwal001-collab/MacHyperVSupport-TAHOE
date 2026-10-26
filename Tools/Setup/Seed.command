#!/bin/bash
# Recovery-only seed into a NEW empty APFS volume, before Apple's OS installer.
# Does not erase/partition, modify EFI, change security, or create user accounts.
set -euo pipefail
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
test "$(id -u)" = 0
test "$#" = 1 || { echo 'Usage: bash Seed.command /Volumes/NEW_EMPTY_VOLUME'; exit 1; }
target=$1
case "$target" in /Volumes/*) ;; *) echo 'Target must be a mounted new volume'; exit 1;; esac
test -d "$target"
test ! -e "$target/System"
test ! -e "$target/Users"
test ! -e "$target/Library"
test ! -e "$target/Applications"
info=$(mktemp /tmp/hvseed-info.XXXXXXXX)
trap 'rm -f "$info"' EXIT
diskutil info -plist "$target" > "$info"
test "$(/usr/libexec/PlistBuddy -c 'Print :FilesystemType' "$info")" = apfs
here=$(cd "$(dirname "$0")" && pwd)
# Recovery has /sbin/sha256 but omits Perl and its shasum wrapper.
(cd "$here"
  while IFS= read -r line; do
    expected=${line%% *}
    relative=${line#*  }
    [[ "$expected" =~ ^[0-9a-f]{64}$ ]]
    case "$relative" in ''|/*|../*|*/../*|*/..) exit 1;; esac
    test "$(/sbin/sha256 -q "$relative")" = "$expected"
    printf '%s: OK\n' "$relative"
  done < payload.sha256
)
support="$target/Library/Application Support/MacHyperVSetup"
mkdir -p "$support" "$target/Library/LaunchDaemons" "$target/Library/LaunchAgents" "$target/Applications"
ditto "$here/MacHyperVSetup.app" "$target/Applications/MacHyperVSetup.app"
ditto "$here/Payload" "$support/Payload"
cp "$here/bootstrap.command" "$support/bootstrap.command"
cp "$here/fish.goldfish64.hyperv-setup.plist" "$target/Library/LaunchDaemons/"
cp "$here/fish.goldfish64.hyperv-setup-ui.plist" "$target/Library/LaunchAgents/"
mkdir -p "$target/Library/Application Support/MacHyperVSupport"
cp "$here/hvshutdownd" "$target/Library/Application Support/MacHyperVSupport/hvshutdownd"
cp "$here/fish.goldfish64.hvshutdownd.plist" "$target/Library/LaunchDaemons/"
chown -R root:wheel "$support" "$target/Applications/MacHyperVSetup.app" "$target/Library/Application Support/MacHyperVSupport"
find "$support" "$target/Applications/MacHyperVSetup.app" -type d -exec chmod 755 {} +
find "$support" "$target/Applications/MacHyperVSetup.app" -type f -exec chmod 644 {} +
chmod 755 "$support/bootstrap.command" "$target/Applications/MacHyperVSetup.app/Contents/MacOS/MacHyperVSetup" "$target/Library/Application Support/MacHyperVSupport/hvshutdownd"
chmod 644 "$target/Library/LaunchDaemons/fish.goldfish64.hyperv-setup.plist" "$target/Library/LaunchDaemons/fish.goldfish64.hvshutdownd.plist" "$target/Library/LaunchAgents/fish.goldfish64.hyperv-setup-ui.plist"
chown root:wheel "$target/Library/LaunchDaemons/fish.goldfish64.hyperv-setup.plist" "$target/Library/LaunchDaemons/fish.goldfish64.hvshutdownd.plist" "$target/Library/LaunchAgents/fish.goldfish64.hyperv-setup-ui.plist"
echo 'INTEGRATED_SETUP_SEEDED: proceed with the normal Apple installation on this volume.'
