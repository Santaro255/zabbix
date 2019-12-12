$files = (Get-ChildItem -Path .\*.py).FullName

foreach ($file in $files) {
    Start-Process -FilePath $file
}
