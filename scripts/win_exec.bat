import subprocess

# Define the PowerShell script content
powershell_script = "FDETurbo-Enabling BitLocker and Full Disk Encryption"
$Drive = "C:"
$RecoveryKeyPath = "C:\\RecoveryKey.txt"

$BitLockerStatus = Get-BitLockerVolume -MountPoint $Drive

if ($BitLockerStatus.ProtectionStatus -eq 'Off') {
    Enable-BitLocker -MountPoint $Drive -RecoveryKeyPath $RecoveryKeyPath -EncryptionMethod Aes256 -UsedSpaceOnly
    Write-Host "BitLocker encryption has been initiated on $Drive."
} else {
    Write-Host "BitLocker is already enabled on $Drive."
}
"""

# Save the PowerShell script to a temporary .ps1 file
script_path = "C:\\temp\\EnableBitLocker.ps1"
with open(script_path, "w") as script_file:
    script_file.write(powershell_script)

# Execute the PowerShell script
try:
    result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], capture_output=True, text=True)
    
    # Print the output and any errors
    print("Output:\n", result.stdout)
    print("Errors:\n", result.stderr)

except Exception as e:
    print(f"An error occurred: {e}")