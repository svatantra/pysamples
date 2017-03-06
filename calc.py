PLUS, MINUS, MUL, DIV ,EOF = ('+', '-', '*', '/','EOF')
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
        """
        Advance in text stream as long as there
        are characters
        :return:
        """
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.ch = self.text[self.pos]
        else:
            self.ch = None

    def skip_whitespace(self):
        while self.ch is not None and self.ch.isspace():
            self.advance()

    def integer(self):
        """
        Keep advancing till there are digits in the stream
        :return:
        """
        num = ''
        while self.ch is not None and self.ch.isdigit():
            num += self.ch
            self.advance()
        return int(num)

    def __iter__(self):
        return self

    def next(self):
        tok = self.get_next_token()
        if tok is None:
            raise StopIteration()
        else:
            return tok

    def get_next_token(self):
        while self.ch is not None:
            if self.ch.isdigit():
                return Token(self.integer(), 'INT')
            if self.ch.isspace():
                self.skip_whitespace()
                continue
            if self.ch in OPERATORS:
                tok = Token(self.ch, self.ch)
                self.advance()
                return tok
            raise Exception('Invalid Character')
        return Token(EOF,None)

    def print_data(self):
        while self.ch is not None:
            print self.ch
            self.advance()

"""
   expr::= fact((PLUS|MINUS)fact)*
   fact::= term((MUL|DIV)term)*
   term::= INTEGER
"""
class Intepreter:
    def __init__(self,text):
        self.lex = Lexer(text)
        self.current_token = self.lex.get_next_token()

    def raise_error(self):
        raise Exception('Invalid syntax')

    def term(self):
        token = self.current_token
        self.consume('INT')
        return token.data

    def consume(self,type):
        if self.current_token.type==type:
            self.current_token = self.lex.get_next_token()
        else:
            self.raise_error()

    def fact(self):
        result = self.term()
        while self.current_token.type in [DIV,MUL]:
            if self.current_token.data == DIV:
                self.consume(DIV)
                result/=self.term()
            elif self.current_token.data == MUL:
                self.consume(MUL)
                result*=self.term()

        return result
    def expr(self):
        result = self.fact()
        while self.current_token.type in [PLUS,MINUS]:
            if self.current_token.data == PLUS:
                self.consume(PLUS)
                result+=self.fact()
            elif self.current_token.data == MINUS:
                self.consume(MINUS)
                result-=self.fact()

        return result


if __name__ == '__main__':

    while True:
        text = raw_input('cal> ')
        intrp = Intepreter(text)

        print intrp.expr()
