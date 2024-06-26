import ply.lex as lex


tokens = (
    'COMMA',
    'IMMEDIATE',
    'LEFT_PAREN',
    'RIGHT_PAREN',
    'LABEL_COLON',
    'REGISTER',
    'F_REGISTER',
    'COMPRESSED_ID',
    'ID',
    'NEWLINE'
)


t_COMMA = r','
t_IMMEDIATE = r'0x[0-9a-fA-F]+|[+-]?[0-9]+'
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'


def t_LABEL_COLON(token):
    r'[a-zA-Z_][a-zA-Z_0-9\.]*[:]'
    token.type = "LABEL_COLON"
    return token


def t_REGISTER(token):
    r'x3[0-1]|x2[0-9]|x1[0-9]|x[0-9]'\
    r'|zero|ra|sp|gp|tp|fp'\
    r'|s1[0-1]|s[0-9]|t[0-6]|a[0-7]'
    token.type = "REGISTER"
    return token


def t_F_REGISTER(token):
    r'ft1[0-1]|ft[0-9]|fs1[0-1]|fs[0-9]|fa[0-7]'\
    r'|f3[0-1]|f2[0-9]|f1[0-9]|f[0-9]'
    token.type = "F_REGISTER"
    return token


def t_COMPRESSED_ID(token):
    r'c\.[a-z0-9]+'
    token.type = "COMPRESSED_ID"
    return token


def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9\.]*'
    token.type = "ID"
    return token


def t_NEWLINE(token):
    r'\n+'
    token.lexer.lineno += len(token.value)
    return token


t_ignore = ' \t\r'


def t_COMMENT(token):
    r'\#.*'
    pass


def t_error(token):
    token.lexer.skip(1)
    error_message = 'Error: illegal character "{}" at line {}'.format(token.value[0], token.lexer.lineno)
    raise Exception(error_message)


lexer = lex.lex()


def reset_lineno():
    lexer.lineno = 1
