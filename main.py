from pprint import pprint

from classes.lexic import Lexer

with open("./data/program_text.txt", 'r') as file:
    program_text = file.read()
    lexer = Lexer(program_text)
    pprint(lexer.tokenise())
