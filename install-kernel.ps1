# run this script to install kernel

$kernelFolder = '~\AppData\Roaming\jupyter\kernels\powershell'
Write-Host "Install kernel in $kernelFolder"
mkdir ~\AppData\Roaming\jupyter\kernels\powershell -ErrorAction SilentlyContinue
cp .\kernel.json ~\AppData\Roaming\jupyter\kernels\powershell

Write-Host "Run 'jupyter kernelspec list' to list all available kernels"
