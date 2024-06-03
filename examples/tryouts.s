
l:
fmadd.s f1, f2, f3, f4
fmadd.s f1, f2, f3, f4, rtz
fnmadd.s f1, f2, f3, f4
fnmadd.s f1, f2, f3, f4, rne
fnmsub.s f11, f12, f31, f14
fnmsub.s f11, f12, f31, f14, rup
jal x20, m
fcvt.s.w f21, x12
fcvt.s.w f11, x22, dyn
fcvt.s.w f10, x21, rup
fcvt.s.wu f31, x22, rtz
jal x1, l
fcvt.w.s x22, f1
fcvt.w.s x23, f22, dyn
fcvt.w.s x10, f31, rup
fcvt.wu.s x31, f30, rtz
m:
fclass.s x20, f30