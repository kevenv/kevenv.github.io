# GIF image format (Part 1 : Format)

intro

## Description
anim = N images (max 15s to few minutes)
256 color palette
transparency color, no alpha
LZW compression > run length
can be uncompressed ~hack of LZW
pretty simple and straightforward
spec is very readable & small

## File
GIF Data Stream: sequential, byte stream, LSB

```
header
LSD
GCT*
other blocks
    GCE*
    Image Descriptor*
        LCT*
        Image data
            sub-blocks
            ...
            block terminator : block w size=0
    ...
trailer : 1 byte = 0x3B
```

## Blocks
```
fixed length if not data block

types
    control blocks (0x80-0xF9) -> change FSM of decoder
        header
        LSD
        GCE*
    graphics-rendering blocks (0x00-0x7F)
        ID
        PTE*
    special purpose blocks (0xFA-0xFF)
        trailer
        comment ext*
        app ext*

labels
    no labels: header, LSD, GCT, LCT
    labeled: ID, extension

extension
    label = 0x21
    ext code = 1 byte
    block size = 1 byte
        PTE,APE
            block size field to be skipped but still data sub-blocks
        CME
            !block size field because no header and cant be 0
    N sub-blocks
    block terminator : block w size=0
```

## Sub-blocks
sub-block and data blocks
vary size
    256 bytes max (including block size field)

image data and ext data has sub-blocks

1st byte = sub-block size (N)
    [0..255]
    block size field (for skipping)
        #bytes remaining in block
        !count block size field
        !count block terminator if present
N bytes = sub-block data

block terminator : sub-block w size=0

sub-blocks parse logic can be shared but 2x fread

## Header
6 bytes
magic
version
GIF87a: base
GIF89a: anim, 1-bit transparency, text overlay
    modern browsers, image editors, and social media platforms ignore the text extension
    most web browsers automatically displaying the frames with a delay time of 0.1 seconds

## Logical Screen Descriptor
7 bytes
w x h
GCT size
transparent color

logical screen
images = frames or subimages

## Global Color Table (GCT)*
array of colors (R,G,B)
N = #colors, max 256
size = 3 x 2^(N+1)

might be sorted in order of importance, most frequent color first

color palette
    1x GCT per file
    1x LCT per image/graphics
    GCT if no LCT
    only use one at a time

## Image

### Image Descriptor
10 bytes
start with 0x2C
pos of image (and size) in screen
interlaced?
size of LCT

### Local Color Table*
same as GCT, can be sorted

### Image data
1st byte = LZW min code size
N sub-blocks
    for each pixel, left to right and from top to bottom
    index to color table
    encoded in LZW

conclusion

## References
- <https://www.w3.org/Graphics/GIF/spec-gif89a.txt>
- <https://en.wikipedia.org/wiki/GIF>
- <https://www.matthewflickinger.com/lab/whatsinagif>
