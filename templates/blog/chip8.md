# Chip8 emulator

intro

One day I got really intrigued about emulators so I read a lot about it and implemented the Chip8. It is usually the first emulator someone would implement due to it's simplicity. I implemented it all from scratch based on the specs I found on the internet. It was one of the most interesting and fun programming project I did!

have you ever wanted to know
how game emulator works?
what magic is neede to run console games on a desktop computer?

I believe that writing a Chip8 emulator is one of the best project to quickly understand how computers work.
I originally wrote one 10 years ago when I was still in high school?
it really opened my eyes and expanded my understanding 
yet relatively few people know about it.

It can be done in a weekend.
written in very few lines of code

In this article I will show you how to implement one in C using the SDL library for graphics.

## Emulation
emulator
	interpreter

simulate the behavior of a real CPU
allow us to run programs made for one CPU on another CPU
state: cpu,ram,rom..
I/O: kbd,display



## Computers
At the core of computers is the CPU.
cpu
    fetch,decode,exec
    instruction, opcode, asm
    formats
        big/little
        fixed size
    ISA
    regs
    clock,speed/freq
    synchronous
    manip bits,binary numbers,letters=ascii
    chips,transistors,bool algebra
stored program = ROM -> RAM
    newman arch
    stack
can comm with ext world via IO
    cpu ins
    io ports
    mmio

## Chip8
chip8 = VM ~soc
emulation impl as real HW for fun, might simplify code
RAM, mmap
!MMIO -> IO ports

|   |   |
| - | - |
| **CPU** | ~500 Hz |
| **RAM** | 4 KB |
| **ROM** | 3.5 KB |
| **Timers** | 2 x timer (8-bit), 60 Hz |
| **Display** | 64 x 32 monochrome (1-bpp), 8 x 15 sprites |
| **Keypad** | 16 keys |
| **Speaker** | Buzzer (1-bit) |

The memory map:
```
    [0 - 511] : Font
    [512 - 4095] : Program (ROM)
```
Notice that devices are not memory mapped, they can only be accessed via specific CPU instructions.

The Chip8 does not have any OS and can only run a single program at a time.

Programs never access the lower 512 bytes of RAM.

SDL hello
file structure

## ROM
User programs are stored in ROM chips (Read Only Memory) and loaded into RAM when the Chip8 resets.

As defined by the memory map above, programs are loaded into RAM at `0x200` and so the CPU will start fetching instructions from this address at reset.

load rom
    mmap

mmap
    [0-511] : font
        lower 512 bytes of memory (0x000-0x1FF), 
        and it is common to store font data there.

        most programs written for the original system
        begin at memory location 512 (0x200) and 
        do not access any of the memory below the
        location 512 (0x200).

    [512-4095] : rom

rom load
    @ 0x200

Where can find ROMs?
Which one is good to start implementing a Chip8 emulator?
    test-char
    pong
    blinky

```C
#include <stdio.h> // fopen
#include <stdlib.h> // malloc

struct rom_t {
    u8* bytes;
    u32 size;
};

bool rom_load(rom_t* rom, const char* file_path)
{
    FILE* file = fopen(file_path, "rb");
    if (!file) {
        return false;
    }

    // get file_size
    fseek(file, 0, SEEK_END);
    rom->size = (u32)ftell(file);
    fseek(file, 0, SEEK_SET);

    // read ROM
    rom->bytes = (u8*)malloc(rom->size);
    fread(rom->bytes, rom->size, 1, file);

    fclose(file);
    return true;
}

void rom_free(rom_t* rom)
{
    free(rom->bytes);
}
```

chip8:
```C
#include <string.h> // memcpy

void chip8_load_rom(chip8_t* chip8, rom_t* rom)
{
    memcpy(&RAM[PC], rom->bytes, rom->size);
}
```

init:
```C
int main(int argc, char* argv[])
{
    // load ROM
    rom_t rom;
    if (!rom_load(&rom, argv[1])) {
        return 1;
    }

    // init chip8
    chip8_t chip8;
    chip8_load_rom(&chip8, &rom);

    // cleanup
    rom_free(&rom);
}
```

## CPU

