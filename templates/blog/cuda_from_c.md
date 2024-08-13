# CUDA from C

When first learning CUDA, we usually define and run kernels within the same `.cu` file and compile it using the CUDA compiler `nvcc`, but what if we want to integrate CUDA to an existing C codebase? In this article, I will show you how to launch CUDA kernels from usual C code.

## Basic kernel
Starting from the basic "hello world" example:

### kernel.cu
```CUDA
#include <stdio.h> // printf

__global__ void hello(int value)
{
    printf("hello from GPU! %d\n", value);
}

int main()
{
    printf("hello from CPU!\n");

    int value = 42;
    hello<<<1,1>>>(value);
    cudaDeviceSynchronize();
    
    cudaError_t error = cudaGetLastError();
    if (error != cudaSuccess) {
        fprintf(stderr, "CUDA ERROR: %s\n", cudaGetErrorString(error));
    }

    printf("done\n");

    return 0;
}
```

## CUDA from C

We move the `main()` function to `app.c`, leaving only the CUDA kernel in `kernel.cu`.

### kernel.cu
```CUDA
#include <stdio.h> // printf

__global__ void hello(int value)
{
    printf("hello from GPU! %d\n", value);
}

extern "C" void hello_kernel(int value)
{
    hello<<<1,1>>>(value);
}
```

### kernel.h
```C
#pragma once

void hello_kernel();
```

### app.c
```C
#include <cuda_runtime.h> // CUDA runtime API
#include <stdio.h> // printf
#include "kernel.h"

int main()
{
    printf("hello from CPU!\n");

    int value = 42;
    hello_kernel(value); // can launch CUDA kernel from normal C code!
    cudaDeviceSynchronize();
    
    cudaError_t error = cudaGetLastError();
    if (error != cudaSuccess) {
        fprintf(stderr, "CUDA ERROR: %s\n", cudaGetErrorString(error));
    }

    printf("done\n");

    return 0;
}
```

We also must wrap the kernel launch within a C function to able to call it from normal C code since the `<<< >>>` syntax is specific to the CUDA compiler `nvcc` and not supported by C compilers.

Finally, we must include `<cuda_runtime.h>` in `app.c` to access functions from the CUDA runtime API such as `cudaDeviceSynchronize()`.

## Build
To build the application we must first compile the CUDA kernel without linking using the CUDA compiler:
```bash
nvcc -c kernel.cu -o kernel.o
```
The `-c` flags compiles the `kernel.cu` source file into an object file `kernel.o` without linking it into an executable.

We then compile the rest of app using a C compiler:
```bash
CFLAGS := -I/usr/local/cuda/include
LDFLAGS := -L/usr/local/cuda/lib64 -lcuda -lcudart 
gcc $(CFLAGS) $(LDFLAGS) app.c kernel.o -o app
```
Linking to CUDA is done via:

- `-lcuda` : libcuda.so (CUDA driver API)
- `-lcudart` : libcudart.so (CUDA runtime API)

The `-I` flag adds a directory to the includes path and the `-L` flag adds a directory to the shared library (.so) search path.

That's it, you can now enjoy CUDA within your existing C code!
