# CUDA - SAXPY

In this article we will create a CUDA kernel that implements _SAXPY_ (Single-precision A X Plus Y), one of the core routine of [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms), a standard linear algebra library commonly used for scientific computing.
The SAXPY function combines vector addition and scalar multiplication:
```C
y = a*x + y

// x,y : vectors of N dimensions (float32)
// a : scalar (float32)
```

## CPU implementation
Let's first see how to implement this on the CPU:
```C
void saxpy_cpu(int n, float a, float* x, float* y)
{
    for (int i = 0; i < n; i++) {
        y[i] = a*x[i] + y[i];
    }
}
```

To use this function, we need some code to initialize the vectors and call the function with those vectors as arguments:
```C
int main()
{
    const int N = 100000000;
    const float a = 2.0f;
    float* x = (float*)malloc(N * sizeof(float));
    float* y = (float*)malloc(N * sizeof(float));
    for (int i = 0; i < N; i++) {
        x[i] = i;
        y[i] = 2.0f*i;
    }

    saxpy_cpu(n, a, x, y);

    free(x);
    free(y);
    return 0;
}
```

## GPU architecture
To implement this function on the GPU we must understand how the GPU execute programs.

A GPU is basically a processor with a ton of cores to compute many things in parallel.

The GPU is a multi-cores processor that is optimized for throughput instead of latency.
A core on a GPU is called a "Streaming Multiprocessor" or "SM" for short.

Each SM is able to run many threads.

The name of the game in GPU programming is to assign useful work to as many SM as possible, keep the GPU busy as often as possible.
This will result fast computation.
doing computation in parallel.
if the computation can be separated without introducing too much communication.

For SAXPY we can easily see that each component of the vector can be added independently so in the best case we would have as many threads as the number of dimensions of the vector. If all threads compute at the same time the operation essentially goes from O(N) to O(1). In order word we can "unroll" the loop.

When we define a kernel, this function will run on N threads in parallel.
each thread runs the same code but will have different exec context.

```CUDA
__global__ void saxpy(int n, float a, float* x, float* y)
{
    y[i] = a*x[i] + y[i]; // where i is the thread's index;
}
```

## CUDA execution model
In CUDA the threads are separated and organized as a **grid of blocks**
and a **block of threads** to map to the capabilities of the GPU.

TODO: diagram

The index of the current thread can be calculated using the following built-in variables:
```CUDA
threadIdx // index of the current thread in a block
blockIdx  // index of the current block in a grid
blockDim  // dimensions of a block
```
These variables are accessible anywhere within a CUDA kernel and are assigned automatically by the hardware for each thread and block.

To help map the problem to the GPU, the CUDA API support multiple dimensions (up to 3D) on thread indexing.
If the array is 2D we use 2D indexing, if the array is 3D we use 3D indexing.

```CUDA
threadIdx.x   threadIdx.y   threadIdx.z
blockIdx.x    blockIdx.y    blockIdx.z
blockDim.x    blockDim.y    blockDim.z
```

CUDA kernels are launched via the `kernel_name<<<grid_dim, block_dim>>>()` syntax. For example:
```CUDA
dim3 grid_dim(4,4,2);    // grid of 4x4x2 blocks
dim3 block_dim(16,16,1); // block of 16x16x1 threads
kernel_name<<<grid_dim, block_dim>>>(); // kernel launch
```
If only one dimension is used then we can use a shorter version:
```CUDA
kernel_name<<<4,16>>>(); // <<<num_blocks, threads_per_block>>>
```

### SAXPY kernel
Now let's get back to our SAXPY problem.
If the number of elements `N` is equal to the number of `threads_per_block`, then only a single block is needed.
```CUDA hl_lines="3 10 12"
__global__ void saxpy(int n, float a, float* x, float* y)
{
    int i = threadIdx.x;
    y[i] = a*x[i] + y[i];
}

int main()
{
    // ...
    int N = 32;
    int threads_per_block = 32;
    int num_blocks = 1;
    saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
    // ...
}
```

In the case of `N = 64`, two blocks would be needed.
```CUDA hl_lines="3 10 12"
__global__ void saxpy(int n, float a, float* x, float* y)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x; // 2D to 1D idx
    y[i] = a*x[i] + y[i];
}

int main()
{
    // ...
    int N = 64;
    int threads_per_block = 32;
    int num_blocks = 2;
    saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
    // ...
}
```

In practice the number of elements `N` rarely fits the `threads_per_block` exactly.
If we have one more element `N = 65` we need another block to run a single thread on that element. This means that the other 63 threads will run unnecessarily and start accessing unallocated memory.
We need to make sure to avoid getting out of bounds in our arrays.
```CUDA hl_lines="4 12 14"
__global__ void saxpy(int n, float a, float* x, float* y)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x; // 2D to 1D idx
    if (i < n) { // avoid out of bounds
        y[i] = a*x[i] + y[i];
    }
}

int main()
{
    // ...
    int N = 65;
    int threads_per_block = 32;
    int num_blocks = 3;
    saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
    // ...
}
```

We can compute the number of blocks needed via the following expression:
```C
num_blocks = (N + threads_per_block-1) / threads_per_block;
```

Finally for a more realistic example, we use `N = 100M` and `threads_per_block = 256`.
```CUDA hl_lines="12 13 14"
__global__ void saxpy(int n, float a, float* x, float* y)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x; // 2D to 1D idx
    if (i < n) { // avoid out of bounds
        y[i] = a*x[i] + y[i];
    }
}

int main()
{
    // ...
    int N = 100000000;
    int threads_per_block = 256;
    int num_blocks = (N + threads_per_block-1) / threads_per_block;
    saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
    // ...
}
```

