from src.assembler.tokenizer import reset_lineno
from src.assembler.parser import paerser
from src.assembler.instruction_info import *


def get_register_index_binary(index) -> str:
    return '{0:05b}'.format(int(index))


def get_immediate_binary_5(value) -> str:
    value &= 0x1f
    return '{0:05b}'.format(int(value))


def get_immediate_binary_12(value) -> str:
    value &= 0xfff
    return '{0:012b}'.format(int(value))


def get_immediate_binary_12b(value) -> (str, str):
    imm_bits = get_immediate_binary_12(value)
    imm_bits_12_10to5 = imm_bits[0] + imm_bits[2:8]
    imm_bits_4to1_11 = imm_bits[8:12] + imm_bits[1]
    return imm_bits_12_10to5, imm_bits_4to1_11


def get_immediate_binary_12s(value) -> (str, str):
    imm_bits = get_immediate_binary_12(value)
    imm_bits_11to5 = imm_bits[0:7]
    imm_bits_4to0 = imm_bits[7:12]
    return imm_bits_11to5, imm_bits_4to0


def get_immediate_binary_20(value) -> str:
    value &= 0xfffff
    return '{0:020b}'.format(int(value))


def get_immediate_binary_20_jal(value) -> str:
    imm_bits = get_immediate_binary_20(value)
    return imm_bits[0] + imm_bits[10:20] + imm_bits[9] + imm_bits[1:9]


def decode_r_instruction(instruction_fields) -> str:
    opcode_bits = R_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    rs2_bits = get_register_index_binary(instruction_fields['rs2'])
    funct3_bits = R_FUNCT3[instruction_fields['opcode']]
    funct7_bits = R_FUNCT7[instruction_fields['opcode']]
    return funct7_bits + rs2_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits


def decode_i_instruction(instruction_fields) -> str:
    opcode_bits = I_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    funct3_bits = I_FUNCT3[instruction_fields['opcode']]
    imm_bits = get_immediate_binary_12(instruction_fields['imm'])
    return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits


def decode_i_shift_instruction(instruction_fields) -> str:
    opcode_bits = I_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    funct3_bits = I_FUNCT3[instruction_fields['opcode']]
    imm_bits = get_immediate_binary_5(instruction_fields['imm'])
    funct7_bits = I_SHIFT_FUNCT7[instruction_fields['opcode']]
    return funct7_bits + imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits


def decode_i_load_instruction(instruction_fields) -> str:
    opcode_bits = I_LOAD_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    funct3_bits = I_LOAD_FUNCT3[instruction_fields['opcode']]
    imm_bits = get_immediate_binary_12(instruction_fields['imm'])
    return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits


def decode_u_instruction(instruction_fields) -> str:
    opcode_bits = U_OPCODE[instruction_fields['opcode']]
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    imm_bits = get_immediate_binary_20(instruction_fields['imm'])
    return imm_bits + rd_bits + opcode_bits


def decode_jal_instruction(instruction_fields, labels, instruction_address) -> str:
    opcode_bits = JAL_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    target_address = labels[instruction_fields['label']]
    imm_value = (target_address - instruction_address) // 2
    imm_bits = get_immediate_binary_20_jal(imm_value)
    return imm_bits + rd_bits + opcode_bits


def decode_jalr_instruction(instruction_fields) -> str:
    opcode_bits = JALR_OPCODE
    rd_bits = get_register_index_binary(instruction_fields['rd'])
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    funct3_bits = JALR_FUNCT3
    imm_bits = get_immediate_binary_12(instruction_fields['imm'])
    return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits


def decode_b_instruction(instruction_fields, labels, instruction_address) -> str:
    opcode_bits = B_OPCODE
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    rs2_bits = get_register_index_binary(instruction_fields['rs2'])
    funct3_bits = B_FUNCT3[instruction_fields['opcode']]
    target_address = labels[instruction_fields['label']]
    imm_value = (target_address - instruction_address) // 2
    imm_bits_12_10to5, imm_bits_4to1_11 = get_immediate_binary_12b(imm_value)
    return imm_bits_12_10to5 + rs2_bits + rs1_bits + funct3_bits + imm_bits_4to1_11 + opcode_bits


def decode_s_instruction(instruction_fields) -> str:
    opcode_bits = S_OPCODE
    rs1_bits = get_register_index_binary(instruction_fields['rs1'])
    rs2_bits = get_register_index_binary(instruction_fields['rs2'])
    funct3_bits = S_FUNCT3[instruction_fields['opcode']]
    imm_bits_11to5, imm_bits_4to0 = get_immediate_binary_12s(instruction_fields['imm'])
    return imm_bits_11to5 + rs2_bits + rs1_bits + funct3_bits + imm_bits_4to0 + opcode_bits


def convert_to_hex(binary_code) -> str:
    hex_result = ""
    codes = binary_code.splitlines()
    for code in codes:
        hex_result += '{0:08x}'.format(int(code, 2)) + "\n"
    return hex_result


def assemble(filename) -> (str, str):
    try:
        with open(filename) as file:
            instruction_address = 0
            labels = {}
            for line in file:
                result = paerser.parse(line)
                if result['type'] == 'label':
                    labels[result['label']] = instruction_address
                else:
                    instruction_address += 4

            binary_code = ""
            instruction_address = 0
            file.seek(0, 0)
            reset_lineno()
            for line in file:
                result = paerser.parse(line)
                # print(result)

                if result['type'] == 'r_instruction':
                    binary_code += decode_r_instruction(result) + "\n"
                elif result['type'] == 'i_instruction':
                    if result['opcode'] in I_SHIFT_INSTRUCTION:
                        binary_code += decode_i_shift_instruction(result) + "\n"
                    else:
                        binary_code += decode_i_instruction(result) + "\n"
                elif result['type'] == 'i_load_instruction':
                    binary_code += decode_i_load_instruction(result) + "\n"
                elif result['type'] == 'u_instruction':
                    binary_code += decode_u_instruction(result) + "\n"
                elif result['type'] == 'jal_instruction':
                    binary_code += decode_jal_instruction(result, labels, instruction_address) + "\n"
                elif result['type'] == 'jalr_instruction':
                    binary_code += decode_jalr_instruction(result) + "\n"
                elif result['type'] == 'b_instruction':
                    binary_code += decode_b_instruction(result, labels, instruction_address) + "\n"
                elif result['type'] == 's_instruction':
                    binary_code += decode_s_instruction(result) + "\n"

                if 'instruction' in result['type']:
                    instruction_address += 4

            return binary_code, convert_to_hex(binary_code)
    except IOError:
        print("No such file!")
        return "", ""
