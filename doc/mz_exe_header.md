MZ EXE Header
-------------
References:
* http://www.delorie.com/djgpp/doc/exe/
* https://www.fileformat.info/format/exe/corion-mz.htm
* https://wiki.osdev.org/MZ
* http://www.tavi.co.uk/phobos/exeformat.html


| Offset  |        |         Field         |  Size  |                                                                 Description                                                                 |
|:-------:|:------:|:---------------------:|:------:|:-------------------------------------------------------------------------------------------------------------------------------------------:|
|  0      |  0x00  |  Signature            |  word  |  0x5A4D (ASCII for 'M' and 'Z')                                                                                                             |
|  2      |  0x02  |  Extra bytes          |  word  |  Number of bytes in the last page[^1].                                                                                                          |
|  4      |  0x04  |  Pages                |  word  |  Number of whole/partial pages[^1].                                                                                                             |
|  6      |  0x06  |  Relocation items     |  word  |  Number of entries in the relocation table.                                                                                                 |
|  8      |  0x08  |  Header size          |  word  |  The number of paragraphs[^2] taken up by the header.                                                                                           |
|  10     |  0x0A  |  Minimum allocation   |  word  |  The number of paragraphs[^2] required by the program, excluding the PSP and program image. If no free block is big enough, the loading stops.  |
|  12     |  0x0C  |  Maximum allocation   |  word  |  The number of paragraphs[^2] requested by the program. If no free block is big enough, the biggest one possible is allocated.                  |
|  14     |  0x0E  |  Initial SS           |  word  |  Relocatable segment address for SS.                                                                                                        |
|  16     |  0x10  |  Initial SP           |  word  |  Initial value for SP.                                                                                                                      |
|  18     |  0x12  |  Checksum             |  word  |  When added to the sum of all other words in the file, the result should be zero.                                                           |
|  20     |  0x14  |  Initial IP           |  word  |  Initial value for IP.                                                                                                                      |
|  22     |  0x16  |  Initial CS           |  word  |  Relocatable segment address for CS.                                                                                                        |
|  24     |  0x18  |  Relocation table     |  word  |  The (absolute) offset to the relocation table.                                                                                             |
|  26     |  0x1A  |  Overlay              |  word  |  Value used for overlay management. If zero, this is the main executable.                                                                   |
|  28     |  0x1C  |  Overlay information  |  N/A   |  Files sometimes contain extra information for the main's program overlay management.                                                       |

[^1]: The size of a page is 512 bytes

[^2]: The size of a paragraph is 16 bytes
