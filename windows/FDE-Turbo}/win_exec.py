# Define the drive to encrypt and the location to save the recovery key
$Drive = "C:"  
$RecoveryKeyPath = "C:\RecoveryKey.txt"  # Change this to your desired recovery key path

# Check if BitLocker is already enabled
$BitLockerStatus = Get-BitLockerVolume -MountPoint $Drive

if ($BitLockerStatus.ProtectionStatus -eq 'Off') {
    Enable-BitLocker -MountPoint $Drive -RecoveryKeyPath $RecoveryKeyPath -EncryptionMethod Aes256 -UsedSpaceOnly

    Write-Host "BitLocker encryption has been initiated on $Drive."
} else {
    Write-Host "BitLocker is already enabled on $Drive."
}