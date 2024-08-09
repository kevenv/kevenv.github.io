# CUDA Tutorial 1 - Setup

Welcome to this tutorial on CUDA! Before we get started we should setup our development environment.

## Installation
1. Install the latest version of the "CUDA Toolkit".

    Download and follow the instructions at
    [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads) to install the toolkit corresponding to your system.

    In my case, I am using Fedora so I need to download and install:

    `Linux / x86_64 / Fedora / 39 / rpm (network)`

2. Reboot your system to make sure that everything is setup and initialized properly.

3. Add the toolkit to your system `PATH`:

    `export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}`

## Validation
Once the CUDA toolkit is installed, it is good to verify that everything works as expected. The best way to do that is to build and run the [cuda-samples](https://github.com/NVIDIA/cuda-samples):
```
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples
make
```

You can then run a sample such as:
```
./Samples/0_Introduction/vectorAdd/vectorAdd
./Samples/5_Domain_Specific/nbody/nbody
```

## First kernel
Now that we know that the CUDA toolkit is installed and working, let's write our first CUDA program.

Create a new file named `hello.cu` with the following code:
```CUDA
#include <stdio.h> // printf

__global__ void hello()
{
    printf("hello from GPU!\n");
}

int main()
{
    printf("hello from CPU!\n");
    
    hello<<<1,1>>>();
    cudaDeviceSynchronize();
    return 0;
}
```

We can immediately see the resemblance to usual C code however some things are different.

The `__global__` attribute signals that the given function should be run on the GPU instead of the CPU, in CUDA parlance this is known as a "CUDA kernel".

To launch our `hello` kernel we must use the syntax `hello<<<1,1>>>()`.
The meaning of the `<<<1,1>>>` will be explained in the next tutorial in details but in this case it specifies that the kernel should run only on a single thread.

Finally we must call `cudaDeviceSynchronize()` to ensure that the kernel finishes executing since kernels on the GPU runs asynchronously to the CPU.

Note that we can use `printf()` on the GPU (and CPU) with `#include <stdio.h>`.

To compile our program we must use the `nvcc` compiler `nvcc hello.cu -o hello`.
After running our program with `./hello` we should see "hello world!" printed on the screen.

## Tools
When developping CUDA programs, a bunch of tools can be useful:

- Find the GPU: `lspci -v | grep VGA`
- GPU driver version: `cat /proc/driver/nvidia/version`
- GPU driver in use: `lspci -n -n -k | grep -A 2 -e VGA -e 3D`
- CUDA compiler version: `nvcc --version`
- Info about the GPU: `nvidia-smi`
- GPU process monitor: `nvtop`

The [cuda-samples](https://github.com/NVIDIA/cuda-samples) contains useful tools as well:

- GPU info: `./Samples/1_Utilities/deviceQuery`
- Test GPU bandwidth: `./Samples/1_Utilities/bandwidthTest/`

### Debugger
It is also worthwhile to learn to use a CUDA debugger such as the [Nsight Visual Studio Code Edition](https://marketplace.visualstudio.com/items?itemName=NVIDIA.nsight-vscode-edition).
As a bonus you also get syntax highlighting and intellisense.

For this to work, make sure that the CUDA toolkit is in your system `PATH` and to use `nvcc -g -G -O0` when compiling kernels.
```
-g  : Generate host-side debug information (CPU).
-G  : Generate device-side debug information (GPU). 
-O0 : Disable optimizations.
```

## Next
This concludes the first tutorial.
Our first kernel didn't do much, in fact it didn't take advantage of the GPU at all since it was running on a single thread.
In the [next one]({{root}}blog/cuda_saxpy.html) we will see how to write a more useful kernel and wake up that GPU!

The source code for this tutorial is available on [GitHub](https://github.com/kevenv/cuda_exercises/tree/master/hello).
