# -*- coding: utf-8 -*-
from jntemplate.nodes import TokenKind


def token_concat(tokes):
    s = ""
    for t in tokes:
        s += str(t)
    return s


def clear_space_token(tokens):
    end = len(tokens)
    i = 0
    while i < end:
        if tokens[i].kind == TokenKind.space:
            del tokens[i]
            i -= 1
            end -= 1
        i = i+1
    return tokens
