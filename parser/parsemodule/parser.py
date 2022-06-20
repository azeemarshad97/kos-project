from parsemodule.bracketParser import *


def p_start(p):
    '''entries : entry
               | entry moreentries'''
    p[0] = treduce(p[1:], [], tplus)


def p_moreentries(p):
    '''moreentries : entry
                   | entry moreentries'''
    p[0] = treduce(p[1:], [], tplus)


# ajouter en dessous "| SP words EP" s'il y a un problème
def p_entry(p):
    '''entry : SP exp EP
             | SP exps EP
             | SBQ entries EBQ
    '''
    if isinstance(p[2][1], str):
        p[0] = [p[2]]
    else:
        p[0] = p[2]


def p_exps(p):
    '''exps : exp
            | exp SEP moreexp
            '''
    p[0] = tparselist(p[1:])


def p_moreexp(p):
    '''moreexp : exp
               | exp SEP moreexp
               '''
    p[0] = tparselist(p[1:])


def p_component(p):
    '''exp : common
           | common_bold
           | place
           | descriptions
           | person
           | page
           | voirs
           '''
    p[0] = p[1]


def p_common_bold(p):
    '''common_bold : SSTRONG words ESTRONG '''
    p[0] = [p[2], "common_bold"]


def p_common(p):
    '''common : word'''
    p[0] = [p[1], "common"]


# TODO: mettre la parenthèse dans p[0]
def p_place(p):
    '''place : SEM words EEM
             | SEM words EEM parenthese'''
    p[0] = [p[2], "Localisation"]


def p_person(p):
    '''person : SSC word ESC
              | SSC descriptions ESC
              | SSC word SEP word ESC
              | SSC word SEP descriptions ESC
              | SSC descriptions SEP word ESC
              | SSC descriptions SEP descriptions ESC
    '''
    if p[3] in [",", ";"]:
        if isinstance(p[2], list):
            p[2] = p[2][0]
        if isinstance(p[4], list):
            p[4] = p[4][0]
        p[0] = [[[p[2], "Personne"], [p[4], "Personne"]], "persons"]
    elif isinstance(p[2], list):
        p[0] = [[[p[2][0], "Personne"]], "persons"]
    else:
        p[0] = [[[p[2], "Personne"]], "persons"]


def p_cross(p):
    '''cross : SPA CROSS EPA'''
    p[0] = [(p[2], "cross")]


def p_title(p):
    '''title : WORD SS WORD ES'''
    p[0] = p[1]+p[3]


# PAGES
def p_page(p):
    '''page : numberminus
            | NUMBERP
            | NUMBER'''
    p[0] = [p[1], "page"]


def p_numberminus(p):
    '''numberminus : NUMBER MINUS NUMBER
                   | NUMBER MINUS NUMBERP
                   | NUMBERP MINUS NUMBER
                   | NUMBERP MINUS NUMBERP
    '''
    p[0] = " ".join(p[1:])


# VOIRS
def p_voirs(p):
    '''voirs : VOIR AUSSI rest_voir_aussis
             | VOIR rest_voir_aussis
            '''
    if len(p[1:]) == 2:
        p[0] = [p[2], "voir"]
    else:
        p[0] = [p[3], "voir aussi"]


def p_rest_voir_aussis(p):
    '''rest_voir_aussis : exp
                        | exp SEP rest_voir_aussis
                   '''
    if len(p[1:]) == 1:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]]+p[3]


def p_type2(p):
    '''type2 : SSC words ESC
             | SSTRONG words ESTRONG
             | SEM words EEM
             | words
             '''
    if len(p[1:]) == 1:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_words(p):
    '''words : word
             | word moreword
             | word SEP moreword
             '''
    p[0] = " ".join(p[1:])


def p_moreword(p):
    '''moreword : word
                | word moreword
                | word SEP moreword
                '''
    p[0] = " ".join(p[1:])


def p_word(p):
    '''word : WORD
            | parenthese'''
    p[0] = " ".join(p[1:])


def p_parenthese(p):
    '''parenthese : SPA parenthesecontents EPA
                  | SSB parenthesecontents ESB
                  | SPA voirs EPA
                  '''
    if isinstance(p[2], list):
        p[0] = "("+str(p[2])+")"
    else:
        p[0] = " ".join(p[1:])


def p_parenthesecontents(p):
    '''parenthesecontents : parenthesecontent
                          | parenthesecontent moreparenthesecontent
                          '''
    p[0] = " ".join(p[1:])


def p_moreparenthesecontent(p):
    '''moreparenthesecontent : parenthesecontent
                             | parenthesecontent moreparenthesecontent
                          '''
    p[0] = " ".join(p[1:])


def p_parenthesecontent(p):
    '''parenthesecontent : words
                         | DOT
                         | SEP
                         | MINUS
                         | APOSTROPHE
                         | NUMBER
                        '''
    p[0] = p[1]


def p_descriptions(p):
    '''descriptions : description
                    | description moredescription'''
    p[0] = [" ".join(p[1:]), "descriptions"]


def p_moredescription(p):
    '''moredescription : description
                       | description moredescription'''
    p[0] = " ".join(p[1:])


def p_description(p):
    '''description : WORD
                   | SLASH
                   | cross
                   | title
                   | MINUS
                   | APOSTROPHE
                   | parenthese
                   '''
    if isinstance(p[1], list):
        p[0] = p[1][0][0]
    else:
        p[0] = p[1]


# Error rule for syntax errors
def p_error(p):
    pass


# Build the parser
parser = yacc.yacc(debug=True)
