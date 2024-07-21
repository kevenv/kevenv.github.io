# Tar file format
On Unix systems, tar (Tape Archive) is a very popular file format to group a hierarchy of files and directories within a single file, otherwise known as an _archive_.
When compressed using gzip (tar.gz), it can compete with the infamous ZIP file format.
This format can also be used as a simple read-only file system, since it supports Unix file permissions.
In this article we will see how to implement a basic file archiver utility that supports tar files.
In [another article]({{root}}blog/gz_format.html) we will see how to compress a tar archive using `gzip` which uses the same compression method as ZIP.

## Format
A tar archive consists of a series of _file entries_ ending with an _end-of-archive_ entry.
[diagram]
Directories are also represented by a file entry.
The archive is divided into blocks of 512 bytes.

A file entry starts with a _header block_ describing the file and can contain zero or more _data blocks_ which contains the file's content right after. The size taken by a file in the archive might be bigger than its actual size as the smallest unit of allocation is the block, we must round up to the nearest block size.

Unused space in blocks is filled with zeros and the end-of-archive entry is simply two or more consecutive zero-filled blocks.

Note that there are multiple variants of the Tar file format.
The GNU tar utility `tar` seems to use the "gnu" format by default (which has a different `magic` + `version`) even though the documentation mentions that the default should be "posix". However both "posix" and "gnu" are based of the "ustar" format (Unix Standard Tar).
To stay out of this mess we will only support the most popular "ustar" format.

### Header
The header fits into a single block.
```C
struct __attribute__((packed)) tar_file_header_t {
    char name[100]; // absolute file path
    char mode[8]; // file permissions (octal)
    char uid[8]; // user ID (octal)
    char gid[8]; // group ID (octal)
    char size[12]; // file size (octal)
    char mtime[12]; // last modified time (octal)
    char chksum[8]; // checksum of header (octal)
    u8 typeflag; // type of file
    char linkname[100]; // absolute file path of the linked-to file
    char magic[6]; // tar file signature "ustar"
    char version[2]; // tar format version "00"
    char uname[32]; // name of user/owner
    char gname[32]; // name of group
    char devmajor[8]; // device major number (octal)
    char devminor[8]; // device minor number (octal)
    char prefix[155]; // prefix for file path if name > 100
};
```

To check the validity of a file entry, the header contains the `magic` and `version` field. In the case of the "ustar" format:
```C
#define TAR_MAGIC      "ustar"
#define TAR_VERSION    "00"
```

### File size
The weirdest and most annoying thing in the tar file format is that the fields containing numbers in the header are stored in **octal (base 8)** encoded as a null terminated ASCII string. We can use the following function to convert:
```C
u64 tar_oct_to_u64(const char* octal_str)
{
    u64 length = strlen(octal_str);
    u64 value = 0;
    for (u64 i = 0; i < length; ++i) {
        value *= 8;
        value += (u64)(octal_str[i] - '0');
    }
    return value;
}
```

The `size` field stores the size of the file in octal, it is set to zero in case of a directory or special files.

### File path
Each string in the header is made of ASCII characters and ends when `\0` is encountered. Note that they are are **not always null terminated**, as the last character can also be part of the string.

The absolute file path is contained in the `name` field.
If the path is bigger than 100 characters, the `prefix` must be used and follows the format `[prefix]/[name]`, for a maximum length of 256 characters (including the `/`). A prefix must be used if the first character of the `prefix` field is not `\0`.