Note that the `threads_per_block` cannot be set arbitrary, it depends on the capability of the GPU. Currently (year 2024) the maximum is 1024.
TODO: how to find this?
The maximum value is not always the one leading to the best performance, it depends on the problem to solve, the kernel implementation and the GPU.

## CUDA API
For the GPU implementation we need to use the CUDA API.
The CUDA API is a simple C-like API providing full access to the GPU compute capabilities.
The documentation is available here:

- CUDA documentation : [https://docs.nvidia.com/cuda/index.html](https://docs.nvidia.com/cuda/index.html)
- CUDA runtime api : [https://docs.nvidia.com/cuda/cuda-runtime-api/index.html](https://docs.nvidia.com/cuda/cuda-runtime-api/index.html)

Every function or structure from the API starts with "cuda" :
```CUDA
cudaMalloc()
cudaFree()
cudaMemcpy()
...
```

Most functions returns a `cudaError_t` that can be checked for successful execution:
```CUDA
cudaError_t error = cudaMalloc(...);
if (error != cudaSuccess) {
    // error happenned running cudaMalloc()
    fprintf(stderr, "CUDA ERROR: %s\n", cudaGetErrorString(error));
    // handle the error
    // ...
}
```

We can also get the last error thrown via `cudaGetLastError()`, this is especially useful as it is the only way to detect errors during kernel launch:
```CUDA
some_kernel<<<num_blocks, threads_per_block>>>();
cudaError_t error = cudaGetLastError();
```

Note that to keep the article's code short **we will ignore most errors handling** but it goes without saying that in production code you should handle them properly if you don't want any bad surprises.

In CUDA the GPU is referred to as the "device" while the CPU is called the "host".
These terms come from the fact that the GPU is a _co-processor_, it works in _parallel_ to the CPU. It is not the main processor running your OS, it works under the supervision of the CPU, the GPU only does what the CPU asks it to.

## GPU implementation
Now that we know a bit more about the CUDA API, let's see how to use it to run SAXPY on the GPU.
The first step is to allocate memory for those vectors on the GPU:
```CUDA
float* d_x;
float* d_y;
cudaMalloc(&d_x, N * sizeof(float));
cudaMalloc(&d_y, N * sizeof(float));
```
As a convention I am appending "d_" to the name of variables when they are used on the GPU instead of the CPU (d for device).

To initialize those vectors we must copy the CPU vectors to the GPU ones.
This can be done using `cudaMemcpy()`. The CUDA version is very similar to the C one but takes an additionnal parameter to specify the "direction" of the copy. In this case we want to copy from the CPU to the GPU so we should use `cudaMemcpyHostToDevice`:
```CUDA
cudaMemcpy(d_x, x, N * sizeof(float), cudaMemcpyHostToDevice);
cudaMemcpy(d_y, y, N * sizeof(float), cudaMemcpyHostToDevice);
```
Under the hood this will trigger a transfer of memory fom the CPU to the GPU via PCI-express.

We can then launch the kernel:
```CUDA
saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
cudaDeviceSynchronize();
```

After the kernel has finished executing we need to get the results back to the CPU.
We can do that by using `cudaMemcpy()` with `cudaMemcpyDeviceToHost` to copy from GPU to CPU memory:
```CUDA
cudaMemcpy(y, d_y, N * sizeof(float), cudaMemcpyDeviceToHost);
```

When we are done with the GPU, we should free the allocated GPU memory:
```CUDA
cudaFree(d_x);
cudaFree(d_y);
```

## Validation
We are done with the GPU implementation but we have no way to know if it is working or not.
Let's compare the output from the GPU implementation to the CPU one:
```CUDA
saxpy_cpu(a, x, y_ref);

for (int i = 0; i < N; i++) {
    if (!equals(y[i], y_ref[i])) {
        printf("failed!\n");
        return 1;
    }
}
printf("passed!\n");
```
Here I am storing the results of the CPU implementation into the `y_ref` array and the one from the GPU into the `y` array so that we can compare them element by element.
Since they are arrays of `float` we should allow some epsilon for equality of elements:
```cuda
#include <math.h> // abs

inline bool equals(float a, float b)
{
    return abs(a - b) < 1e-12;
}
```

## Performance analysis
Now that we've implemented the same algorithm on the GPU and the CPU, it would be useful to compare the execution time and confirm that the GPU is actually faster.

A quick way to figure out the elapsed time of a particular function in C is to use the `clock()` function from the `time.h` standard library:
```C
#include <time.h> // clock

clock_t t1 = clock();

// thing to measure
saxpy_cpu(N, a, x, y_ref);

clock_t t2 = clock();

long elapsed = t2 - t1;
printf("CPU time: %ld ticks\n", elapsed);
```
Here the unit for the time returned by `clock()` is CPU "clock ticks".

We can use the same technique to measure the GPU implementation but be mindful to also include `cudaDeviceSynchronize()` in the measurement otherwise we would only measure the time to launch the kernel not to execute it:
```cuda
clock_t t1 = clock();

saxpy<<<num_blocks, threads_per_block>>>(N, a, d_x, d_y);
cudaDeviceSynchronize();

clock_t t2 = clock();
printf("GPU time: %ld ticks\n", t2 - t1);
```

On my machine I get:
```
CPU time: 81835 ticks
GPU time: 4792 ticks
```
The CPU is noticably slower than the GPU as expected.

Note that SAXPY is very simple so its performance is not limited by the arithmetic intensity (_compute-bound_) but is is limited by the memory transfers (_bandwidth-bound_).
However, it can still benefit from GPU acceleration if the problem size `N` is large enough.

## Next
This concludes our article. 

The source code for this article is available on [GitHub](https://github.com/kevenv/cuda_exercises/tree/master/saxpy).
