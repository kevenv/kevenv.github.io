# Bash Cheatsheet

## Useful commands
- `dirname [file]` : get path of a file
- `pushd [directory]` : push cwd to stack, set cwd to directory
- `popd` : pop stack to cwd
- `exit [status]` : terminate a script
- `set -e` : terminate script if any cmds exits with error
- `A || B` : exec B only if A fails

## Variables
- `VAR=VALUE` : set variable
- `${VAR}` : get variable
- `$VAR` : get variable
- `VAR=$(CMD)` : store result of cmd exec in variable

## Special variables
- `$0` : first arg of script = name of script
- `$@` : cmd args of script
- `$#` : num of args
- `$?` : exit status of last command executed
- `${BASH_SOURCE}` : filename+path of the current script being executed
- `#!/bin/bash` : Specifies which shell should be used to execute the script

## Conditions
```bash
if [ ... ]; then
    # something
elif [ ... ]; then
    # something else
else
    # something else
fi
```

### Conditional expressions
Always enclose variable with `" "`!

- `VAR == "debug"` : == string
- `"$VAR" != "string"` : != string
- `-eq 0` : == value
- `! -eq 0` : != value
- `-gt 0` : > value
- `-v VAR` : variable is set/exists
- `-z VAR` : variable is unset/empty
- `-n "$VAR"` : string in variable is empty
- `-f "file.txt"` : file exists
