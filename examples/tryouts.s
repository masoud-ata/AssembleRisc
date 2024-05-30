
c.ebreak
c.slli64 x31
c.slli64 x1
c.lwsp x1, 4(x2)
c.lwsp x21, 252(x2)
c.flwsp f21, 252(x2)
c.fldsp f21, 248(x2)
c.fldsp f1, 8(x2)

c.swsp x21, 252(x2)
c.fswsp f21, 248(x2)
c.fsdsp f1, 8(x2)
c.fsdsp f1, 248(x2)