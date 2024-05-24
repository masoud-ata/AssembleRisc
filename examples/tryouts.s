fadd.s	ft11,fs6,fa3,rne
fsub.s	ft11,fs6,fa3,rtz
c.mv x8, x8
fmul.s	ft11,fs6,fa3
fdiv.s	ft0,fa1,fs9,rup
feq.s	a1,fa2,fa3
flt.s	s5,fs6,fs7
fle.s	x1,fa0,ft10
fsqrt.s f30, f4, rup
fsqrt.s f30, f4, rmm
fsqrt.s f30, f4, rdn
fsqrt.s f30, f4
fmv.x.w x29, f31
fmv.w.x f29, x31
fmv.w.x f0, x0
lb x4, 0(x12)
lh x4, 0(x12)
lw x4, 0(x12)
flw f4, 0(x12)
fsw f4, 0(x12)
fsw f30, 0(t4)
fsw fa7, 0(a7)
c.beqz x15, l
ret
jalr x0, 0(x1)
c.beqz x15, 12
l:
ebreak
ecall
c.addi x8, 1
c.addi x8, -1
c.slli x8, 31
csrrw x1, sstateen3, x2
csrrw x1, 0x141, x2
csrrc x1, mhpmevent3, x2
csrrs x1, mhpmevent31, x2