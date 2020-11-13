#!/usr/local/env python3
import struct
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

        if DEBUG or DEBUG_DWARF2:
            print("line program header:")
            for key, value in self.lnp_header:
                print("{} => {}".format(key, value))

    def process_file(self, target_addr):
        while 1:
            if self.indx >= self.size:
                break;

            # each CU has it own line number program header
            self.read_line_number_program_header()


            self.state_machine(target_addr)

            """
            go to the next prologue
            """
            # indx = end_cu_indx
            # # round up to 4 byets aligned
            # indx = ((indx + 4 - 1) / 4) * 4
            # if result[3] != -1:
            #     # found
            #     break

    def state_machine(self, target_addr):
        sm = { 
            "address" : 0, 
            "file" : 1, 
            "line" : 1, 
            "column" : 0, 
            "is_stmt" : 0, 
            "basic_block" : "false", 
            "end_sequence" : "false" 
        }

        end_cu_indx = stmt_ptr + prologue["unit_length"]
        i = indx
        while i < end_cu_indx:
            opcode = ord(data[i])

            if DEBUG or DEBUG_DWARF2:
                print("    i =", i, "indx =", indx, "stmt_ptr =", stmt_ptr, "unit_length =", prologue["unit_length"])
                print("    opcode = 0x%02X" % opcode)
                print("    base_addr = 0x%02X" % base_addr, "address = 0x%02X" % sm["address"], "target_addr = 0x%02X" % target_addr)

            if opcode >= prologue["opcode_base"]:
                # special opcode
                # get the adjusted opcode
                adj_opcode = opcode - prologue["opcode_base"]
                i += 1

                # step 1: add a signed integer to the line register
                sm["line"] += prologue["line_base"] + (adj_opcode % prologue["line_range"])

                # step 2: multiply an unsigned integer by the minimum_instruction_length filed of the statement program prologue and add the result to the address register
                sm["address"] += (adj_opcode / prologue["line_range"]) * prologue["minimum_instruction_length"]

                # step 3: append a row to the matrix using the current values of the state machine registers
                if (base_addr <= target_addr) & (sm["address"] >= target_addr):
                    # found
                    result[1] = dir[dir_indx]
                    result[2] = file_names[sm["file"] - 1]
                    result[3] = sm["line"]
                    break

                # step 4: set the basic_block register to "false"
                sm["basic_block"] = "false"
            elif opcode == 0:
                # extended opcode
                val, length = decode_uleb128(data[i + 1], end_cu_indx - i)
                opcode = ord(data[i + length + 1])
                i += value + length + 1

                if opcode == DW_LNE_end_sequence:
                    # set end_sequence register as true
                    sm["end_sequence"] = "true"

                    # append a row to the matrix using the current vaules of the state machine registers
                    # noteXXX: cannot use "address >= target_addr" since this is the end of a sequence
                    if (base_addr <= target_addr) & (sm["address"] > target_addr):
                        # found
                        result[1] = dir[dir_indx]
                        result[2] = file_names[sm["file"] - 1]
                        result[3] = sm["line"]
                        break

                    # reset registers
                    sm = { 
                        "address" : 0, 
                        "file" : 1, 
                        "line" : 1, 
                        "column" : 0, 
                        "is_stmt" : 0, 
                        "basic_block" : "false", 
                        "end_sequence" : "false" 
                    }
                elif opcode == DW_LNE_set_address:
                    # set the address register to the relocatable address
                    sm["address"] = ord(data[i + uleb128[1] + 2])
                    sm["address"] |= ord(data[i + uleb128[1] + 3]) << 8
                    sm["address"] |= ord(data[i + uleb128[1] + 4]) << 16
                    sm["address"] |= ord(data[i + uleb128[1] + 5]) << 24
                    base_addr = sm["address"]
                elif opcode == DW_LNE_define_file:
                    pass
                else:
                    print("ERROR: unknown extended opcode")
                    return result
            else:
                # standard opcode
                if opcode == DW_LNS_copy:
                    i += 1
                    if (base_addr <= target_addr) & (sm["address"] >= target_addr):
                        # found
                        result[1] = dir[dir_indx]
                        result[2] = file_names[sm["file"] - 1]
                        result[3] = sm["line"]
                        break
                    sm["basic_block"] = "false"
                elif opcode == DW_LNS_advance_pc:
                    val, length = decode_uleb128(data[i + 1: end_cu_indx], end_cu_indx - i)
                    sm["address"] += val * prologue["minimum_instruction_length"]
                    i += length + 1
                elif opcode == DW_LNS_advance_line:
                    val, length = decode_leb128(data[i + 1: end_cu_indx], end_cu_indx - i)
                    sm["line"] += val
                    i += length + 1
                elif opcode == DW_LNS_set_file:
                    sm["file"] , length = decode_uleb128(data[i + 1: end_cu_indx], end_cu_indx - i)
                    i += length + 1
                elif opcode == DW_LNS_set_column:
                    sm["column"], length = decode_uleb128(data[i + 1: end_cu_indx], end_cu_indx - i) 
                    i += length + 1
                elif opcode == DW_LNS_negate_stmt:
                    if sm["is_stmt"] == "true":
                        sm["is_stmt"] = "false"
                    else:
                        sm["is_stmt"] = "true"
                    i += 1
                elif opcode == DW_LNS_set_basic_block:
                    sm["basic_block"] = "true"
                    i += 1
                elif opcode == DW_LNS_const_add_pc:
                    sm["address"] += ((255 - prologue["opcode_base"]) / prologue["line_range"]) * prologue["minimum_instruction_length"]
                    i += 1
                elif opcode == DW_LNS_fixed_advance_pc:
                    adv = struct.unpack("<H", data[i + 1: end_cu_indx])
                    sm["address"] += adv
                    i += 3
                else:
                    print("ERROR: unknown standard opcode")
                    return result

            # skip if this statement program is not the candidate
            if sm["address"] != 0:
                if sm["address"] > target_addr:
                    break
                if (target_addr - sm["address"]) > 0x10000:
                    break