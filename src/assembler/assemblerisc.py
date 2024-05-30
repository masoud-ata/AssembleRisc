from assembler.tokenizer import reset_lineno
from assembler.parser import parser
from assembler.instruction_info import *
from assembler.immediate_generator import *


class AssembleRisc:
    def __init__(self):
        self.parse_info = {}
        self.instruction_address = 0
        self.labels_table = {}
        self.assembly_sequence = ""
        self.instruction_handlers = {
            'r_instruction': self._decode_r_instruction,
            'i_instruction': self._decode_i_instruction,
            'i_shift_instruction': self._decode_i_shift_instruction,
            'i_load_instruction': self._decode_i_load_instruction,
            'u_instruction': self._decode_u_instruction,
            'jal_instruction': self._decode_jal_instruction,
            'jalr_instruction': self._decode_jalr_instruction,
            'b_instruction': self._decode_b_instruction,
            's_instruction': self._decode_s_instruction,
            'fence_instruction': self._decode_fence_instruction,
            'compressed_r_instruction': self._decode_compressed_r_instruction,
            'compressed_i_instruction': self._decode_compressed_i_instruction,
            'compressed_b_instruction': self._decode_compressed_b_instruction,
            'compressed_l_load_instruction': self._decode_compressed_l_load_instruction,
            'compressed_l_store_instruction': self._decode_compressed_l_store_instruction,
            'compressed_j_instruction': self._decode_compressed_j_instruction,
            'compressed_j_r_instruction': self._decode_compressed_j_r_instruction,
            'floating_point_r_instruction': self._decode_floating_point_r_instruction
        }

    def _decode_r_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = R_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        rs2_bits = get_register_index_binary(instruction['rs2'])
        funct3_bits = R_FUNCT3[instruction['opcode']]
        funct7_bits = R_FUNCT7[instruction['opcode']]
        return funct7_bits + rs2_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_i_instruction(self) -> str:
        instruction = self.parse_info
        if instruction['opcode'] in I_ENVIRONMENT_INSTRUCTIONS + I_CSR_INSTRUCTIONS + I_CSRI_INSTRUCTIONS:
            opcode_bits = I_SYSTEM_OPCODE
        else:
            opcode_bits = I_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        funct3_bits = I_FUNCT3[instruction['opcode']]
        imm_bits = get_immediate_binary_12(instruction['imm'])
        return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_i_shift_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = I_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        funct3_bits = I_FUNCT3[instruction['opcode']]
        imm_bits = get_immediate_binary_5(instruction['imm'])
        funct7_bits = I_SHIFT_FUNCT7[instruction['opcode']]
        return funct7_bits + imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_i_load_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = I_LOAD_OPCODE[instruction['opcode']]
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        funct3_bits = I_LOAD_FUNCT3[instruction['opcode']]
        imm_bits = get_immediate_binary_12(instruction['imm'])
        return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_u_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = U_OPCODE[instruction['opcode']]
        rd_bits = get_register_index_binary(instruction['rd'])
        imm_bits = get_immediate_binary_20(instruction['imm'])
        return imm_bits + rd_bits + opcode_bits

    def _decode_jal_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = JAL_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        imm_bits = get_immediate_binary_20_jal(instruction['imm'])
        return imm_bits + rd_bits + opcode_bits

    def _decode_jalr_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = JALR_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        funct3_bits = JALR_FUNCT3
        imm_bits = get_immediate_binary_12(instruction['imm'])
        return imm_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_b_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = B_OPCODE
        rs1_bits = get_register_index_binary(instruction['rs1'])
        rs2_bits = get_register_index_binary(instruction['rs2'])
        funct3_bits = B_FUNCT3[instruction['opcode']]
        if 'imm' in instruction:
            imm_value = instruction['imm'] // 2
        else:
            target_address = self.labels_table[instruction['label']]
            imm_value = (target_address - self.instruction_address) // 2
        imm_bits_12_10to5, imm_bits_4to1_11 = get_immediate_binary_12b(imm_value)
        return imm_bits_12_10to5 + rs2_bits + rs1_bits + funct3_bits + imm_bits_4to1_11 + opcode_bits

    def _decode_s_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = S_OPCODE[instruction['opcode']]
        rs1_bits = get_register_index_binary(instruction['rs1'])
        rs2_bits = get_register_index_binary(instruction['rs2'])
        funct3_bits = S_FUNCT3[instruction['opcode']]
        imm_bits_11to5, imm_bits_4to0 = get_immediate_binary_12s(instruction['imm'])
        return imm_bits_11to5 + rs2_bits + rs1_bits + funct3_bits + imm_bits_4to0 + opcode_bits

    def _decode_fence_instruction(self) -> str:
        def fence_operand_to_bits(op: str) -> str:
            replace_dict = {"i": "8", "o": "4", "r": "2", "w": "1"}
            pred_vals = "".join([replace_dict.get(c, c) for c in op])
            return get_immediate_binary_4(sum([int(x) for x in pred_vals]))
        instruction = self.parse_info
        pred, succ = instruction['pred'], instruction['succ']
        pred_bits, succ_bits = fence_operand_to_bits(pred), fence_operand_to_bits(succ)
        opcode_bits = FENCE_OPCODE
        rs1_bits = '00000'
        rd_bits = '00000'
        funct3_bits = FENCE_FUNCT3[instruction['opcode']]
        return '0000' + pred_bits + succ_bits + rs1_bits + funct3_bits + rd_bits + opcode_bits

    def _decode_compressed_r_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = '01'
        if instruction['opcode'] in [INSTRUCTION_C_ADD, INSTRUCTION_C_MV]:
            opcode_bits = '10'
            if int(instruction['rd']) == 0 or int(instruction['rs2']) == 0:
                error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
                raise Exception(error_message)
            rd_bits = get_register_index_binary(instruction['rd'])
            rs2_bits = get_register_index_binary(instruction['rs2'])
            func_bit = COMPRESSED_R_FUNCT[instruction['opcode']]
            return '100' + func_bit + rd_bits + rs2_bits + opcode_bits
        else:
            if (
                    int(instruction['rd']) < 8 or int(instruction['rd']) > 15 or
                    int(instruction['rs2']) < 8 or int(instruction['rs2']) > 15
            ):
                error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
                raise Exception(error_message)
            rd_bits = get_compressed_register_index_binary(instruction['rd'])
            rs2_bits = get_compressed_register_index_binary(instruction['rs2'])
            funct_bits = COMPRESSED_R_FUNCT[instruction['opcode']]
            return '100' + '0' + '11' + rd_bits + funct_bits + rs2_bits + opcode_bits

    def _decode_compressed_i_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = COMPRESSED_I_OPCODE[instruction['opcode']]
        rd_bits = get_compressed_register_index_binary(instruction['rd'])
        if instruction['opcode'] == INSTRUCTION_C_ADDI4SPN:
            imm_bits = get_immediate_binary_8_addi4spn(instruction['imm'])
            funct3_bits = COMPRESSED_I_FUNCT3[instruction['opcode']]
            return funct3_bits + imm_bits + rd_bits + opcode_bits
        elif (
            instruction['opcode'] in [
                INSTRUCTION_C_ADDI, INSTRUCTION_C_LI, INSTRUCTION_C_LUI, INSTRUCTION_C_SLLI,
                INSTRUCTION_C_ADDI16SP, INSTRUCTION_C_NOP, INSTRUCTION_C_ADDI4SPN, INSTRUCTION_C_EBREAK,
                INSTRUCTION_C_SLLI64, INSTRUCTION_C_LWSP, INSTRUCTION_C_FLWSP, INSTRUCTION_C_FLDSP
            ]
        ):
            if instruction['opcode'] == INSTRUCTION_C_LUI and int(instruction['rd']) == 2:
                error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
                raise Exception(error_message)
            if instruction['opcode'] == INSTRUCTION_C_ADDI16SP and int(instruction['rd']) != 2:
                error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
                raise Exception(error_message)
            rd_bits = get_register_index_binary(instruction['rd'])
            if instruction['opcode'] in [INSTRUCTION_C_FLDSP]:
                imm_bits = get_immediate_binary_6_ldsp(instruction['imm'])
            elif instruction['opcode'] in [INSTRUCTION_C_LWSP, INSTRUCTION_C_FLWSP]:
                imm_bits = get_immediate_binary_6_lwsp(instruction['imm'])
            elif instruction['opcode'] == INSTRUCTION_C_ADDI16SP:
                imm_bits = get_immediate_binary_6_addi16sp(instruction['imm'])
            else:
                imm_bits = get_immediate_binary_6(instruction['imm'])
            imm_bits_part1, imm_bits_part2 = imm_bits[0], imm_bits[1:6]
            funct3_bits = COMPRESSED_I_FUNCT3[instruction['opcode']]
            return funct3_bits + imm_bits_part1 + rd_bits + imm_bits_part2 + opcode_bits
        else:
            if int(instruction['rd']) < 8 or int(instruction['rd']) > 15:
                error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
                raise Exception(error_message)
            rd_bits = get_compressed_register_index_binary(instruction['rd'])
            imm_bits = get_immediate_binary_6(instruction['imm'])
            funct2_bits = COMPRESSED_I_FUNCT2[instruction['opcode']]
            return '100' + imm_bits[0] + funct2_bits + rd_bits + imm_bits[1:6] + opcode_bits

    def _decode_compressed_b_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = '01'
        rs1_bits = get_compressed_register_index_binary(instruction['rs1'])
        funct3_bits = COMPRESSED_B_FUNCT3[instruction['opcode']]
        if 'imm' in instruction:
            imm_value = instruction['imm'] // 2
        else:
            target_address = self.labels_table[instruction['label']]
            imm_value = (target_address - self.instruction_address) // 2
        imm_bits_8_4to3, imm_bits_7to6_2to1_5 = get_immediate_binary_8_compressed_b(imm_value)
        return funct3_bits + imm_bits_8_4to3 + rs1_bits + imm_bits_7to6_2to1_5 + opcode_bits

    def _decode_compressed_l_load_instruction(self) -> str:
        instruction = self.parse_info
        if instruction['opcode'] in [INSTRUCTION_C_LW, INSTRUCTION_C_FLW] and int(instruction['imm']) % 4 != 0:
            error_message = 'Error: illegal immediate operand at line {}'.format(str(instruction['lineno']))
            raise Exception(error_message)
        if instruction['opcode'] == INSTRUCTION_C_FLD and int(instruction['imm']) % 8 != 0:
            error_message = 'Error: illegal immediate operand at line {}'.format(str(instruction['lineno']))
            raise Exception(error_message)
        opcode_bits = '00'
        rd_bits = get_compressed_register_index_binary(instruction['rd'])
        rs1_bits = get_compressed_register_index_binary(instruction['rs1'])
        funct3_bits = COMPRESSED_L_FUNCT3[instruction['opcode']]
        if instruction['opcode'] in [INSTRUCTION_C_LW, INSTRUCTION_C_FLW]:
            imm_bits_part1, imm_bits_part2 = get_immediate_binary_5_compressed_l(instruction['imm'])
        else:
            imm_bits_part1, imm_bits_part2 = get_immediate_binary_5_compressed_l_d(instruction['imm'])
        return funct3_bits + imm_bits_part1 + rs1_bits + imm_bits_part2 + rd_bits + opcode_bits

    def _decode_compressed_l_store_instruction(self) -> str:
        instruction = self.parse_info
        if instruction['opcode'] in [INSTRUCTION_C_SW, INSTRUCTION_C_FSW] and int(instruction['imm']) % 4 != 0:
            error_message = 'Error: illegal immediate operand at line {}'.format(str(instruction['lineno']))
            raise Exception(error_message)
        if instruction['opcode'] == INSTRUCTION_C_FSD and int(instruction['imm']) % 8 != 0:
            error_message = 'Error: illegal immediate operand at line {}'.format(str(instruction['lineno']))
            raise Exception(error_message)
        opcode_bits = '00'
        rs2_bits = get_compressed_register_index_binary(instruction['rs2'])
        rs1_bits = get_compressed_register_index_binary(instruction['rs1'])
        funct3_bits = COMPRESSED_L_FUNCT3[instruction['opcode']]
        if instruction['opcode'] in [INSTRUCTION_C_SW, INSTRUCTION_C_FSW]:
            imm_bits_part1, imm_bits_part2 = get_immediate_binary_5_compressed_l(instruction['imm'])
        else:
            imm_bits_part1, imm_bits_part2 = get_immediate_binary_5_compressed_l_d(instruction['imm'])
        return funct3_bits + imm_bits_part1 + rs1_bits + imm_bits_part2 + rs2_bits + opcode_bits

    def _decode_compressed_j_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = '01'
        imm_bits = get_immediate_binary_11_compressed_j(instruction['imm'])
        funct3_bits = COMPRESSED_J_FUNCT3[instruction['opcode']]
        return funct3_bits + imm_bits + opcode_bits

    def _decode_compressed_j_r_instruction(self) -> str:
        instruction = self.parse_info
        if int(instruction['rs1']) == 0:
            error_message = 'Error: illegal operands at line {}'.format(str(instruction['lineno']))
            raise Exception(error_message)

        opcode_bits = '10'
        rs1_bits = get_register_index_binary(instruction['rs1'])
        funct4_bits = COMPRESSED_J_R_FUNCT4[instruction['opcode']]
        return funct4_bits + rs1_bits + '00000' + opcode_bits

    def _decode_floating_point_r_instruction(self) -> str:
        instruction = self.parse_info
        opcode_bits = FLOATING_POINT_R_OPCODE
        rd_bits = get_register_index_binary(instruction['rd'])
        rs1_bits = get_register_index_binary(instruction['rs1'])
        rs2_bits = get_register_index_binary(instruction['rs2'])
        rm_funct3_bits = instruction['rm_funct3']
        funct7_bits = FLOATING_POINT_R_FUNCT7[instruction['opcode']]
        return funct7_bits + rs2_bits + rs1_bits + rm_funct3_bits + rd_bits + opcode_bits

    def find_labels_pass(self) -> None:
        self.instruction_address = 0
        for line in self.assembly_sequence.splitlines(keepends=True):
            self.parse_info = parser.parse(line)
            if self.parse_info['type'] == 'label':
                self.labels_table[self.parse_info['label']] = self.instruction_address
            else:
                if 'compressed' in self.parse_info['type']:
                    self.instruction_address += 2
                elif 'instruction' in self.parse_info['type']:
                    self.instruction_address += 4

    def parse_instructions_pass(self) -> str:
        binary_code = ""
        self.instruction_address = 0

        reset_lineno()
        for line in self.assembly_sequence.splitlines(keepends=True):
            self.parse_info = parser.parse(line)
            # print(self.parse_info)

            if 'instruction' in self.parse_info['type']:
                binary_code += self.instruction_handlers[self.parse_info['type']]() + "\n"
                if 'compressed' in self.parse_info['type']:
                    self.instruction_address += 2
                else:
                    self.instruction_address += 4

        return binary_code

    def assemble(self, filename) -> str:
        try:
            with open(filename) as file:
                self.assembly_sequence = file.read() + "\n"
                self.find_labels_pass()
                binary_code = self.parse_instructions_pass()
                return binary_code
        except IOError:
            error_message = 'Error: file {} not found'.format(filename)
            raise Exception(error_message)