## Keypad
User inputs can be done via the _keypad_, consisting of 16 keys indexed from 0 to F.
The keys are laid out in the following way:
```
| 1 2 3 C |
| 4 5 6 D |
| 7 8 9 E |
| A 0 B F |
```

Games will often use the 2,4,6,8 keys as arrow keys:
```
|   2   |
| 4   6 |
|   8   |
```

The keypad is only accessible via the following CPU instructions:

- `LD Vx, K` (FX0A) : wait for any key press
- `SKP Vx` (EX9E) : skip next instruction if key is pressed
- `SKNP Vx` (EXA1) : skip next instruction if key is not pressed

In our implementation each device external to the Chip8 SoC such as the keypad has its own struct.
Chip8 can refer to it via pointers.
this is done to map the real hw

```C
#include <string.h> // memset

#define N_KEYS 16

struct keypad_t {
    bool keys[N_KEYS];
};

void keypad_reset(keypad_t* keypad)
{
    memset(keypad->keys, false, N_KEYS*sizeof(bool));
}

bool keypad_pressed(keypad_t* keypad, u8 key)
{
    return keypad->keys[key];
}

bool keypad_any_pressed(keypad_t* keypad, u8* key)
{
    for (u8 i = 0; i < N_KEYS; i++) {
        if (keypad->keys[i]) {
            *key = i;
            return true;
        }
    }
    return false;
}
```

impl
```C
bool chip8_tick(chip8_t* chip8)
{
    // ...

    // execute
    switch (op1) {
        case 0xE:
            switch (op2) {
                case 0x9E: // EX9E
                    PC = keypad_pressed(chip8->keypad, V[x]) ? PC+2 : PC;
                    break;
                case 0xA1: // EXA1
                    PC = !keypad_pressed(chip8->keypad, V[x]) ? PC+2 : PC;
                    break;
            }
            break;
        case 0xF:
            switch (op2) {
                case 0x0A: // FX0A
                    u8 key;
                    if (keypad_any_pressed(chip8->keypad, &key)) {
                        V[x] = key;
                        PC = PC+2; // skip next instruction
                    }
                    else {
                        PC = PC-2; // wait until pressed
                    }
                    break;
            }
            break;
    }

    // ...
}
```

stuff
```C
struct chip8_t {
    // ...
    keypad_t* keypad;
    // ...
};
```

Init: vhook to SDL
```C
int main(int argc, char* argv[])
{
    // ...

    // init chip8
    chip8_t chip8;
    keypad_t keypad;
    chip8.keypad = &keypad;
    keypad_reset(&keypad);
    
    // tick emulator
    bool running = true;
    while (running) {
        // ...

        // handle events
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
                break;
            }
        }

        // update
        update_keypad(&keypad);

        // ...
    }

    // ...
}
```

update like:
```C
void update_keypad(keypad_t* keypad)
{
    const u8* keys = SDL_GetKeyboardState(NULL);
    keypad->keys[0] = keys[SDL_SCANCODE_X];
    keypad->keys[1] = keys[SDL_SCANCODE_1];
    keypad->keys[2] = keys[SDL_SCANCODE_2];
    keypad->keys[3] = keys[SDL_SCANCODE_3];
    keypad->keys[4] = keys[SDL_SCANCODE_Q];
    keypad->keys[5] = keys[SDL_SCANCODE_W];
    keypad->keys[6] = keys[SDL_SCANCODE_E];
    keypad->keys[7] = keys[SDL_SCANCODE_A];
    keypad->keys[8] = keys[SDL_SCANCODE_S];
    keypad->keys[9] = keys[SDL_SCANCODE_D];
    keypad->keys[10] = keys[SDL_SCANCODE_Z];
    keypad->keys[11] = keys[SDL_SCANCODE_C];
    keypad->keys[12] = keys[SDL_SCANCODE_4];
    keypad->keys[13] = keys[SDL_SCANCODE_R];
    keypad->keys[14] = keys[SDL_SCANCODE_F];
    keypad->keys[15] = keys[SDL_SCANCODE_V];
}
```

## Display

## Timers
Two _timers_ are available in the Chip8:

- **Delay timer (DT)**, used for scheduling events.
- **Sound timer (ST)**, used for producing sounds.

Both timers consist of a 8-bit register used as counter.
The counter is automatically decremented at 60Hz until it reaches zero.

