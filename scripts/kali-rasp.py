import subprocess

# Mount the microSD card
subprocess.run(["sudo", "mkdir", "-vp", "/mnt/chroot/"])
subprocess.run(["sudo", "mount", "/dev/sdX2", "/mnt/chroot/"])
subprocess.run(["sudo", "mount", "/dev/sdX1", "/mnt/chroot/boot/"])
subprocess.run(["sudo", "mount", "-t", "proc", "none", "/mnt/chroot/proc"])
subprocess.run(["sudo", "mount", "-t", "sysfs", "none", "/mnt/chroot/sys"])
subprocess.run(["sudo", "mount", "-o", "bind", "/dev", "/mnt/chroot/dev"])
subprocess.run(["sudo", "mount", "-o", "bind", "/dev/pts", "/mnt/chroot/dev/pts"])

# Install required packages
subprocess.run(["sudo", "apt", "install", "-y", "qemu-user-static"])
subprocess.run(["sudo", "cp", "/usr/bin/qemu-aarch64-static", "/mnt/chroot/usr/bin/"])

subprocess.run(["sudo", "env", "LANG=C", "chroot", "/mnt/chroot/"], shell=True)
subprocess.run(["apt", "update"])
subprocess.run(["apt", "install", "-y", "busybox", "cryptsetup", "dropbear-initramfs", "lvm2"])
subprocess.run(["apt", "install", "-y", "kalipi-kernel", "kalipi-bootloader", "kalipi-re4son-firmware"])

# Edit boot options
subprocess.run(["vim", "/boot/cmdline.txt"])

# Update fstab
subprocess.run(["vim", "/etc/fstab"])

# Configure encrypted partitions 
subprocess.run(["echo", "-e", "'crypt\tPARTUUID=ed889dad-02\tnone\tluks'", ">", "/etc/crypttab"], shell=True)
subprocess.run(["dd", "if=/dev/zero", "of=/tmp/fakeroot.img", "bs=1M", "count=20"])
subprocess.run(["cryptsetup", "luksFormat", "/mnt/chroot/tmp/fakeroot.img"])
subprocess.run(["cryptsetup", "luksOpen", "/mnt/chroot/tmp/fakeroot.img", "crypt"])
subprocess.run(["mkfs.ext4", "/dev/mapper/crypt"])

# Configure SSH keys
subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096"])
subprocess.run(["sudo", "cp", "~/.ssh/id_rsa_dropbear.pub", "/mnt/chroot/"])

# Configure for encryption
subprocess.run(["vim", "/etc/initramfs-tools/hooks/zz-cryptsetup"])
subprocess.run(["chmod", "+x", "/etc/initramfs-tools/hooks/zz-cryptsetup"])
subprocess.run(["grep", "-q", "dm_crypt", "/etc/initramfs-tools/modules", "||", "echo", "dm_crypt", ">>", "/etc/initramfs-tools/modules"], shell=True)

# Configure remote SSH unlock
subprocess.run(["vim", "/etc/initramfs-tools/unlock.sh"])
subprocess.run(["chmod", "+x", "/etc/initramfs-tools/unlock.sh"])
subprocess.run(["vim", "/etc/dropbear/initramfs/authorized_keys"])
subprocess.run(["cat", "id_rsa.pub", ">>", "/etc/dropbear/initramfs/authorized_keys", "&&", "rm", "-v", "id_rsa.pub"], shell=True)
subprocess.run(["vim", "/usr/share/initramfs-tools/scripts/init-premount/dropbear"])