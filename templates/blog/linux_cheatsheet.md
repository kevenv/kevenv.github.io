# Linux Cheatsheet

## Paths
- `.` : current directory
- `..` : parent directory
- `~` : home directory
- `../relative/path` : relative path
- `/absolute/path` : absolute path

## Pipes
- `A | B` : run A and transfer its output to B
- `A & B` : run A then B
- `A && B` : run A then B only if A succeeds
- `| grep [some string]` : filter out stdout

## Redirect
- `>` : stdout
- `<` : stdin
- `&>` : stdout + stderr
- `1>` : stdout
- `2>` : stderr

## Basic
- `cd [directory]` : change directory
- `ls [directory]` : list files & directories
    - -l : list
    - -a : all (hidden too)
    - -h : human sizes
- `cp [src] [dst]` : copy src to dst
    - -r : recursive (directory)
- `rm [file or directory]` : remove file or directory
    - -r : recursive (directory)
    - -f : force
- `mkdir [directory]` : create directory
    - p : create parent directories as needed
- `ln -s [target] [symlink]` : create a symlink
- `touch [file]` : create empty file, mark file as newly edited
- `source [file]` : execute a `.sh` file within the current shell
- `cat [file]` : print file to the screen
- `file [file]` : get file type
- `stat [file]` : get file info
- `man [cmd]` : show manual for cmd
- `pwd` : show current directory
- `which [cmd]` : show where cmd is located
- `find` : find files
    - `find [directory] -name [file]` : find file in directory
    - `find [directory] -name *.[ext]` : find all files of a given type
    - `find [directory] -type f -exec grep "[text]" '{}' \; -print` : find text in files

## Permissions
- `sudo [cmd]` : run a cmd as root
- `chmod [file]` : change file permissions
    - -R : recursive
    - +x : make a file executable
    - +rw : make a file read-write
    - -w : make a file read-only
- `chown [owner]:[group] [file]` : change the owner of a file
- `groups [user]` : list groups of a user
- `cat /etc/group` : list all groups

## Environment variables
- `export [var]=[name]` : set an env variable
- `echo $[var]` : print env variable
- `echo $PATH` : show system PATH
- `export PATH=$PATH:[directory path]` : add directory to system PATH
- `echo "export PATH=$PATH:[directory path]" >> ~/.bashrc` : change the system PATH permanently

## Other
- `ssh -p [port] [user]@[ip]` : login to SSH
- `reboot` : reboot system
- `poweroff` : shutdown system
- `wget` : ?
- `zip` : ?
- `unzip` : ?
- `hexdump` : dump file as hexa
- `find . -name [file] | entr [cmd]` : run a cmd whenever a file changes

## Disk
- `lsblk` : list disk
- `fdisk -l` : disk info
- `fdisk [disk]` : partition disk
- `mount [disk name] [directory]` : mount disk
- `umount [directory]` : unmount disk
- `cat /proc/mounts` : mount info

## Info
- `uname -a` : show kernel version
- `lspci` : list PCI devices (Bus:Device.Function)
    - -v : verbose
    - -vv : very verbose
    - -tv : tree
    - -k : kernel modules/drivers in use
    - -n : ID of PCI device (VendorID:deviceID)
- `lsusb` : list USB devices
    - -v : verbose
    - -t : tree
- `ifconfig` : show network info
- `nvidia-smi` : show GPU info
- `df -h` : show disk usage
- `free -h --si` : show how much RAM
- `htop` : list process, kill process
- `sensors` : show temperature
- `watch -t -n 1 "sensors | grep 'Core 0:'"` : show CPU temperature
- `cat /proc/[pid]` : procfs, running processes
- `cat /proc/meminfo` : memory info
- `cat /proc/cpuinfo` : CPU info (CPUID)
- `cat /proc/interrupts` : interrupts in
- `cat /proc/ioports` : IO ports
- `cat /proc/iomem` : MMIO
- `cat /proc/stat` : all process stats
- `cat /proc/[pid]/stat` : process stats
- `iftop` : list TCP sockets
- `netstat -nat` : list TCP sockets

## Kernel
- `lsmod` : list kernel modules
    - also `cat /proc/modules`
- `insmod [module].ko` : install kernel module
- `rmmod [module]` : remove kernel module
- `dmesg | tail -n 5` : show kernel log
- `ls -l /dev` : list device files
    - major, minor
- `cat /proc/devices` : list assigned device numbers
- `mknod [device] c [major] [minor]` : create character device
- `rmnod [device]`
- `head -c 1 [file]` : output the first byte of a file

## Filesystem
[FSH](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)

- `/proc` : procfs, running processes
- `/dev` : udev, devices files
- `/sys` : sysfs, devices/bus/drivers/kernel
    - `/sys/bus/pci/devices`

## Fedora

### DNF
- `dnf search [package]` : search for package in repos
- `dnf info [package]` : get info about package
- `dnf install [package]` : install package
- `dnf remove [package]` : remove package
- `dnf list installed` : list installed packages
- `dnf list available` : list all availables packages
- `dnf upgrade` : upgrade/update all packages
- `dnf autoremove` : remove unused packages
- `dnf clean all` : clear cached packages
- `dnf history` : show dnf history
- `dnf repolist all` : list packages repos
- `dnf provides [file]` : find package that provides a file
- `dnf repoquery -l [package]` : list files in package
- `dnf repoquery --requires [package]`: list dependencies of package
- `dnf repoquery --whatrequires [package]` : list packages that depends on a package

### Services
- `systemctl status [service]` : get status of service
- `systemctl enable [service]` : enable service at boot
- `systemctl disable [service]` : disable service at boot
- `systemctl start [service]` : start service
- `systemctl stop [service]` : stop service
- `systemctl restart [service]` : restart service
- `systemctl list-units` : list services running

## Python
- `pip list` : list installed python libs
- `pip install --user [lib]` : install python lib
- `pip install --user -r requirements.txt` : install all python libs in requirements file
- `pipreqs requirements.txt` : create requirements.txt for current project
- `python -m http.server` : run HTTP server

### Virtual Environment (venv)
- `python -m venv [venv]` : create venv
- `source [venv]/bin/activate` : enable venv
- `pip freeze > requirements.txt` : create requirements.txt
- `deactivate` : disable venv
- `rm -rf [venv]` : remove venv

### Debugger (pdb)
?