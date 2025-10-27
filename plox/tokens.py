from dataclasses import dataclass
from token_type import TokenType

@dataclass
class Token():
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"