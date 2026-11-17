#Requires -RunAsAdministrator
<#
Install native Qaroshi Windows layouts. No background service or network.
Modifies Windows keyboard registry and System32 only with consent.
#>
param(
  [ValidateSet('qwerty','azerty','dvorak')][string]$Layout='qwerty',
  [switch]$Uninstall
)
$ErrorActionPreference='Stop'
$settings=@{
  qwerty=@{ Dll='qrqwer1.dll'; Id='A1010409'; Name='Qaroshi QWERTY' }
  azerty=@{ Dll='qrazrt1.dll'; Id='A1020409'; Name='Qaroshi AZERTY' }
  dvorak=@{ Dll='qrdvor1.dll'; Id='A1030409'; Name='Qaroshi DVORAK' }
}
$layoutInfo=$settings[$Layout]
$registry="HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\$($layoutInfo.Id)"
$filename=$layoutInfo.Dll
$system64=Join-Path $env:windir "System32\$filename"
$system32=Join-Path $env:windir "SysWOW64\$filename"
$base=Split-Path -Parent $MyInvocation.MyCommand.Path
if($Uninstall) {
  if(Test-Path $registry) {
    $current=(Get-ItemProperty -Path $registry -ErrorAction SilentlyContinue).'Layout File'
    if($current -ne $filename) {
      throw "Refusing to remove registry key $registry; its DLL is not $filename."
    }
    Remove-Item -Path $registry -Force
  }
  Write-Host "Registry entry removed. Sign out and back in before deleting installed DLLs."
  exit 0
}
if(Test-Path $registry){
  throw "Keyboard ID $($layoutInfo.Id) is already registered; refusing overwrite."
}
$src64=Join-Path $base "amd64\$filename"
$src32=Join-Path $base "wow64\$filename"
if(!(Test-Path $src64) -or !(Test-Path $src32)){
  throw "Missing compiled x64 and WOW64 DLLs. Download the compiled Windows native artifact."
}
if((Test-Path $system64) -or (Test-Path $system32)){
  throw "A same-named keyboard DLL already exists. Refusing to overwrite."
}
Copy-Item -Path $src64 -Destination $system64
try {
  Copy-Item -Path $src32 -Destination $system32
  New-Item -Path $registry -Force | Out-Null
  New-ItemProperty -Path $registry -Name "Layout File" -Value $filename -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registry -Name "Layout Text" -Value $layoutInfo.Name -PropertyType String -Force | Out-Null
} catch {
  Remove-Item -Path $registry -Force -ErrorAction SilentlyContinue
  Remove-Item -Path $system64 -Force -ErrorAction SilentlyContinue
  Remove-Item -Path $system32 -Force -ErrorAction SilentlyContinue
  throw
}
Write-Host "Installed $($layoutInfo.Name). Sign out/in or restart; add it in Windows input settings."
