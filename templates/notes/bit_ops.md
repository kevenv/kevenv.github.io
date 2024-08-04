# Bitwise operations

## Manipulating bits
|Operator|Name|Example|
|--|----|-------|
|~|not|~1010 = 0101|
|&|and|1011 & 0011 = 0011|
|`|`|or|1011 `|` 0011 = 1011|
|^|xor|1011 ^ 0011 = 1000|
|<<|left shift|1011 << 1 = 0110|
|>>|right shift|1011 >> 1 = 0101|

### Test
Test if bit *i* of *value* is set to 1.
```C
(value & ((u32)1 << i)) != 0
```
ex:
```
   0 1 1 1  value
&  0 1 0 0  (1 << i)
   -------
=  0 1 0 0  
```

### Get
Get bit *i* of *value*.
```C
bit = (value >> i) & ((u32)1)
```

### Set
Set bit *i* of *value* to 1.
```C
value |= ((u32)1 << i)
```
ex:
```
   0 0 1 1  value
|  0 1 0 0  (1 << i)
   -------
=  0 1 1 1
```

### Clear
Set bit *i* of *value* to 0.
```C
value &= ~((u32)1 << i)
```
ex:
```
~  0 1 0 0   (1 << i)
=  1 0 1 1  ~(1 << i)

   0 1 1 1  value
&  1 0 1 1  ~(1 << i)
   -------
=  0 0 1 1
```

### Toggle
Toggle bit *i* of *value* (1 <-> 0).
```C
value =^ ((u32)1 << i)
```
ex:
```
   0 1 1 1  value
^  0 1 0 0  (1 << i)
   -------
=  0 0 1 1

   0 0 1 1  value
^  0 1 0 0  (1 << i)
   -------
=  0 1 1 1
```

### Change
Set bit *i* of *value* to *n* (0 or 1).
```C
value = (value & ~((u32)1 << i)) | (n << i);
```
or
```C
if (n) {
    value |= ((u32)1 << i); // set
} 
else {
    value &= ~((u32)1 << i); // clear
}
```

## Bit flag / bit field

```C
flags |= FLAG1 | FLAG2; // set flags
flags &= ~FLAG3; // clear flags
if (flags & FLAG1) { // check flag
    // ...
}
```

## Bitmask
```C
mask = 0x000F000F;
masked_value = value & mask;
```

## Binary numbers (Base 2)
| Symbol | Value |
|--------|-------|
| 0      | 0     |
| 1      | 1     |

The syntax in C is `0b01010111`.

## Hexadecimal numbers (Base 16)
| Symbol | Value |
|--------|-------|
| 0      | 0     |
| 1      | 1     |
| 2      | 2     |
| 3      | 3     |
| 4      | 4     |
| 5      | 5     |
| 6      | 6     |
| 7      | 7     |
| 8      | 8     |
| 9      | 9     |
| A      | 10    |
| B      | 11    |
| C      | 12    |
| D      | 13    |
| E      | 14    |
| F      | 15    |

The syntax in C is `0xF0FD`.

## Conversions
TODO:

- hex <-> bin
    - 1 hex = 4 bits (2^4=16)
- bin <-> dec
    - convert to hex first
- hex <-> dec
    - 0-9 : same
    - A-F : 10-15

## Negative numbers (2s complement)
- Negative numbers are also known as _signed integers_.
- They are usually encoded using _Two's complement_.
    - MSB = sign bit (0 = positive, 1 = negative)
    - only one representation for zero = 0
    - range `[-n, n/2-1]`, where n = number of bits
    - addition is the same as unsigned integers

### Example
```
n = 3
2^3 = 8

unsigned:
[0,7]

signed:
[-(8/2),(8/2-1)]
[-4,3]
```

|Bits|Unsigned|Signed|
|----|--------|------|
|000|0|0|
|001|1|1|
|010|2|2|
|011|3|3|
|100|4|-4|
|101|5|-3|
|110|6|-2|
|111|7|-1|

### Convert unsigned <-> signed
ex:
```C
// signed = ~unsigned + 1
2 = 0b010
-2 = ~2 + 1 = ~0b010 + 0b001 = 0b101 + 0b001 = 0b110

// unsigned = ~(signed - 1) or
// unsigned = ~signed + 1
-2 = 0b110
2 = ~(-2) + 1 = ~0b110 + 0b001 = 0b001 + 0b001 = 0b010
```

## Addition (+)
```
      (1)(1)
    1  0  1  1
+   0  0  1  1
    ----------
=   1  1  1  0
```

## Substraction (-)
Substraction is the same as addition with a negative number (2s complement).

ex: 2 - 3 = 2 + (-3) = -1
```
           unsigned  signed
    0 1 0     2         2
+   1 0 1     5        -3
    -----
=   1 1 1     7        -1
```
