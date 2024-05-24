import ply.yacc as yacc

from assembler.tokenizer import tokens
from assembler.instruction_info import *
from assembler.pre_process import get_x_register_index, get_f_register_index
from assembler.csr_registers import CSR_ENCODING_TABLE


def to_int(field: str) -> int:
    if '0x' in field:
        return int(field, 16)
    else:
        return int(field)


def p_instruction_no_args(p):
    """expression : ID NEWLINE"""
    if p[1] in I_ENVIRONMENT_INSTRUCTIONS:
        p[0] = {
            'type': 'i_instruction',
            'opcode': p[1],
            'rd': '0',
            'rs1': '0',
            'imm': 0 if p[1] == INSTRUCTION_ECALL else 1,
            'lineno': p.lineno(1)
        }
    elif p[1] == 'nop':
        p[0] = {
            'type': 'i_instruction',
            'opcode': 'addi',
            'rd': get_x_register_index('x0'),
            'rs1': get_x_register_index('x0'),
            'imm': 0,
            'lineno': p.lineno(1)
        }
    elif p[1] == 'ret':
        p[0] = {
            'type': 'jalr_instruction',
            'opcode': 'jalr',
            'rd': get_x_register_index('x0'),
            'rs1': get_x_register_index('x1'),
            'imm': 0,
            'lineno': p.lineno(1)
        }
    else:
        error_message = f'Error: unrecognized instruction at line {p.lineno(1)}'
        raise Exception(error_message)


def p_label(p):
    """expression : LABEL_COLON NEWLINE"""
    p[0] = {
        'type': 'label',
        'label': p[1].replace(":", ""),
        'lineno': p.lineno(1)
    }


def p_instruction_xreg_xreg_xreg(p):
    """expression : ID register COMMA register COMMA register NEWLINE"""
    p[0] = {
        'type': 'r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_x_register_index(p[4]),
        'rs2': get_x_register_index(p[6]),
        'lineno': p.lineno(1)
    }


def p_instruction_xreg_xreg_imm(p):
    """expression : ID register COMMA register COMMA IMMEDIATE NEWLINE"""
    if p[1] in B_INSTRUCTIONS:
        p[0] = {
            'type': 'b_instruction',
            'opcode': p[1],
            'rs1': get_x_register_index(p[2]),
            'rs2': get_x_register_index(p[4]),
            'imm': to_int(p[6]),
            'lineno': p.lineno(1)
        }
    else:
        instruction = 'i_shift_instruction' if p[1] in I_SHIFT_INSTRUCTIONS else 'i_instruction'
        p[0] = {
            'type': instruction,
            'opcode': p[1],
            'rd': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[4]),
            'imm': to_int(p[6]),
            'lineno': p.lineno(1)
        }


def p_instruction_xreg_imm_xreg(p):
    """expression : ID register COMMA IMMEDIATE COMMA register NEWLINE"""
    if p[1] not in I_CSR_INSTRUCTIONS:
        error_message = f'Error: illegal or incomplete instruction at line {p.lineno(1)}'
        raise Exception(error_message)
    p[0] = {
        'type': 'i_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_x_register_index(p[6]),
        'imm': to_int(p[4]),
        'lineno': p.lineno(1)
    }


def p_instruction_xreg_id_xreg(p):
    """expression : ID register COMMA ID COMMA register NEWLINE"""
    if p[1] not in I_CSR_INSTRUCTIONS:
        error_message = f'Error: illegal or incomplete instruction at line {p.lineno(1)}'
        raise Exception(error_message)
    if p[4] not in CSR_ENCODING_TABLE:
        error_message = f'Error: unkown CSR {p[4]} at line {p.lineno(1)}'
        raise Exception(error_message)
    p[0] = {
        'type': 'i_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_x_register_index(p[6]),
        'imm': CSR_ENCODING_TABLE[p[4]],
        'lineno': p.lineno(1)
    }


