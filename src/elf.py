#!/usr/local/env python3

from utils import DEBUG, DEBUG_ELF

class ELF:
    def __init__(self, path):
        self.fp = open(path, "rb")
        # elf header
        self.elf_hdr = {}
        # section header array
        self.sh_tbl = []

    def read_elf_header(self):
        # # result = [function_name, source_file, line_nr]
        # result = [ "", "", -1 ]
        elf_hdr = self.elf_hdr
        temp = struct.unpack("<BBBBBBBBBBBBBBBBHHLLLLLHHHHHHH", self.fp.read(54))
        elf_hdr["ident"] = temp[0]
        elf_hdr["type"] = temp[16]
        elf_hdr["machine"] = temp[17]
        elf_hdr["version"] = temp[18]
        elf_hdr["entry"] = temp[19]
        elf_hdr["phoff"] = temp[20]
        elf_hdr["shoff"] = temp[21]
        elf_hdr["flags"] = temp[22]
        elf_hdr["ehsize"] = temp[23]
        elf_hdr["phentsize"] = temp[24]
        elf_hdr["phnum"] = temp[25]
        elf_hdr["shentsize"] = temp[26]
        elf_hdr["shnum"] = temp[27]
        elf_hdr["shstrndx"] = temp[28]

    def read_section_header(self):
        fp = self.fp
        elf_hdr = self.elf_hdr
        sh_tbl = self.sh_tbl
        fp.seek(elf_hdr["shoff"], 0)
        for i in range (0, elf_hdr["shnum"]):
            data = fp.read(elf_hdr["shentsize"])
            temp = struct.unpack("<LLLLLLLLLL", data)
            sh = {}
            sh["name"] = temp[0]
            sh["type"] = temp[1]
            sh["flags"] = temp[2]
            sh["addr"] = temp[3]
            sh["offset"] = temp[4]
            sh["size"] = temp[5]
            sh["link"] = temp[6]
            sh["info"] = temp[7]
            sh["addralign"] = temp[8]
            sh["entsize"] = temp[9]
            sh_tbl.append(sh)
    
    def read_section_by_name(self, target_name):
        fp = self.fp
        elf_hdr = self.elf_hdr
        sh_tbl = self.sh_tbl
        
        number_sh = -1
        for i in range (0, elf_hdr["shnum"]):
            name = str_tbl[sh_tbl[i]["name"]:].split('\0')
            if debug == 1:
                print "section", i, ":", name[0]
            if name[0] == target_name:
                number_sh = i
        if number_sh == -1:
            sys.exit(nr_internal)
        

        fp.seek(sh_tbl[number_sh]["offset"], 0)
        data = fp.read(sh_tbl[number_sh]["size"])
        
        if DEBUG or DEBUG_ELF:
            for key, value in sh_tbl[number_sh]:
                print("{} => {}".format(key, value))
        return data

