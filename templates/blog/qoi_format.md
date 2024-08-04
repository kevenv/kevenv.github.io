# QOI image format

In this article we will show how to implement an image encoder and decoder for the _QOI_ (Quite OK Image) format, a relatively new image format created by the game developer _Dominic Szablewski_ that has generated a lot of interest recently in the computer graphics community due to its simplicity.

QOI is a very simple lossless image format that is easy to understand and fast to encode, yet compresses images to a comparable size as the much more complex _PNG_ image format.
Thus it sits between _BMP_ (uncompressed) and _PNG_ (compressed) in terms of compression ratio.
The author claims that QOI is 3-4x faster than PNG to decode and 20-50x faster to encode!

If you are new to image formats we recommend looking at our [previous article on BMP]({{root}}blog/bmp_format.html) in which we show how to build an image viewer, capable of loading BMP images. We will extend the same image viewer to QOI in this article.

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
The QOI compression algorithm essentially chooses between 4 techniques to compress each pixel or group of pixels:

1. Run
2. Index
3. Difference
4. Full (uncompressed)

Those methods were choosen to tradeoff quality with complexity after surely many iterations while testing with all kind of images.

### 1. Run
We have already seen the first method in the section above on data compression however the specific implementation of RLE used in QOI is a bit different.

A run is defined based on the previous pixel decoded.

In case of a run, the previous pixel decoded is simply repeated a specific number of time, its _run-length_.
The run-length is stored on 6-bit and a bias of -1 is used to avoid lengths of zero.
The range of valid values would thus be [0,2^6-1] = [0,63] -> [1,64].
Run-length of 63 and 64 and illegal and reserved, leaving only [1,62] as valid.

It uses 6-bit to store the run-length.
The run-length is stored with a bias of -1 to avoid length of 0

### 2. Index
If a repetition is not detected, we can use the next best thing and send an _index_ to a previously seen pixel instead.
QOI keeps a buffer of 64 pixels that have been previously seen at any time, those are not necessarily the last pixels seen up to that point.

This buffer could be implemented as a list but to find matching pixel it uses a hashmap.

Each time a new pixel is decoded it is added to this buffer by using a hash function:
```C
u32 hash = last_pixel.r * 3 + last_pixel.g * 5 + last_pixel.b * 7 + last_pixel.a * 11;
u8 index = (u8)(hash % 64);
prev_pixels[index] = last_pixel;
```

The hashmap key is a hash function based on the pixel's value.
The prime numbers series 3,5,7,11 ensures a good uniformity and the % 64 wrap the index to fit into the array.

The use of a hashmap like this also accelerates finding matches, which will be useful in the image encoder. : instead of a stack/queue of pixels, we use a hashmap
when decoding, need to query/find if pixel is in cache -> slow in array O(N) but hashmap is O(1)
hashmap of pixels
key = hash fct based on pixel values
collision -> fixed size cache

The index is stored in 6-bit [0,63]

### 3. Difference
Pixels that are physically very close to each other usually vary slightly in value but it is rare that they have the exact same value.

When the _difference_ in value between two pixels is small, it is more efficient to store this difference instead of the full value. 

Therefore, instead of sending the pixel value, we can send the _difference_ with the previous pixel.

QOI has two variants of the difference method, one for very small difference and the other for bigger ones.

[/]The second variant takes advantage of the fact that human eyes are most sensitive to green, meaning that we are able to distinghish between many more shades of green than red or blue.

QOI allocates more bits for the green channel in this variant.
[/]bias towards bigger diff of G? nature = trees,grass?

green channel is used to indicate the general direction of
change : luminance
usually brightness chg > color chg?

encode diff using 2 bytes - 2-bit tag = 2*8-2=14bits
14/3 ~= 4.7

dr dg db
5   5  4
4   4  6

dr-dg dg db-dr
4     6  4

dr: 2^4-1=16-1 - 8 = [-8, 7]
dg: 2^6-1=64-1 - 32 = [-32,31]

dr-dg: [-8--32,7-31] = [24,-24]

RGB -> YUV / YCbCr
    Y=luminance ~G
    chrominance:
    U=B-Y
    V=R-Y
its called "luma" but not really YUV,maybe just because looks similar

It is important to notice that the difference method does not encode the alpha channel (A).
therefore this method can only be used if the A channel did not change from the previous pixel.

