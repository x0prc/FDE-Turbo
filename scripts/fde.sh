#!/bin/sh
MountPoint=/tmp-keydisk-mount
KeyFileName=LinuxPassPhraseFileName
echo "Trying to get the key from disks..." >&2
mkdir -p $MountPoint
modprobe vfat >/dev/null 2>&1
modprobe ntfs >/dev/null 2>&1
sleep 2
OPENED=0
cd /sys/block
for DEV in sd*; do
  echo "> Trying device: $DEV..." >&2
  mount -t vfat -r /dev/${DEV}1 $MountPoint >/dev/null|| mount -t ntfs -r /dev/${DEV}1 $MountPoint >/dev/null
  if [ -f $MountPoint/$KeyFileName ]; then
    cat $MountPoint/$KeyFileName
    umount $MountPoint 2>/dev/null
    OPENED=1
    break
  fi
  umount $MountPoint 2>/dev/null
done
if [ $OPENED -eq 0 ]; then
  echo "FAILED to find suitable passphrase file..." >&2
  echo -n "Try to enter your password: " >&2
  read -s -r A </dev/console
  echo -n "$A"
else
  echo "Success loading keyfile!" >&2
fi