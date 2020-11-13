#!/usr/local/env python3

DEBUG = 0
DEBUG_ELF = 0
DEBUG_DWARF2 = 0

def decode_uleb128(data, size):
    val = 0
    shift = 0
    len = 0
    for i in range(0, size):
        len += 1
        val |= (ord(data[i]) & 0x7f) << shift
        shift += 7
        if (ord(data[i]) & 0x80) == 0:
            break
    return val, len


def decode_leb128(data, size):
    val = 0
    shift = 0
    len = 0
    for i in range(0, size):
        len += 1
        val |= (ord(data[i]) & 0x7f) << shift
        shift += 7
        if (ord(data[i]) & 0x80) == 0:
            break
    if (shift < size) & ((ord(data[i]) & 0x40) != 0):
        val |= -(1 << shift)

    return val, len
