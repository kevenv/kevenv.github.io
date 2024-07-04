# Fedora Setup

## Install Fedora
- install using ISO
    - enable third-party repos
- dnf update all
- reboot

## Install NV drivers
- nv driver
- cuda driver
- wayland

## Install Wayland
- switch wayland/xorg : via login screen
- know which app is using Xwayland : `xlsclients`

### Chrome
```
chrome://flags/
"Preferred Ozone platform" = auto
```

### Electron apps
```
source ~/.bash_profile
    export ELECTRON_OZONE_PLATFORM_HINT=auto
        auto
        wayland
        x11

cp /usr/share/applications/code.desktop ~/.local/share/applications/code
    Exec=/usr/share/code/code --new-window %F
    --enable-features=UseOzonePlatform,WaylandWindowDecorations --ozone-platform=wayland
```
    
### SDL apps
```
export SDL_VIDEODRIVER=wayland
```

## Remove useless apps
Remove using "Gnome Software":

- calendar
- weather
- online account
- thunderbird

## Install Gnome Extensions
```
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo`
flatpak install flathub com.mattjakeman.ExtensionManager`
```
- Arc Menu
- Dash to Panel
- system-monitor-next
- freon

## Configure
config gnome + exts

## Install apps
- veracrypt
```
build from source: https://launchpad.net/veracrypt/trunk/1.26.7/+download/veracrypt-1.26.7-setup.tar.bz2
```
- keepassXC
- FreeFileSync
- gnome tweaks
- dconf editor
- screenshot tool
```
gnome-screenshot
cmd: gnome-screenshot -i -a
https://ubuntuhandbook.org/index.php/2022/04/get-back-gnome-screenshot-ubuntu-2204/
```
- htop

- chrome
```
sudo dnf install fedora-workstation-repositories
sudo dnf config-manager --set-enabled google-chrome
sudo dnf install google-chrome-stable
```
- sublime text
- sublime merge
```
sudo rpm -v --import https://download.sublimetext.com/sublimehq-rpm-pub.gpg
sudo dnf config-manager --add-repo https://download.sublimetext.com/rpm/stable/x86_64/sublime-text.repo
sudo sudo dnf install sublime-text
```
- vscode
```
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null
dnf check-update
sudo dnf install code
```
- insync
```
sudo rpm --import https://d2t3ff60b2tol4.cloudfront.net/repomd.xml.key
nano /etc/yum.repos.d/insync.repo
    [insync]
    name=insync repo
    baseurl=http://yum.insync.io/fedora/$releasever/
    gpgcheck=1
    gpgkey=https://d2t3ff60b2tol4.cloudfront.net/repomd.xml.key
    enabled=1
    metadata_expire=120m
sudo yum install insync
```
- discord
```
sudo dnf install https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf clean all
sudo dnf install discord

nano ~/.config/discord/settings.json
    "SKIP_HOST_UPDATE": true
```

## Install extra apps
- fsearch
```
dnf copr enable cboxdoerfer/fsearch
dnf install fsearch
```
- imhex
- inkscape
- pinta
- remmina
- virtual machine manager

## RPM Fusion repos
- `rpmfusion-nonfree-nvidia-driver`
- `rpmfusion-nonfree-updates` (discord)

## COPR
Fedora Copr = AUR
