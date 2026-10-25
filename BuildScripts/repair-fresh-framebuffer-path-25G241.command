#!/bin/bash
# Scoped repair of this test's initial staging-path Aux. No live kext load.
set -euo pipefail
test "$(id -u)" = 0
test "$(sw_vers -buildVersion)" = 25G241
test "$(uname -m)" = x86_64
module=/Library/Extensions/MacHyperVFramebuffer.kext
aux=/Library/KernelCollections/AuxiliaryKernelExtensions.kc
boot=/System/Library/KernelCollections/BootKernelExtensions.kc
system=/System/Library/KernelCollections/SystemKernelExtensions.kc
test "$(shasum -a 256 "$module/Contents/MacOS/MacHyperVFramebuffer" | awk '{print $1}')" = d8a079d47d61988aabe40cb788b015979c27384135b57339e854d5c017792122
backup=$(mktemp -d /Users/Shared/HVFreshPathRepair.XXXXXXXX)
exec > >(tee "$backup/repair.txt") 2>&1
echo "BACKUP $backup"
cp -p "$aux" "$backup/OriginalAux.kc"
cmp "$aux" "$backup/OriginalAux.kc"
shasum -a 256 "$boot" "$system" > "$backup/base-before.sha256"
kmutil inspect -A "$aux" -V release > "$backup/original-inspect.txt"
grep -Eq '^fish\.goldfish64\.MacHyperVFramebuffer[[:space:]]+0\.9\.10[[:space:]]+/Users/Shared/HVFreshFramebuffer\.[A-Za-z0-9]+/stage/MacHyperVFramebuffer\.kext$' "$backup/original-inspect.txt"
awk '$1 ~ /^[A-Za-z0-9_-]+\./ {print $1, $2}' "$backup/original-inspect.txt" | sort > "$backup/original-versions.txt"
printf '%s\n' 'com.apple.driver.AppleMobileDevice 4.0' 'com.highpoint-tech.kext.HighPointIOP 4.4.5' 'com.highpoint-tech.kext.HighPointRR 4.22.1' 'fish.goldfish64.MacHyperVFramebuffer 0.9.10' | sort > "$backup/expected.txt"
cmp "$backup/original-versions.txt" "$backup/expected.txt"
kmutil create -n aux -V release -a x86_64 -x \
  -p "$module" -p /Library/Extensions/HighPointIOP.kext \
  -p /Library/Extensions/HighPointRR.kext \
  -p /Library/Apple/System/Library/Extensions/AppleMobileDevice.kext \
  -B "$boot" -S "$system" -A "$backup/CanonicalAux.kc" > "$backup/build.log" 2>&1
kmutil inspect -A "$backup/CanonicalAux.kc" -V release > "$backup/canonical-inspect.txt"
awk '$1 ~ /^[A-Za-z0-9_-]+\./ {print $1, $2}' "$backup/canonical-inspect.txt" | sort > "$backup/canonical-versions.txt"
cmp "$backup/canonical-versions.txt" "$backup/expected.txt"
grep -Eq '^fish\.goldfish64\.MacHyperVFramebuffer[[:space:]]+0\.9\.10[[:space:]]+/Library/Extensions/MacHyperVFramebuffer\.kext$' "$backup/canonical-inspect.txt"
shasum -a 256 -c "$backup/base-before.sha256"
restore() {
  trap - ERR
  cp -p "$backup/OriginalAux.kc" "$aux"
  cmp "$backup/OriginalAux.kc" "$aux"
  /usr/sbin/kcditto > "$backup/rollback-kcditto.log" 2>&1
  echo 'PATH_REPAIR_FAILED; original Aux restored; NO REBOOT.'
  exit 1
}
trap restore ERR
temporary="${aux}.path-$(date -u +%Y%m%dT%H%M%SZ)-$$"
test ! -e "$temporary"
cp -p "$backup/CanonicalAux.kc" "$temporary"
chown root:wheel "$temporary"
chmod 644 "$temporary"
mv -f "$temporary" "$aux"
/usr/sbin/kcditto > "$backup/kcditto.log" 2>&1
cmp "$aux" "$backup/CanonicalAux.kc"
shasum -a 256 -c "$backup/base-before.sha256"
trap - ERR
cat "$backup/canonical-inspect.txt"
shasum -a 256 "$aux"
echo "CANONICAL_FRAMEBUFFER_AUX_INSTALLED $backup"
echo 'No live load or automatic restart; verify loaded UUID after normal reboot.'
