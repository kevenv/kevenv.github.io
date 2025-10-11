# Fedora cheatsheet

## DNF
- `dnf search [package]` : search for package in repos
- `dnf info [package]` : get info about package
- `dnf install [package]` : install package
- `dnf remove [package]` : remove package
- `dnf erase [package]` : remove package+deps+config (careful!)
- `dnf list --installed` : list installed packages
- `dnf list --available` : list all availables packages
- `dnf list --installed *pattern*`: list packages with pattern
- `dnf upgrade --refresh` : upgrade/update all packages
    - `-v` : verbose
    - `--exclude=kernel*,*nvidia*` : exclude some packages
- `dnf autoremove` : remove unused packages
- `dnf clean all` : clear cached packages
- `dnf history` : show dnf history
- `dnf repo list --all` : list repos
- `dnf config-manager --add-repo [some_repo.repo]` : add repo
- `dnf config-manager --set-enabled [repo]` : enable repo
- `dnf config-manager --set-disabled [repo]` : disable repo
- `rm /etc/yum.repos.d/[repo]` : remove repo
- `dnf repository-packages [repo] list --installed` : list all packages installed from specific repo
- `dnf provides [file]` : find package that provides a file
- `dnf repoquery -l [package]` : list files in package
- `dnf repoquery --requires [package]`: list dependencies of package
- `dnf repoquery --whatrequires [package]` : list packages that depends on a package

## Services
- `systemctl status [service]` : get status of service
- `systemctl enable [service]` : enable service at boot
- `systemctl disable [service]` : disable service at boot
- `systemctl start [service]` : start service
- `systemctl stop [service]` : stop service
- `systemctl restart [service]` : restart service
- `systemctl list-units` : list services running

## Flatpak
- `flatpak install [app]` : install an app
- `flatpak list` : list installed apps
- `flatpak update` : update all apps
- `flatpak search [app]` : search for an app in Flathub repo
- `flatpak run [app]` : run an app

## COPR
Fedora COPR = AUR

- `sudo dnf copr enable [repo]/[package]`
- `sudo dnf install [package]`
