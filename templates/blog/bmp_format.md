# BMP image format

In this article we will see how images are stored in files, specifically _BMP_ files.
The _Bitmap_ or _BMP_ file is one of the simplest image format, it is widely used to store uncompressed images.
Most notably, it is the default file format used by the now famous _Microsoft Paint_.
After our deep dive into the image format, we will show how to implement a simple BMP image viewer in C with the SDL library.

## Image
What is an image?
When we take a picture with a camera, it collects the light _intensity_ and _color_ of what is in front of it for a fraction of a second, freezing a moment in time onto its sensor.
We call that collection of light an _image_.
The image captured on the sensor is essentially a miniaturized version of the 3D scene seen from the point of view of the camera, it projects the 3D scene onto the camera sensor (2D).

<p align="center">
    <img src="{{rootImages}}blog/bmp_camera.svg" alt="Camera Imaging">
</p>

The camera sensor does not have infinite resolution, in fact the sensor is actually a grid of tiny sensors capturing light at different positions. This divides the image into a 2D grid of _pixels_, where each pixel represents the color at a specific position.

<p align="center">
    <img src="{{rootImages}}blog/bmp_pixels.svg" style="height: 150px;" alt="Image Pixels">
</p>

Due to how the human visual system works, it turns out that we can encode any color using three numbers: R (Red), G (Green) and B (Blue). Those three numbers are often referred to as _color channels_ and they form the _RGB color space_.
This is easier to understand when thinking about mixing lights of different colors:
<p align="center">
    <img src="{{rootImages}}blog/bmp_rgb.svg" style="height: 150px;" alt="RGB color model">
</p>

For example by mixing a red light with a green one we obtain a yellow light.
We can get white by merging all the lights together and we get black when all the lights are closed.
By mixing all three fundamental light colors we can make all the possible colors:
<p align="center">
    <img src="{{rootImages}}blog/bmp_colors.svg" alt="Colors Spectrum">
</p>

To be able to recreate any color using the R,G,B triplet we need to be able to 
change the intensity of each color channel, resulting in different shades of a given color:
<p align="center">
    <img src="{{rootImages}}blog/bmp_r_grad.svg" alt="R channel values">
</p>

In nature there is a whole continuous spectrum of colors but computers can only manipulate discrete numbers, therefore we need to assign a number to each color intensity.
The most common color resolution or _color depth_ is 24-bpp (bits per pixel), that is each color channel is encoded using 8-bit and fits in a single byte.
This means that there is a maximum of 2^8 = 256 different values per channel.
All three channels together allows us to define a total of 2^24 = 16 777 216 colors!

## PPM
To store an image we need to know the value of each pixel and the dimensions of the image (width x height).

Say we have a 3x2 image of 6 pixels:
<p align="center">
    <img src="{{rootImages}}blog/bmp_simple.svg" alt="A simple BMP image">
</p>

The simplest way to store this image in a file would probably be something like this:
```
3 x 2       # width x height

255 0   0   # red
0   255 0   # green
0   0   255 # blue
255 255 255 # white
255 0   255 # purple
255 255 0   # yellow
```

This is basically what the _PPM_ (Portable PixMap) format does:
```
P3
3 2
255
255 0   0
0   255 0
0   0   255
255 255 255
255 0   255
255 255 0
```

The only difference is the presence of a _file header_.
The first line is the file signature (used to recognize the file type):

- `P3` pixels are encoded as ASCII characters
- `P6` pixels are encoded as binary numbers

The second line is the width and height.
The third line is the maximum value of each pixel channel, usually 255 for 8-bit channels.
Any string starting with `#` is considered a comment.
The pixels data follow the header and are specified from left to right, top to bottom.

In the case of the ASCII format, triplets are stored as ASCII characters representing the underlying values and each channel is separated by a whitespace. There is usually one line per pixel.
For example, a purple pixel (R,G,B = 255,0,255) will be encoded as:
```
255 0 255
```

For the binary format, each pixel takes only 3 bytes and is encoded as a R,G,B triplet in this exact order.
A channel is encoded as a 8-bit unsigned value and takes 1 byte.
It should be obvious that the ASCII format is a lot more wasteful, a single pixel takes 12 bytes!

Note that the file header is _always_ encoded as ASCII characters even in the binary format.

## BMP
The BMP format is not much more complicated than PPM.
While it does support various encoding and compression methods we will not go over those since in practice BMP is mostly used for uncompressed 24-bpp images.

