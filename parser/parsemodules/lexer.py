import ply.lex as lex
from modules.open_and_format import open_and_format

reserved = {
        "voir": "VOIR",
        "aussi": "AUSSI",
        "not": "NOT"
        }

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'NUMBERP',
   'WORD',
   'PARENTHESE',
   'SLASH',
   'SEP',
   'SSTRONG',
   'ESTRONG',
   'SEM',
   'EEM',
   'SSC',
   'ESC',
   'MINUS',
   'SP',
   'EP',
   'SBQ',
   'EBQ',
   'UNKNOWN',
   'SS',
   'ES',
   'SPA',
   'EPA',
   'APOSTROPHE',
   'CROSS',
   'STAR',
   'BR',
   'SSB',
   'ESB',
   'DOT'
]+list(reserved.values())


# A regular expression rule with some action code

t_ignore = ' \t'

def t_SLASH(t):
    r'/'
    return t

def t_NUMBERP(t):
    r'\d+p'
    return t

def t_NUMBER(t):
    r'\d+'
    return t

def t_MINUS(t):
    r'—|-|–'
    return t

def t_WORD(t):
    r'[a-zA-ZÉÀÂÎæämüöûœôàâçéèêëî\-\.]+'
    t.type = reserved.get(t.value, 'WORD')
    return t

def t_SEP(t):
    r', | ;'
    return t

def t_SSTRONG(t):
   r'<strong>'
   return t

def t_ESTRONG(t):
    r'</strong>'
    return t

def t_SEM(t):
    r'<\ *em\ *>' 
    return t

def t_EEM(t):
    r'</\ *em\ *>'
    return t

def t_SSC(t):
    r'<span\ +class="smallcaps"\ *>'
    return t

def t_ESC(t):
    r'</\ *span\ *>'
    return t


def t_SP(t):
    r'<p>' 
    return t

def t_EP(t):
    r'</p>'
    return t

def t_SBQ(t):
    r'<blockquote>' 
    return t

def t_EBQ(t):
    r'</blockquote>'
    return t

def t_SS(t):
    r'<\ *sup\ *>' 
    return t

def t_ES(t):
    r'</\ *sup\ *>'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_APOSTROPHE(t):
    r'’'
    return t

def t_SPA(t):
    r'\(' 
    return t

def t_EPA(t):
    r'\)'
    return t

def t_CROSS(t):
    r'†'
    return t

def t_STAR(t):
    r'\*'
    return t

def t_BR(t):
    r'<\ *br\ */>'
    return t

def t_SSB(t):
    r'\[' 
    return t

def t_ESB(t):
    r'\]'
    return t

def t_UNKNOWN(t):
    r'.+'
    return t


# A string containing ignored characters (spaces and tabs)


def t_error(t):
    # Error handling rule
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


lexer.input("78p")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
