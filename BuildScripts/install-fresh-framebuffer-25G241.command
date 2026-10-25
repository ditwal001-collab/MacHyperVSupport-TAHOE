#!/bin/bash
# First installation ONLY: observed three-module Intel Tahoe 25G241 Aux inventory.
# Run from a read-only ISO beside the verified Release Framebuffer.zip.
# No security changes, Boot/System rebuild, or automatic restart.
set -euo pipefail
test "$(id -u)" = 0
test "$(sw_vers -buildVersion)" = 25G241
test "$(uname -m)" = x86_64
destination=/Library/Extensions/MacHyperVFramebuffer.kext
test ! -e "$destination"
aux=/Library/KernelCollections/AuxiliaryKernelExtensions.kc
boot=/System/Library/KernelCollections/BootKernelExtensions.kc
system=/System/Library/KernelCollections/SystemKernelExtensions.kc
exe=Contents/MacOS/MacHyperVFramebuffer
expected=d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122
test -x /usr/sbin/kcditto
backup=$(mktemp -d /Users/Shared/HVFreshFramebuffer.XXXXXXXX)
exec > >(tee "$backup/install.txt") 2>&1
echo "BACKUP $backup"
cp -p "$aux" "$backup/OriginalAux.kc"
cmp "$aux" "$backup/OriginalAux.kc"
shasum -a 256 "$boot" "$system" > "$backup/base-before.sha256"
kmutil inspect -A "$aux" -V release > "$backup/original-inspect.txt"
awk '$1 ~ /^[A-Za-z0-9_-]+\./ {print $1, $2}' "$backup/original-inspect.txt" | sort > "$backup/original-versions.txt"
printf '%s\n' 'com.apple.driver.AppleMobileDevice 4.0' 'com.highpoint-tech.kext.HighPointIOP 4.4.5' 'com.highpoint-tech.kext.HighPointRR 4.22.1' | sort > "$backup/expected-original.txt"
cmp "$backup/original-versions.txt" "$backup/expected-original.txt"
find /System/Volumes/Preboot -type f -name AuxiliaryKernelExtensions.kc -print0 > "$backup/preboot-paths.bin"
while IFS= read -r -d '' file; do
  mkdir -p "$backup/preboot$(dirname "$file")"
  cp -p "$file" "$backup/preboot$file"
  cmp "$file" "$backup/preboot$file"
done < "$backup/preboot-paths.bin"
ditto -x -k "$(dirname "$0")/Framebuffer.zip" "$backup/stage"
new="$backup/stage/MacHyperVFramebuffer.kext"
test "$(shasum -a 256 "$new/$exe" | awk '{print $1}')" = "$expected"
test "$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$new/Contents/Info.plist")" = fish.goldfish64.MacHyperVFramebuffer
chown -R root:wheel "$new"
find "$new" -type d -exec chmod 755 {} +
find "$new" -type f -exec chmod 644 {} +
chmod 755 "$new/$exe"
# Build privately BEFORE touching the installed bundle or active Aux collection.
if ! kmutil create -n aux -V release -a x86_64 -x \
  -p "$new" -p /Library/Extensions/HighPointIOP.kext \
  -p /Library/Extensions/HighPointRR.kext \
  -p /Library/Apple/System/Library/Extensions/AppleMobileDevice.kext \
  -B "$boot" -S "$system" -A "$backup/CandidateAux.kc" > "$backup/build.log" 2>&1; then
  cat "$backup/build.log"
  echo 'PRIVATE_BUILD_FAILED; active bundle and Aux unchanged; NO REBOOT.'
  exit 1
fi
kmutil inspect -A "$backup/CandidateAux.kc" -V release > "$backup/candidate-inspect.txt"
awk '$1 ~ /^[A-Za-z0-9_-]+\./ {print $1, $2}' "$backup/candidate-inspect.txt" | sort > "$backup/candidate-versions.txt"
{ cat "$backup/expected-original.txt"; echo 'fish.goldfish64.MacHyperVFramebuffer 0.9.10'; } | sort > "$backup/expected-candidate.txt"
cmp "$backup/candidate-versions.txt" "$backup/expected-candidate.txt"
shasum -a 256 -c "$backup/base-before.sha256"
changed=0
restore() {
  trap - ERR
  echo 'INSTALL_FAILED; restoring original Aux/Preboot; NO REBOOT.'
  if [ "$changed" = 1 ]; then
    if [ -e "$destination" ]; then mv "$destination" "$backup/FailedInstalledFramebuffer.kext"; fi
    cp -p "$backup/OriginalAux.kc" "$aux"
    cmp "$backup/OriginalAux.kc" "$aux"
    while IFS= read -r -d '' file; do cp -p "$backup/preboot$file" "$file"; done < "$backup/preboot-paths.bin"
  fi
  exit 1
}
trap restore ERR
changed=1
ditto "$new" "$destination"
test "$(shasum -a 256 "$destination/$exe" | awk '{print $1}')" = "$expected"
# The boot collection must describe the final /Library/Extensions path, not
# the private probe path. Keep the first candidate only as a no-mutation probe.
kmutil create -n aux -V release -a x86_64 -x \
  -p "$destination" -p /Library/Extensions/HighPointIOP.kext \
  -p /Library/Extensions/HighPointRR.kext \
  -p /Library/Apple/System/Library/Extensions/AppleMobileDevice.kext \
  -B "$boot" -S "$system" -A "$backup/CanonicalAux.kc" > "$backup/canonical-build.log" 2>&1
kmutil inspect -A "$backup/CanonicalAux.kc" -V release > "$backup/canonical-inspect.txt"
awk '$1 ~ /^[A-Za-z0-9_-]+\./ {print $1, $2}' "$backup/canonical-inspect.txt" | sort > "$backup/canonical-versions.txt"
cmp "$backup/canonical-versions.txt" "$backup/expected-candidate.txt"
grep -Eq '^fish\.goldfish64\.MacHyperVFramebuffer[[:space:]]+0\.9\.10[[:space:]]+/Library/Extensions/MacHyperVFramebuffer\.kext$' "$backup/canonical-inspect.txt"
temp_aux="${aux}.fresh-$(date -u +%Y%m%dT%H%M%SZ)-$$"
test ! -e "$temp_aux"
cp -p "$backup/CanonicalAux.kc" "$temp_aux"
chown root:wheel "$temp_aux"
chmod 644 "$temp_aux"
mv -f "$temp_aux" "$aux"
/usr/sbin/kcditto > "$backup/kcditto.log" 2>&1
shasum -a 256 -c "$backup/base-before.sha256"
cmp "$aux" "$backup/CanonicalAux.kc"
trap - ERR
cat "$backup/canonical-inspect.txt"
shasum -a 256 "$destination/$exe" "$aux"
echo "FRESH_FRAMEBUFFER_INSTALLED $backup"
echo 'Verify loaded UUID after a normal restart; no automatic reboot performed.'