The structure of the BMP file for the simplest case is as follow:
<p align="center">
    <img src="{{rootImages}}blog/bmp_format.svg" alt="Structure of BMP file">
</p>

It consists of a _file header_ followed by an _info header_.
The pixels of the image are usually stored right after.

### File header
```C
struct __attribute__((packed)) bmp_file_header_t {
    char type[2]; // signature (BM)
    u32 size; // size of the file
    u16 reserved1;
    u16 reserved2;
    u32 offset; // offset to the image data
};
```

The first two bytes of the file header define the file signature which should be "BM" in ASCII characters and is used to detect that the file is a BMP file.

The most important thing to get from this header is the `offset` in bytes where the image data is stored.
It also contains the size of the file and a few reserved bytes that we can ignore.

Note here that it is important to specify `__attribute__((packed))` to make sure that the binary representation of the `struct` matches the spec exactly and does not contain any padding.

### Info header
```C
struct __attribute__((packed)) bmp_info_header_t {
    u32 size; // size of the header
    u32 width; // width of the image
    u32 height; // height of the image
    u16 planes; // hardcoded to 1
    u16 bpp; // bits per pixel

    u32 compression; // compression method
    u32 image_size; // size of the image

    // unused with 24-bpp:
    u32 pixels_per_meter_x;
    u32 pixels_per_meter_y;
    u32 used_colors;
    u32 important_colors;
};
```

Most of the fields of the info header are self explanatory but the `size` one needs further explanations.
There are multiple versions of the BMP file format, each version adds more functionalities and is specified with a different info header.
The size of the info header will allow us to determine the type of info header:

- `BITMAPCOREHEADER` : the original header
- `BITMAPINFOHEADER` : extends core header to support compression and color palettes
- `BITMAPV4HEADER` : extends info header to support color spaces
- `BITMAPV5HEADER` : extends v4 header to support ICC color profiles

We will only handle `BITMAPINFOHEADER` as it is the most common by far.

Since we assume that the image is 24-bpp uncompressed:

- `compression = 0`
- `bpp = 24`
- `image_size = width x height x 3 bytes`

### Image
Contrary to common intuition, the pixels in BMP are stored from left to right but starts from the _bottom_ first. This means that we will need to flip the image vertically to show it correctly on screen.

Each pixel takes 3 bytes and is encoded as a R,G,B triplet in the B,G,R order.
Some padding bytes might be added to each row of the pixels grid to make it 4-byte aligned, meaning that the length of each row must be a multiple of 4 bytes.
This is done to make it fit inside an array of `u32`.

### Implementation
All together we can load a BMP image very easily without needing any external libraries:

1. Read the file
2. Parse both headers
3. Fill a buffer with the pixels stored in the file.

```C
#include <stdio.h> // fopen
#include <stdlib.h> // malloc

struct image_t {
    u8* pixels;
    u32 w;
    u32 h;
};

image_t* bmp_load(const char* file_name)
{
    // open BMP file
    FILE* file = fopen(file_name, "rb");
    if (!file) {
        return NULL;
    }

    // parse file header
    bmp_file_header_t file_header;
    fread(&file_header, sizeof(file_header), 1, file);
    
    // parse info header
    bmp_info_header_t info_header;
    fread(&info_header, sizeof(info_header), 1, file);
    
    // alloc buffer for pixels
    image = (image_t*)malloc(sizeof(image_t));
    image->w = info_header.width;
    image->h = info_header.height;
    u32 image_size = image->w * image->h * 4;
    image->pixels = (u8*)malloc(image_size);
    u8* tmp = (u8*)malloc(image_size);

    // fill buffer with pixels from file
    fseek(file, file_header.offset, SEEK_SET);
    fread(tmp, info_header.image_size, 1, file);

    // convert RGB24 -> RGB888
    // flip image in Y
    for (u32 y = 0; y < image->h; ++y) {
        for (u32 x = 0; x < image->w; ++x) {
            u32 pitch = ((image->w * 3) + 3) & ~3; // 4-byte alignment
            u32 y_ = image->h-1 - y; // flip image in Y
            image->pixels[(x + y * image->w) * 4 + 0] = tmp[x*3 + y_ * pitch + 0]; // B
            image->pixels[(x + y * image->w) * 4 + 1] = tmp[x*3 + y_ * pitch + 1]; // G
            image->pixels[(x + y * image->w) * 4 + 2] = tmp[x*3 + y_ * pitch + 2]; // R
            image->pixels[(x + y * image->w) * 4 + 3] = 255;                       // A (unused)
        }
    }
    free(tmp);

    fclose(file);
    return image;
}

void bmp_free(image_t* image)
{
    free(image->pixels);
    free(image);
}
```

