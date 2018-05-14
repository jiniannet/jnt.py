# -*- coding: utf-8 -*-
from abc import abstractclassmethod, ABCMeta
from jntemplate.core import VariableTag, ValueTag, IfTag, ElseifTag, ElseTag, \
    ForeachTag, FunctionTag, ExpressionTag, SetTag, EndTag, TextTag, ReferenceTag,\
    IncludeTag, IndexTag
import jntemplate.utils
from jntemplate.nodes import TokenKind

__all__ = ["VariableParser", "StringParser", "SetParser", "NumberParser",
           "LoadParser", "IncludeParser", "IfParser", "FunctionParser",
           "ForeachParser", "EndParser", "ElseifParser", "EleseParser",
           "BooleanParser", "IndexParser", "ComplexParser"]


class TagParser(object):
    @abstractclassmethod
    def parse(self, template_parser, tc):
        pass


class VariableParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and len(tc) == 1 \
                and tc[0].kind == TokenKind.text_data:
            tag = VariableTag()
            tag.name = tc[0].string()
            return tag
        return None


class IndexParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and len(tc) > 3 \
                and tc[-1].kind == TokenKind.right_bracket:
            y = len(tc) - 1
            x = -1
            pos = 0
            i = y

            while i >= 0:
                if tc[i].kind == TokenKind.dot and pos == 0:
                    return None
                if tc[i].kind == TokenKind.right_bracket:
                    pos += 1
                    i -= 1
                    continue
                if tc[i].kind == TokenKind.left_bracket:
                    pos -= 1
                    if pos == 0 and x == -1:
                        x = i
                i -= 1

            if x == -1:
                return None

            tag = IndexTag()
            tag.container = template_parser.read(tc[0: x])
            tag.index = template_parser.read(tc[x + 1: y])
            return tag
        return None


class StringParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and len(tc) == 3 \
                and tc[0].kind == TokenKind.string_start \
                and tc[1].kind == TokenKind.string \
                and tc[2].kind == TokenKind.string_end:
            tag = ValueTag()
            tag.value = tc[1].text
            return tag
        return None


class SetParser(TagParser):
    def parse(self, template_parser, tc):
        if tc == None or template_parser == None:
            return None

        if len(tc) == 5 \
                and tc[0].text == "set" \
                and tc[1].kind == TokenKind.left_parentheses \
                and tc[3].text == "=" \
                and tc[-1].kind == TokenKind.right_parentheses:

            tag = SetTag()
            tag.name = tc[2].text
            coll = tc[4: -1]
            tag.value = template_parser.read(coll)
            return tag

        # if len(tc) == 2 \
        #         and tc[0].kind == TokenKind.text_data \
        #         and tc[1].kind == TokenKind.operator \
        #         and (tc[1].text == "++" or tc[1].text == "--"):

        #     tag = SetTag()
        #     tag.name = tc[0].text
        #     child = ExpressionTag()
        #     child.add_child()
        #     tag.value = template_parser.read(coll)
        #     return tag

        if len(tc) > 2 \
                and tc[0].kind == TokenKind.text_data \
                and tc[1].text == "=":

            tag = SetTag()
            tag.name = tc[0].text
            coll = tc[2:]
            tag.value = template_parser.read(coll)
            return tag

        return None


class NumberParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and len(tc) == 1 \
                and tc[0].kind == TokenKind.number:
            tag = ValueTag()
            if tc[0].text.find('.') == -1:
                tag.value = int(tc[0].text)
            else:
                tag.value = float(tc[0].text)
            return tag

        return None


class LoadParser(TagParser):

    def parse(self, template_parser, tc):
        return None


class IncludeParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 2 \
                and tc[0].text == "include" \
                and tc[1].TokenKind == TokenKind.left_parentheses \
                and tc[-1].TokenKind == TokenKind.right_parentheses:
            tag = IncludeTag()
            tag.path = template_parser.read(tc[2:-1])
            return tag


class IfParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 3 \
                and tc[0].text == "if":
            # n = len(tc)
            if tc[1].kind != TokenKind.left_parentheses \
                    or tc[-1].kind != TokenKind.right_parentheses:
                raise Exception("syntax error near :%s line:%d col:%d" % jntemplate.utils.token_concat(
                    tc) % tc[0].begin_line % tc[0].begin_column)
            tag = IfTag()
            child_tag = ElseifTag()
            coll = tc[2: -1]
            child_tag.test = template_parser.read(coll)
            child_tag.first = coll[0]
            tag.add_child(child_tag)

            while template_parser.next():
                if isinstance(template_parser.tag, EndTag):
                    tag.add_child(template_parser.tag)
                    return tag
                elif isinstance(template_parser.tag, ElseifTag) or \
                        isinstance(template_parser.tag, ElseTag):
                    tag.add_child(template_parser.tag)
                else:
                    tag.children[-1].add_child(template_parser.tag)
            raise Exception("if is not properly closed by a end tag:%s line:%d col:%d" %
                            jntemplate.utils.token_concat(tc) % tc[0].begin_line % tc[0].begin_column)

        return None


class FunctionParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 2 \
                and tc[0].kind == TokenKind.text_data \
                and tc[1].kind == TokenKind.left_parentheses \
                and tc[-1].kind == TokenKind.right_parentheses:

            tag = FunctionTag()
            tag.name = tc[0].text
            pos = 0
            start = 2
            end = 0
            i = 2
            max = len(tc)

            while i < max:
                end = i
                if tc[i].kind == TokenKind.comma:
                    if pos == 0:
                        coll = tc[start: end]
                        if len(coll) > 0:
                            tag.add_child(template_parser.read(coll))
                        start = i + 1
                else:
                    if tc[i].kind == TokenKind.left_parentheses:
                        pos += 1
                    elif tc[i].kind == TokenKind.right_parentheses:
                        pos == 1
                    if i == len(tc) - 1:
                        coll = tc[start: end]
                        if len(coll) > 0:
                            tag.add_child(template_parser.read(coll))
                i += 1
            return tag
        return None


class ForeachParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 4 \
                and (tc[0].text == "for" or tc[0].text == "foreach") \
                and tc[1].kind == TokenKind.left_parentheses \
                and tc[2].kind == TokenKind.text_data \
                and tc[3].text == "in" \
                and tc[-1].kind == TokenKind.right_parentheses:
            tag = ForeachTag()
            tag.name = tc[2].text
            coll = tc[4:-1]
            tag.source = template_parser.read(coll)
            while template_parser.next():
                tag.add_child(template_parser.tag)
                if isinstance(template_parser.tag, EndTag):
                    return tag
            raise Exception("foreach is not properly closed by a end tag:%s line:%d col:%d" %
                            jntemplate.utils.token_concat(tc) % tc[0].begin_line % tc[0].begin_column)


class EndParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) == 1 \
                and tc[0].text == "end":
            return EndTag()
        return None


class ElseifParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 3 \
                and (tc[0].text == "elseif" or tc[0].text == "elif") \
                and tc[1].kind == TokenKind.left_parentheses \
                and tc[-1].kind == TokenKind.right_parentheses:
            tag = ElseifTag()
            coll = tc[2:-1]
            tag.test = template_parser.read(coll)
            return tag
        return None


class EleseParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) == 1 \
                and tc[0].text == "else":
            return ElseTag()
        return None


class BooleanParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) == 1 \
                and (tc[0].text == "true" or tc[0].text == "false"):
            tag = ValueTag()
            if tc[0].text == "true":
                tag.value = True
            else:
                tag.value = False
            return tag
        return None


class ComplexParser(TagParser):
    def parse(self, template_parser, tc):
        if tc != None \
                and template_parser != None \
                and len(tc) > 2:
            start = 0
            end = 0
            pos = 0
            is_func = False

            data = []
            queue = []

            for i in range(len(tc)):
                end = i
                if tc[i].kind == TokenKind.left_parentheses:
                    if pos == 0:
                        if i > 0 and tc[i - 1].kind == TokenKind.text_data:
                            is_func = True
                    pos += 1
                elif tc[i].kind == TokenKind.right_parentheses:
                    if pos > 0:
                        pos -= 1
                    else:
                        raise Exception("syntax error near ):%s  line:%d  col:%d" % jntemplate.utils.token_concat(
                            tc) % tc[0].begin_line % tc[0].begin_column)
                    if pos == 0:
                        if not is_func:
                            queue.append(tc[start + 1: end])
                        else:
                            queue.append(tc[start: end+1])
                        data.append(None)
                        start = i + 1
                elif pos == 0 and (tc[i].kind == TokenKind.dot or tc[i].kind == TokenKind.operator):
                    if end > start:
                        queue.append(tc[start: end])
                        data.append(None)
                    start = i + 1
                    data.append(tc[i])
                if i == len(tc) - 1 and end >= start:
                    if start == 0 and end == i:
                        raise Exception("Unexpected  tag:%s line:%d col:%d" % jntemplate.utils.token_concat(
                            tc) % tc[0].begin_line % tc[0].begin_column)
                    queue.append(tc[start: end+1])
                    data.append(None)
                    start = i + 1

            if len(queue) == 1 and queue[0] == tc:
                return None

            tags = []
            i = 0
            while i < len(data):
                if data[i] == None:
                    tags.append(template_parser.read(queue[0]))
                    del queue[0]
                elif data[i].kind == TokenKind.dot:
                    if len(tags) == 0 or i == len(data) - 1 or data[i + 1] != None:
                        raise Exception("syntax error near :%s line:%d col:%d" % jntemplate.utils.token_concat(
                            tc) % tc[0].begin_line % tc[0].begin_column)
                    if isinstance(tags[-1], ReferenceTag):
                        tags[-1].add_child(template_parser.read(queue[0]))
                        del queue[0]
                    else:
                        t = ReferenceTag()
                        t.add_child(tags[-1])
                        t.add_child(template_parser.read(queue[0]))
                        del queue[0]
                        tags[-1] = t
                    i += 1
                elif data[i].kind == TokenKind.operator:
                    tags.append(TextTag())
                    tags[-1].first = data[i]
                i += 1

            if len(tags) == 1:
                return tags[0]

            if len(tags) > 1:
                t = ExpressionTag()
                for i in range(len(tags)):
                    t.add_child(tags[i])
                tags.clear()
                return t
            i += 1
        return None
