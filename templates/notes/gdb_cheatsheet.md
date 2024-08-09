# GDB cheatsheet

- `gdb ./[program]` : debug program with GDB
- `gdb --args ./[program] [args]` : debug program with GDB

must compile the program using flags `-O0 -g`.

## Basic
- `r`: run program
- `bt` : show call stack / backtrace
- `up` : move up call stack
- `down` : move down call stack
- `frame` : show stack frame
- `n` : next
- `s` : step into
- `c` : continue
- `finish` : step out of function
- `ni` : next instruction
- `si` : step into instruction
- `q` : quit

## Breakpoints
- `b [line]` : add breakpoint at line X of current file
- `b [function]` : add breakpoint at function X
- `b *[address]` : add breakpoint at address/pointer X
- `info break` : list breakpoints
- `clear` : delete all breakpoints
- `watch [X]` : add watchpoint on variable X

## Info
- `p [X]` : print variable X
- `p/x [X]` : print variable X in hexadecimal
- `p [c expression]` : print C expression
- `display [X]` : print variable X each step
- `what [X]` : print type of variable X
- `i frame` : show stack frame
- `i locals` : show local variables
- `i args` : show function args
- `i registers ax rip rbp cs ss ds` : show registers
- `display/i $pc` : show PC when changed
- `x/100xg $sp` : print stack memory
    - 100 : number of entries
    - x : hexadecimal
    - g : 8 bytes per entry
- `set var [X]` : change variable value

## Code
- `l` : shows the next set of code
- `l -` : show the prev set of code
- `l [line]` : show code on line X
- `l [start line, end line]` : show code at line S to E
- `l [function]` : show code of function X
- `disassemble` : show ASM code
- `file [code file]` : load code file
- `file [bin]` : load ELF bin and symbols

## Split view (TUI)
- `tui enable/disable` : enable tui for split view
- `layout split` : layout code/asm
- `layout asm` : layout asm
- `layout reg` : layout regisers

## Reverse debugging
- `target record-full` : enable reverse debugging
- `rn` : reverse next
- `rs` : reverse step
- `rc` : reverse continue

might not always work properly!

## Remote
- `tar rem [ip]:[port]` : connect to remote target (localhost -> :1234)
- `symbol-file [bin]` : load symbols
- `gdb -x=[script.gdb]` : load GDB script (text file with a list of GDB commands)

## Valgrind
- `valgrind ./[program]` : run program under valgrind
    - --leak-check=full : detect memory leaks, read after free

must compile the program using flags `-O0 -g`.
