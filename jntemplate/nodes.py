# -*- coding: utf-8 -*-

from enum import Enum
from jntemplate.runtime import _get_environment_variable 

__all__ = ["Token", "OperatorElement", "TokenKind", "FlagMode",
           "Scanner", "Lexer", "VariableScope"]


class Token(object):
    def __init__(self, kind, text):
        self.text = text
        self.begin_line = 0
        self.begin_column = 0
        self.end_line = 0
        self.end_column = 0
        self.kind = kind
        self.next = None

    def string(self):
        return self.text

    def compare(self, other):
        if self.begin_line > other.begin_line:
            return 1
        if self.begin_line < other.begin_line:
            return -1
        if self.begin_column > other.begin_column:
            return 1
        if self.begin_column < other.begin_column:
            return -1
        return 0

    def __str__(self):
        return self.string()


class OperatorElement(object):
    def __init__(self, text):
        self.text = text

    def string(self):
        return self.text

    def __str__(self):
        return self.text


class TokenKind(Enum):
    none = 0
    text = 1
    text_data = 2
    tag = 3
    tag_start = 4
    tag_end = 5
    string = 6
    number = 7
    left_bracket = 8
    right_bracket = 9
    left_parentheses = 10
    right_parentheses = 11
    new_line = 12
    dot = 13
    string_start = 14
    string_end = 15
    space = 16
    punctuation = 17
    operator = 18
    comma = 19
    eof = 20


class FlagMode(Enum):
    none = 0
    logogram = 1
    full = 2
    comment = 3


class Scanner(object):
    def __init__(self, text):
        self.index = 0
        self._start = 0
        self._document = text
        if text == None:
            self._count = 0
        else:
            self._count = len(text)

    def next(self, i=1):
        if self.index + i > self._count:
            return False
        self.index += i
        return True

    def back(self, i=1):
        if (self.index < i):
            return False
        self.index -= i
        return True

    def read(self, i=0):
        if self.index + i >= self._count:
            return None
        return self._document[self.index + i]

    def is_end(self):
        return self.index >= self._count

    def IsMatch(self, arr, n=0):
        n = self.index + n
        if self._count >= n + len(arr):
            for i in range(len(arr)):
                if self._document[n + i] != arr[i]:
                    return False
            return True
        return False

    def get_escapestring(self):
        value = self.sub_escape_string(self._start, self.index)
        self._start = self.index
        return value

    def get_string(self):
        value = self.sub_string(self._start, self.index)
        self._start = self.index
        return value

    def sub_escape_string(self, x, y):
        chars = []
        num = x
        while(num < y):
            if self._document[num] == '\\' and num < self._count-1:
                if self._document[num + 1] == '0':
                    chars.append('\0')
                    num += 1
                elif self._document[num + 1] == '"':
                    chars.append('"')
                    num += 1
                elif self._document[num + 1] == '\'':
                    chars.append('\'')
                    num += 1
                elif self._document[num + 1] == '\\':
                    chars.append('\\')
                    num += 1
                elif self._document[num + 1] == 'a':
                    chars.append('\a')
                    num += 1
                elif self._document[num + 1] == 'b':
                    chars.append('\b')
                    num += 1
                elif self._document[num + 1] == 'f':
                    chars.append('\f')
                    num += 1
                elif self._document[num + 1] == 'n':
                    chars.append('\n')
                    num += 1
                elif self._document[num + 1] == 'r':
                    chars.append('\r')
                    num += 1
                elif self._document[num + 1] == 't':
                    chars.append('\t')
                    num += 1
                elif self._document[num + 1] == 'v':
                    chars.append('\v')
                    num += 1
                else:
                    chars.append(self._document[num])
            else:
                chars.append(self._document[num])
            num += 1
        return "".join(chars)

    def sub_string(self, x, y):
        return self._document[x:y]