def p_instruction_xreg_imm_lparen_xreg_rparen(p):
    """expression : ID register COMMA IMMEDIATE LEFT_PAREN register RIGHT_PAREN NEWLINE"""
    if p[1] == INSTRUCTION_JALR:
        p[0] = {
            'type': 'jalr_instruction',
            'opcode': p[1],
            'rd': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }
    elif p[1] in I_LOAD_INSTRUCTIONS:
        p[0] = {
            'type': 'i_load_instruction',
            'opcode': p[1],
            'rd': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }
    else:
        p[0] = {
            'type': 's_instruction',
            'opcode': p[1],
            'rs2': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }


def p_instruction_xreg_imm(p):
    """expression : ID register COMMA IMMEDIATE NEWLINE"""
    instruction = 'jal_instruction' if p[1] == INSTRUCTION_JAL else 'u_instruction'
    p[0] = {
        'type': instruction,
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'imm': to_int(p[4]),
        'lineno': p.lineno(1)
    }


def p_instruction_xreg_xreg_id(p):
    """expression : ID register COMMA register COMMA ID NEWLINE"""
    p[0] = {
        'type': 'b_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'rs2': get_x_register_index(p[4]),
        'label': p[6],
        'lineno': p.lineno(1)
    }


def p_compressed_instruction_xreg_xreg(p):
    """expression : COMPRESSED_ID register COMMA register NEWLINE"""
    p[0] = {
        'type': 'compressed_r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs2': get_x_register_index(p[4]),
        'lineno': p.lineno(1)
    }


