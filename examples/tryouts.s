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
csrrw x20, mtinst, x16
csrrs x21, 0x34a, x17
csrrc x22, mtinst, x15
csrrwi x10, mtinst, 6
csrrsi x11, 0x34a, 7
csrrci x12, mtinst, 0x5

fence r, r
fence rw, r
fence i, r
fence o, r
fence io, r
fence iorw, iorw
fence iorw, i
fence iorw, o
fence iorw, r
fence iorw, w
fence iorw, rw
fence iorw, io
fence iorw, ir
fence iorw, irw
fence iorw, iw
fence iow, iw
fence irw, iw
fence orw, orw
fence or, orw
fence.i