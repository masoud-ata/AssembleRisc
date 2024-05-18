addi x3, x0, 5
jal x2, label3
label:
sw x3, 12(x13)
lb x31, 4(x0)
bne x1, x2, label
add x1, x2, x3
lui x1, 10
sw x3, 12(x13)
lb x31, 4(x0)
bne x1, x2, label
add x1, x2, x3
lui x1, 10
jal x2, label
label2:
sw x3, 12(x13)
lb x31, 4(x0)
bne x1, x2, label
add x1, x2, x3
lui x1, 10
jal x2, label2
label3:
lui x1, 10