class Lexer(object):
    def __init__(self, text):
        self._document = text
        self._prefix = _get_environment_variable("prefix")
        self._flag = _get_environment_variable("flag")
        self._suffix = _get_environment_variable("suffix") 
        self.reset()

    def reset(self):
        self._flagmode = FlagMode.none
        self._line = 1
        self._column = 1
        self._kind = TokenKind.text
        self._startColumn = 1
        self._startLine = 1
        self._scanner = Scanner(self._document)
        self._collection = []
        self._pos = []

    def get_token(self, kind):
        if kind == TokenKind.string_start:
            token = Token(self._kind, self._scanner.get_escapestring())
        else:
            token = Token(self._kind, self._scanner.get_string())
        token.begin_line = self._startLine
        token.begin_column = self._startColumn
        token.end_column = self._column
        self.begin_line = self._line
        self._kind = kind
        self._start_column = self._column
        self._start_line = self._line
        return token

    def next(self, i=1):
        if self._scanner.next(i):
            if self._scanner.read() == '\n':
                self._line += 1
                self._column = 1
            else:
                self._column += 1
            return True
        return False

    def _is_tag_start(self):
        if self._scanner.is_end() or self._flagmode != FlagMode.none:
            return False
        find = True
        for i in range(len(self._prefix)):
            if self._prefix[i] != self._scanner.read(i):
                find = False
                break
        if find:
            self._flagmode = FlagMode.full
            return True
        if self._scanner.read() == self._flag:
            if self._scanner.read(1) == '*':
                self._flagmode = FlagMode.comment
                return True
            elif self._scanner.read(1).isalpha():
                self._flagmode = FlagMode.logogram
                return True
        return False

    def allow_char(self, value):
        if value == None:
            return False
        if value == '_' or value.isalnum():
            return True
        return False

    def _is_tag_end(self):
        if self._flagmode != FlagMode.none and len(self._pos) == 0:
            if self._scanner.is_end():
                return True
            if self._scanner.read() != '.':
                if self._flagmode == FlagMode.full:
                    for i in range(len(self._suffix)):
                        if self._suffix[i] != self._scanner.read(i):
                            return False
                    return True
                elif self._flagmode == FlagMode.comment:
                    if self._scanner.read() == '*' and self._scanner.read(1) == self._flag:
                        return True
                    else:
                        return False
                else:
                    val = self._scanner.read()
                    if ((val == '(' or val == '[' or self.allow_char(val)) and self.allow_char(self._scanner.read(-1))) \
                            or (self.allow_char(val) and (self._scanner.read(-1) == '.')):
                        return False
                    return True
        return False

    def parse(self):
        if self._kind != TokenKind.eof:
            run = True
            while run:
                if self._flagmode != FlagMode.none:
                    if self._flagmode == FlagMode.comment:
                        self.next()
                        self.get_token(TokenKind.text_data)
                        self.read_comment_token()
                    else:
                        if self._flagmode == FlagMode.full:
                            self.next(len(self._prefix) - 1)
                        kind = self.get_kind(self._scanner.read())
                        self.add_token(kind)
                        if self._kind == TokenKind.string_start:
                            self._pos.append('"')
                        elif self._kind == TokenKind.left_parentheses:
                            self._pos.append("(")
                        elif self._kind == TokenKind.left_bracket:
                            self._pos.append("[")
                    self.read_token()
                elif self._is_tag_start():
                    self.add_token(TokenKind.tag_start)
                run = self.next()
            self.add_token(TokenKind.eof)
        if self._flagmode != FlagMode.none:
            self._flagmode = FlagMode.none
            self.append_token(Token(TokenKind.tag_end, ""))
        return self._collection

    def add_token(self, kind):
        token = self.get_token(kind)
        self.append_token(token)

    def append_token(self, token):
        if len(self._collection) > 0 and self._collection[-1].next == None:
            self._collection[-1].next = token
        self._collection.append(token)

    def read_end_token(self):
        if self._is_tag_end():
            add = True
            if self._flagmode == FlagMode.full:
                self.add_token(TokenKind.tag_end)
                self.next(len(self._suffix))
            elif self._flagmode == FlagMode.comment:
                self.get_token(TokenKind.tag_end)
                self.next(2)
                add = False
            else:
                self.add_token(TokenKind.tag_end)
            self._flagmode = FlagMode.none
            if self._is_tag_start():
                token = self.get_token(TokenKind.tag_start)
            else:
                token = self.get_token(TokenKind.text)
            if add:
                self.append_token(token)
            return True
        return False

    def read_comment_token(self):
        while self.next():
            if self.read_end_token():
                break

    def get_prev_char_count(self, c):
        i = 1
        while self._scanner.read(-i) == c:
            i = i+1
        i = i-1
        return i

    def read_token(self):
        while self.next():
            if self._scanner.read() == '"':
                if len(self._pos) > 0 and self._pos[-1] == "\"":
                    if self._scanner.read(-1) != '\\' or self.get_prev_char_count('\\') % 2 == 0:
                        if self._kind == TokenKind.string_start:
                            self.add_token(TokenKind.string)
                        self.add_token(TokenKind.string_end)
                        self._pos.pop()
                    continue

                if self._kind == TokenKind.tag_start or self._kind == TokenKind.left_bracket or self._kind == TokenKind.left_parentheses or self._kind == TokenKind.operator or self._kind == TokenKind.punctuation or self._kind == TokenKind.comma or self._kind == TokenKind.space:
                    self.add_token(TokenKind.string_start)
                    self._pos.append("\"")
                    continue

            if self._kind == TokenKind.string_start:
                self.add_token(TokenKind.string)
                continue

            if self._kind == TokenKind.string:
                continue

            if self._scanner.read() == '(' or self._scanner.read() == '[':
                self._pos.append(self._scanner.read())
            elif (self._scanner.read() == ')' and len(self._pos) > 0 and self._pos[-1] == "(") \
                    or (self._scanner.read() == ']' and len(self._pos) > 0 and self._pos[-1] == "["):
                self._pos.pop()
                # if self._pos.count == 1:
            elif self.read_end_token():
                break

            # TokenKind tk
            # 正负数符号识别
            if self._scanner.read() == '+' or self._scanner.read() == '-':
                if self._scanner.read(1).isnumeric() and self._kind != TokenKind.number and self._kind != TokenKind.right_bracket and self._kind != TokenKind.right_parentheses and self._kind != TokenKind.string and self._kind != TokenKind.tag and self._kind != TokenKind.text_data:
                    tk = TokenKind.number
                else:
                    tk = TokenKind.operator
            else:
                tk = self.get_kind(self._scanner.read())
            # if (self.kind == tk || (tk == TokenKind.Number && self.kind == TokenKind.TextData))
            if (self._kind != tk or self._kind == TokenKind.left_parentheses or self._kind == TokenKind.right_parentheses) and (tk != TokenKind.number or self._kind != TokenKind.text_data):
                if tk != TokenKind.dot or self._kind != TokenKind.number:
                    self.add_token(tk)

    def get_kind(self, c):
        if self._flagmode == FlagMode.none:
            return TokenKind.text
        if c == ' ':
            return TokenKind.space
        if c == '(':
            return TokenKind.left_parentheses
        if c == ')':
            return TokenKind.right_parentheses
        if c == '[':
            return TokenKind.left_bracket
        if c == ']':
            return TokenKind.right_bracket
        if c.isnumeric():
            return TokenKind.number
        if c == '*' or c == '-' or c == '+' or c == '/' or c == '>' or c == '<' or c == '=' or c == '!' or c == '&' or c == '|' or c == '~' or c == '^' or c == '?' or c == '%':
            return TokenKind.operator
        if c == ',':
            return TokenKind.comma
        if c == '.':
            return TokenKind.dot
        if c == '"':
            return TokenKind.string_start
        if c == ';':
            return TokenKind.punctuation
        return TokenKind.text_data


class VariableScope(object):
    def __init__(self, parent=None):
        self.parent = parent
        self._dict = {}

    def clear(self, cls_all=False):
        self._dict.clear()
        if cls_all and self.parent != None:
            self.parent.clear(cls_all)

    def get(self, key):
        if(key == None):
            return None
        if self._dict.__contains__(key):
            return self._dict[key]
        if self.parent != None:
            return self.parent.get(key)
        return None

    def set(self, key, value):
        if key != None:
            self._dict[key] = value

    def chang_value(self, key, value):
        if key == None:
            return False
        if self._dict.__contains__(key):
            self._dict[key] = value
            return True
        if self.parent != None:
            return self.parent.changValue(key, value)
        return False

    def push(self, key, value):
        self.set(key, value)

    def contains_key(self, key):
        if self._dict.__contains__(key):
            return True
        if self.parent != None:
            return self.parent.contains_key(key)
        return False

    def remove(self, key):
        return self._dict.pop(key)