### File permissions
The name of the user and group of a file is stored in the `uname` and `gname` fields respectively. `uid` and `gid` contain the corresponding Unix user ID and group ID in octal.
The [Unix file permissions](https://en.wikipedia.org/wiki/File-system_permissions#POSIX_permissions) are stored in the `mode` field in octal.
```C
//   U: user, G: group, O: other
//   R: read, W: write, X: execute
#define TAR_MODE_O_X      (1 << 0)
#define TAR_MODE_O_W      (1 << 1)
#define TAR_MODE_O_R      (1 << 2)
#define TAR_MODE_G_X      (1 << 3)
#define TAR_MODE_G_W      (1 << 4)
#define TAR_MODE_G_R      (1 << 5)
#define TAR_MODE_U_X      (1 << 6)
#define TAR_MODE_U_W      (1 << 7)
#define TAR_MODE_U_R      (1 << 8)
#define TAR_MODE_RESERVED (1 << 9)
#define TAR_MODE_GID_X    (1 << 10)
#define TAR_MODE_UID_X    (1 << 11)
```

### File type
The `typeflag` field contains the type of file, i.e. if it is a file, a directory or a special file.
Our implementation will only support files and directories.
```C
enum tar_type_t {
    TAR_TYPE_NORMAL0          = '\0',
    TAR_TYPE_NORMAL           = '0',
    TAR_TYPE_HARD_LINK        = '1',
    TAR_TYPE_SYMBOLIC_LINK    = '2',
    TAR_TYPE_CHARACTER_DEVICE = '3',
    TAR_TYPE_BLOCK_DEVICE     = '4',
    TAR_TYPE_DIRECTORY        = '5',
    TAR_TYPE_FIFO             = '6',
    TAR_TYPE_RESERVED         = '7',
};
```

When the file is a _hard link_ or a _symbolic link_, the `linkname` field specifies the absolute path of what it is linked to.
Note that the linked-to path is limited to 100 characters and does not use the `prefix`.

When the file is a _device file_, the `devmajor` and `devminor` fields contain the device number, which is used to associate the device to a device driver in a Unix system. Those fields are in octal.

### Modified time
The date and time of the last time that the file was modified (modified time) is stored in the `mtime` field as octal. It is simply a [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time), the number of seconds between a particular date and the Unix epoch (January 1st 1970 at UTC).
It can be decoded using a function like this:
```C
#include <time.h> // time_t

void tar_get_mtime(tar_file_header_t* header, char* mtime, u32 size)
{
    u64 mtime_timestamp = tar_oct_to_u64(header->mtime);
    time_t timestamp = (time_t)mtime_timestamp;
    struct tm* time_info = localtime(&timestamp);
    strftime(mtime, size, "%Y-%m-%d %H:%M:%S", time_info);
}
```

### Checksum
Finally, the `chksum` field contains the sum of all bytes in the header in octal. It can be used to validate that the file entry is valid.
```C
u32 tar_compute_checksum(tar_file_header_t* header)
{
    u32 checksum = 0;
    u8* bytes = (u8*)header;
    for (u32 i = 0; i < sizeof(tar_file_header_t); ++i) {
        if (i >= 148 && i < 148+8) {
            checksum += (u8)' '; // must count "chksum" as spaces
        }
        else {
            checksum += bytes[i];
        }
    }
    return checksum;
}
```

## List
only basic fields

## Create

## Extract

## References
- Specification:
    - [https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/tar.h.html](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/tar.h.html)
    - [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_13_06](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_13_06)
    - [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_18_03](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_18_03)
- GNU Tar:
    - [https://www.gnu.org/software/tar/manual/html_node/index.html](https://www.gnu.org/software/tar/manual/html_node/index.html)
    - [https://www.gnu.org/software/tar/manual/html_node/Standard.html#Standard](https://www.gnu.org/software/tar/manual/html_node/index.html)
    - [https://www.gnu.org/software/tar/manual/html_node/Formats.html#Formats](https://www.gnu.org/software/tar/manual/html_node/Formats.html#Formats)
- Wiki:
    - [https://wiki.osdev.org/USTAR](https://wiki.osdev.org/USTAR)
    - [https://wiki.osdev.org/Tar](https://wiki.osdev.org/Tar)
    - [https://en.wikipedia.org/wiki/Tar_(computing)](https://en.wikipedia.org/wiki/Tar_(computing))
