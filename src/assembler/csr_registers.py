CSR_ENCODING_TABLE = {
    'fflags': 0x001,
    'frm': 0x002,
    'fcsr': 0x003,

    'cycle': 0xc00,
    'time': 0xc01,
    'instret': 0xc02,
    'hpmcounter3': 0xc03,
    'hpmcounter4': 0xc04,
    'hpmcounter5': 0xc05,
    'hpmcounter6': 0xc06,
    'hpmcounter7': 0xc07,
    'hpmcounter8': 0xc08,
    'hpmcounter9': 0xc09,
    'hpmcounter10': 0xc0a,
    'hpmcounter11': 0xc0b,
    'hpmcounter12': 0xc0c,
    'hpmcounter13': 0xc0d,
    'hpmcounter14': 0xc0e,
    'hpmcounter15': 0xc0f,
    'hpmcounter16': 0xc10,
    'hpmcounter17': 0xc11,
    'hpmcounter18': 0xc12,
    'hpmcounter19': 0xc13,
    'hpmcounter20': 0xc14,
    'hpmcounter21': 0xc15,
    'hpmcounter22': 0xc16,
    'hpmcounter23': 0xc17,
    'hpmcounter24': 0xc18,
    'hpmcounter25': 0xc19,
    'hpmcounter26': 0xc1a,
    'hpmcounter27': 0xc1b,
    'hpmcounter28': 0xc1c,
    'hpmcounter29': 0xc1d,
    'hpmcounter30': 0xc1e,
    'hpmcounter31': 0xc1f,
    'cycleh': 0xc80,
    'timeh': 0xc81,
    'instreth': 0xc82,
    'hpmcounter3h': 0xc83,
    'hpmcounter4h': 0xc84,
    'hpmcounter5h': 0xc85,
    'hpmcounter6h': 0xc86,
    'hpmcounter7h': 0xc87,
    'hpmcounter8h': 0xc88,
    'hpmcounter9h': 0xc89,
    'hpmcounter10h': 0xc8a,
    'hpmcounter11h': 0xc8b,
    'hpmcounter12h': 0xc8c,
    'hpmcounter13h': 0xc8d,
    'hpmcounter14h': 0xc8e,
    'hpmcounter15h': 0xc8f,
    'hpmcounter16h': 0xc90,
    'hpmcounter17h': 0xc91,
    'hpmcounter18h': 0xc92,
    'hpmcounter19h': 0xc93,
    'hpmcounter20h': 0xc94,
    'hpmcounter21h': 0xc95,
    'hpmcounter22h': 0xc96,
    'hpmcounter23h': 0xc97,
    'hpmcounter24h': 0xc98,
    'hpmcounter25h': 0xc99,
    'hpmcounter26h': 0xc9a,
    'hpmcounter27h': 0xc9b,
    'hpmcounter28h': 0xc9c,
    'hpmcounter29h': 0xc9d,
    'hpmcounter30h': 0xc9e,
    'hpmcounter31h': 0xc9,

    'sstatus': 0x100,
    'sie': 0x104,
    'stvec': 0x105,
    'scounteren': 0x106,

    'senvcfg': 0x10a,

    'scountinhibit': 0x120,

    'sscratch': 0x140,
    'sepc': 0x141,
    'scause': 0x142,
    'stval': 0x143,
    'sip': 0x144,
    'scountovf': 0xda0,

    'satp': 0x180,

    'scontext': 0x5a8,

    'sstateen0': 0x10c,
    'sstateen1': 0x10d,
    'sstateen2': 0x10e,
    'sstateen3': 0x10f,

    'hstatus': 0x600,
    'hedeleg': 0x602,
    'hideleg': 0x603,
    'hie': 0x604,
    'hcounteren': 0x606,
    'hgeie': 0x607,
    'hedelegh': 0x612,

    'htval': 0x643,
    'hip': 0x644,
    'hvip': 0x645,
    'htinst': 0x64a,
    'hgeip': 0xe12,

    'henvcfg': 0x60a,
    'henvcfgh': 0x61a,

    'hgatp': 0x680,

    'hcontext': 0x6a8,

    'htimedelta': 0x605,
    'htimedeltah': 0x615,

    'hstateen0': 0x60c,
    'hstateen1': 0x60d,
    'hstateen2': 0x60e,
    'hstateen3': 0x60f,
    'hstateen0h': 0x61c,
    'hstateen1h': 0x61d,
    'hstateen2h': 0x61e,
    'hstateen3h': 0x61f,

    'vsstatus': 0x200,
    'vsie': 0x204,
    'vstvec': 0x205,
    'vsscratch': 0x240,
    'vsepc': 0x241,
    'vscause': 0x242,
    'vstval': 0x243,
    'vsip': 0x244,
    'vsatp': 0x280,

    'mvendorid': 0xf11,
    'marchid': 0xf12,
    'mimpid': 0xf13,
    'mhartid': 0xf14,
    'mconfigptr': 0xf15,

    'mstatus': 0x300,
    'misa': 0x301,
    'medeleg': 0x302,
    'mideleg': 0x303,
    'mie': 0x304,
    'mtvec': 0x305,
    'mcounteren': 0x306,
    'mstatush': 0x310,
    'medelegh': 0x312,

    'mscratch': 0x340,
    'mepc': 0x341,
    'mcause': 0x342,
    'mtval': 0x343,
    'mip': 0x344,
    'mtinst': 0x34a,
    'mtval2': 0x34b,

    'menvcfg': 0x30a,
    'menvcfgh': 0x31a,
    'mseccfg': 0x747,
    'mseccfgh': 0x757,

    'pmpaddr0': 0x3b0,
    'pmpaddr1': 0x3b1,
    'pmpaddr63': 0x3ef,

    'mstateen0': 0x30c,
    'mstateen1': 0x30d,
    'mstateen2': 0x30e,
    'mstateen3': 0x30f,
    'mstateen0h': 0x31c,
    'mstateen1h': 0x31d,
    'mstateen2h': 0x31e,
    'mstateen3h': 0x31f,

    'mnscratch': 0x740,
    'mnepc': 0x741,
    'mncause': 0x742,
    'mnstatus': 0x744,

    'mcycle': 0xb00,
    'minstret': 0xb02,
    'mcycleh': 0xb80,
    'minstreth': 0xb82,

    'mcountinhibit': 0x320,

    'tselect': 0x7a0,
    'tdata1': 0x7a1,
    'tdata2': 0x7a2,
    'tdata3': 0x7a3,
    'mcontext': 0x7a8,

    'dcsr': 0x7b0,
    'dpc': 0x7b1,
    'dscratch0': 0x7b2,
    'dscratch1': 0x7b3
}


def fill_table(starting_val: int, r: range, key: str, key2: str = ''):
    val = starting_val
    for i in r:
        CSR_ENCODING_TABLE[key + str(i) + key2] = val
        val += 1


fill_table(0x3a0, range(0, 16), 'pmpcfg')
fill_table(0x3b0, range(0, 64), 'pmpaddr')
fill_table(0xb03, range(3, 32), 'mhpmcounter')
fill_table(0xb83, range(3, 32), 'mhpmcounter', 'h')
fill_table(0x323, range(3, 32), 'mhpmevent')
fill_table(0x723, range(3, 32), 'mhpmevent', 'h')
