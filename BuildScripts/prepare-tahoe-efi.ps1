param(
    [Parameter(Mandatory = $true)][string]$SourceEFI,
    [Parameter(Mandatory = $true)][string]$ExpectedSHA256,
    [Parameter(Mandatory = $true)][string]$OutputEFI,
    [Parameter(Mandatory = $true)][string]$OCValidatePath,
    [switch]$Prepare
)
# Offline preparation of a NEW EFI copy, before attaching it to a VM.
# The source and all existing images/backups are preserved. Never starts a VM.
$ErrorActionPreference = 'Stop'
$source = [IO.Path]::GetFullPath($SourceEFI)
$output = [IO.Path]::GetFullPath($OutputEFI)
$validator = [IO.Path]::GetFullPath($OCValidatePath)
$scriptDirectory = if ($PSScriptRoot) { $PSScriptRoot } else { Join-Path (Get-Location) 'BuildScripts' }
$helper = Join-Path $scriptDirectory 'enable-tahoe-iservices-patch.py'
if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw 'Source EFI missing' }
if ((Get-Item -LiteralPath $source).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source is a reparse point' }
if ([IO.Path]::GetExtension($output) -ne '.vhdx') { throw 'Output must be a new VHDX' }
if (Test-Path -LiteralPath $output) { throw 'Output exists; never overwrite an image' }
if (-not (Test-Path -LiteralPath $validator -PathType Leaf)) { throw 'ocvalidate missing' }
$sourceImage = Get-VHD -Path $source
if ($sourceImage.Attached -or $sourceImage.ParentPath) { throw 'Source must be unmounted and independent' }
$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sourceHash -ne $ExpectedSHA256.ToLowerInvariant()) { throw 'Source EFI hash mismatch' }
if (-not $Prepare) {
    [ordered]@{source_sha256=$sourceHash;new_efi=$output;checks='existing paired Apple-services workaround plus ocvalidate';starts_vm=$false} | ConvertTo-Json
    return
}
if (-not (Test-Path -LiteralPath (Split-Path -Parent $output) -PathType Container)) { throw 'Output parent must exist' }
if ((Get-Item -LiteralPath (Split-Path -Parent $output)).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Output parent is a reparse point' }
$stage = Join-Path (Split-Path -Parent $output) ('efi-preparation-private-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -ErrorAction Stop | Out-Null
# Exclusive create also protects against a file appearing after the first check.
$inputStream = [IO.File]::OpenRead($source)
try {
    $outputStream = [IO.File]::Open($output, [IO.FileMode]::CreateNew)
    try { $inputStream.CopyTo($outputStream) } finally { $outputStream.Dispose() }
} finally { $inputStream.Dispose() }
if ((Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHash) { throw 'EFI copy hash mismatch' }
$mount = Join-Path $stage 'mount'
New-Item -ItemType Directory -Path $mount | Out-Null
$mounted = $false
$accessAdded = $false
try {
    $image = Mount-VHD -Path $output -NoDriveLetter -Passthru
    $mounted = $true
    $efiDisk = $image | Get-Disk
    $partitions = @(Get-Partition -DiskNumber $efiDisk.Number | Where-Object { $_.Size -gt 64MB })
    if ($partitions.Count -ne 1) { throw 'Expected one EFI data partition; image layout unsupported' }
    $partitionNumber = $partitions[0].PartitionNumber
    Add-PartitionAccessPath -DiskNumber $efiDisk.Number -PartitionNumber $partitionNumber -AccessPath ($mount + '\')
    $accessAdded = $true
    $config = Join-Path $mount 'EFI/OC/config.plist'
    $beforeHash = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant()
    Copy-Item -LiteralPath $config -Destination (Join-Path $stage 'config.before-private.plist')
    $checkText = & py -3 $helper --config $config --expected-sha256 $beforeHash --check
    if ($LASTEXITCODE -ne 0) { throw 'Existing EFI pair validation failed; no VM may use this output' }
    $check = $checkText | ConvertFrom-Json
    $patched = -not $check.pair_enabled
    if ($patched) {
        $newConfig = Join-Path $stage 'config.patched-private.plist'
        & py -3 $helper --config $config --expected-sha256 $beforeHash --output $newConfig
        if ($LASTEXITCODE -ne 0) { throw 'Guarded EFI correction failed' }
        & $validator $newConfig
        if ($LASTEXITCODE -ne 0) { throw 'ocvalidate rejected corrected plist' }
        Copy-Item -LiteralPath $newConfig -Destination $config
    } else {
        & $validator $config
        if ($LASTEXITCODE -ne 0) { throw 'ocvalidate rejected existing plist' }
    }
    $afterHash = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant()
} finally {
    try {
        if ($accessAdded) { Remove-PartitionAccessPath -DiskNumber $efiDisk.Number -PartitionNumber $partitionNumber -AccessPath ($mount + '\') }
    } finally {
        if ($mounted) { Dismount-VHD -Path $output }
    }
}
if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHash) { throw 'Source changed; investigate before using output' }
$receipt = [ordered]@{source_sha256=$sourceHash;prepared_efi_sha256=(Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant();config_before_sha256=$beforeHash;config_after_sha256=$afterHash;apple_services_pair_enabled=$true;changed_existing_flag=$patched;ocvalidate='PASS';starts_vm=$false}
$receipt | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $stage 'preparation-private.json') -Encoding UTF8
$receipt | ConvertTo-Json
