# CUDA - GPU memory

There are many kinds of memory in a GPU but in this section we are interested in RAM, the biggest chunk of memory used for textures and data.
The main characteristic used to describe RAM is its **size**, more RAM allows processing more data at a time. Its **bandwidth**, how fast can we transfer data to it, is also an important aspect that affects performance.

The specs of the memory used in the GeForce RTX 4090 is given below.

|||
|----|-----|
| **Memory size** | 24 GB |
| **Memory type** | GDDR6X |
| **Memory interface width** | 384-bit |
| **Memory clock (data rate)** | 21 Gbps |
| **Memory bandwidth** | 1008 GB/s |
| **PCI Express interface** | Gen 4 (x16: 31.508 GB/s) |

## Memory interconnect
To understand those specs we must understand how the CPU, GPU and the GPU memory are interconnected.

There is a link between the GPU and its RAM but there is also a link between the GPU and the CPU.
The bandwidth of the PCI-e bus is for the transfer of data between the GPU and the CPU, while the memory bandwidth is between the GPU and its GDDR RAM.

The PCI-e bus is not only used to transfer data between the CPU and the GPU but also to communicate and program the GPU via MMIO registers.

The bandwidth of GDDR will usually be much bigger than the bandwidth of PCI-e.

```
GPU
    [GDDR6X]
      |
    [GPU]
      | (PCI-e)
MOTHERBOARD
      | 
    [CPU] -- [DRAM controller] -- [DDR5]
        (PCI-e)
```

## GDDR
The type of RAM used in a GPU is usually _GDDR SDRAM (Graphics Double Data Rate Synchronous Dynamic Random-Access Memory)_, which is similar to the _DDR SDRAM_ used with the CPU but optimized for throughput instead of latency.

The _DDR (Double Data Rate)_ technology essentially transfers data on both the rising and falling edges of the memory clock signal, effectively doubling the data rate (2 bits of data can be transfered during each clock cycle).

The GDDR6X used in the RTX 4090 is the 6th generation of GDDR and is able to transmit 4 bits of data per cycle thanks to fancy signal modulation.

A single chip of GDDR has N data pins, in the case of 4090 = 384, each pin can transmit in parallel one bit at the memory clock rate.
DDR

1008 GB/s, GDDR size = 24GB
1008/24 = can W whole RAM 42 times in 1 second
doesnt fit int RAM, so its not about the data size but how much R/W per second can you do => how fast the RAM is
#memory access per seconds

## Memory bandwidth
The memory bandwidth is the number of bytes that can be transfered per second.
The theoretical maximum memory bandwidth can be computed as follow:
```
21 Gbps * 384 bit / 8 bit/byte = 1008 GB/s
```

memory clock speed
    Gbps (Giga Bits Per Second) = data rate
    GHz = base clock
    
    GDDR
        memory clock speed is usually described in terms of the data rate per pin
        not just the base clock.
            
    data rate: 21 Gbps
        clock * 8 / E9 * 4 (DDR + PAM4: two bits per symbol to be transmitted) instead of *2 (DDR)
        cycle/s * bit/byte bit/cycle

    https://www.reddit.com/r/pcmasterrace/comments/1b3xxyl/why_is_gddr6x_better_then_gddr6_in_gaming/

    PAM4 : 4 signal levels instead of 2 (2^2-bit=4)

Note that this is much higher than the maximum PCI-e 4.0 bandwidth of 31.508 GB/s (using x16: 16 lanes).
So the data transfer between the CPU and the GPU using PCI-e will be the bottleneck.

If its internal clock runs at 100 MHz, then the effective rate is 200 MT/s, because there are 100 million rising edges per second and 100 million falling edges per second of a clock signal running at 100 MHz.

## Effective memory bandwidth
In practice we rarely reach the maximum memory bandwidth.
To compute the effective memory bandwidth of a given CUDA kernel, we can use the kernel execution time:
```
bw = (R + W) / (t * 10^9) in GB/s

R: number of bytes read from VRAM
W: number of bytes write to VRAM
t: elapsed time (ms)
```

For our SAXPY example:
```
// read x and y, each an array of float (4 bytes)
R = N * 4 * 2
// write y
W = N * 4 * 1
bw = (N*4*3) / t
```

## References
- <https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf> (Appendix A)
- <https://en.wikipedia.org/wiki/GDDR6_SDRAM#GDDR6X>
- <https://www.micron.com/content/dam/micron/global/public/products/technical-marketing-brief/gddr6x-pam4-2x-speed-tech-brief.pdf>
