INSTRUCTION_ADD = 'add'
INSTRUCTION_SUB = 'sub'
INSTRUCTION_SLL = 'sll'
INSTRUCTION_SLT = 'slt'
INSTRUCTION_SLTU = 'sltu'
INSTRUCTION_XOR = 'xor'
INSTRUCTION_SRL = 'srl'
INSTRUCTION_SRA = 'sra'
INSTRUCTION_OR = 'or'
INSTRUCTION_AND = 'and'

INSTRUCTION_ADDI = 'addi'
INSTRUCTION_SLTI = 'slti'
INSTRUCTION_SLTIU = 'sltiu'
INSTRUCTION_XORI = 'xori'
INSTRUCTION_ORI = 'ori'
INSTRUCTION_ANDI = 'andi'

INSTRUCTION_SLLI = 'slli'
INSTRUCTION_SRLI = 'srli'
INSTRUCTION_SRAI = 'srai'

INSTRUCTION_LB = 'lb'
INSTRUCTION_LH = 'lh'
INSTRUCTION_LW = 'lw'
INSTRUCTION_LBU = 'lbu'
INSTRUCTION_LHU = 'lhu'

INSTRUCTION_LUI = 'lui'
INSTRUCTION_AUIPC = 'auipc'

INSTRUCTION_BEQ = 'beq'
INSTRUCTION_BNE = 'bne'
INSTRUCTION_BLT = 'blt'
INSTRUCTION_BGE = 'bge'
INSTRUCTION_BLTU = 'bltu'
INSTRUCTION_BGEU = 'bgeu'

INSTRUCTION_SB = 'sb'
INSTRUCTION_SH = 'sh'
INSTRUCTION_SW = 'sw'

INSTRUCTION_JAL = 'jal'
INSTRUCTION_JALR = 'jalr'

INSTRUCTION_C_SUB = 'c.sub'
INSTRUCTION_C_XOR = 'c.xor'
INSTRUCTION_C_OR = 'c.or'
INSTRUCTION_C_AND = 'c.and'
INSTRUCTION_C_ADD = 'c.add'
INSTRUCTION_C_MV = 'c.mv'

INSTRUCTION_C_ADDI = 'c.addi'
INSTRUCTION_C_LI = 'c.li'
INSTRUCTION_C_LUI = 'c.lui'
INSTRUCTION_C_SLLI = 'c.slli'

INSTRUCTION_C_SRLI = 'c.srli'
INSTRUCTION_C_SRAI = 'c.srai'
INSTRUCTION_C_ANDI = 'c.andi'

INSTRUCTION_C_BEQZ = 'c.beqz'
INSTRUCTION_C_BNEZ = 'c.bnez'

INSTRUCTION_C_LW = 'c.lw'
INSTRUCTION_C_SW = 'c.sw'

INSTRUCTION_C_J = 'c.j'
INSTRUCTION_C_JAL = 'c.jal'

INSTRUCTION_C_JR = 'c.jr'
INSTRUCTION_C_JALR = 'c.jalr'

INSTRUCTION_MUL = 'mul'
INSTRUCTION_MULH = 'mulh'
INSTRUCTION_MULHSU = 'mulhsu'
INSTRUCTION_MULHU = 'mulhu'
INSTRUCTION_DIV = 'div'
INSTRUCTION_DIVU = 'divu'
INSTRUCTION_REM = 'rem'
INSTRUCTION_REMU = 'remu'


R_INSTRUCTIONS = [
    INSTRUCTION_ADD, INSTRUCTION_SUB, INSTRUCTION_SLL, INSTRUCTION_SLT, INSTRUCTION_SLTU,
    INSTRUCTION_XOR, INSTRUCTION_SRL, INSTRUCTION_SRA, INSTRUCTION_OR, INSTRUCTION_AND,

    INSTRUCTION_MUL, INSTRUCTION_MULH, INSTRUCTION_MULHSU, INSTRUCTION_MULH,
    INSTRUCTION_DIV, INSTRUCTION_DIVU, INSTRUCTION_REM, INSTRUCTION_REMU
]

I_INSTRUCTIONS = [
    INSTRUCTION_ADDI, INSTRUCTION_SLTI, INSTRUCTION_SLTIU, INSTRUCTION_XORI, INSTRUCTION_ORI, INSTRUCTION_ANDI
]

