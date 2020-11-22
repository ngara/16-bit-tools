#!/usr/bin/env python3
# Reference:  http://www.delorie.com/djgpp/doc/exe/

# The goal is to disassemble a standard MZ EXE file and properly read it.

import sys
import codecs
import struct


filename = sys.argv[1]

with open(filename, "rb") as _fp:
    data = _fp.read()

# struct.unpack reference:
# c - char (1 byte string)
# b - signed char (1 integer)
# B - unsigned char (1 integer)
# h - signed short (2 integer)
# H - unsigned short (2 integer)
#

# 00-01 Magic Number 'MZ' of MZ EXE format
magic_number = b"".join(struct.unpack("cc", data[0:2])).decode("utf-8")

# 02-03 The number of bytes in the last block fo the program that are actually
#       used.  If this value is zero, the entire last 512 bytes are used
# 04-05 Number of blocks in the flie that are part of the EXE file.  If 02-03
#       is non-zero, only that much of the last block is used.
(last_block_bytes, num_blocks) = struct.unpack("HH", data[2:6])

print(last_block_bytes, num_blocks)
