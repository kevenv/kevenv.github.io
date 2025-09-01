# Fedora + Nvidia

## Install

### 1. Add RPM fusion repos
```bash
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

### 2. Install Nvidia drivers from RPM fusion
install:
```
sudo dnf update
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

### 3. Install CUDA toolkit
```
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora41/x86_64/cuda-fedora41.repo
sudo dnf clean all
sudo dnf module disable nvidia-driver # disable nvidia drivers from CUDA repo
sudo dnf install cuda-toolkit-12-9
```
add toolkit to path:
```
export PATH=/usr/local/cuda-12.9/bin${PATH:+:${PATH}}
```
avoid updating CUDA toolkit:
```
dnf config-manager --set-disabled cuda-fedora41-x86_64 # avoid updating CUDA toolkit, conflicts w RPM fusion
dnf clean all
reboot
```
validate:
```
nvcc --version # can call CUDA compiler
```

## Nvidia
1. GPU drivers
    - display driver
    - cuda driver
2. CUDA toolkit

## GPU drivers
types:

- proprietary (deprecated)
- proprietary, open kernel modules
- open source (nouveau)
	- only display drivers

sources:

- from RPM fusion repo (Fedora)
    - display: `sudo dnf install akmod-nvidia`
    - cuda: `sudo dnf install xorg-x11-drv-nvidia-cuda`
    - precompiled kernel modules
	- latest drivers
	- defaults to open kernel modules (for new GPUs)
	- no CUDA toolkit
- from CUDA repo (Nvidia)
    - display+cuda: `sudo dnf -y module install nvidia-driver:latest-dkms`
    - DKMS compiled kernel modules
	- defaults to open kernel modules
	- drivers are older
	- CUDA toolkit

## RPM fusion

### Groups
- free / non-free (nvidia drivers)
- release < updates < updates-testing < tainted
- view repos online: <https://muug.ca/mirror/rpmfusion/nonfree/fedora/>

### Setup
```
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf config-manager --enable fedora-cisco-openh264
```

- <https://rpmfusion.org/Configuration>
- <https://rpmfusion.org/Howto/NVIDIA>
- <https://rpmfusion.org/Howto/CUDA>

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

## Use open kernel modules with RPM fusion

### Pre-build
v575+: `akmod-nvidia` now has auto detection to switch to open when GPU supports it.

### From source
```
sudo dnf install rpmfusion-nonfree-release-tainted
sudo dnf swap akmod-nvidia akmod-nvidia-open
```

<https://rpmfusion.org/Howto/NVIDIA#Kernel_Open>

<https://discussion.fedoraproject.org/t/testers-required-nvidia-driver-in-rpmfusion-nonfree-updates-testing/154781/3>

## Install CUDA toolkit and drivers from CUDA repo
```
sudo dnf install kernel-devel-matched kernel-headers
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/cuda-fedora39.repo
sudo dnf clean expire-cache
sudo dnf install --allowerasing nvidia-open
sudo dnf clean all
sudo dnf -y install cuda-toolkit-12-9
sudo reboot
nvidia-smi
nvcc --version
```

Now using open kernel modules by default:

<https://developer.nvidia.com/blog/nvidia-transitions-fully-towards-open-source-gpu-kernel-modules/>
<https://github.com/NVIDIA/open-gpu-kernel-modules>

580.76.05, 12/08/2025
<https://www.nvidia.com/en-us/drivers/details/252613/>
<https://us.download.nvidia.com/XFree86/Linux-x86_64/580.76.05/README/kernel_open.html>
<https://www.phoronix.com/news/NVIDIA-580.76.05-Linux>

## CUDA toolkit
- only from CUDA repo (NVIDIA official repo)
- view online: <https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/>

```
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora39/x86_64/cuda-fedora39.repo
sudo dnf clean all

sudo dnf module disable nvidia-driver
sudo dnf install cuda-toolkit-12-4
```

drivers from RPM fusion + CUDA toolkit from CUDA repo
    use drivers from RPM fusion because it updates at the same time as Fedora
    while NV might be much later...
    but the CUDA toolkit is only available in the CUDA repo

    CUDA packages from rpmfusion are mostly not compatible with CUDA packages from NV official
    how to know if they are compatible?

## Debug
"modular filtering" : `nvidia-driver` module in `cuda-fedora39.repo` conflicts with RPM fusion.

- `sudo dnf module list`
- `sudo dnf module disable [module]`

## Manual install
<https://www.if-not-true-then-false.com/2015/fedora-nvidia-guide/>

<https://www.if-not-true-then-false.com/2018/install-nvidia-cuda-toolkit-on-fedora/>