I_SHIFT_INSTRUCTIONS = [INSTRUCTION_SLLI, INSTRUCTION_SRLI, INSTRUCTION_SRAI]

I_LOAD_INSTRUCTIONS = [INSTRUCTION_LB, INSTRUCTION_LH, INSTRUCTION_LW, INSTRUCTION_LBU, INSTRUCTION_LHU]

U_INSTRUCTIONS = [INSTRUCTION_LUI, INSTRUCTION_AUIPC]

B_INSTRUCTIONS = [INSTRUCTION_BEQ, INSTRUCTION_BNE, INSTRUCTION_BLT, INSTRUCTION_BGE, INSTRUCTION_BLTU, INSTRUCTION_BGEU]

S_INSTUCTIONS = [INSTRUCTION_SB, INSTRUCTION_SH, INSTRUCTION_SW]

J_INSTRUCTIONS = [INSTRUCTION_JAL, INSTRUCTION_JALR]

COMPRESSED_R_INSTRUCTIONS = [INSTRUCTION_C_SUB, INSTRUCTION_C_XOR, INSTRUCTION_C_OR, INSTRUCTION_C_AND, INSTRUCTION_C_ADD, INSTRUCTION_C_MV]

COMPRESSED_I_INSTRUCTIONS = [
    INSTRUCTION_C_ADDI, INSTRUCTION_C_LI, INSTRUCTION_C_LUI, INSTRUCTION_C_SLLI,
    INSTRUCTION_C_SRLI, INSTRUCTION_C_SRAI, INSTRUCTION_C_ANDI
]

COMPRESSED_B_INSTRUCTIONS = [INSTRUCTION_C_BEQZ, INSTRUCTION_C_BNEZ]

COMPRESSED_L_INSTRUCTIONS = [INSTRUCTION_C_LW, INSTRUCTION_C_SW]

COMPRESSED_J_INSTRUCTIONS = [INSTRUCTION_C_J, INSTRUCTION_C_JAL]

COMPRESSED_J_R_INSTRUCTIONS = [INSTRUCTION_C_JR, INSTRUCTION_C_JALR]

ALL_INSTRUCTIONS = (
    R_INSTRUCTIONS + I_INSTRUCTIONS + I_SHIFT_INSTRUCTIONS + I_LOAD_INSTRUCTIONS +
    U_INSTRUCTIONS + B_INSTRUCTIONS + S_INSTUCTIONS + J_INSTRUCTIONS +
    COMPRESSED_R_INSTRUCTIONS + COMPRESSED_I_INSTRUCTIONS + COMPRESSED_B_INSTRUCTIONS +
    COMPRESSED_L_INSTRUCTIONS + COMPRESSED_J_INSTRUCTIONS + COMPRESSED_J_R_INSTRUCTIONS
)


R_OPCODE = '0110011'
I_LOAD_OPCODE = '0000011'
I_OPCODE = '0010011'
U_OPCODE = {
    INSTRUCTION_LUI: '0110111',
    INSTRUCTION_AUIPC: '0010111'
}
B_OPCODE = '1100011'
S_OPCODE = '0100011'
JAL_OPCODE = '1101111'
JALR_OPCODE = '1100111'


R_FUNCT3 = {
    INSTRUCTION_ADD: '000',
    INSTRUCTION_SUB: '000',
    INSTRUCTION_SLL: '001',
    INSTRUCTION_SLT: '010',
    INSTRUCTION_SLTU: '011',
    INSTRUCTION_XOR: '100',
    INSTRUCTION_SRL: '101',
    INSTRUCTION_SRA: '101',
    INSTRUCTION_OR: '110',
    INSTRUCTION_AND: '111',

    INSTRUCTION_MUL: '000',
    INSTRUCTION_MULH: '001',
    INSTRUCTION_MULHSU: '010',
    INSTRUCTION_MULHU: '011',
    INSTRUCTION_DIV: '100',
    INSTRUCTION_DIVU: '101',
    INSTRUCTION_REM: '110',
    INSTRUCTION_REMU: '111'
}

