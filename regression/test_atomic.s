lr.w x5, (x19)
sc.w.aq t1, x31, (t0)
amoswap.w t1, t0, (x30)
amoadd.w t1, t0, (x30)
amoxor.w t1, t0, (x30)
amoand.w t1, t0, (x30)
amoor.w t1, t0, (x30)
amomin.w t1, t0, (x30)
amomax.w.aq t1, t0, (x30)
amominu.w.rl t1, t0, (x30)
amomaxu.w.aqrl t1, t0, (x30)
amomax.w t1, t0, (x30)
amominu.w t1, t0, (x30)
amomaxu.w t1, t0, (x30)