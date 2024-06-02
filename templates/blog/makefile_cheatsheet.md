# Makefile Cheatsheet

## Usage
`make` looks for the file named `Makefile` in the CWD.

- `make` : make the first target
- `make all` : make all targets
- `make clean` : clean the build

### Options
- `-j [num of jobs]` : specify how many threads
- `-d` : show debug info
- `--debug` : show more debug info
- `-p` : show rules and variable values
- `--trace` : trace make (verbose)

## Target
```Makefile

all: target

target:	dep1 dep2
	build cmds

dep1:
    build cmds

dep2:
    build cmds

clean:
    clean cmds

.PHONY clean all
```

## Variable
- `VAR := VALUE` : set variable, expands immediately (at the time of assignment)
- `VAR = VALUE` : set variable, expands lazily (at the time of use)
- `$(VAR)` : get variable

### Multi-lines
```Makefile
VAR := VERY VERY VERY \
       VERY VERY LONG \
       CMD
```

## Common variables
- `CC` : path to the C compiler
- `CFLAGS` : C compiler flags
- `LD` : path to the C linker
- `LDFLAGS` : C linker flags
- `TARGET` : name of the executable
- `SRC` : list of all source files
- `OBJ` : list of all object files

## Special variables
- `%.o` : match all .o files
- `$@` : target
- `$<` : first dependency of target
- `$^` : all dependencies of target

For example:
```Makefile
output.txt: input1.txt input2.txt
    cat $^ > $@
# $^ : input1.txt input2.txt
# $@ : output.txt
# $< : input1.txt
```

## Other
- `.PHONY clean all` : make sure that the target always rebuilds
- `.DEFAULT_GOAL := all` : change the default target
- `$(SRC:.c=.o)` : generate list of .o from list of .c
- `$(addprefix $(BUILD_DIR), $(SRC:.c=.o))`
- `$(patsubst %.c, $(BUILD_DIR)/%.o, $(SRC))`

## Detect changes in .h dependencies
1. Use `gcc` with:
    - `-MMD` : generate dependency files (.d)
    - `-MP` : avoid errors if header file (.h) is deleted/renamed
2. Use `-include $(OBJ:.o=.d)` in the Makefile to include all dependency files (.d)
