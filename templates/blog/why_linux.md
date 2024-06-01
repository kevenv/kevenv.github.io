# Why Linux?

After using Windows most of my life, I chose to move to Linux because I am sick and tired of the new direction of Windows.
Unfortunately Linux isn't perfect either, it is much more fragile and does not work as well with proprietary stuff.

I am now in the stage of my life where I just want things to work.
I don't want to spend time debugging, configuring and fixing issues.
Life is too short, I want my computer to work whenever I need it so that I can focus on projects that I find interesting.

This is why my setup is now:

- Desktop with Fedora for programming projects
- Macbook with MacOS for casual stuff (web, email, video streaming, pictures...)

## Philosophy
After years of working in the software industry I have realized that
software can break in the most absurd stupid ways
due to thing that should have no link to each others but yet they somehow do.
Absolutely anything and everything can break it and Murphy's Law says that if there is a way for something to break it will.
The universe is against you on this, the second law of thermodynamics says that entropy only increases.

When we talk about "Linux" as an OS, we mean a linux _distribution_, meaning the Linux kernel with a bunch of packages and apps "taped" together.

I said that Linux is fragile, this is probably the main reason. It is not an OS but a collection of OS sharing most stuff but each one is annoyingly a little bit different from each other.
Everything is highly customizable, no one has the same configuration, leading to untested use cases and bugs!

On top of that, big components of the OS are developped by wastly different teams of people
from all over the world with sometimes hard philosophical opinions, leading to harsh disagreements and even project forks. No wonder it sometimes feels like an inconsistent mess.

This is why I now try to use everything by default. This is the most tested configuration which in theory should have lower chance of stupid bugs.

## Why Fedora?
### Fedora
- <i class='bx bx-plus' ></i> set it and forget, just works
- <i class='bx bx-plus' ></i> popular
    - used by kernel devs (Linus Torvalds)
- <i class='bx bx-plus' ></i> backed by Red Hat
    - commercial support
    - upstream of RHEL
    - major contributor of kernel, gnome, wayland, systemd, pulseaudio, kvm...
- <i class='bx bx-plus' ></i> target audience seems to be devs
- <i class='bx bx-plus' ></i> has the newest stuff first
- <i class='bx bx-minus' ></i> packages manager is slow

### Ubuntu
- <i class='bx bx-plus' ></i> most popular, most commercial support
- <i class='bx bx-minus' ></i> target everyone
    - going the same way as Windows (corporate BS)
- <i class='bx bx-minus' ></i> strange bugs
- <i class='bx bx-minus' ></i> outdated packages
- <i class='bx bx-minus' ></i> not a fan of Unity interface

### Arch
- <i class='bx bx-plus' ></i> great documentation
- <i class='bx bx-plus' ></i> pacman
- <i class='bx bx-plus' ></i> AUR
- <i class='bx bx-plus' ></i> rolling-release
    - in theory this is great but in practice it's annoying
- <i class='bx bx-minus' ></i> too much setup
- <i class='bx bx-minus' ></i> too much maintenance
- <i class='bx bx-minus' ></i> too much customization -> bugs

After using it daily for a few years, it is not for me.

## Why Gnome?
- Gnome
    - <i class='bx bx-plus' ></i> pretty & finished
    - <i class='bx bx-plus' ></i> default for Fedora (and many other)
    - <i class='bx bx-plus' ></i> best wayland support
    - <i class='bx bx-minus' ></i> new UI is strange, need extensions like `Dash to Panel` and `Arc Menu`
    - <i class='bx bx-minus' ></i> strong opinions (no tray icons seriously??)
- KDE
    - <i class='bx bx-plus' ></i> full featured
    - <i class='bx bx-minus' ></i> ugly, messy, bloated UI
    - <i class='bx bx-minus' ></i> wayland support is less good
- Xfce
    - <i class='bx bx-plus' ></i> light & fast
    - <i class='bx bx-minus' ></i> missing basic features
    - <i class='bx bx-minus' ></i> doesn't feel finished
    - <i class='bx bx-minus' ></i> no wayland support
    - <i class='bx bx-minus' ></i> not as many users, not as many devs -> bugs

## Why Windows sucks
- <i class='bx bx-plus' ></i> it just works
- <i class='bx bx-plus' ></i> best hardware compatibility by far
- <i class='bx bx-plus' ></i> most commercial support
- <i class='bx bx-plus' ></i> great for games

As a dev environment it is not that great:

- <i class='bx bx-minus' ></i> reboot automatically after updates and no way to disable it
- <i class='bx bx-minus' ></i> updates that need multiple reboots to install more updates
- <i class='bx bx-minus' ></i> install & update programs (setup.exe)
    - `winget` now but not everything is in there and doesn't always work
- <i class='bx bx-minus' ></i> install dev libs
    - `vcpkg` now
- <i class='bx bx-minus' ></i> terminal & shell is not that nice
    - `Windows Terminal` now but it's slow as hell
    - `WSL` but its not the same, it's a weird mix with weirds bugs, runs in a VM

Even for casual stuff it is becoming a massive pain to use:

- <i class='bx bx-minus' ></i> telemetry
- <i class='bx bx-minus' ></i> bloated
    - cortana
    - AI
    - web apps
- <i class='bx bx-minus' ></i> stupid UI changes -> messy inconsistent UI
    - mix of XP old ones, new ones, new new ones..
- <i class='bx bx-minus' ></i> slow apps
    - the new UI apps are slow as hell, the new image viewer is a disaster
- <i class='bx bx-minus' ></i> arbitrary hardware requirements (programmed obsolescence)

## Why MacOS sucks
- <i class='bx bx-plus' ></i> pretty & cohesive
- <i class='bx bx-plus' ></i> easy
- <i class='bx bx-plus' ></i> great integration with other Apple products
- <i class='bx bx-plus' ></i> better privacy than most other tech companies
- <i class='bx bx-plus' ></i> great hardware, battery life
- <i class='bx bx-minus' ></i> pain to develop on
    - feels like Unix but not Unix, tons of little incompatible annoyances
    - strong opinions, "the Apple way"
    - not a big fan of `homebrew`, not official, can break things
    - Xcode LOL!
- <i class='bx bx-minus' ></i> buggy, crashes (yes even with latest HW & SW doing casual stuff...)
- <i class='bx bx-minus' ></i> closed ecosystem (golden jail)
    - they do a very good job at making sure you only use their products and not the one of competitors..
- <i class='bx bx-minus' ></i> programmed obsolescence
- <i class='bx bx-minus' ></i> expensive hardware

## Why Linux sucks
- <i class='bx bx-plus' ></i> free
- <i class='bx bx-plus' ></i> open source
- <i class='bx bx-plus' ></i> light & fast
- <i class='bx bx-plus' ></i> nice dev environment
- <i class='bx bx-minus' ></i> buggy, fragile, things often break
- <i class='bx bx-minus' ></i> inconsistent: many distributions, many desktop environments
- <i class='bx bx-minus' ></i> distributing binaries is very hard
    - now there is `flatpak` and `snap` (great now we have two standards...)
- <i class='bx bx-minus' ></i> proprietary apps might not work well
- <i class='bx bx-minus' ></i> UI apps are often ugly
