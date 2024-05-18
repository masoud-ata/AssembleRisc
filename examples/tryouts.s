addi x3, x0, 5
label:
sw x3, 12(x13)
lb x31, 4(x0)
bne x1, x2, label
