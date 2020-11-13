#!/usr/local/env python3
from utils import decode_leb128, decode_uleb128

# define opcode
# standard opcode
DW_LNS_copy = 1
DW_LNS_advance_pc = 2
DW_LNS_advance_line = 3
DW_LNS_set_file = 4
DW_LNS_set_column = 5
DW_LNS_negate_stmt = 6
DW_LNS_set_basic_block = 7
DW_LNS_const_add_pc = 8
DW_LNS_fixed_advance_pc = 9
# extended opcode
DW_LNE_end_sequence = 1
DW_LNE_set_address = 2
DW_LNE_define_file = 3

debug = 0

class DWARF2:
    def __init__(self, data):
        self.lnp_header = {}
        self.data = data
        self.indx = 0
        self.stmt_ptr = 0
    
    def read_line_number_program_header(self):
        temp = struct.unpack("<LHLBBBBB", self.data[self.indx: self.indx + 15])
        self.lnp_header["unit_length"] = temp[0]
        self.lnp_header["version"] = temp[1]
        self.lnp_header["header_length"] = temp[2]
        self.lnp_header["minimum_instruction_length"] = temp[3]
        self.lnp_header["default_is_stmt"] = temp[4]
        self.lnp_header["line_base"] = temp[5]
        self.lnp_header["line_range"] = temp[6]
        self.lnp_header["opcode_base"] = temp[7]
        self.stmt_ptr = self.indx + 4
        self.indx = self.indx + 15

        if debug == 1:
            print("line program header:")
            for key, value in self.lnp_header:
                print("{} => {}".format(key, value))

    def process_file(self):
        while 1:
            if self.indx >= self.size:
                break;
            
            # each CU has it own line number program header
            self.read_line_number_program_header()

                        
