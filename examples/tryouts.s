
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
fence
fence iorw, iorw
c.lui x5, 0x1e
c.addi16sp sp, 32
c.addi16sp sp, 496
c.addi16sp sp, -512
c.nop

c.addi4spn x8, x2, 1020
c.addi4spn x8, x2, 4
c.flw f15, 124(x8)
c.fld f15, 248(x8)
c.fld f15, 8(x14)
c.fsw f8, 4(x8)
c.fsd f15, 248(x8)
c.fsd f15, 8(x14)

c.lwsp x1, 4(x2)
c.lwsp x21, 252(x2)
c.flwsp f21, 252(x2)
c.fldsp f21, 248(x2)
c.fldsp f1, 8(x2)
