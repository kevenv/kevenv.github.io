# Git Cheatsheet

## Flow
```
[Working directory] -> [Staging Area (Index)] -> [Repository] -> [Remote]
                   add                      commit           push
```

## Basic
- `git init` : init directory as a git repo
- `git clone [url]` : clone repo
- `git branch` : list branches
- `git checkout [branch]` : switch branch
- `git checkout -b [branch]` : create new branch
- `git checkout [commit]` : switch branch to specific commit
- `git fetch` : fetch changes
- `git pull` : fetch + merge changes
- `git push` : push changes
    - `git push origin [branch]` : push branch
    - `git push --force origin [branch]` : push branch after rebase
- `git add [file]` : add changes
    - `git add .` : add all changes
    - `git add -p` : add changes interactively
- `git commit -m "[message]"` : commit changes
- `git status` : status of local repo
- `git diff [file a] [file b]` : diff two files
    - `--cached` : diff the added files
    - `-b` : ignore endlines
    - `-w` : ignore whitespaces
    - `--name-only` : only list files
- `git -c core.fileMode=false diff` : diff two files, ignore file permissions

## Stash & Patch
- `git stash`
    - `save "[message]"` : stash current changes
    - `list` : show stash
    - `pop` : pop stash
    - `drop` : drop stash
    - `apply stash@{0}` : apply stash
    - `show -p stash@{0}` : show stash changes
- `git show -p stash@{0} > [patch file].patch` : create patch from stash
- `git diff > [patch file].patch` : create patch from unstaged changes
- `git diff --cached > [patch file].patch` : create patch from staged changes
- `git apply [patch file].patch` : apply patch file

## Info
- `git log` : show changes log
- `git remote -v` : list remote
- `git remote show origin` : info on remote
- `git remote add [remote name] [remote url]` : add remote

## Merge
- `git rebase [src branch]` : rebase current branch from another branch
- `git merge [branch]` : merge branch into current branch
- `git cherry-pick [commit]` : pull specific commit

## Revert
- `git reset --soft [commit]` : unstage commit
- `git reset --hard [commit]` : undo commit
- `git checkout [file]` : revert local change to a file
- `git reset --hard HEAD` : revert all local changes
- `git reset --soft HEAD~1` : undo local commit, not pushed yet
- `git revert [commit]` : create revert commit
- `git clean -xdf`
    - `-n` : dry run
    - `-x` : ignore `.gitignore`
    - `-d` : recursive
    - `-f` : force
    - `-X` : only ignored files

## Submodules
- `git clone --recursive` : clone with submodules
- `git submodule update --init --recursive` : pull submodules after clone
- `git submodule add [submodule url]` : add submodule

### Remove submodule
1. `git rm [submodule]`
2. `rm -rf .git/modules/[submodule]`
3. `git config --remove-section submodule.[submodule]`
4. `git commit`

## Binary files - LFS (Large File Storage)
1. `git lfs install` : install LFS, once per user
2. `git lfs track "*.[file type]"` : add file type to track with LFS
3. `git add .gitattributes` : make sure that this is tracked

## Config
- `cat ~/.gitconfig` : show git config
```
[user]
	name = [FIRST NAME] [LAST NAME]
	email = [EMAIL]
[credential]
	helper = store
[log]
	date = local
[format]
	pretty = format:%C(yellow)%h %Cblue%>(12)%ad %Cgreen%<(7)%aN%Cred%d %Creset%s
```

## GitHub password
GitHub is no longer accepting account passwords, need to use PAT (Personal Access Token).

- Create a PAT using [https://github.com/settings/tokens](https://github.com/settings/tokens)
- `git config --global credential.helper store`
    - Stores the PAT in `~/.git-credentials` (plain text).
- `git pull`
    - Enter the PAT as password, won't be asked ever again.
