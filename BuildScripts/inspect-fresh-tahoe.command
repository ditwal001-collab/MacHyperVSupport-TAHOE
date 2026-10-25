#!/bin/bash
# Read-only guest inventory apart from a new, exclusive report directory.
# Does not install kexts, rebuild caches, change security or reboot.
set -euo pipefail
if [ "$(id -u)" != 0 ]; then
  echo 'Run using sudo bash /Volumes/HVFRESH/Inspect.command'
  exit 1
fi
report=$(mktemp -d /Users/Shared/HVFreshInspect.XXXXXXXX)
exec > >(tee "$report/inspect.txt") 2>&1
echo "REPORT $report"
sw_vers
uname -m
csrutil status
sysctl kern.bootargs
for bundle in fish.goldfish64.MacHyperVSupport fish.goldfish64.MacHyperVFramebuffer; do
  kextstat -b "$bundle"
done
for file in \
  /System/Library/KernelCollections/BootKernelExtensions.kc \
  /System/Library/KernelCollections/SystemKernelExtensions.kc \
  /Library/KernelCollections/AuxiliaryKernelExtensions.kc; do
  if [ -f "$file" ]; then
    shasum -a 256 "$file"
  else
    echo "ABSENT $file"
  fi
done
aux=/Library/KernelCollections/AuxiliaryKernelExtensions.kc
if [ -f "$aux" ]; then
  kmutil inspect -A "$aux" -V release > "$report/aux-inspect.txt"
  cat "$report/aux-inspect.txt"
fi
for directory in /Library/Extensions /Library/Apple/System/Library/Extensions; do
  if [ -d "$directory" ]; then
    find "$directory" -type d -name '*.kext' -prune -print
  fi
done
echo 'INSPECTION_COMPLETE; no kext, collection, security or lifecycle change.'
