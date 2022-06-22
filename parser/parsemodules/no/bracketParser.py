import ply.yacc as yacc
from parsemodule.lexer import *
# from modules.tools import treduce, tplus, tparselist, ttolist
from modules.open_and_format import open_and_format, open_and_format2

# parser number two

def p_start2(p):
    '''brackets : SP
                | EP'''
    p[0] = "bracket: "+p[1]

# Error rule for syntax errors
def p_error(p):
    pass

# Build the parser
parser2 = yacc.yacc(debug=True)
