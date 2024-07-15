# QOI image format

In this article we will show how to implement an image encoder and decoder for the _QOI_ (Quite OK Image) format, a relatively new image format created by the game developer _Dominic Szablewski_ that has generated a lot of interest recently in the computer graphics community due to its simplicity.

QOI is a very simple lossless image format that is easy to understand and fast to encode, yet compresses images to a comparable size as the much more complex _PNG_ image format.
Thus it sits between _BMP_ (uncompressed) and _PNG_ (compressed) in term of compression ratio.
The author claims that QOI is 3-4x faster than PNG to decode and 20-50x faster to encode!

If you are new to image formats we recommend looking at our [previous article on BMP](https://kevenv.com/blog/bmp_format.html) in which we show how to build an image viewer, capable of loading BMP images. We will extend the same image viewer to QOI in this article.

## Intro to data compression
QOI is a good introduction to _lossless data compression_, meaning that the original image can be recovered exactly without any loss in quality.

Data can usually be compressed much further by accepting a loss in quality,
those methods are said to be _lossy_ and are much more complex as they exploit the limits of perception of the human visual (or auditive) system.
In other words, things that humans cannot see (or hear) are removed from the data.
This is what the _JPEG_ format does for images.
As you might have noticed, those methods end up being very specific to the kind of data to compress (image, sound, video...).

How can we make the files smaller without loosing any information neccessary to be able to recover the original file?
This is achieved by taking advantage of _redundancies_ in the data.
We find _repetitive patterns_ and replace them by an equivalent compressed representation.
Files can only be compressed if they have a lot of redundancy, there is no magic here.
In practice raw data is usually not encoded the most efficient way and is compressible.

One of the simplest technique to do lossless data compression is _RLE_ (Run Length Encoding).
Say we have the following data:
```
2 5 5 5 5 5 5 5 3 3
```
Each number can fit in a single byte so the whole data takes 10 bytes.
This is the most straightforward and naive scheme possible but we can encode it more efficiently by noticing the repetition of "5" and "3":
```
(1 x 2) (7 x 5) (2 x 3)
```
This encoding scheme is known as _RLE_ and compresses the data to 6 bytes, a 40% decrease in size!
Notice that the longer the repetition, the more the data can be compressed.

An image can be compressed that way but since it is rare to have repetitions of pixels with exactly the same value, it is not very effective.
Images are made of pixels with 3 color channels (R,G,B) so instead of doing RLE on bytes it makes more sense to do it on pixels, groups of 3 bytes:
```
[255 128 150] [255 128 150] [255 128 150] = (3 x [255 128 150])
```

## Compression algorithm
The QOI compression algorithm essentially chooses between 4 techniques to compress each pixel or a group of pixels:

1. Run
2. Index
3. Difference
4. Full (uncompressed)

Those methods were choosen to tradeoff quality with complexity after surely many iterations while testing with all kind of images.

### 1. Run
We have already seen the first method in the section above on data compression.
The specific implementation of RLE used in QOI is a bit different however.
A run is defined based on the previous pixel decoded.
It uses 6-bit to store the run-length
The run-length is stored with a bias of -1 to avoid length of 0
2^6 = 64 [0-63] -> [1,64], 63,64 are illegal and reserved.
so the range is 1..62

### 2. Index
If a repetition is not detected we can use the next best thing and send an index to a previously seen pixel instead.
QOI keeps a buffer of 64 pixels that have been previously seen at any time, those are not necessarily the last pixels seen up to that point.
Each time a new pixel is decoded it is added to this buffer by using a hash function:
```C
u32 hash = last_pixel.r * 3 + last_pixel.g * 5 + last_pixel.b * 7 + last_pixel.a * 11;
u8 index = (u8)(hash % 64);
prev_pixels[index] = last_pixel;
```

### 3. Difference
Pixels that are physically very close to each other
usually vary slightly in value but it is rare that they have the exact same value.
RLE with some margin to find
instead of sending the pixel value, we can send the difference with the previous pixel.

green channel : human most sensitive to green, able to distinghish between many more shades of green than red or blue.

### 4. Full
The last method is used when we are out of options and none of the previous ones worked or resulted in compression. In that case we just send the raw pixel in the order R,G,B,A (RGB or RGBA).

One thing to notice is that none of those methods take much advantage of the specific properties of images.
To keep things simple QOI treats the image as a single 1D stream of pixels and not a 2D grid like PNG does.
The compression method is thus not able to detect the 2D spatial redundancies that are common in images. This is probably one of the reason why PNG is more efficient.

## File format
Now that we have seen how QOI compresses images, let's analyze the actual file format.
A QOI file starts with a fixed size _header_ followed by a list of _chunks_ containing the compressed pixels data.

<p align="center">
    <img src="{{rootImages}}blog/qoi_format.svg" alt="QOI file format">
</p>

### Header
```C
struct __attribute__((packed)) qoi_header_t {
    char magic[4]; // file signature "qoif"
    u32 width;     // image width in pixels (BE)
    u32 height;    // image height in pixels (BE)
    u8 channels;   // 3 = RGB, 4 = RGBA
    u8 colorspace; // qoi_color_space_t
};
```

The header contains only the essential information to decode the image, nothing else.
The first few bytes of the header are the _file signature_, also known as the _magic number_ of the file, and is only used to identify the type of file. The signature for QOI is "quoif" in ASCII characters.

The `width` and `height` of the image follows the file signature. Annoyingly they are encoded as _big-endian_, pressumably to make those values easy to see when looking at the raw binary data. We need to convert them to _little-endian_ by using a routine like this:
```C
u32 big_to_little(u32 value)
{
    return ((value & 0x000000FF) << 24) |
           ((value & 0x0000FF00) << 8)  |
           ((value & 0x00FF0000) >> 8)  |
           ((value & 0xFF000000) >> 24);
}
```

The number of _color channels_ (3 for RGB and 4 for RGBA) is specified in the `channels` field.
Finally `colorspace` contains the type of _color space_ in which the image is encoded:
```C
enum qoi_color_space_t {
    QOI_COLOR_SPACE_SRGB   = 0, // sRGB with linear alpha (most common)
    QOI_COLOR_SPACE_LINEAR = 1  // all channels linear
};
```

### Chunks
Images are encoded row by row from left to right, top to bottom.
The compressed pixels data consists of a series of _chunks_ varying in size.
Each chunk starts with a 8-bit or 2-bit _tag_ identifying the type.
A chunk can have up to 4 bytes of data bytes following its tag.

<p align="center">
    <img src="{{rootImages}}blog/qoi_chunk.svg" alt="QOI chunk format">
</p>

There are 6 types of chunks corresponding to the different compression methods:

<p align="center">
    <img src="{{rootImages}}blog/qoi_tags.svg" alt="QOI tags format">
</p>

Conveniently, all chunks are byte aligned which allow us to treat it as a single _byte stream_.
The stream should end when all the pixels have been decoded but the end of the stream 
is also marked with the following sequence of 8 bytes:
```
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01
```

## Decoder
Loading a QOI image necessiates to open the file, parse the header, allocate a buffer for the pixels and decode the chunks.
After our explanation on the QOI file format and its compression algorithm, you should be able to write an image decoder and we encourage you to do so **before looking at the implementation below** as it is a great learning exercise to validate that you understand the format correctly.

An implementation for a QOI decoder could look something like:
```C
#include <stdio.h> // fopen
#include <stdlib.h> // malloc

image_t* qoi_load(const char* file_name)
{
    // open QOI file
    FILE* file = fopen(file_name, "rb");
    if (!file) {
        return NULL;
    }

    // parse header
    qoi_header_t header;
    fread(&header, sizeof(header), 1, file);
    header.width = big_to_little(header.width);
    header.height = big_to_little(header.height);
    
    // alloc buffer for pixels
    image_t* image = (image_t*)malloc(sizeof(image_t));
    image->w = header.width;
    image->h = header.height;
    image->pixels = (u8*)malloc(image->w * image->h * 4);

    // read byte stream into temporary buffer
    fseek(file, 0, SEEK_END);
    u64 file_size = ftell(file);
    u64 bytes_size = file_size - sizeof(header);
    u8* bytes = (u8*)malloc(bytes_size);
    fseek(file, sizeof(header), SEEK_SET);
    fread(bytes, bytes_size, 1, file);

    // decode chunks
    qoi_decode_chunks(image, bytes);

    free(bytes);
    fclose(file);
    return image;
}

void qoi_free(image_t* image)
{
    free(image->pixels);
    free(image);
}
```
To avoid making unecessary `fread()` syscalls, we read the whole byte stream of chunks all at once and store it in a temporary buffer named `bytes`.

The code to decode the chunks (the core of the compression algorithm) is as follow:
```C
#define QOI_BUFFER_SIZE 64

// tags
#define QOI_OP_RGB   0b11111110
#define QOI_OP_RGBA  0b11111111
#define QOI_OP_INDEX 0b00000000
#define QOI_OP_DIFF  0b01000000
#define QOI_OP_LUMA  0b10000000
#define QOI_OP_RUN   0b11000000

#define QOI_MASK_2B  0b11000000

void qoi_decode_chunks(image_t* image, u8* bytes)
{
    // decode chunks as a byte stream
    rgba_t last_pixel; // last pixel, must be initialized as (0,0,0,255)
    last_pixel.r = 0;
    last_pixel.g = 0;
    last_pixel.b = 0;
    last_pixel.a = 255;
    rgba_t prev_pixels[QOI_BUFFER_SIZE] = {0}; // running array of previously seen pixels, must be zero-initialized
    u32 idx = 0; // index of current pixel
    u32 i = 0; // index of current byte in stream
    while (idx < image->w * image->h) {
        u8 byte = bytes[i++];

        // 4. Full
        if (byte == QOI_OP_RGB) {
            last_pixel.r = bytes[i++];
            last_pixel.g = bytes[i++];
            last_pixel.b = bytes[i++];
            image_set_pixel(image, idx++, last_pixel);
        }
        else if (byte == QOI_OP_RGBA) {
            last_pixel.r = bytes[i++];
            last_pixel.g = bytes[i++];
            last_pixel.b = bytes[i++];
            last_pixel.a = bytes[i++];
            image_set_pixel(image, idx++, last_pixel);
        }
        // 2. Index
        else if ((byte & QOI_MASK_2B) == QOI_OP_INDEX) {
            u8 index = byte & 0b00111111;
            last_pixel = prev_pixels[index];
            image_set_pixel(image, idx++, last_pixel);
        }
        // 3. Difference
        else if ((byte & QOI_MASK_2B) == QOI_OP_DIFF) {
            u8 dr = ((byte >> 4) & 0b11) - 2;
            u8 dg = ((byte >> 2) & 0b11) - 2;
            u8 db = ((byte >> 0) & 0b11) - 2;
            last_pixel.r += dr;
            last_pixel.g += dg;
            last_pixel.b += db;
            image_set_pixel(image, idx++, last_pixel);
        }
        else if ((byte & QOI_MASK_2B) == QOI_OP_LUMA) {
            u8 byte2 = bytes[i++];
            u8 dg = (byte & 0b00111111) - 32;
            u8 db_dg = ((byte2 >> 0) & 0b1111) - 8;
            u8 dr_dg = ((byte2 >> 4) & 0b1111) - 8;
            last_pixel.r += (u8)(dr_dg + dg);
            last_pixel.g += dg;
            last_pixel.b += (u8)(db_dg + dg);
            image_set_pixel(image, idx++, last_pixel);
        }
        // 1. Run
        else if ((byte & QOI_MASK_2B) == QOI_OP_RUN) {
            u8 run_length = (byte & 0b00111111) + 1;
            for (u8 k = 0; k < run_length; ++k) {
                image_set_pixel(image, idx++, last_pixel);
            }
        }

        // store last pixel in previous pixels buffer
        prev_pixels[qoi_hash(last_pixel) % QOI_BUFFER_SIZE] = last_pixel;
    }
}

void image_set_pixel(image_t* image, u32 idx, rgba_t color)
{
    image->pixels[idx*4 + 0] = color.r;
    image->pixels[idx*4 + 1] = color.g;
    image->pixels[idx*4 + 2] = color.b;
    image->pixels[idx*4 + 3] = color.a;
}
```
This is the whole thing! It is pretty amazing to see that compressing images efficiently could be that short and easy to implement.

Note that for convenience this code uses a _union_ with an _anonymous struct_ to treat RGBA values sometimes as a `u32` and sometimes as four `u8` components:
```C
// color value in the ABGR8888 format (R,G,B,A order)
union rgba_t {
    struct {
        u8 r, g, b, a;
    };
    u32 rgba;
};
```

## Encoder
We have seen how to implement an image decoder but to create a QOI image, we must write an encoder.
An image encoder is usually much more complex than a decoder and slower to run.
QOI has been designed with the goal of making a very fast encoder (and decoder).
It achieves this objective primarily because of its simplicity, sacrificing compression ratio in favor of speed.

This concludes our article on ...

In this article **we have omitted proper errors handling** to keep the code short, please see the full source code available on [GitHub](https://github.com/kevenv/image_viewer) for more details.

## References
- [https://qoiformat.org/](https://qoiformat.org/)
- [https://phoboslab.org/log/2021/11/qoi-fast-lossless-image-compression](https://phoboslab.org/log/2021/11/qoi-fast-lossless-image-compression)
- [https://en.wikipedia.org/wiki/QOI_(image_format)](https://en.wikipedia.org/wiki/QOI_(image_format))
- [https://en.wikipedia.org/wiki/Run-length_encoding](https://en.wikipedia.org/wiki/Run-length_encoding)
