from dataclasses import dataclass, field
from typing import List
from ptoken.token import Token
from ptoken.token_type import TokenType

@dataclass
class Scanner:
    source: str
    tokens: List[Token] = field(default_factory=list)
    start: int = 0
    current: int = 0
    line: int = 1

    keywords = {
        "and":    "AND",
        "class":  "CLASS",
        "else":   "ELSE",
        "false":  "FALSE",
        "for":    "FOR",
        "fun":    "FUN",
        "if":     "IF",
        "nil":    "NIL",
        "or":     "OR",
        "print":  "PRINT",
        "return": "RETURN",
        "super":  "SUPER",
        "this":   "THIS",
        "true":   "TRUE",
        "var":    "VAR",
        "while":  "WHILE",
    }

    def scan_tokens(self):
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
                
    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        ch: chr = self.advance()
        match ch:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end(): 
                        self.advance()
                else: self.add_token(TokenType.SLASH)
            case ' ': pass
            case '\r': pass
            case '\t': pass
            case '\n': self.line += 1
            case '"': self.string()
            case 'o':
                if self.match('r'):
                    self.add_token(TokenType.OR)
            case _: 
                if self.is_digit(ch):
                    self.number()
                elif self.is_alpha(ch):
                    self.identifier()
                else:
                    #Lox.error(self.line, "Unexpected character.")
                    print(f"[line {self.line}] Error: Unexpected character '{ch}'")

    def advance(self):
        ch =  self.source[self.current]
        self.current += 1
        return ch
    
    def add_token(self, type: TokenType, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: chr):
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True
    
    def peek(self):
        if (self.is_at_end()): return '\0'
        return self.source[self.current]
    
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            #Lox.error(self.line, "Unterminated string.")
            print(f"[line {self.line}] Error: Unterminated string.")

        # closing "
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, ch):
        return ch >= '0' and ch <= '9'
    
    def number(self):
        while self.is_digit(self.peek()): self.advance()

        # look for fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # consume the "."
            self.advance()

            while self.is_digit(self.peek()): self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def peak_next(self):
        if (self.current + 1 >= len(self.source)): return '\0'
        return self.source[self.current + 1]
    
    def is_alpha(self, ch):
        return (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z') or ch == '_'

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        type: TokenType = self.keywords.get(text)
        if type != None: type = TokenType.IDENTIFIER
        self.add_token(type)

    def is_alpha_numeric(self, ch):
        return self.is_alpha(ch) or self.is_digit(ch)
