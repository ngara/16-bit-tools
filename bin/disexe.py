#!/usr/bin/env python3

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


def print_hex(data):
    # Thanks https://stackoverflow.com/questions/9100662
    # /how-to-print-integers-as-hex-strings-using-json-dumps-in-python
    print(
        json.dumps(
            json.loads(
                json.dumps(data),
                parse_int=lambda i: hex(int(i)).upper().replace("X", "x"),
            ),
            indent=2,
            sort_keys=True,
        )
    )


def read_mz_exe_header(data):
    if data[0:2] != b"MZ":
        raise BadFormatException("get_mz_exe: Magic Number is not MZ!")

    # MZ EXE Header
    # -------------
    # See doc/mz_exe_header.md for more information
    exe = {}
    exe["signature"] = data[0:2].decode("utf-8")
    (
        exe["bytes_in_last_block"],
        exe["blocks_in_file"],
        exe["num_relocs"],
        # Offset of assembled/linked image (the load module)
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
    ) = struct.unpack("<" + "H" * 13, data[2:28])
    # There may be overlay information of varying size at offset 28

    # The offset of the beginning of the EXE data is computed like this:
    exe["exe_data_start"] = exe["header_paragraphs"] * 16

    # The offset of the byte just after the EXE data
    exe["extra_data_start"] = exe["blocks_in_file"] * 512
    if exe["bytes_in_last_block"]:
        exe["extra_data_start"] -= 512 - exe["bytes_in_last_block"]

    # Relocation table
    # ----------------
    # See doc/mz_exe_header.md for more information
    #
    # After the header, there follow the relocation items, which are used to
    # span multpile segments. The relocation items have the following format :
    #       OFFSET              Count TYPE   Description
    #       0000h                   1 word   Offset within segment
    #       0002h                   1 word   Segment of relocation
    # To get the position of the relocation within the file, you have to
    # compute the physical adress from the segment:offset pair, which is done
    # by multiplying the segment by 16 and adding the offset and then adding
    # the offset of the binary start. Note that the raw binary code starts on
    # a paragraph boundary within the executable file. All segments are
    # relative to the start of the executable in memory, and this value must
    # be added to every segment if relocation is done manually.
    exe["reloc_table"] = []
    for i in range(exe["num_relocs"]):
        loc = exe["reloc_table_offset"] + (i * 4)
        (offset, segment) = struct.unpack("HH", data[loc : loc + 4])
        exe["reloc_table"].append({"offset": offset, "segment": segment})

    #

    return exe


if __name__ == "__main__":
    filename = sys.argv[1]

    # Read data from argv[1] filename - this will need to be refactored for
    # streaming so that a large file can be read
    with open(filename, "rb") as _fp:
        data = _fp.read()

    # Check Signature
    if data[0:2] == b"MZ":
        exe = read_mz_exe_header(data)

    # Print out structure
    reloc_table = exe["reloc_table"]
    exe["reloc_table"] = []
    print_hex(exe)
    print("Relocations: %s" % len(reloc_table))
