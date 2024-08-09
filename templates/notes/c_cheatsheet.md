# C cheatsheet

## GCC flags
```
-Wall -Wextra -Wconversion -Werror
-Wpedantic -pedantic-errors ???
-Wno-sign-conversion -Wno-unused-variable -Wno-unused-function -Wno-unused-parameter
-std=c99
-O0 -g
```

## Restrict
- hints to compiler that for the lifetime of the pointer, no other pointer will be used to access the object to which it points
- limits the effects of pointer aliasing (dst == src)
- allows the compiler to make optimizations
- <https://en.wikipedia.org/wiki/Restrict#:~:text=In%20the%20C%20programming%20language,object%20to%20which%20it%20points>

## Utils
```C
// stringify a C expression
#define TO_STR(expr) #expr

// ceil(a / b)
#define DIV_CEIL(a, b) (((a) + (b)-1) / (b))

// align an address to a power of 2
#define ALIGN(p, a)  (((u64)(p) + (a)-1) & ~((a)-1))
```