### 4. Full
The last method is used when we are out of options and none of the previous ones worked or resulted in compression. In that case we just send the raw pixel in the order R,G,B,A (or RGB), one byte per color channel.

One thing to notice is that none of those methods take much advantage of the specific properties of images.
To keep things simple, QOI treats the image as a single 1D stream of pixels and not a 2D grid like PNG does.
The compression method is thus not able to detect the 2D spatial redundancies that are common in images. This is probably one of the reason why PNG is more efficient.

## File format
Now that we have seen how QOI compresses images, let's analyze the actual file format.
A QOI file starts with a fixed size _header_ followed by a list of _chunks_ containing the compressed pixels data.

![QOI file format]({{rootImages}}blog/qoi_format.svg)

### Header
```C
struct __attribute__((packed)) qoi_header_t {
    char magic[4]; // file signature "qoif"
    u32 width; // image width in pixels (BE)
    u32 height; // image height in pixels (BE)
    u8 channels; // 3 = RGB, 4 = RGBA
    u8 colorspace; // qoi_color_space_t
};
```

The header contains only the essential information to decode the image, nothing else.
The first few bytes of the header are the _file signature_, also known as the _magic number_ of the file, and is only used to identify the type of file. The signature for QOI is "qoif" in ASCII characters.

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
    QOI_COLOR_SPACE_SRGB = 0, // sRGB with linear alpha (most common)
    QOI_COLOR_SPACE_LINEAR = 1, // all channels linear
};
```

### Chunks
Images are encoded row by row from left to right, top to bottom.
The compressed pixels data consists of a series of _chunks_ varying in size.
Each chunk starts with a 8-bit or 2-bit _tag_ identifying the type.
A chunk can have up to 4 bytes of data bytes following its tag.

![QOI chunk format]({{rootImages}}blog/qoi_chunk.svg)

There are 6 types of chunks corresponding to the different compression methods:

![QOI tags format]({{rootImages}}blog/qoi_tags.svg)

Conveniently, all chunks are byte aligned which allow us to treat it as a single _byte stream_.
The stream should end when all the pixels have been decoded but the end of the stream 
is also marked with the following sequence of 8 bytes:
```
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01
```

## Decoder
Loading a QOI image necessitates to open the file, parse the header, allocate a buffer for the pixels and decode the chunks.
After our explanation on the QOI file format and its compression algorithm, you should be able to write an image decoder and we encourage you to do so **before looking at the implementation below** as it is a great learning exercise to validate that you understand the format correctly.

An implementation for a QOI decoder could look something like this:
```C
#include <stdio.h> // fopen
#include <stdlib.h> // malloc

struct image_t {
    u8* pixels;
    u32 w;
    u32 h;
    u8 channels; // 3: RGB (24-bpp), 4: RGBA (32-bpp))
};

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
    image->channels = header.channels;
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
We can find the size of the byte stream from the size of the QOI file.
The file size can be determined by moving to the end of the file via `fseek()` and by using `ftell()` to get the current position in the file (in bytes).

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

#define QOI_MASK_2B 0b11000000

