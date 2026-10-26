param(
    [Parameter(Mandatory = $true)][string]$VMName,
    [Parameter(Mandatory = $true)][string]$Directory,
    [Parameter(Mandatory = $true)][string]$PreparedEFI,
    [Parameter(Mandatory = $true)][string]$SwitchName,
    [Parameter(Mandatory = $true)][string]$SerialPipe,
    [string]$OCValidatePath,
    [ValidateRange(64,4096)][int]$SystemDiskGiB = 512,
    [switch]$Create
)
# Reproduce the fresh-test hardware profile using NEW paths only.
# Default: print a plan. -Create explicitly creates ONE new VM; never starts it.
# No existing VM, switch, disk, backup or host security setting is modified.
# Input EFI is a separate unmounted source copy. Prepare another NEW EFI before
# VM creation, validating/enabling the existing paired Apple-services workaround.
$ErrorActionPreference = 'Stop'
if ($VMName -notmatch '^[A-Za-z0-9_-]+$') { throw 'Use a simple explicit VM name' }
if (-not $SerialPipe.StartsWith('\\.\pipe\')) { throw 'A local named pipe is required' }
if (Get-VM -Name $VMName -ErrorAction SilentlyContinue) { throw 'VM already exists; refusing modification' }
$root = [IO.Path]::GetFullPath($Directory).TrimEnd('\')
$efi = [IO.Path]::GetFullPath($PreparedEFI)
if (-not $efi.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Prepared EFI must be inside the new test directory'
}
if (-not (Test-Path -LiteralPath $efi -PathType Leaf)) { throw 'Prepared EFI file is missing' }
if ((Get-Item -LiteralPath $efi).Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw 'EFI must be a real file, not a reparse point'
}
$image = Get-VHD -Path $efi
if ($image.Attached -or $image.ParentPath) { throw 'EFI must be unmounted and independent' }
$null = Get-VMSwitch -Name $SwitchName -ErrorAction Stop
$system = Join-Path $root 'System.blank.vhdx'
$configuration = Join-Path $root 'vm'
$receipt = Join-Path $root 'vm-created-private.json'
$readyEFI = Join-Path $root 'EFI.setup.vhdx'
foreach ($path in @($system, $configuration, $receipt, $readyEFI)) {
    if (Test-Path -LiteralPath $path) { throw ('Output already exists: ' + $path) }
}
$efiHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $efi).Hash.ToLowerInvariant()
$plan = [ordered]@{
    target = $VMName
    generation = 2
    processors = 8
    fixed_memory_gib = 24
    new_system_gib = $SystemDiskGiB
    secure_boot = 'Off on the NEW VM only, matching the tested OpenCore profile'
    source_efi_sha256 = $efiHash
    prepared_efi_sha256 = $null
    apple_services_preflight = 'Prepare and validate NEW offline EFI copy before VM creation'
    starts_vm = $false
    modifies_existing_vm_or_switch = $false
}
if (-not $Create) {
    $plan | ConvertTo-Json
    Write-Output 'Plan only. Review inputs; -Create explicitly creates this new VM.'
    return
}
if (-not $OCValidatePath) { throw '-Create requires -OCValidatePath (matching OpenCore version)' }
$scriptDirectory = if ($PSScriptRoot) { $PSScriptRoot } else { Join-Path (Get-Location) 'BuildScripts' }
$prepare = [ScriptBlock]::Create((Get-Content -LiteralPath (Join-Path $scriptDirectory 'prepare-tahoe-efi.ps1') -Raw))
& $prepare -SourceEFI $efi -ExpectedSHA256 $efiHash -OutputEFI $readyEFI -OCValidatePath $OCValidatePath -HelperDirectory $scriptDirectory -Prepare
if (-not (Test-Path -LiteralPath $readyEFI) -or (Get-VHD -Path $readyEFI).Attached) { throw 'EFI preparation did not finish safely' }
$readyHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $readyEFI).Hash.ToLowerInvariant()
$plan['prepared_efi_sha256'] = $readyHash
$plan['apple_services_preflight'] = 'PASS: existing paired workaround enabled, ocvalidate passed'
New-VHD -Path $system -SizeBytes ([int64]$SystemDiskGiB * 1GB) -Dynamic -LogicalSectorSizeBytes 512 -PhysicalSectorSizeBytes 4096 | Out-Null
New-VM -Name $VMName -Generation 2 -MemoryStartupBytes 24GB -NoVHD -Path $configuration -SwitchName $SwitchName | Out-Null
Set-VMProcessor -VMName $VMName -Count 8
Set-VMMemory -VMName $VMName -DynamicMemoryEnabled $false
Set-VM -Name $VMName -AutomaticCheckpointsEnabled $false -AutomaticStartAction Nothing -AutomaticStopAction Save
Set-VMFirmware -VMName $VMName -EnableSecureBoot Off
Set-VMVideo -VMName $VMName -ResolutionType Single -HorizontalResolution 1920 -VerticalResolution 1080
Add-VMHardDiskDrive -VMName $VMName -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 0 -Path $readyEFI
Add-VMHardDiskDrive -VMName $VMName -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 1 -Path $system
$boot = Get-VMHardDiskDrive -VMName $VMName | Where-Object ControllerLocation -eq 0
Set-VMFirmware -VMName $VMName -FirstBootDevice $boot
Set-VMComPort -VMName $VMName -Number 1 -Path $SerialPipe
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $efi).Hash.ToLowerInvariant() -ne $efiHash) {
    throw 'Source EFI changed during creation; leave VM Off and investigate'
}
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $readyEFI).Hash.ToLowerInvariant() -ne $readyHash) {
    throw 'Prepared EFI changed during creation; leave VM Off and investigate'
}
$plan['created_utc'] = [DateTime]::UtcNow.ToString('o')
$plan['state'] = (Get-VM -Name $VMName).State.ToString()
$json = $plan | ConvertTo-Json
$stream = [IO.File]::Open($receipt, [IO.FileMode]::CreateNew)
try {
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($json + "`n")
    $stream.Write($bytes, 0, $bytes.Length)
} finally { $stream.Dispose() }
Write-Output 'New VM prepared and left Off. Start its unique serial receiver BEFORE boot.'
