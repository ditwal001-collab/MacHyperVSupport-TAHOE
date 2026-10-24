param([string]$OutputRoot = 'evidence/packages')
$ErrorActionPreference = 'Stop'
& py -3 (Join-Path $PSScriptRoot 'export-maintainer-package.py') --output-root $OutputRoot
if ($LASTEXITCODE -ne 0) { throw 'Maintainer export or patch verification failed.' }
