# Fedora + Nvidia

## RPM fusion

### Organization
- free / non-free (nvidia drivers)
- release < updates < updates-testing < tainted
- view repos online: https://muug.ca/mirror/rpmfusion/nonfree/fedora/  

### Setup
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf config-manager --enable fedora-cisco-openh264
```

- [https://rpmfusion.org/Configuration](https://rpmfusion.org/Configuration)
- [https://rpmfusion.org/Howto/NVIDIA](https://rpmfusion.org/Howto/NVIDIA)
- [https://rpmfusion.org/Howto/CUDA](https://rpmfusion.org/Howto/CUDA)

### Repos
```
rpmfusion-nonfree-release
    akmod-nvidia-535.129.03-1.fc39
    kmod-nvidia-535.129.03-1.fc39
    xorg-x11-drv-nvidia-535.129.03-2.fc39
    xorg-x11-drv-nvidia-cuda-535.129.03-2.fc39
rpmfusion-nonfree-updates
    akmod-nvidia-550.90.07-1.fc39
    kmod-nvidia-550.90.07-1.fc39
    xorg-x11-drv-nvidia-550.90.07-1.fc39
    xorg-x11-drv-nvidia-cuda-550.90.07-1.fc39
rpmfusion-nonfree-release-tainted
    kmod-nvidia-open-550.90.07-1.fc39
    akmod-nvidia-open-550.90.07-1.fc39

rpmfusion-nonfree-nvidia-driver
    akmod-nvidia-550.90.07-1.fc39
    kmod-nvidia-550.90.07-1.fc39
    xorg-x11-drv-nvidia-550.90.07-1.fc39
    xorg-x11-drv-nvidia-cuda-550.90.07-1.fc39

Fedora third-party repos (Gnome Software)
    rpmfusion-nonfree-nvidia-driver
    rpmfusion-nonfree-steam

    subset of rpmfusion-nonfree-updates
```

## Nvidia drivers
types:

- display driver
- cuda driver

sources:

- from RPM fusion repo
    - display: `sudo dnf install akmod-nvidia`
    - cuda: `sudo dnf install xorg-x11-drv-nvidia-cuda`
- from NV repo
    - display+cuda: `sudo dnf -y module install nvidia-driver:latest-dkms`

## CUDA toolkit
- only from NV repo (NVIDIA official repo)
- view online: [https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/](https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/)
    
```
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/cuda-fedora39.repo
sudo dnf clean all

sudo dnf module disable nvidia-driver
sudo dnf install cuda-toolkit-12-4
```

drivers from RPM fusion + cuda toolkit from NV repo
    use drivers from RPM fusion because it updates at the same time as Fedora
    while NV might be much later...
    but the cuda toolkit is only available in the NV repo

    cuda packages from rpmfusion are mostly not compatible with cuda packages from NV official
    how to know if they are compatible?

## Install Nvidia drivers
install:
```
sudo dnf update -y
reboot
sudo dnf install akmod-nvidia
sudo dnf install xorg-x11-drv-nvidia-cuda
```
validate:
```
lspci -k | grep nvidia  # gpu
nvidia-smi              # gpu driver version
echo $XDG_SESSION_TYPE  # wayland enabled
```

## Install CUDA toolkit
```
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/cuda-fedora39.repo
sudo dnf clean all
sudo dnf module disable nvidia-driver # disable nvidia drivers from NV repo
sudo dnf install cuda-toolkit-12-4
```
add toolkit to path:
```
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}
```
avoid updating cuda toolkit:
```
dnf config-manager --set-disabled cuda-fedora39-x86_64 # avoid updating cuda toolkit, conflicts w RPM fusion
dnf clean all
reboot
```
validate:
```
nvcc --version # can call cuda compiler
```

## Debug
"modular filtering" : `nvidia-driver` module in `cuda-fedora39.repo` conflicts with RPM fusion.

- `sudo dnf module list`
- `sudo dnf module disable [module]`

## Nvidia open source kernel drivers
https://download.nvidia.com/XFree86/Linux-x86_64/555.42.02/README/kernel_open.html

## Open source drivers (nouveau)
nvidia
nvidia_modeset
nvidia_drm
nvidia_uvm
nvidia-peermem

blacklist nvidia_modeset nvidia_drm
w modprobe.blacklist
rd.driver.blacklist

add RUN+="/usr/libexec/gdm-runtime-config set daemon WaylandEnable true to end of /usr/lib/udev/rules.d/61-gdm.rules

## Manual install
https://www.if-not-true-then-false.com/2015/fedora-nvidia-guide/
https://www.if-not-true-then-false.com/2018/install-nvidia-cuda-toolkit-on-fedora/
