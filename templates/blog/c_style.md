# C style

- use spaces (1 tab = 4 spaces)
- snake_case everything
- comments: `// comment` or `/* comment */`

## Names
- filename : `my_file.h`
- define/macro: `MY_CONSTANT`
- function: `my_function()`
- var/const var: `my_var`
- global: `g_global_var`
- ptr: `int* my_pointer` (pointer as part of type)

## Struct/Union
```C
typedef struct my_struct_t my_struct_t;
struct my_struct_t {
    int some_var;
};

void some_fct(my_struct_t my_struct)
{
    my_struct_t my_struct2;
    my_struct2.some_var = 3;
}
```

## Enum
```C
typedef enum my_enum_t my_enum_t;
enum my_enum_t {
    MY_ENUM_CASE_1,
    MY_ENUM_CASE_2,
};

void some_fct(my_enum_t my_enum)
{
    my_enum_t my_enum = MY_ENUM_CASE_1;
}
```

## Typedef
```C
typedef u64 physical_address_t
```

## Forward declaration
- faster compile
- less dependencies
- avoid circular dependencies
- defines interface

`typedef struct my_struct_t my_struct_t`
instead of
`struct my_struct_t`

## Braces
```C
int fct()
{
    if (condition) {
        do_something();
    }
    else {
        do_thing();
    }
}
```
- always use {}
- space between if and ()

## Switch
```C
switch (type) {
case case_1:
    do_stuff();
    break;
case case_2:
    do_other_stuff();
    break;
default:
    do_some_stuff();
    break;
}
```

## Const
- use for function args
- do not use within functions scope
- use in other cases **only if** strictly necessary, add a comment

## Headers
- includes in alphabetical order
- list what is used in each header : `#include <stddef.h> // NULL`

```C
/*
 * Copyright (c) 2024, Keven Villeneuve.
 *
 * SPDX-License-Identifier: MIT License
 */

#pragma once

#include "my_file.h"

#include <stdio> // std first
#include "some_other.h"

[...]

// one empty line at end
```

## Default int type
- use `u32` by default & counters
- use unsigned by default
    - overflow is well defined
    - easy to understand
    - < 0 invalid/impossible -> remove branching
    - better compiler warnings
    - tell intents
- use 32-bit by default
    - `u64` is native but 2x more space -> more cache miss
- never use `size_t` or `uint_fast32_t`
	- size depends on arch
    - long to type
	- name is weird : size or idx?
    - no one seems to agree on when to use
- use signed only if needed
- use `u64` only if need more space
- use specific size if needed

```C
#include <stdbool.h> // bool
#include <stddef.h> // NULL
#include <stdint.h> // uint_t

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

typedef int8_t i8;
typedef int16_t i16;
typedef int32_t i32;
typedef int64_t i64;
```

### References
This is very controversial, no one seems to agree...

- [https://www.reddit.com/r/cpp/comments/3fli94/should_i_use_signed_or_unsigned_ints/](https://www.reddit.com/r/cpp/comments/3fli94/should_i_use_signed_or_unsigned_ints/)
- [https://www.learncpp.com/cpp-tutorial/unsigned-integers-and-why-to-avoid-them/](https://www.learncpp.com/cpp-tutorial/unsigned-integers-and-why-to-avoid-them/)
- [https://www.quora.com/Should-I-prefer-unsigned-int-or-size_t-instead-of-int-for-loops-in-C](https://www.quora.com/Should-I-prefer-unsigned-int-or-size_t-instead-of-int-for-loops-in-C)
- [https://softwareengineering.stackexchange.com/questions/411128/is-using-64-bit-integers-long-long-faster-than-less-bits-ones](https://softwareengineering.stackexchange.com/questions/411128/is-using-64-bit-integers-long-long-faster-than-less-bits-ones)
- [https://www.learncpp.com/cpp-tutorial/fixed-width-integers-and-size-t/](https://www.learncpp.com/cpp-tutorial/fixed-width-integers-and-size-t/)
- [https://www.reddit.com/r/C_Programming/comments/e4hro6/when_to_use_size_t/](https://www.reddit.com/r/C_Programming/comments/e4hro6/when_to_use_size_t/)

## GCC flags
```
-Wall -Wextra -Wconversion -Werror
-Wpedantic -pedantic-errors ???
-Wno-sign-conversion -Wno-unused-variable -Wno-unused-function -Wno-unused-parameter
-std=c99
-O0 -g
```

## Utils
```C
// stringify a C expression
#define TO_STR(expr) #expr

// ceil(a / b)
#define DIV_CEIL(a, b) (((a) + (b)-1) / (b))

// align an address to a power of 2
#define ALIGN(p, a)  (((u64)(p) + (a)-1) & ~((a)-1))
```
