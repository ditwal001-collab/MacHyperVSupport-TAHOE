param(
    [Parameter(Mandatory = $true)][string]$VMName,
    [Parameter(Mandatory = $true)][string]$OutputPath
)
# Read one explicitly named VM; export only non-identifying configuration.
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $OutputPath) { throw 'Refusing to overwrite an existing profile' }
$vm = Get-VM -Name $VMName
$cpu = Get-VMProcessor -VM $vm
$memory = Get-VMMemory -VM $vm
$firmware = Get-VMFirmware -VM $vm
$video = Get-VMVideo -VM $vm
$network = @(Get-VMNetworkAdapter -VM $vm | ForEach-Object {
    $switch = Get-VMSwitch -Id $_.SwitchId
    [ordered]@{
        switch_type = [string]$switch.SwitchType
        mac_spoofing = [string]$_.MacAddressSpoofing
        dhcp_guard = [string]$_.DhcpGuard
        router_guard = [string]$_.RouterGuard
    }
})
$storage = @(Get-VMHardDiskDrive -VM $vm | ForEach-Object {
    $disk = Get-VHD -Path $_.Path
    [ordered]@{
        controller_type = [string]$_.ControllerType
        controller_number = $_.ControllerNumber
        controller_location = $_.ControllerLocation
        format = [string]$disk.VhdFormat
        type = [string]$disk.VhdType
        capacity_bytes = $disk.Size
        logical_sector_bytes = $disk.LogicalSectorSize
        physical_sector_bytes = $disk.PhysicalSectorSize
    }
})
$serial = @(Get-VMComPort -VM $vm | ForEach-Object {
    [ordered]@{port = $_.Name; configured = -not [string]::IsNullOrEmpty($_.Path)}
})
$profile = [ordered]@{
    collected_utc = [DateTime]::UtcNow.ToString('o')
    scope = 'Read-only current snapshot of one explicitly named test VM; not a historical before/after proof'
    generation = $vm.Generation
    configuration_version = $vm.Version
    state = [string]$vm.State
    uptime_seconds = [math]::Floor($vm.Uptime.TotalSeconds)
    cpu = [ordered]@{count = $cpu.Count; nested_virtualization = $cpu.ExposeVirtualizationExtensions;
        migration_compatibility = $cpu.CompatibilityForMigrationEnabled;
        legacy_compatibility = $cpu.CompatibilityForOlderOperatingSystemsEnabled;
        hardware_threads_per_core = $cpu.HwThreadCountPerCore;
        limit_percent = $cpu.Maximum; reserve_percent = $cpu.Reserve; relative_weight = $cpu.RelativeWeight}
    memory = [ordered]@{dynamic = $memory.DynamicMemoryEnabled; startup_bytes = $memory.Startup}
    firmware = [ordered]@{secure_boot = [string]$firmware.SecureBoot;
        network_boot_protocol = [string]$firmware.PreferredNetworkBootProtocol;
        console_mode = [string]$firmware.ConsoleMode}
    display = [ordered]@{resolution_type = [string]$video.ResolutionType;
        maximum_width = $video.HorizontalResolution; maximum_height = $video.VerticalResolution}
    network = $network
    disks = $storage
    serial = $serial
    automatic_checkpoints = $vm.AutomaticCheckpointsEnabled
    checkpoint_type = [string]$vm.CheckpointType
    automatic_start_action = [string]$vm.AutomaticStartAction
    automatic_stop_action = [string]$vm.AutomaticStopAction
    privacy = 'No VM/host/switch names, IDs, MACs, addresses, disk/pipe paths or credentials exported'
}
$json = $profile | ConvertTo-Json -Depth 10
$encoding = New-Object System.Text.UTF8Encoding($false)
$stream = [System.IO.File]::Open($OutputPath, [System.IO.FileMode]::CreateNew)
try {
    $bytes = $encoding.GetBytes($json + "`n")
    $stream.Write($bytes, 0, $bytes.Length)
} finally { $stream.Dispose() }
Write-Output 'Read-only anonymized Hyper-V profile saved'
