![header](https://github.com/user-attachments/assets/5dc00add-e286-4d6b-a51c-e7e5ae564bbc)
GUI Installer Menus for Shell Scripts to automate the process on various Linux distributions and Windows.

# Prerequisites
- Ubuntu/Fedora/Kali on Raspberry Pi for Linux Disk Encryption
- Windows 10/11 for Windows Disk Encryption
- Reboot after installation

# Motivation
Full Disk Encryption is the most essential Step 1's of installing an Operating System on your disk. I am trying to make this repository easy to maintain, learn, collaborate and install and configure FDE. 

# Documentation
## For Linux Based Distributions
### Script Installation
- Install the [.deb](https://github.com/x0prc/FDE-Turbo/blob/main/debian/FDETurbo.deb) package (GUI Installer).
- Export the script contents to the directory: `/usr/local/sbin/`
- Change the crypt config flag in `/etc/crypttab` to: <br>
  `xxx_crypt uuid=xxxxxxxxxxxxxxxxxxxxx none luks,discard,keyscript=/usr/local/sbin/azure_crypt_key.sh`
- Add executable permissions to the script: <br>
  `sudo chmod +x /usr/local/sbin/azure_crypt_key.sh`
- Edit `/etc/initramfs-tools/modules` by appending <br>
  `vfat ntfs nls_cp437 nls_utf8 nls_iso8859-1`
- Run `update-initramfs -u -k all` to update the initramfs.

### Disk Encryption
1. Create a separate unencrypted boot drive.
2. Encrypt the **root drive** during installation.
3. Provide the passphrase that was uploaded to the key vault.
4. Finish partitioning and boot the machine.
5. When prompted for the passphrase, use the one provided earlier.

## For Windows 10/11 on x64/ARM
- Install using the [.exe](https://github.com/x0prc/FDE-Turbo/blob/main/windows/FDESetup.exe) package (GUI Installer).
- Also download the [Folder](https://github.com/x0prc/FDE-Turbo/tree/main/windows/FDE-Turbo%7D) for completing the requirements.

## For Kali on Raspberry Pi
Understand and execute this [script](https://github.com/x0prc/FDE-Turbo/blob/main/scripts/kali-rasp.py).

## NOTE : This method has been tested on Ubuntu 24.04 and previous versions. This also works for Kali on Raspberry Pi.
