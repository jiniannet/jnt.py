
# -*- coding: utf-8 -*-
from jntemplate.nodes import OperatorElement

__all__ = ["calculate_boolean", "is_operator", "get_priority",
           "get_reverse_polish_notation", "calculate", "calculate_and",
           "calculate_or", "equals", "calculate_reverse_polish_notation",
           "calculate_value"]


def calculate_boolean(value):
    if value == None:
        return False
    if isinstance(value, int):
        return value != 0
    if isinstance(value, float):
        return value != 0
    if isinstance(value, str):
        return not (value == None or value == "")
    if isinstance(value, bool):
        return value
    return True


def is_operator(value):
    if value == "||" \
            or value == "|" \
            or value == "&" \
            or value == "&&" \
            or value == ">" \
            or value == ">=" \
            or value == "<" \
            or value == "<=" \
            or value == "==" \
            or value == "!=" \
            or value == "+" \
            or value == "-" \
            or value == "*" \
            or value == "/" \
            or value == "(" \
            or value == ")" \
            or value == "%" \
            or value == "and" \
            or value == "or":
        return True
    return False


def get_priority(c):
    if c == "||" \
            or c == "|" \
            or c == "&" \
            or c == "&&" \
            or c == "Or" \
            or c == "LogicalOr" \
            or c == "LogicAnd" \
            or c == "And":
        return 5
    if c == ">" \
            or c == ">=" \
            or c == "<" \
            or c == "<=" \
            or c == "==" \
            or c == "!=" \
            or c == "GreaterThan" \
            or c == "GreaterThanOrEqual" \
            or c == "LessThan" \
            or c == "LessThanOrEqual" \
            or c == "Equal" \
            or c == "NotEqual":
        return 6
    if c == "+" \
            or c == "-" \
            or c == "Plus" \
            or c == "Minus":
        return 7
    if c == "%" \
            or c == "*" \
            or c == "Percent" \
            or c == "Times" \
            or c == "/" \
            or c == "Divided":
        return 8
    return 9


# def get_reverse_polish_notation(value):
#     """ProcessExpression"""
#     value = value.replace("  ", "")
#     result = []
#     j = 0
#     i = 0
#     num = None

#     for i in range(len(value)):
#         if value[i] == '+' \
#                 or value[i] == '-' \
#                 or value[i] == '*' \
#                 or value[i] == '/' \
#                 or value[i] == '(' \
#                 or value[i] == ')' \
#                 or value[i] == '%':
#             if j < i:
#                 num = value.Substring(j, i - j)
#                 if (num.IndexOf('.') == -1)
#                     result.Add(Int32.Parse(value.Substring(j, i - j)))
#                 else
#                     result.Add(Double.Parse(value.Substring(j, i - j)))
#                 j = i
#             result.Add(OperatorConvert.Parse(value[i].ToString()))
#             j += 1
#     if (j < i)
#     {
#         result.Add(Double.Parse(value.Substring(j, i - j)))
#     }
#     return ProcessExpression(result.ToArray())

def get_reverse_polish_notation(value):
    post = []
    stack = []

    for i in range(len(value)):
        if value[i] == None or not isinstance(value[i], OperatorElement):
            post.append(value[i])
            continue
        if value[i].text == "(" \
                or value[i].text == "LeftParentheses":
            stack.append(value[i])
        if value[i].text == ")" \
                or value[i].text == "RightParentheses":
            while len(stack) > 0:
                op = stack.pop()
                if str(op) == "(":
                    break
                else:
                    post.append(op)

        if value[i].text == "+" \
                or value[i].text == "-" \
                or value[i].text == "*" \
                or value[i].text == "%" \
                or value[i].text == "/" \
                or value[i].text == "||" \
                or value[i].text == "|" \
                or value[i].text == "&&" \
                or value[i].text == "&" \
                or value[i].text == ">" \
                or value[i].text == ">=" \
                or value[i].text == "<" \
                or value[i].text == "<=" \
                or value[i].text == "==" \
                or value[i].text == "!=" \
                or value[i].text == "or" \
                or value[i].text == "and" \
                or value[i].text == "Plus" \
                or value[i].text == "Minus" \
                or value[i].text == "Times" \
                or value[i].text == "Percent" \
                or value[i].text == "Divided" \
                or value[i].text == "LogicalOr" \
                or value[i].text == "Or" \
                or value[i].text == "LogicAnd" \
                or value[i].text == "And" \
                or value[i].text == "GreaterThan" \
                or value[i].text == "GreaterThanOrEqual" \
                or value[i].text == "LessThan" \
                or value[i].text == "LessThanOrEqual" \
                or value[i].text == "Equal" \
                or value[i].text == "NotEqual":
            if len(stack) == 0:
                stack.append(value[i])
            else:
                if get_priority(value[i].text) > get_priority(stack[-1].text):
                    stack.append(value[i])
                else:
                    if stack[-1].text != "(":
                        post.append(stack.pop())
                    stack.append(value[i])
        else:
            post.append(value[i])

    while len(stack) > 0:
        post.append(stack.pop())
    post.reverse()
    return post


def calculate(x,  y,  opt):
    if opt == "||" or opt == "or":
        return calculate_or(x, y)
    if opt == "&&" or opt == "and":
        return calculate_and(x, y)
    if type(x) != type(y):
        if isinstance(x, bool):
            y = calculate_boolean(y)
        if isinstance(y, bool):
            x = calculate_boolean(x)
        if isinstance(x, float) and str(y).isdigit():
            y = float(y)
        if isinstance(y, float) and str(x).isdigit():
            x = float(x)
        if isinstance(x, int) and str(y).isdigit():
            y = int(y)
        if isinstance(y, int) and str(x).isdigit():
            x = int(x)
        if isinstance(x, str):
            y = str(y)
        if isinstance(y, str):
            x = str(x)
    return calculate_value(x, y, opt)


def calculate_and(x,  y):
    if not calculate_boolean(x):
        return False
    if not calculate_boolean(y):
        return False
    return True


def calculate_or(x,  y):
    if calculate_boolean(x):
        return True
    if calculate_boolean(y):
        return True
    return False


def equals(x, y):
    if x == None or y == None:
        if x == None and y == None:
            return True
        return False
    if type(x) == type(y):
        if x == y:
            return True
        return False
    return False


def calculate_reverse_polish_notation(post):
    # post = []
    # while len(value) > 0:
    #     post.append(value.pop())
    #post = value
    stack = []

    while len(post) > 0:
        obj = post.pop()
        if obj != None and isinstance(obj, OperatorElement):
            y = stack.pop()
            x = stack.pop()
            stack.append(calculate(x, y, str(obj)))
        else:
            stack.append(obj)
    return stack.pop()


def calculate_value(x,  y,  opt):
    if opt == "+":
        return x + y
    if opt == "-":
        return x - y
    if opt == "*":
        return x * y
    if opt == "/":
        return x / y
    if opt == "%":
        return x % y
    if opt == ">=":
        return x >= y
    if opt == "<=":
        return x <= y
    if opt == "<":
        return x < y
    if opt == ">":
        return x > y
    if opt == "==":
        return x == y
    if opt == "!=":
        return x != y
    if opt == "|":
        return x | y
    if opt == "&":
        return x & y
    if opt == "||" or opt == "or":
        return x or y
    if opt == "&&" or opt == "and":
        return x and y
    raise Exception("Operator \"" + opt + "\" can not be applied operand \"" +
                    str(type(x)) + "\" and \"" + str(type(y)) + "\"")
