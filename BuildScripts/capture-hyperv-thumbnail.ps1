param(
    [Parameter(Mandatory = $true)][string]$VMName,
    [Parameter(Mandatory = $true)][string]$OutputPath
)
# Read exactly one selected VM's framebuffer; no input or lifecycle action.
# A fresh thumbnail is diagnostic evidence, not proof of a fresh VMConnect view.
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $OutputPath) { throw 'Refusing to overwrite an image' }
$id = (Get-VM -Name $VMName).Id.ToString()
$vm = Get-WmiObject -Namespace root\virtualization\v2 -Class Msvm_ComputerSystem -Filter ("Name='" + $id + "'")
$settings = @($vm.GetRelated('Msvm_VirtualSystemSettingData')) | Where-Object VirtualSystemType -eq 'Microsoft:Hyper-V:System:Realized'
if (@($settings).Count -ne 1) { throw 'Ambiguous realized settings' }
$service = Get-WmiObject -Namespace root\virtualization\v2 -Class Msvm_VirtualSystemManagementService
$arguments = $service.GetMethodParameters('GetVirtualSystemThumbnailImage')
$arguments['TargetSystem'] = $settings.__PATH
$arguments['WidthPixels'] = [uint16]1280
$arguments['HeightPixels'] = [uint16]720
$result = $service.InvokeMethod('GetVirtualSystemThumbnailImage', $arguments, $null)
if ($result.ReturnValue -ne 0) { throw ('Thumbnail result ' + $result.ReturnValue) }
$data = [byte[]]$result.ImageData
$offset = 0
if ($data.Length -eq (1280 * 720 * 2 + 4)) { $offset = 4 }
if (($data.Length - $offset) -ne 1280 * 720 * 2) { throw 'Unexpected thumbnail layout' }
Add-Type -AssemblyName System.Drawing
$image = New-Object System.Drawing.Bitmap(1280, 720, [System.Drawing.Imaging.PixelFormat]::Format16bppRgb565)
try {
    $rect = New-Object System.Drawing.Rectangle(0, 0, 1280, 720)
    $locked = $image.LockBits($rect, [System.Drawing.Imaging.ImageLockMode]::WriteOnly, [System.Drawing.Imaging.PixelFormat]::Format16bppRgb565)
    try { [Runtime.InteropServices.Marshal]::Copy($data, $offset, $locked.Scan0, 1280 * 720 * 2) }
    finally { $image.UnlockBits($locked) }
    $stream = [IO.File]::Open([IO.Path]::GetFullPath($OutputPath), [IO.FileMode]::CreateNew)
    try { $image.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png) }
    finally { $stream.Dispose() }
} finally { $image.Dispose() }
Write-Output $OutputPath
