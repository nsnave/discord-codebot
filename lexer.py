'''
Referenced:
https://stackoverflow.com/a/10047501/11039508


'''

import re
from enum import Enum

class Token(Enum):
    CMD = 1
    ARG = 2
    PIPE = 3
    AND = 4
    OR = 5
    END = 6
    BACK = 7
    LPAREN = 8
    RPAREN = 9
    REDIR_IN = 10
    REDIR_IN_HERE = 11
    REDIR_OUT = 12
    REDIR_OUT_APP = 13
    LIMIT_STR = 14

class State(Enum):
    START = 1
    SUB_CMD = 2
    HERE = 3


class Lexer:

    FILE_REGEX = "([^ !$`&*()+]|(\\[ !$`&*()+]))+"

    rmap = {
        Token.CMD: FILE_REGEX,
        Token.ARG: FILE_REGEX,
        Token.PIPE: "\|",
        Token.AND: "&&",
        Token.OR: "\|\|",
        Token.END: "&",
        Token.BACK: ";",
        Token.LPAREN: "\(",
        Token.RPAREN: "\)",
        Token.REDIR_IN: "<",
        Token.REDIR_IN_HERE: "<<",
        Token.LIMIT_STR: "\w+",
        Token.REDIR_OUT: ">",
        Token.REDIR_OUT_APP: ">>"
    }

    search_order = [
        Token.CMD,
        Token.ARG,
        Token.OR,
        Token.PIPE,
        Token.AND,
        Token.END,
        Token.BACK,
        Token.LPAREN,
        Token.RPAREN,
        Token.REDIR_IN_HERE,
        Token.REDIR_IN,
        Token.LIMIT_STR,
        Token.REDIR_OUT_APP,
        Token.REDIR_OUT
    ]

    state = State.START
    def lex(self, cmd_str):
        while True:
            
