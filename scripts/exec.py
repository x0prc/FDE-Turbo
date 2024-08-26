import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os

shell_script = """#!/bin/sh
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
"""

# Function to execute the shell script
def run_script():
    with open("temp_script.sh", "w") as file:
        file.write(shell_script)

    os.chmod("temp_script.sh", 0o755)

    process = subprocess.Popen(["./temp_script.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, stdout.decode())  # Insert stdout
    output_text.insert(tk.END, stderr.decode())   # Insert stderr

# Create the main window
root = tk.Tk()
root.title("Shell Script Executor")

# Create a button to run the script
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=10)

# Create a scrolled text area to display output
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()