I_LOAD_FUNCT3 = {
    INSTRUCTION_LB: '000',
    INSTRUCTION_LH: '001',
    INSTRUCTION_LW: '010',
    INSTRUCTION_LBU: '100',
    INSTRUCTION_LHU: '101'
}

I_FUNCT3 = {
    INSTRUCTION_ADDI: '000',
    INSTRUCTION_SLTI: '010',
    INSTRUCTION_SLTIU: '011',
    INSTRUCTION_XORI: '100',
    INSTRUCTION_ORI: '110',
    INSTRUCTION_ANDI: '111',
    INSTRUCTION_SLLI: '001',
    INSTRUCTION_SRLI: '101',
    INSTRUCTION_SRAI: '101'
}

B_FUNCT3 = {
    INSTRUCTION_BEQ: '000',
    INSTRUCTION_BNE: '001',
    INSTRUCTION_BLT: '100',
    INSTRUCTION_BGE: '101',
    INSTRUCTION_BLTU: '110',
    INSTRUCTION_BGEU: '111'
}

S_FUNCT3 = {
    INSTRUCTION_SB: '000',
    INSTRUCTION_SH: '001',
    INSTRUCTION_SW: '010'
}

JALR_FUNCT3 = '000'


R_FUNCT7 = {
    INSTRUCTION_ADD: '0000000',
    INSTRUCTION_SUB: '0100000',
    INSTRUCTION_SLL: '0000000',
    INSTRUCTION_SLT: '0000000',
    INSTRUCTION_SLTU: '0000000',
    INSTRUCTION_XOR: '0000000',
    INSTRUCTION_SRL: '0000000',
    INSTRUCTION_SRA: '0100000',
    INSTRUCTION_OR: '0000000',
    INSTRUCTION_AND: '0000000',

    INSTRUCTION_MUL: '0000001',
    INSTRUCTION_MULH: '0000001',
    INSTRUCTION_MULHSU: '0000001',
    INSTRUCTION_MULHU: '0000001',
    INSTRUCTION_DIV: '0000001',
    INSTRUCTION_DIVU: '0000001',
    INSTRUCTION_REM: '0000001',
    INSTRUCTION_REMU: '0000001'
}

I_SHIFT_FUNCT7 = {
    INSTRUCTION_SLLI: '0000000',
    INSTRUCTION_SRLI: '0000000',
    INSTRUCTION_SRAI: '0100000'
}


COMPRESSED_R_FUNCT = {
    INSTRUCTION_C_SUB: '00',
    INSTRUCTION_C_XOR: '01',
    INSTRUCTION_C_OR: '10',
    INSTRUCTION_C_AND: '11',
    INSTRUCTION_C_ADD: '1',
    INSTRUCTION_C_MV: '0'
}

COMPRESSED_I_OPCODE = {
    INSTRUCTION_C_ADDI: '01',
    INSTRUCTION_C_LI: '01',
    INSTRUCTION_C_LUI: '01',
    INSTRUCTION_C_SLLI: '10',
    INSTRUCTION_C_SRLI: '01',
    INSTRUCTION_C_SRAI: '01',
    INSTRUCTION_C_ANDI: '01'
}

COMPRESSED_I_FUNCT3 = {
    INSTRUCTION_C_ADDI: '000',
    INSTRUCTION_C_LI: '010',
    INSTRUCTION_C_LUI: '011',
    INSTRUCTION_C_SLLI: '000'
}

COMPRESSED_B_FUNCT3 = {
    INSTRUCTION_C_BEQZ: '110',
    INSTRUCTION_C_BNEZ: '111'
}

COMPRESSED_L_FUNCT3 = {
    INSTRUCTION_C_LW: '010',
    INSTRUCTION_C_SW: '110'
}

COMPRESSED_J_FUNCT3 = {
    INSTRUCTION_C_J: '101',
    INSTRUCTION_C_JAL: '001',
}

COMPRESSED_I_FUNCT2 = {
    INSTRUCTION_C_SRLI: '00',
    INSTRUCTION_C_SRAI: '01',
    INSTRUCTION_C_ANDI: '10'
}

COMPRESSED_J_R_FUNCT4 = {
    INSTRUCTION_C_JR: '1000',
    INSTRUCTION_C_JALR: '1001',
}
