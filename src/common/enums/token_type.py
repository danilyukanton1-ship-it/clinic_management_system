from enum import Enum


class TokenType(str, Enum):
    REFRESH = "refresh"
    ACCESS = "access"
