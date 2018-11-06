import string


class Token(object):
    Identifier = 'Identifier'
    Integer = 'Integer'
    Delimiter = 'Delimiter'
    DoubleDelimiter = 'DoubleDelimiter'
    Keyword = 'Keyword'
    Literal = 'Literal'
    eof = 'END-OF-FILE'
    operator = 'OP'
    block_start = 'START'
    block_end = 'END'

    keywords = ['procedure', 'var', 'Integer', 'TDrawBuffer', 'Begin', 'if', 'and', 'then', 'End']

    def __init__(self, type, value, line, line_no, line_pos):
        self.type = type
        self.value = value
        self.line = line
        self.line_pos = line_pos - len(value)
        self.line_no = line_no

    def __str__(self):
        # return '{0}:{1}'.format(self.line_no + 1, self.line_pos).ljust(10) + self.type.ljust(15) + self.value
        return '{0}:{1}'.format(self.line_no + 1, self.line_pos) + ',' + self.type + ',' + self.value


class Lexer(object):
    eof_marker = '$'
    whitespace = ' \t\n'
    newline = '\n'
    # comment_marker = '#'
    delimiters = ['.', ':', ';', '(', ')', '=', '-', '+', ',', '[', ']', '<', '>']
    double_delimiter = [':=', '<>']
    match = ''
    char = ''

    def __init__(self, code):
        super(Lexer, self).__init__()

        with open('./lexem_errors.txt', 'w') as file:
            pass

        self.code = code
        self.cursor = 0
        self.tokens = []

        self.lines = code.split(Lexer.newline)
        self.line_no = 0
        self.line_pos = 0

    def get_next_char(self):
        self.cursor += 1
        self.line_pos += 1
        if self.cursor > len(self.code):
            return Lexer.eof_marker

        return self.code[self.cursor - 1]

    def tokenise(self):
        self.char = self.get_next_char()
        while self.char != Lexer.eof_marker:

            # ignore whitespace
            if self.char in Lexer.whitespace:
                if self.char in Lexer.newline:
                    self.line_no += 1
                    self.line_pos = 0
                self.char = self.get_next_char()

            # comment
            # elif char in Lexer.comment_marker:
            #     while char not in Lexer.newline:
            #         char = self.get_next_char()

            # identifier token
            elif self.char in string.ascii_letters:
                self.match = self.char
                self.char = self.get_next_char()
                while self.char in (string.ascii_letters + string.digits):
                    self.match += self.char
                    self.char = self.get_next_char()

                if self.char not in (self.delimiters + [' ', Lexer.newline, Lexer.eof_marker]):
                    self.unrecognized_lexem()
                else:
                    token = Token(Token.Identifier, self.match, self.lines[self.line_no], self.line_no, self.line_pos)

                    if self.match in Token.keywords:
                        token.type = Token.Keyword

                    self.tokens.append(token)

            # Integer token
            elif self.char in string.digits:
                self.match = self.char
                self.char = self.get_next_char()
                while self.char in string.digits:
                    self.match += self.char
                    self.char = self.get_next_char()

                if self.char not in (self.delimiters + [' ', self.newline]):
                    self.unrecognized_lexem()

                token = Token(Token.Integer, self.match, self.lines[self.line_no], self.line_no, self.line_pos)
                self.tokens.append(token)
            elif self.char == "'":
                self.match = self.char
                self.char = self.get_next_char()
                while self.char != "'":
                    self.match += self.char
                    self.char = self.get_next_char()
                self.match += self.char
                self.tokens.append(Token(Token.Literal, self.match + self.char, self.lines[self.line_no], self.line_no,
                                         self.line_pos))
                self.char = self.get_next_char()

            elif self.char in self.delimiters:
                self.match = self.char
                self.char = self.get_next_char()

                if (self.match + self.char) in self.double_delimiter:
                    token = Token(Token.DoubleDelimiter, self.match + self.char, self.lines[self.line_no], self.line_no,
                                  self.line_pos)
                    self.char = self.get_next_char()
                else:
                    token = Token(Token.Delimiter, self.match, self.lines[self.line_no], self.line_no,
                                  self.line_pos)
                self.tokens.append(token)

            else:
                self.match = self.char
                self.unrecognized_lexem()
                # raise ValueError(
                #     'Unexpected character found: {0}:{1} -> {2}\n{3}'.format(self.line_no + 1, self.line_pos + 1,
                #                                                              self.char,
                #                                                              self.lines[self.line_no]))

        return self.tokens

    def unrecognized_lexem(self):
        self.char = self.get_next_char()
        while self.char not in (self.delimiters + [' ', Lexer.newline, Lexer.eof_marker]):
            self.match += self.char
            self.char = self.get_next_char()

        with open('./lexem_errors.txt', 'a') as file:
            file.write("'" + self.match + "' unrecognized lexem.\n")
