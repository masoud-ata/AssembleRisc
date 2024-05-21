# AssembleRisc
A Python assembler for RISC-V


## Requirements
The assembler has been tested using Python 3.6 on both Linux and windows. It uses the `ply` package (Python Lex-Yacc), which is listed in the `requirements.txt` file, and therefore can be installed with the following command:

`pip install -r requirements.txt`

## How to run
First, `cd` to the `src` directory. By default, the assembler takes the `examples\tryouts.s` as input and can be invoked like:

    $ python main.py

If you want to use another file as input, then you can run the `main.py` file with your input assembly file (here assumed to be named `my_asm.s` and in the same `src` directory):

    $ python main.py -i my_asm.s

The output files, both in textual binary and hexadeciaml, are placed in the `output` directory.


## Supported instructions
### RV32I
| Instruction | Format | Supported | Instruction | Format | Supported | 
|:-----------:|:------:|:---------:|:-----------:|:------:|:---------:|
|     add     |   R    |  &check;  |     sb      |   S    |  &check;  |
|     sub     |   R    |  &check;  |     sh      |   S    |  &check;  |
|     sll     |   R    |  &check;  |     sw      |   S    |  &check;  |
|     slt     |   R    |  &check;  |     beq     |   B    |  &check;  |
|    sltu     |   R    |  &check;  |     bne     |   B    |  &check;  |
|     xor     |   R    |  &check;  |     blt     |   B    |  &check;  |   
|     srl     |   R    |  &check;  |     bge     |   B    |  &check;  |   
|     sra     |   R    |  &check;  |    bltu     |   B    |  &check;  |   
|     or      |   R    |  &check;  |    bgeu     |   B    |  &check;  | 
|     and     |   R    |  &check;  |     lui     |   U    |  &check;  | 
|    addi     |   I    |  &check;  |    auipc    |   U    |  &check;  | 
|    slti     |   I    |  &check;  |     jal     |   J    |  &check;  | 
|    sltiu    |   I    |  &check;  |    jalr     |   J    |  &check;  | 
|    xori     |   I    |  &check;  |    fence    |   I    |    |   
|     ori     |   I    |  &check;  |   fence.i   |   I    |    | 
|    andi     |   I    |  &check;  |    ecall    |   I    |    |  
|    slli     |   I    |  &check;  |   ebreak    |   I    |    |  
|    srli     |   I    |  &check;  |    csrrw    |   I    |    |  
|    srai     |   I    |  &check;  |    csrrs    |   I    |    | 
|     lb      |   I    |  &check;  |    csrrc    |   I    |    | 
|     lh      |   I    |  &check;  |   csrrwi    |   I    |    | 
|     lw      |   I    |  &check;  |   csrrsi    |   I    |    | 
|     lbu     |   I    |  &check;  |   csrrci    |   I    |    | 
|     lhu     |   I    |  &check;  |   