The only difference between the timers is that when `ST` is greater than zero, a sound is emitted through the speaker.

Timers are controlled via three CPU instructions:

- `LD Vx, DT` (FX07) : get DT
- `LD DT, Vx` (FX15) : set DT
- `LD ST, Vx` (FX18) : set ST

In our implementation the timers are part of the Chip8 SoC:
```C
#define DT    chip8->DT
#define ST    chip8->ST

struct chip8_t {
    // ...

    // Timers
    u8 DT; // delay timer, 60Hz
    u8 ST; // sound timer, 60Hz

    // ...
};

void chip8_reset(chip8_t* chip8)
{
    // ...

    DT = 0;
    ST = 0;

    // ...
}

void chip8_timers_tick(chip8_t* chip8)
{
    if (DT > 0) DT--;
    if (ST > 0) ST--;
}

bool chip8_tick(chip8_t* chip8)
{
    // ...

    // execute
    switch (op1) {
        case 0xF:
            switch (op2) {
                case 0x07: // FX07
                    V[x] = DT;
                    break;
                case 0x15: // FX15
                    DT = V[x];
                    break;
                case 0x18: // FX18
                    ST = V[x];
                    break;
            }
            break;
    }

    // ...
}
```

To increment the timers are the right rate:
```C
#define CPU_FREQ_HZ   500
#define TIMER_FREQ_HZ 60

int main(int argc, char* argv[])
{
    // ...

    // tick emulator
    u32 cycles = 0;
    bool running = true;
    while (running) {
        // tick @ 60Hz
        if (cycles >= CPU_FREQ_HZ / TIMER_FREQ_HZ) {
            cycles = 0;

            // ...
            chip8_timers_tick(&chip8);
            // ...
        }

        SDL_Delay((u32)(1.0f/CPU_FREQ_HZ*1000));
        cycles++;
    }

    // ...
}
```

## Speaker
For sound effects, the Chip8 includes a _speaker_ that can only do one tone, a single "beep" sound (1-bit audio). The speaker is ON whenever `ST` is greater than zero, otherwise it is OFF.

We use a simple finite state machine (FSM) to keep the speaker implementation decoupled from the SDL support code.

TODO: impl w FSM + SDL Mixer

```C
// RESET -> START -> PLAYING -> STOP -> RESET
enum speaker_state_t {
    SPEAKER_RESET,
    SPEAKER_START,
    SPEAKER_PLAYING,
    SPEAKER_STOP
};

struct speaker_t {
    speaker_state_t state;
};

void speaker_reset(speaker_t* speaker)
{
    speaker->state = SPEAKER_RESET;
}

void speaker_tick(speaker_t* speaker, u8 ST)
{
    if (speaker->state == SPEAKER_RESET && ST > 0) {
        speaker->state = SPEAKER_START;
    }
    else if(speaker->state == SPEAKER_PLAYING && ST == 0) {
        speaker->state = SPEAKER_STOP;
    }
}
```


Init it:
```C
int main(int argc, char* argv[])
{
    // ...

    // init chip8
    speaker_t speaker;
    speaker_reset(&speaker);

    // ...
}
```

And tick it:
```C
int main(int argc, char* argv[])
{
    // ...

    // tick emulator
    u32 cycles = 0;
    bool running = true;
    while (running) {
        // tick @ 60Hz
        if (cycles >= CPU_FREQ_HZ / TIMER_FREQ_HZ) {
            cycles = 0;

            // ...
            chip8_timers_tick(&chip8);
            speaker_tick(&speaker, chip8.ST);
            if (speaker.state == SPEAKER_START) {
                speaker.state = SPEAKER_PLAYING;
            }
            if (speaker.state == SPEAKER_STOP) {
                speaker.state = SPEAKER_RESET;
            }
            // ...
        }

        SDL_Delay((u32)(1.0f/CPU_FREQ_HZ*1000));
        cycles++;
    }

    // ...
}
```

conclusion

## References
- <https://en.wikipedia.org/wiki/CHIP-8>
- <http://devernay.free.fr/hacks/chip8/C8TECH10.HTM>
- <https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Technical-Reference>
- <https://github.com/mattmikolay/chip-8/wiki/Mastering-CHIP%E2%80%908>
- <https://chip-8.github.io/>
