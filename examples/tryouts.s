addi x31, x0, -56
addi x24, x0, -100
addi x30, x0, 102
c.li x15, 1
c.addi x15, 9
addi x16, x0, 1
addi x1, x0, 0
auipc x1, 2
jal x27, -524288
jalr x27, -1024(x1)
slli x5, x11, 4
srli x15, x21, 8
srai x18, x13, 31
c.j -2048
c.jal 1022
c.jr x17
c.jalr x29
nop
nop
addi x0, x0, 0
mul x12, x10, x5
mulh x31, t0, a1
mulhsu x1, x11, x2
mulhu t2, t4, t5
div x21, x13, x15
divu x21, x13, x15
rem x21, x13, x15
remu x20, x30, x29
