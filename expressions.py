from dataclasses import dataclass
from abc import ABC

from tokens import Token

class Expr(ABC):
    pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

