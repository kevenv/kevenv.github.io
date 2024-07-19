# Tar file format

since it supports unix file permissions and users
can also be used as a simple read-only FS

many variants:
[/]gnu?
ustar
posix = ustar without limits + extra features
    This archive format will be the default format for future versions of GNU tar.
    any tar implementation able to read ‘ustar’ archives should be able to read most ‘posix’ archives as well

ustar archive
series of fixed-size logical record of 512b
file = header logical record + data logical records
end of archive = atleast two 512-octet logical records, zero initialized


// USTAR or TAR (Unix Standard TAR)
// - Portable archive without compression
// - hierarchy of files and folders -> single file

record or sector or block?

// - array of 512 bytes sectors
// - 2 kind of sectors:
//     - metadata
//     - data
// - little endian
// - file size stored as ASCII octal string
// - space left in sectors is filled with zeros
// - end = at least two consecutive zero-filled sectors

// file and directory
//   1 metadata sector
//   N data sectors (N rounded up to 512 bytes)

## Format

## List

## Create

## Extract

## References
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/tar.h.html
https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_13_06
https://pubs.opengroup.org/onlinepubs/9699919799/utilities/pax.html#tag_20_92_18_03

https://www.gnu.org/software/tar/manual/html_node/index.html
https://www.gnu.org/software/tar/manual/html_node/Standard.html#Standard
https://www.gnu.org/software/tar/manual/html_node/Formats.html#Formats

https://wiki.osdev.org/USTAR
https://wiki.osdev.org/Tar
https://en.wikipedia.org/wiki/Tar_(computing)