Filling the buffer with pixels (lines 30 to 51) is a bit more involved and deserves more explanations.

The BMP pixels are stored in the _RGB24_ format but a screen usually expects a _RGB888_ format.
RGB24 is tightly packed into 3 bytes (B,G,R) while RGB888 is stored as 4 bytes with the last byte being ignored (B,G,R,_).

To convert it we need to allocate a temporary buffer `tmp` to hold the pixels stored bottom to top, convert it to RGB888 and flip the image at the same time in `image->pixels`. The `image->pixels` array is the final pixels buffer that will be used directly by our image viewer to be displayed on screen.

## Image viewer
Now that we understand the format, we can write a simple image viewer that is able to open BMP images.
We choose to use the SDL2 library to open a window in which we can show the image.
The basic code template for a typical SDL2 app should be something like this:
```C
#include <SDL2/SDL.h>

int main(int argc, char* argv[])
{
    // 1. init
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        return 1;
    }
    SDL_Window* window = SDL_CreateWindow("Image Viewer",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        800, 600
        SDL_WINDOW_SHOWN
    );
    if (!window) {
        return 1;
    }
    SDL_Surface* window_surface = SDL_GetWindowSurface(window);

    // main loop
    bool running = true;
    SDL_Event event;
    while (running) {
        // handle events
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }
        }

        // 2. render
        u32 color = SDL_MapRGBA(window_surface->format, 0, 0, 0, 255);
        SDL_FillRect(window_surface, NULL, color);
        SDL_UpdateWindowSurface(window);

        // sleep
        SDL_Delay(30);
    }

    // 3. cleanup
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
```
An SDL app can be compiled using `gcc -lSDL2 app.c -o app`.

To transform this app into an image viewer we must do three things:

1. Load the image
2. Create a "SDL surface" which contains the image
3. Blit the surface to the window

For the first two steps we load the image and create a SDL surface for it during init:
```C
// 1. init

// load image
image_t* image = bmp_load(file_name);

// copy image to SDL surface
SDL_Surface* image_surface = SDL_CreateRGBSurfaceWithFormatFrom(
    image->pixels, image->w, image->h, 
    32, image->w * 4, SDL_PIXELFORMAT_RGB888
);
```

We must also make sure to free it after use:
```C
// 3. cleanup
SDL_FreeSurface(image_surface);
bmp_free(image);
```

Once the image has been copied to the surface properly, we can blit it to the window's surface:
```C hl_lines="4"
// 2. render
u32 color = SDL_MapRGBA(window_surface->format, 0, 0, 0, 255);
SDL_FillRect(window_surface, NULL, color);
SDL_BlitSurface(image_surface, NULL, window_surface, NULL);
SDL_UpdateWindowSurface(window);
```

That's it! We now have an image viewer that can read BMP images!
Notice that due to the simplicity of the BMP format we need very few lines of code to implement a basic image viewer.

In this article **we have omitted proper errors handling** to keep the code short, please see the full source code available on [GitHub](https://github.com/kevenv/image_viewer) for more details.

## References
- BMP specification:
    - [https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage](https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-storage)
    - [https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-header-types](https://learn.microsoft.com/en-us/windows/win32/gdi/bitmap-header-types)
    - [https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapfileheader](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapfileheader)
    - [https://learn.microsoft.com/en-us/previous-versions/dd183376(v=vs.85)](https://learn.microsoft.com/en-us/previous-versions/dd183376(v=vs.85))
- [https://en.wikipedia.org/wiki/BMP_file_format](https://en.wikipedia.org/wiki/BMP_file_format)
- [https://www.loc.gov/preservation/digital/formats/fdd/fdd000189.shtml](https://www.loc.gov/preservation/digital/formats/fdd/fdd000189.shtml)
- [https://netpbm.sourceforge.net/doc/ppm.html](https://netpbm.sourceforge.net/doc/ppm.html)
- [https://en.wikipedia.org/wiki/Netpbm](https://en.wikipedia.org/wiki/Netpbm)
