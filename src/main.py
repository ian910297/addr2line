#!/usr/bin/env python

"""
lsba: List Source code by Address
"""

import sys
import getopt
import struct
import os

def usage():
    print "Usage: lsba [-e|--elf] elf_path [-s|--source] source_path"
    print "            [-h]"
    print "       -e|--elf: specify full path of the ELF file"
    print "       -s|--source: specify full path of MAUI load"
    print "       -h: show this help"

def read_debug_line(data, size, target_addr, debug):
    # assume cannot-find by default
    result = [ "", "", "", -1 ]

    # initialize state machine
    sm = { "address" : 0, "file" : 1, "line" : 1, "column" : 0, "is_stmt" : 0, "basic_block" : "false", "end_sequence" : "false" }


    """
        execute the line number program
    """

    while 1:
        # read starndard opcode lengths array
        std_opcode_len = []
        for i in range(0, prologue["opcode_base"] - 1):
            std_opcode_len.append(copy.copy(ord(data[indx])))
            indx = indx + 1
        prologue["standard_opcode_lengths"] = std_opcode_len

        if debug == 1:
            print "    standard_opcode_lengths =", prologue["standard_opcode_lengths"]

        # read include directories
        dir = []
        temp_dir = data[indx: i + prologue["unit_length"]].split('\0')
        temp_len = 0
        for i in range(0, len(temp_dir)):
            dir.append(copy.copy(temp_dir[i]))
            if temp_dir[i] == '':
                temp_len += 1
                break
            else:
                temp_len += len(temp_dir[i]) + 1
        indx += temp_len

        if debug == 1:
            print "    include directories =", dir

        # read file names
        file_names = []
        i = indx
        while 1:
            # first entry
            # read file_name
            file_name = data[i: i + prologue["unit_length"]].split('\0')[0]
            i += len(file_name) + 1

            # read dir_indx
            dir_indx, length = decode_uleb128(data[i: i + prologue["unit_length"]], prologue["header_length"])
            i += length

            # read file time
            file_time, length = decode_uleb128(data[i: i + prologue["unit_length"]], prologue["header_length"])
            i += length

            # read file length
            file_len, length = decode_uleb128(data[i: i + prologue["unit_length"]], prologue["header_length"])
            i += length

            file_names.append(copy.copy(file_name))

            if data[i] == '\0':
                break

        indx = i + 1

        if debug == 1:
            print "    file_names =", ",".join(file_names)
            print "    dir_indx =", dir_indx
            print "    time =", file_time
            print "    length =", file_len
            print ""

    return result


# def list_source(load_path, dir, file_name, line, debug):
#     full_path = ""

#     try:
#         if debug == 1:
#             print "    open", load_path + file_name
#         f = open(load_path + file_name)
#         full_path = file_name
#     except IOError:
#         # try to add a prefix of path
#         if debug == 1:
#             print "    fail to open", load_path + file_name
#             print "    open", load_path + dir + file_name
#         try:
#             f = open(load_path + dir + file_name)
#             full_path = load_path + dir + file_name
#         except IOError:
#             if dir == "":
#                 print "fail to open", load_path + file_name
#             else:
#                 print "fail to open", load_path + file_name, "or", load_path + dir + file_name

#     if full_path == "":
#         return

#     try:
#         try:

#             start_line = line - 10
#             if start_line < 0:
#                 start_line = 0
#             end_line = line + 10

#             cur_line = 1
#             while 1:
#                 source = f.readline()
#                 if source == "":
#                     break
#                 if (cur_line >= start_line) & (cur_line <= end_line):
#                     print "%7d" % cur_line, "  ", source[:len(source) - 1]
#                 cur_line += 1
#                 if cur_line > end_line:
#                     break;

def lsba(argv):
        try:
            # result = [function_name, source_file, line_nr]
            result = [ "", "", -1 ]

            result = read_debug_line(data, sh_tbl[nr_sh]["size"], addr, debug)
            if result[3] == -1:
                print "fail to find source file for 0x%X" % addr
                print ""
            else:
                print "source file information:"
                print "    diretory =", result[1]
                print "    file name =", result[2]
                print "    line number =", result[3]
                print ""

                print "list source:"
                print ""
                list_source(load_path, result[1], result[2], result[3], debug)


def parse_option(argv):
    try:
        opts, args = getopt.getopt(argv, "hde:s:", ["elf=", "source="])
    except getopt.GetoptError:
        usage()
        sys.exit(er_invalid_arg)

    elf_path = ""
    source_path = ""

    for opt, arg in opts:
        if opt == "-d":
            debug = 1
        elif opt == "-h":
            usage()
            sys.exit(er_show_help)
        elif opt in ("--elf", "-e"):
            elf_path = arg
        elif opt in ("--source", "-s"):
            source_path = arg

    if elf_path == "":
        usage()
        sys.exit(er_invalid_arg)

    if source_path == "":
        # use MAUI directory structure by default
        (path, name) = os.path.split(elf_path)
        if path != "":
            source_path = os.path.abspath(path + os.path.sep + ".." + os.path.sep + ".." + os.path.sep)

    if len(source_path) != 0:
        if source_path[len(source_path) - 1] != os.path.sep:
            source_path += os.path.sep

if __name__ == "__main__":
    parse_option(sys.argv[1:])

    while 1:
        addr = raw_input()