def p_compressed_instruction_xreg_imm(p):
    """expression : COMPRESSED_ID register COMMA IMMEDIATE NEWLINE"""
    if p[1] in COMPRESSED_B_INSTRUCTIONS:
        x_reg_index = int(get_x_register_index(p[2]))
        if x_reg_index < 8 or x_reg_index > 15:
            error_message = f'Error: illegal operands at line {p.lineno(1)}'
            raise Exception(error_message)
        p[0] = {
            'type': 'compressed_b_instruction',
            'opcode': p[1],
            'rs1': get_x_register_index(p[2]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }
    else:
        p[0] = {
            'type': 'compressed_i_instruction',
            'opcode': p[1],
            'rd': get_x_register_index(p[2]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }


def p_compressed_instruction_xreg_id(p):
    """expression : COMPRESSED_ID register COMMA ID NEWLINE"""
    x_reg_index = int(get_x_register_index(p[2]))
    if x_reg_index < 8 or x_reg_index > 15:
        error_message = f'Error: illegal operands at line {p.lineno(1)}'
        raise Exception(error_message)
    p[0] = {
        'type': 'compressed_b_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'label': p[4],
        'lineno': p.lineno(1)
    }


def p_compressed_instruction_xreg_imm_lparen_xreg_rparen(p):
    """expression : COMPRESSED_ID register COMMA IMMEDIATE LEFT_PAREN register RIGHT_PAREN NEWLINE"""
    if p[1] == INSTRUCTION_C_LW:
        p[0] = {
            'type': 'compressed_l_load_instruction',
            'opcode': p[1],
            'rd': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }
    else:
        p[0] = {
            'type': 'compressed_l_store_instruction',
            'opcode': p[1],
            'rs2': get_x_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }


def p_compressed_instruction_imm(p):
    """expression : COMPRESSED_ID IMMEDIATE NEWLINE"""
    p[0] = {
        'type': 'compressed_j_instruction',
        'opcode': p[1],
        'imm': to_int(p[2]),
        'lineno': p.lineno(1)
    }


def p_compressed_instruction_xreg(p):
    """expression : COMPRESSED_ID register NEWLINE"""
    if p[1] not in COMPRESSED_J_R_INSTRUCTIONS:
        error_message = f'Error: illegal or incomplete instruction at line {p.lineno(1)}'
        raise Exception(error_message)
    p[0] = {
        'type': 'compressed_j_r_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_freg_freg(p):
    """expression : ID f_register COMMA f_register COMMA f_register NEWLINE"""
    opcode = p[1]
    if opcode in FLOATING_POINT_R_WITH_FUNCT3_DEST_X_INSTRUCTIONS:
        error_message = f'Error: illegal operands at line {p.lineno(1)}'
        raise Exception(error_message)
    has_funct3 = opcode in FLOATING_POINT_R_WITH_FUNCT3_INSTRUCTIONS
    rm_funct3 = FLOATING_POINT_R_FUNCT3[opcode] if has_funct3 else FLOATING_POINT_ROUNDING_MODES['dyn']

    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_f_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': get_f_register_index(p[6]),
        'rm_funct3': rm_funct3,
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_freg_freg_id(p):
    """expression : ID f_register COMMA f_register COMMA f_register COMMA ID NEWLINE"""
    rm = p[8]
    if rm not in FLOATING_POINT_ROUNDING_MODES:
        error_message = f'Error: illegal rounding mode at line {p.lineno(1)}'
        raise Exception(error_message)

    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_f_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': get_f_register_index(p[6]),
        'rm_funct3': FLOATING_POINT_ROUNDING_MODES[p[8]],
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_xreg_freg_freg(p):
    """expression : ID register COMMA f_register COMMA f_register NEWLINE"""
    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': get_f_register_index(p[6]),
        'rm_funct3': FLOATING_POINT_R_FUNCT3[p[1]],
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_freg(p):
    """expression : ID f_register COMMA f_register NEWLINE"""
    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_f_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': '0',
        'rm_funct3': FLOATING_POINT_ROUNDING_MODES['dyn'],
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_freg_id(p):
    """expression : ID f_register COMMA f_register COMMA ID NEWLINE"""
    rm = p[6]
    if rm not in FLOATING_POINT_ROUNDING_MODES:
        error_message = f'Error: illegal rounding mode at line {p.lineno(1)}'
        raise Exception(error_message)

    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_f_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': '0',
        'rm_funct3': FLOATING_POINT_ROUNDING_MODES[p[6]],
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_xreg_freg(p):
    """expression : ID register COMMA f_register NEWLINE"""
    if p[1] != INSTRUCTION_FMV_X_W:
        error_message = f'Error: incorrect or unrocognized instruction at line {p.lineno(1)}'
        raise Exception(error_message)

    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_f_register_index(p[4]),
        'rs2': '0',
        'rm_funct3': '000',
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_xreg(p):
    """expression : ID f_register COMMA register NEWLINE"""
    if p[1] != INSTRUCTION_FMV_W_X:
        error_message = f'Error: incorrect or unrocognized instruction at line {p.lineno(1)}'
        raise Exception(error_message)

    p[0] = {
        'type': 'floating_point_r_instruction',
        'opcode': p[1],
        'rd': get_f_register_index(p[2]),
        'rs1': get_x_register_index(p[4]),
        'rs2': '0',
        'rm_funct3': '000',
        'lineno': p.lineno(1)
    }


def p_floating_point_instruction_freg_imm_lparen_xreg_rparen(p):
    """expression : ID f_register COMMA IMMEDIATE LEFT_PAREN register RIGHT_PAREN NEWLINE"""
    if p[1] not in FLOATING_POINT_LOAD_STORE_INSTRUCTIONS:
        error_message = f'Error: incorrect or unrocognized instruction at line {p.lineno(1)}'
        raise Exception(error_message)

    if p[1] == INSTRUCTION_FLW:
        p[0] = {
            'type': 'i_load_instruction',
            'opcode': p[1],
            'rd': get_f_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }
    elif p[1] == INSTRUCTION_FSW:
        p[0] = {
            'type': 's_instruction',
            'opcode': p[1],
            'rs2': get_f_register_index(p[2]),
            'rs1': get_x_register_index(p[6]),
            'imm': to_int(p[4]),
            'lineno': p.lineno(1)
        }


def p_xreg(p):
    """register : REGISTER"""
    reg_number = int(get_x_register_index(p[1]))
    p[0] = p[1]


def p_freg(p):
    """f_register : F_REGISTER"""
    reg_number = int(get_f_register_index(p[1]))
    p[0] = p[1]


def p_newline(p):
    """expression : NEWLINE"""
    p[0] = {
        'type': 'new_line',
        'lineno': p.lineno(1)
    }


def p_error(p):
    if p:
        error_message = f'Error: invalid or incomplete token "{str(p.value)}" found at line {str(p.lineno)}'
        raise Exception(error_message)
    else:
        error_message = 'Error'
        raise Exception(error_message)


parser = yacc.yacc()
