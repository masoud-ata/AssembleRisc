# AssembleRisc
A Python assembler for RISC-V with support for RV32I, RV32C, RV32M, and RV32F extensions


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
|    xori     |   I    |  &check;  |    fence    |   I    |  &check;  |   
|     ori     |   I    |  &check;  |   fence.i   |   I    |  &check;  | 
|    andi     |   I    |  &check;  |    ecall    |   I    |  &check;  |  
|    slli     |   I    |  &check;  |   ebreak    |   I    |  &check;  |  
|    srli     |   I    |  &check;  |    csrrw    |   I    |  &check;  |  
|    srai     |   I    |  &check;  |    csrrs    |   I    |  &check;  | 
|     lb      |   I    |  &check;  |    csrrc    |   I    |  &check;  | 
|     lh      |   I    |  &check;  |   csrrwi    |   I    |  &check;  | 
|     lw      |   I    |  &check;  |   csrrsi    |   I    |  &check;  | 
|     lbu     |   I    |  &check;  |   csrrci    |   I    |  &check;  | 
|     lhu     |   I    |  &check;  |   

### RV32C
| Instruction | Format | Supported | Instruction | Format | Supported | 
|:-----------:|:------:|:---------:|:-----------:|:------:|:---------:|
|    c.and    |   CA   |  &check;  |   c.srai    |   CB   |  &check;  |
|    c.or     |   CA   |  &check;  |   c.andi    |   CB   |  &check;  |
|    c.xor    |   CA   |  &check;  |    c.add    |   CR   |  &check;  |
|    c.sub    |   CA   |  &check;  |    c.mv     |   CR   |  &check;  |
|    c.lw     |   CL   |  &check;  |     c.j     |   CJ   |  &check;  |
|    c.sw     |   CS   |  &check;  |    c.jal    |   CJ   |  &check;  |
|   c.beqz    |   CB   |  &check;  |    c.jr     |   CR   |  &check;  | 
|   c.bneq    |   CB   |  &check;  |   c.jalr    |   CR   |  &check;  | 
|    c.li     |   CI   |  &check;  |    c.nop    |        |    | 
|    c.lui    |   CI   |  &check;  | c.addi16sp  |        |    | 
|   c.addi    |   CI   |  &check;  | c.addi4spn  |        |    | 
|   c.slli    |   CI   |  &check;  |    c.fld    |        |    | 
|   c.srli    |   CB   |  &check;  |    c.flw    |        |    |
|  c.slli64   |        |           |    c.fsd    |        |    | 
|   c.fldsp   |        |           |    c.fsw    |        |    |
|   c.lwsp    |        |           |    c.nop    |        |    |
|   c.flwsp   |        |           |  c.ebreak   |        |    |
|   c.fsdsp   |        |           |             |        |    |
|   c.swsp    |        |           |             |        |    |
|   c.fswsp   |        |           |             |        |    |


### RV32M
| Instruction | Format | Supported | Instruction | Format | Supported | 
|:-----------:|:------:|:---------:|:-----------:|:------:|:---------:|
|     mul     |   R    |  &check;  |     div     |   R    |  &check;  |
|    mulh     |   R    |  &check;  |    divu     |   R    |  &check;  |
|   mulhsu    |   R    |  &check;  |     rem     |   R    |  &check;  |
|    mulhu    |   R    |  &check;  |    remu     |   R    |  &check;  |

### RV32F
| Instruction | Format | Supported | Instruction | Format | Supported | 
|:-----------:|:------:|:---------:|:-----------:|:------:|:---------:|
|   fadd.s    |   R    |  &check;  |    feq.s    |   R    |  &check;  |
|   fsub.s    |   R    |  &check;  |    flt.s    |   R    |  &check;  |    
|   fmul.s    |   R    |  &check;  |    fle.s    |   R    |  &check;  |    
|   fdiv.s    |   R    |  &check;  |   fsqrt.s   |   R    |  &check;  | 
|   fmv.x.w   |   R    |  &check;  |     flw     |   I    |  &check;  |   
|   fmv.w.x   |   R    |  &check;  |     fsw     |   S    |  &check;  | 
