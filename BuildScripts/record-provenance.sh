#!/bin/bash
set -eu
mkdir -p provenance
{
  printf 'source='; git rev-parse HEAD
  printf 'sdk='; git -C MacKernelSDK rev-parse HEAD
  printf 'run=%s attempt=%s\n' "$GITHUB_RUN_ID" "$GITHUB_RUN_ATTEMPT"
  printf 'ref=%s image=%s version=%s\n' "$GITHUB_REF" "${ImageOS:-unknown}" "${ImageVersion:-unknown}"
  sw_vers
  xcodebuild -version
  xcrun clang --version
  xcodebuild -showsdks
} > provenance/environment.txt
for dependency in Lilu.kext clang32; do
  if [ -d "$dependency" ]; then
    find "$dependency" -type f -exec shasum -a 256 {} \;
  fi
done > provenance/dependency-sha256.txt
if [ -d build ]; then
  find build -type f \( -name '*.zip' -o -path '*/Contents/MacOS/*' \) -exec shasum -a 256 {} \; > provenance/build-sha256.txt
  while IFS= read -r binary; do
    printf '\n%s\n' "$binary"
    xcrun nm -u "$binary"
  done < <(find build -type f -path '*/MacHyperVSupportMonterey.kext/Contents/MacOS/MacHyperVSupportMonterey') > provenance/monterey-imports.txt
fi
