from __future__ import annotations

def left_pad(string: str, length: int, char: str = " ") -> str:
    return (char * (length - len(string))) + string

def right_pad(string: str, length: int, char: str = " ") -> str:
    return string + (char * (length - len(string) ))