void qoi_decode_chunks(image_t* image, u8* bytes)
{
    // decode chunks as a byte stream
    rgba_t last_pixel; // last pixel, must be initialized as (0,0,0,255)
    last_pixel.r = 0;
    last_pixel.g = 0;
    last_pixel.b = 0;
    last_pixel.a = 255;
    rgba_t prev_pixels[QOI_BUFFER_SIZE] = {0}; // running array of previously seen pixels, must be zero-initialized
    u8 run_length = 0;
    u32 idx = 0; // index of current byte in stream
    for (u32 i = 0; i < image->w * image->h; i++) {
        if (run_length > 0) {
            run_length--;
        }
        else {
            u8 byte = bytes[idx++];

            // 4. Full
            if (byte == QOI_OP_RGB) {
                last_pixel.r = bytes[idx++];
                last_pixel.g = bytes[idx++];
                last_pixel.b = bytes[idx++];
            }
            else if (byte == QOI_OP_RGBA) {
                last_pixel.r = bytes[idx++];
                last_pixel.g = bytes[idx++];
                last_pixel.b = bytes[idx++];
                last_pixel.a = bytes[idx++];
            }
            // 2. Index
            else if ((byte & QOI_MASK_2B) == QOI_OP_INDEX) {
                u8 index = byte & 0b00111111;
                last_pixel = prev_pixels[index];
            }
            // 3. Difference
            else if ((byte & QOI_MASK_2B) == QOI_OP_DIFF) {
                u8 dr = ((byte >> 4) & 0b11) - 2;
                u8 dg = ((byte >> 2) & 0b11) - 2;
                u8 db = ((byte >> 0) & 0b11) - 2;
                last_pixel.r += dr;
                last_pixel.g += dg;
                last_pixel.b += db;
            }
            else if ((byte & QOI_MASK_2B) == QOI_OP_LUMA) {
                u8 byte2 = bytes[idx++];
                u8 dg = (byte & 0b00111111) - 32;
                u8 db_dg = ((byte2 >> 0) & 0b1111) - 8;
                u8 dr_dg = ((byte2 >> 4) & 0b1111) - 8;
                last_pixel.r += (u8)(dr_dg + dg);
                last_pixel.g += dg;
                last_pixel.b += (u8)(db_dg + dg);
            }
            // 1. Run
            else if ((byte & QOI_MASK_2B) == QOI_OP_RUN) {
                run_length = (byte & 0b00111111) + 1;
                run_length--;
            }

            // store last pixel in previous pixels buffer
            prev_pixels[qoi_hash(last_pixel) % QOI_BUFFER_SIZE] = last_pixel;
        }

        // store pixel
        image->pixels[i * 4 + 0] = last_pixel.r;
        image->pixels[i * 4 + 1] = last_pixel.g;
        image->pixels[i * 4 + 2] = last_pixel.b;
        image->pixels[i * 4 + 3] = last_pixel.a;
    }
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

To manipulate bits we make use of a many _bitwise operations_, if you are unfamiliar with them or need a refresher, we invite you to read [our article]({{root}}notes/bit_ops.html) on the subject.

## Encoder
We have seen how to implement an image decoder but to create a QOI image, we must write an encoder.
An image encoder is usually much more complex than a decoder and slower to run.
QOI has been designed with the goal of making a very fast encoder (and decoder).
It achieves this objective primarily because of its simplicity, sacrificing compression ratio in favor of speed.

The encoder does essentially the reverse of the decoder: create a new file, write the header to the file, encode the chunks and finally write the chunks to the file.

```C
bool qoi_save(image_t* image, const char* file_name)
{
    // create new file
    FILE* file = fopen(file_name, "wb");
    if (!file) {
        return false;
    }

    // write header
    qoi_header_t header;
    memcpy(header.magic, QOI_MAGIC, 4);
    header.width = little_to_big(image->w);
    header.height = little_to_big(image->h);
    header.channels = image->channels;
    header.colorspace = (u8)QOI_COLOR_SPACE_SRGB;
    fwrite(&header, sizeof(header), 1, file);

    // encode chunks
    u8* bytes = (u8*)malloc(image->w * image->h * image->channels);
    u32 bytes_size = 0; // compressed size should be smaller than original size
    qoi_encode_chunks(image, bytes, &bytes_size);

    // write chunks
    fwrite(bytes, bytes_size, 1, file);
    free(bytes);

    fclose(file);
    return true;
}
```
The code is straighforward, the only tricky thing is to allocate a buffer to store the chunks that is big enough **before** we know what will be the final compressed size. We use the original image size knowing that the compressed size should be smaller even with the overhead of the file format (header and tags). Indeed if it was not the case then our "compression" wasn't very successful...

### Chunks encoding
Now for the chunks encoding we need to loop through all the pixels and each time choose one of the four compression methods.
Since we want to minimize the size of the image data, the method chosen should provide the best compression possible.
To choose a method we should try each one starting from the best to the worst:

1. Run (most efficient)
2. Index
3. Difference
4. Full (least efficient)

Sometimes a method will not be possible, for example if the pixel is not found in the index or the difference with the last pixel is too big.
Remember also that if the alpha channel changes we cannot use the _difference_ method.
The encoder, like the decoder, must keep the last pixel and a buffer of 64 previous pixels.

One thing that is quite nice about the QOI is that the encoder can be written piece by piece since each method is independent.
We can implement one method, test it and notice the change in file size.
This is very useful for development and debugging.
Beware though that because of this, a buggy encoder can produce a valid image that is not as compressed as it should be.
Simply producing an image that can be loaded by an image viewer does not mean that the encoder is properly implemented.

An implementation for the chunks encoding should look like this:
```C
void qoi_encode_chunks(image_t* image, u8* bytes, u32* bytes_size)
{
    // encode chunks as a byte stream
    rgba_t last_pixel; // last pixel, must be initialized as (0,0,0,255)
    last_pixel.r = 0;
    last_pixel.g = 0;
    last_pixel.b = 0;
    last_pixel.a = 255;
    rgba_t prev_pixels[QOI_BUFFER_SIZE] = {0}; // running array of previously seen pixels, must be zero-initialized
    u32 run_length = 0;
    u32 idx = 0; // index of current byte in stream
    for (u32 i = 0; i < image->w * image->h; i++) {
        rgba_t pixel;
        pixel.r = image->pixels[i * 4 + 0];
        pixel.g = image->pixels[i * 4 + 1];
        pixel.b = image->pixels[i * 4 + 2];
        pixel.a = image->pixels[i * 4 + 3];

        if (pixel.rgba == last_pixel.rgba) {
            run_length++;
            if (run_length == 62) { // TODO: check end?
                // 1. Run
                bytes[idx++] = QOI_OP_RUN | (u8)(run_length - 1);
                run_length = 0;
            }
        }
        else {   
            i32 dr = pixel.r - last_pixel.r;
            i32 dg = pixel.g - last_pixel.g;
            i32 db = pixel.b - last_pixel.b;
            i32 dr_dg = dr - dg;
            i32 db_dg = db - dg;

            u8 index = qoi_hash(pixel) % QOI_BUFFER_SIZE;

            // 1. Run
            if (run_length > 0) {
                assert(run_length <= 62);
                bytes[idx++] = QOI_OP_RUN | (u8)(run_length - 1);
                run_length = 0;
            }

            // 2. Index
            if (pixel.rgba == prev_pixels[index].rgba) {
                bytes[idx++] = QOI_OP_INDEX | index;
            }
            else if (pixel.a == last_pixel.a) {
                // 3. Difference
                if (
                    (dr >= -2 && dr <= 1) && 
                    (dg >= -2 && dg <= 1) && 
                    (db >= -2 && db <= 1)) {
                    
                    bytes[idx++] = QOI_OP_DIFF | ((u8)(dr + 2) << 4) | ((u8)(dg + 2) << 2) | ((u8)(db + 2) << 0);
                }
                else if (
                    (dg >= -32 && dg <= 31) &&
                    (dr_dg >= -8 && dr_dg <= 7 ) &&
                    (db_dg >= -8 && db_dg <= 7 )) {
                    
                    bytes[idx++] = QOI_OP_LUMA | (u8)(dg + 32);
                    bytes[idx++] = ((u8)(dr_dg + 8) << 4) | ((u8)(db_dg + 8) << 0);
                }
                // 4. Full
                else {
                    bytes[idx++] = QOI_OP_RGB;
                    bytes[idx++] = pixel.r;
                    bytes[idx++] = pixel.g;
                    bytes[idx++] = pixel.b;
                }
            }
            else {
                // 4. Full
                bytes[idx++] = QOI_OP_RGBA;
                bytes[idx++] = pixel.r;
                bytes[idx++] = pixel.g;
                bytes[idx++] = pixel.b;
                bytes[idx++] = pixel.a;
            }
            
            // store last pixel in previous pixels buffer
            last_pixel = pixel;
            prev_pixels[index] = last_pixel;
        }
    }

    // end of stream
    for (u32 i = 0; i < 7; i++) {
        bytes[idx++] = 0x00;
    }
    bytes[idx++] = 0x01;

    *bytes_size = idx - 1;
}
```
Notice that the code for the encoder is not much more complicated than the decoder.

You should now have a QOI image decoder and encoder that is fully compliant with the specification.
QOI can be used in place of PNG for faster compression and decompression at the expense of slightly bigger file sizes. Note however that PNG supports a whole bunch more options and metadata that can be useful depending on your needs.

In this article **we have omitted proper errors handling** to keep the code short, please see the full source code available on [GitHub](https://github.com/kevenv/image_viewer) for more details.

## References
- <https://qoiformat.org/>
- <https://phoboslab.org/log/2021/11/qoi-fast-lossless-image-compression>
- <https://en.wikipedia.org/wiki/QOI_(image_format)>
- <https://en.wikipedia.org/wiki/Run-length_encoding>
