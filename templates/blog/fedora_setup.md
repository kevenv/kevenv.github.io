# Fedora Setup

## Install Fedora
- install using ISO
    - enable third-party repos
- dnf update all
- reboot

## Install Nvidia drivers
See [Fedora + Nvidia]({{root}}blog/fedora_nvidia.html)

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

Cleanup:

- `dnf autoremove`

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

- gnome remote desktop : `settings/sharing/remote desktop`

### Keyboard shortcuts
- switch applications = disabled
- swtich windows = alt+tab
- take a screenshot interactively = disabled
- switch to next input source = alt+a
- switch to prev input src = shift+alt+a

### SSH
- `systemctl enable sshd.service`
- `systemctl start sshd.service`
- `/etc/ssh/sshd_config`

## Install apps
- veracrypt
```
build from source: https://launchpad.net/veracrypt/trunk/1.26.7/+download/veracrypt-1.26.7-setup.tar.bz2
```
- keepassXC
- freefilesync
- gnome tweaks
- dconf editor
- vlc
- screenshot tool
```
gnome-screenshot / gnu screenshot
cmd: gnome-screenshot -i -a
https://ubuntuhandbook.org/index.php/2022/04/get-back-gnome-screenshot-ubuntu-2204/
```
- dnf5
```
sudo dnf install dnf5
sudo ln -s /usr/bin/dnf5 /usr/local/bin/dnf
```
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
sudo dnf copr enable cboxdoerfer/fsearch
sudo dnf install fsearch
```
- strace
```
sudo dnf copr enable xfgusta/strace-with-colors
sudo dnf install strace-with-colors
```
- inkscape
- pinta
- remmina
- virtual machine manager
- imhex
- wireshark
- pulseview
- gtkwave
- gtkterm
- clion

## RPM Fusion
- `rpmfusion-nonfree-nvidia-driver`
- `rpmfusion-nonfree-updates` (discord)

## COPR
Fedora COPR = AUR

- `sudo dnf copr enable [repo]/[package]`
- `sudo dnf install [package]`
