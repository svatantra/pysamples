PLUS, MINUS, MUL, DIV = ('+', '-', '*', '/')
OPERATORS = [PLUS, MINUS, MUL, DIV]


class Token:
    def __init__(self, data, type):
        self.data = data
        self.type = type

    def __str__(self):
        return '(%s,%s)' % (self.data, self.type)

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.ch = self.text[0]

    def advance(self):
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.ch = self.text[self.pos]
        else:
            self.ch = None

    def skip_whitespace(self):
        while self.ch != None and self.ch.isspace():
            self.advance()

    def integer(self):
        num = ''
        while self.ch != None and self.ch.isdigit():
            num += self.ch
            self.advance()
        return int(num)

    def __iter__(self):
        return self

    def next(self):
        tok = self.get_next_token()
        if tok == None:
            raise StopIteration()
        else:
            return tok

    def get_next_token(self):
        while self.ch != None:
            if self.ch.isdigit():
                return Token(self.integer(), 'INT')
            if self.ch.isspace():
                self.skip_whitespace()
                continue
            if self.ch in OPERATORS:
                tok = Token(self.ch, 'OPERATOR')
                self.advance()
                return tok

    def print_data(self):
        while self.ch != None:
            print self.ch
            self.advance()


if __name__ == '__main__':
    lex = Lexer(' 34 + 45 -87 -67')
    for tok in lex:
        print tok

    print lex.get_next_token()
