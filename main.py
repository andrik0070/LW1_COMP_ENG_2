from pprint import pprint

from classes.lexic import Lexer

with open("./data/program_text.txt", 'r') as file:
    program_text = file.read()
    lexer = Lexer(program_text)
    with open("./lexems.txt", 'w+') as lexem_file:
        lexem_file.truncate()
        for token in lexer.tokenise():
            lexem_file.write(token.__str__() + '\n')
