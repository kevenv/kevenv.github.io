# Linux cheatsheet

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
    - -p : create parent directories as needed
- `ln -s [target] [symlink]` : create a symlink
- `touch [file]` : create empty file, mark file as newly edited
- `source [file]` : execute a `.sh` file within the current shell
- `cat [file]` : print file to the screen
- `tree -a` : print directory hierarchy
    - -a : show all files (hidden)
    - -L [max depth] : max depth
- `tail -n [num of lines] [file]` : show last N lines of a file
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
- `scp [src path] [user]@[ip]:[dst path]` : copy file to remote
    - -p [port] : specify port
    - -r : recursive (directory)
- `scp [user]@[ip]:[src path] [dst path]` : copy file from remote
- `reboot` : reboot system
- `poweroff` : shutdown system
- `wget` : ?
- `tar -czvf [output file] [input dir]` : create tar file (`tar.gz`)
- `tar -xvf [input file] -C [output dir]` : extract tar file
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
- `fastfetch` : system info
- `uname -a` : show kernel version
- `lscpu` : list CPU info
- `lspci` : list PCI devices (Bus:Device.Function)
    - -v : verbose
    - -vv : very verbose
    - -tv : tree
    - -k : kernel modules/drivers in use
    - -n : ID of PCI device (VendorID:deviceID)
- `lsusb` : list USB devices
    - -v : verbose
    - -t : tree
- `nvidia-smi` : show GPU info
- `ifconfig` : show network info
- `iftop` : list TCP sockets
- `netstat -nat` : list TCP sockets
- `df -shc * | sort -rh` : show disk usage
    - -s : summary
    - -h : human readable
    - -c : show total
    - -b : bytes
    - --apparent size
    - -d [max depth] : max depth
- `free -h --si` : show how much RAM
- `htop` : list process, kill process
- `sensors` : show temperature
- `watch -t -n 1 "sensors | grep 'Core 0:'"` : show CPU temperature
- `nmap -Pn -p- -v [ip]` : find open ports
- `strace` : trace syscalls
- `cat /proc/[pid]` : procfs, running processes
- `cat /proc/meminfo` : memory info
- `cat /proc/cpuinfo` : CPU info (CPUID)
- `cat /proc/interrupts` : interrupts in
- `cat /proc/ioports` : IO ports
- `cat /proc/iomem` : MMIO
- `cat /proc/driver/nvidia/` : GPU info
- `cat /proc/stat` : all process stats
- `cat /proc/[pid]/stat` : process stats

## Kernel
- `lsmod` : list kernel modules
    - also `cat /proc/modules`
- `modprobe [module]` : load kernel module and dependencies
- `insmod [module].ko` : install kernel module
- `rmmod [module]` : remove kernel module
- `modinfo -F [info] [module]`: get info about kernel module
- `dmesg | tail -n 5` : show kernel log
    - -W : show live
- `ls -l /dev` : list device files
    - major, minor
- `cat /proc/devices` : list assigned device numbers
- `mknod [device] c [major] [minor]` : create character device
- `rmnod [device]`
- `head -c 1 [file]` : output the first byte of a file

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
- `0>` : stdin
- `1>` : stdout
- `2>` : stderr
- `2>&1` : stderr to stdout, can use `cmd | tee out.txt` to also print on screen

## Bash profile
- `~/.bashrc`
    - executed every new shell
- `~/.bash_profile`
    - executed once per login
    - inherit `~/.bashrc`

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
- `dnf erase [package]` : remove package+deps+config (careful!)
- `dnf list installed` : list installed packages
- `dnf list available` : list all availables packages
- `dnf list installed *pattern*`: list packages with pattern
- `dnf upgrade` : upgrade/update all packages
    - `-v` : verbose
    - `--exclude=kernel*,*nvidia*` : exclude some packages
- `dnf autoremove` : remove unused packages
- `dnf clean all` : clear cached packages
- `dnf history` : show dnf history
- `dnf repolist all` : list repos
- `dnf config-manager --add-repo [some_repo.repo]` : add repo
- `dnf config-manager --set-enabled [repo]` : enable repo
- `dnf config-manager --set-disabled [repo]` : disable repo
- `rm /etc/yum.repos.d/[repo]` : remove repo
- `dnf repository-packages [repo] list --installed` : list all packages installed from specific repo
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
