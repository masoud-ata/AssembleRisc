import ply.yacc as yacc

from assembler.tokenizer import tokens
from assembler.instruction_info import *
from assembler.pre_process import get_x_register_index, get_f_register_index


def to_int(field: str) -> int:
    if '0x' in field:
        return int(field, 16)
    else:
        return int(field)


def p_expression_no_argument(p):
    """expression : ID NEWLINE"""
    if p[1] == 'nop':
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
            'opcode': p[1],
            'rd': get_x_register_index('x0'),
            'rs1': get_x_register_index('x1'),
            'imm': 0,
            'lineno': p.lineno(1)
        }
    else:
        error_message = 'Error: unrecognized instruction at line {}'.format(p.lineno(1))
        raise Exception(error_message)


def p_expression_label(p):
    """expression : LABEL_COLON NEWLINE"""
    p[0] = {
        'type': 'label',
        'label': p[1].replace(":", ""),
        'lineno': p.lineno(1)
    }


def p_expression_r_instruction(p):
    """expression : ID register COMMA register COMMA register NEWLINE"""
    p[0] = {
        'type': 'r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_x_register_index(p[4]),
        'rs2': get_x_register_index(p[6]),
        'lineno': p.lineno(1)
    }


def p_expression_i_instruction(p):
    """expression : ID register COMMA register COMMA IMMEDIATE NEWLINE"""
    instruction = 'i_shift_instruction' if p[1] in I_SHIFT_INSTRUCTIONS else 'i_instruction'
    p[0] = {
        'type': instruction,
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs1': get_x_register_index(p[4]),
        'imm': to_int(p[6]),
        'lineno': p.lineno(1)
    }


def p_expression_iload_s_jalr_instruction(p):
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


def p_expression_u_instruction(p):
    """expression : ID register COMMA IMMEDIATE NEWLINE"""
    instruction = 'jal_instruction' if p[1] == INSTRUCTION_JAL else 'u_instruction'
    p[0] = {
        'type': instruction,
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'imm': to_int(p[4]),
        'lineno': p.lineno(1)
    }


def p_expression_jal_instruction(p):
    """expression : ID register COMMA ID NEWLINE"""
    p[0] = {
        'type': 'jal_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'label': p[4],
        'lineno': p.lineno(1)
    }


def p_expression_b_instruction(p):
    """expression : ID register COMMA register COMMA ID NEWLINE"""
    p[0] = {
        'type': 'b_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'rs2': get_x_register_index(p[4]),
        'label': p[6],
        'lineno': p.lineno(1)
    }


def p_expression_compressed_r_instruction(p):
    """expression : COMPRESSED_ID register COMMA register NEWLINE"""
    p[0] = {
        'type': 'compressed_r_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'rs2': get_x_register_index(p[4]),
        'lineno': p.lineno(1)
    }


def p_expression_compressed_i_instruction(p):
    """expression : COMPRESSED_ID register COMMA IMMEDIATE NEWLINE"""
    p[0] = {
        'type': 'compressed_i_instruction',
        'opcode': p[1],
        'rd': get_x_register_index(p[2]),
        'imm': to_int(p[4]),
        'lineno': p.lineno(1)
    }


def p_expression_compressed_b_instruction(p):
    """expression : COMPRESSED_ID register COMMA ID NEWLINE"""
    p[0] = {
        'type': 'compressed_b_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'label': p[4],
        'lineno': p.lineno(1)
    }


def p_statement_compressed_l_instruction(p):
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


def p_expression_compressed_j_instruction(p):
    """expression : COMPRESSED_ID IMMEDIATE NEWLINE"""
    p[0] = {
        'type': 'compressed_j_instruction',
        'opcode': p[1],
        'imm': to_int(p[2]),
        'lineno': p.lineno(1)
    }


def p_expression_compressed_j_r_instruction(p):
    """expression : COMPRESSED_ID register NEWLINE"""
    if p[1] not in COMPRESSED_J_R_INSTRUCTIONS:
        error_message = 'Error: illegal or incomplete instruction at line {}'.format(p.lineno(1))
        raise Exception(error_message)
    p[0] = {
        'type': 'compressed_j_r_instruction',
        'opcode': p[1],
        'rs1': get_x_register_index(p[2]),
        'lineno': p.lineno(1)
    }


def p_expression_floating_point_r_instruction(p):
    """expression : ID f_register COMMA f_register COMMA f_register NEWLINE"""
    opcode = p[1]
    if opcode in FLOATING_POINT_R_WITH_FUNCT3_DEST_X_INSTRUCTIONS:
        error_message = 'Error: illegal operands at line {}'.format(p.lineno(1))
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


def p_expression_floating_point_r_with_rm_instruction(p):
    """expression : ID f_register COMMA f_register COMMA f_register COMMA ID NEWLINE"""
    rm = p[8]
    if rm not in FLOATING_POINT_ROUNDING_MODES:
        error_message = 'Error: illegal rounding mode at line {}'.format(p.lineno(1))
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


def p_expression_floating_point_r_destination_x_instruction(p):
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


def p_expression_floating_point_r_2_reg_instruction(p):
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


def p_expression_floating_point_r_2_reg_with_rm_instruction(p):
    """expression : ID f_register COMMA f_register COMMA ID NEWLINE"""
    rm = p[6]
    if rm not in FLOATING_POINT_ROUNDING_MODES:
        error_message = 'Error: illegal rounding mode at line {}'.format(p.lineno(1))
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


def p_expression_floating_point_r_moveto_x_instruction(p):
    """expression : ID register COMMA f_register NEWLINE"""
    if p[1] != INSTRUCTION_FMV_X_W:
        error_message = 'Error: incorrect or unrocognized instruction at line {}'.format(p.lineno(1))
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


def p_expression_floating_point_r_moveto_f_instruction(p):
    """expression : ID f_register COMMA register NEWLINE"""
    if p[1] != INSTRUCTION_FMV_W_X:
        error_message = 'Error: incorrect or unrocognized instruction at line {}'.format(p.lineno(1))
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


def p_expression_floating_point_load_instruction(p):
    """expression : ID f_register COMMA IMMEDIATE LEFT_PAREN register RIGHT_PAREN NEWLINE"""
    if p[1] not in FLOATING_POINT_LOAD_STORE_INSTRUCTIONS:
        error_message = 'Error: incorrect or unrocognized instruction at line {}'.format(p.lineno(1))
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


def p_register(p):
    """register : REGISTER"""
    reg_number = int(get_x_register_index(p[1]))
    p[0] = p[1]


def p_floating_point_register(p):
    """f_register : F_REGISTER"""
    reg_number = int(get_f_register_index(p[1]))
    p[0] = p[1]


def p_statement_newline(p):
    """expression : NEWLINE"""
    p[0] = {
        'type': 'new_line',
        'lineno': p.lineno(1)
    }


def p_error(p):
    if p:
        error_message = 'Error: invalid or incomplete token "{}" found at line {}'.format(str(p.value), str(p.lineno))
        raise Exception(error_message)
    else:
        error_message = 'Error'
        raise Exception(error_message)


parser = yacc.yacc()
