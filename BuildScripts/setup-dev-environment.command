#!/bin/bash
# User-scoped setup for the authorized Intel Tahoe development guest.
# No sudo, security changes, restart, driver changes or existing-app replacement.
set -euo pipefail
test "$(uname -m)" = x86_64
test "$(sw_vers -productVersion | cut -d. -f1)" = 26
test "$(id -u)" != 0
umask 022
run=$(mktemp -d "$HOME/Library/Logs/HVDevSetup.XXXXXXXX")
exec > >(tee "$run/setup.log") 2>&1
echo "SETUP_LOG $run"
trap 'echo "SETUP_FAILED: inspect the log; no reboot or automatic removal."' ERR
mkdir -p "$HOME/Applications" "$HOME/.local/bin" "$HOME/Developer"
app="$HOME/Applications/Visual Studio Code.app"
sdk="$HOME/Applications/dotnet10"
test ! -e "$app"
test ! -e /Applications/Visual\ Studio\ Code.app
test ! -e "$sdk"
test ! -e "$HOME/.local/bin/code"
test ! -e "$HOME/.local/bin/dotnet"
echo 'Downloading pinned stable Intel builds from Microsoft.'
curl --fail --location --retry 3 --proto '=https' --tlsv1.2 \
  'https://vscode.download.prss.microsoft.com/dbazure/download/stable/e646868227c3e3a9e3f24277c8c7220be42c0be7/VSCode-darwin.zip' -o "$run/VSCode.zip"
echo '89d32274b13fdcd92a3c9ad933eaf0f005ba4c131558c18cd68c16a9589e7537  '"$run/VSCode.zip" | shasum -a 256 -c -
ditto -x -k "$run/VSCode.zip" "$run/code"
codesign --verify --deep --strict "$run/code/Visual Studio Code.app"
spctl --assess --type execute --verbose "$run/code/Visual Studio Code.app"
curl --fail --location --retry 3 --proto '=https' --tlsv1.2 \
  'https://builds.dotnet.microsoft.com/dotnet/Sdk/10.0.402/dotnet-sdk-10.0.402-osx-x64.tar.gz' -o "$run/dotnet.tar.gz"
echo '1628e0a07261f5bd54dde370c53b90cb72f0c88667d7cde34bd62997a29ff8f32310f81e08c85962a2b0221c05368df37fb04909b6f1431b293f445ecf895292  '"$run/dotnet.tar.gz" | shasum -a 512 -c -
mkdir "$sdk"
tar -xzf "$run/dotnet.tar.gz" -C "$sdk"
ditto "$run/code/Visual Studio Code.app" "$app"
ln -s "$app/Contents/Resources/app/bin/code" "$HOME/.local/bin/code"
ln -s "$sdk/dotnet" "$HOME/.local/bin/dotnet"
export DOTNET_ROOT="$sdk"
export PATH="$HOME/.local/bin:$DOTNET_ROOT:$DOTNET_ROOT/tools:$PATH"
export LANG=en_US.UTF-8
export DOTNET_CLI_UI_LANGUAGE=en-US
for profile in "$HOME/.zprofile" "$HOME/.zshrc"; do
  if [ -e "$profile" ]; then cp -p "$profile" "$run/$(basename "$profile").before"; fi
  cat >> "$profile" <<'PROFILE'

# Tahoe development tools (user-scoped)
export DOTNET_ROOT="$HOME/Applications/dotnet10"
export PATH="$HOME/.local/bin:$DOTNET_ROOT:$DOTNET_ROOT/tools:$PATH"
export LANG=en_US.UTF-8
export DOTNET_CLI_UI_LANGUAGE=en-US
PROFILE
done
"$sdk/dotnet" --info
test "$("$sdk/dotnet" --version)" = 10.0.402
test "$("$sdk/dotnet" --list-sdks | wc -l | tr -d ' ')" = 1
"$app/Contents/Resources/app/bin/code" --version
"$app/Contents/Resources/app/bin/code" --locale en --install-extension ms-dotnettools.csdevkit
smoke="$HOME/Developer/Dotnet10Smoke-$(date -u +%Y%m%dT%H%M%SZ)"
"$sdk/dotnet" new console --framework net10.0 --output "$smoke"
"$sdk/dotnet" run --project "$smoke"
"$app/Contents/Resources/app/bin/code" --list-extensions --show-versions
open -a "$app" --args --locale en "$smoke"
echo 'VSCODE_DOTNET_SETUP_VERIFIED'
echo 'Xcode installation and iOS validation are separate, not completed by this script.'
