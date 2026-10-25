param(
    [Parameter(Mandatory = $true)][string]$VMName,
    [Parameter(Mandatory = $true)][string]$Directory,
    [Parameter(Mandatory = $true)][string]$PreparedEFI,
    [Parameter(Mandatory = $true)][string]$SwitchName,
    [Parameter(Mandatory = $true)][string]$SerialPipe,
    [switch]$Create
)
# Reproduce the fresh-test hardware profile using NEW paths only.
# Default: print a plan. -Create explicitly creates ONE new VM; never starts it.
# No existing VM, switch, disk, backup or host security setting is modified.
# The prepared private EFI must already be a separate unmounted working copy.
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
foreach ($path in @($system, $configuration, $receipt)) {
    if (Test-Path -LiteralPath $path) { throw ('Output already exists: ' + $path) }
}
$efiHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $efi).Hash.ToLowerInvariant()
$plan = [ordered]@{
    target = $VMName
    generation = 2
    processors = 8
    fixed_memory_gib = 24
    new_system_gib = 400
    secure_boot = 'Off on the NEW VM only, matching the tested OpenCore profile'
    prepared_efi_sha256 = $efiHash
    starts_vm = $false
    modifies_existing_vm_or_switch = $false
}
if (-not $Create) {
    $plan | ConvertTo-Json
    Write-Output 'Plan only. Review inputs; -Create explicitly creates this new VM.'
    return
}
New-VHD -Path $system -SizeBytes 400GB -Dynamic -LogicalSectorSizeBytes 512 -PhysicalSectorSizeBytes 4096 | Out-Null
New-VM -Name $VMName -Generation 2 -MemoryStartupBytes 24GB -NoVHD -Path $configuration -SwitchName $SwitchName | Out-Null
Set-VMProcessor -VMName $VMName -Count 8
Set-VMMemory -VMName $VMName -DynamicMemoryEnabled $false
Set-VM -Name $VMName -AutomaticCheckpointsEnabled $false -AutomaticStartAction Nothing -AutomaticStopAction Save
Set-VMFirmware -VMName $VMName -EnableSecureBoot Off
Set-VMVideo -VMName $VMName -ResolutionType Maximum -HorizontalResolution 1920 -VerticalResolution 1080
Add-VMHardDiskDrive -VMName $VMName -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 0 -Path $efi
Add-VMHardDiskDrive -VMName $VMName -ControllerType SCSI -ControllerNumber 0 -ControllerLocation 1 -Path $system
$boot = Get-VMHardDiskDrive -VMName $VMName | Where-Object ControllerLocation -eq 0
Set-VMFirmware -VMName $VMName -FirstBootDevice $boot
Set-VMComPort -VMName $VMName -Number 1 -Path $SerialPipe
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $efi).Hash.ToLowerInvariant() -ne $efiHash) {
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
