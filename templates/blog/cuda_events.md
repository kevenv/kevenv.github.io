# CUDA - Events (Measuring timings)

In the [article on SAXPY]({{{root}}}blog/cuda_saxpy.html) we have seen how to measure the kernel execution time using CPU timers, this is fine to get a quick idea of the timings but there is a more accurate way to do this using **CUDA events**.

## API
- `cudaEventCreate()` : Create an event.
- `cudaEventDestroy()` : Destroy an event.
- `cudaEventRecord()` : Record an event.
- `cudaEventSynchronize()` : Wait for the event to complete.
- `cudaEventElapsedTime()` : Get the time between two recorded events.

See the [documentation](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html#group__CUDART__EVENT) for details.

## Usage
CUDA events allow creating GPU timestamp that can be used to get the elapsed time between two points in time.

Events are recorded for a given CUDA stream, the [default stream](
https://docs.nvidia.com/cuda/cuda-runtime-api/stream-sync-behavior.html#stream-sync-behavior__default-stream) is used when passing `0`.

Events do not need to be recreated to take multiple measurements, `cudaEventRecord()` can be called multiple times on the same event since every call first resets the event.

```CUDA hl_lines="16"
#include <stdio.h> // printf

int main()
{
    // create events
    cudaStream_t stream = 0; // use default CUDA stream
    cudaEvent_t start;
    cudaEvent_t stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    
    // start recording
    cudaEventRecord(start, stream);

    // launch kernel
    kernel<<<num_blocks, threads_per_block>>>(...);

    // stop recording
    cudaEventRecord(stop, stream);
    // wait for events to finish
    cudaEventSynchronize(stop);

    // get elapsed time
    float elapsed_ms = 0.0f;
    cudaEventElapsedTime(&elapsed_ms, start, stop);
    printf("elapsed time: %f ms\n", elapsed_ms);

    // destroy events
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    return 0;
}
```

The way I believe this works under the hood is:
```C
// GPU: commands queue
[]

// CPU: cudaEventRecord(start, stream);
[ record timestamp to event "start" ]

// CPU: kernel<<<num_blocks, threads_per_block>>>(...);
// (GPU can start executing operations from this point)
[ record timestamp to event "start" ]
[ launch kernel "kernel" ]

// CPU: cudaEventRecord(stop, stream);
[ record timestamp to event "start" ]
[ launch kernel "kernel" ]
[ record timestamp to event "stop" ]

// GPU: record timestamp to event "start"
[ launch kernel "kernel" ]
[ record timestamp to event "stop" ]

// GPU: launch kernel "kernel"
[ record timestamp to event "stop" ]

// GPU: record timestamp to event "stop"
[]

// CPU: cudaEventSynchronize(stop);
```

The source code for this article is available on [GitHub](https://github.com/kevenv/cuda_exercises/tree/master/events).
