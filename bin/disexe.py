#!/usr/bin/env python3
# Reference:  http://www.delorie.com/djgpp/doc/exe/

# The goal is to disassemble a standard MZ EXE file and properly read it.

import sys
import codecs
import struct
import json


class BadFormatException(Exception):
    pass


# Python's struct.unpack reference:
# c - char (1-byte string)
# b - signed char (1-byte integer)
# B - unsigned char (1-byte integer)
# h - signed short (2-byte integer)
# H - unsigned short (2-byte integer)


# 00-01 Magic Number 'MZ' of MZ EXE format
# 02-03 The number of bytes in the last block fo the program that are actually
#       used.  If this value is zero, the entire last 512 bytes are used
# 04-05 Number of blocks in the flie that are part of the EXE file.  If 02-03
#       is non-zero, only that much of the last block is used.
def get_mz_exe(data):
    if data[0:2] != b"MZ":
        raise BadFormatException("get_mz_exe: Magic Number is not MZ!")

    exe = {}
    (
        exe["signature"],
        exe["bytes_in_last_block"],
        exe["blocks_in_file"],
        exe["num_relocs"],
        exe["header_paragraphs"],
        exe["min_extra_paragraphs"],
        exe["max_extra_paragraphs"],
        exe["ss"],
        exe["sp"],
        exe["checksum"],
        exe["ip"],
        exe["cs"],
        exe["reloc_table_offset"],
        exe["overlay_number"],
    ) = struct.unpack("H" * 14, data[0:28])

    # The offset of the beginning of the EXE data is computed like this:
    exe["exe_data_start"] = exe["header_paragraphs"] * 16

    # The offset of the byte just after the EXE data
    exe["extra_data_start"] = exe["blocks_in_file"] * 512
    if exe["bytes_in_last_block"]:
        exe["extra_data_start"] -= 512 - exe["bytes_in_last_block"]

    # Relocation table read:
    exe["reloc_table"] = []
    for i in range(exe["num_relocs"]):
        loc = exe["reloc_table_offset"] + (i * 2)
        (offset, segment) = struct.unpack("HH", data[loc : loc + 4])
        exe["reloc_table"].append({"offset": offset, "segment": segment})

    return exe


if __name__ == "__main__":
    filename = sys.argv[1]

    # Read data from argv[1] filename - this will need to be refactored for
    # streaming so that a large file can be read
    with open(filename, "rb") as _fp:
        data = _fp.read()

    # Check Signature
    print(data[0:2])
    if data[0:2] == b"MZ":
        exe = get_mz_exe(data)

    # Print out structure
    print(json.dumps(exe, indent=2, sort_keys=True))
