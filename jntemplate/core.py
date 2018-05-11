# -*- coding: utf-8 -*-
from abc import abstractclassmethod, ABCMeta
from jntemplate.nodes import OperatorElement, TokenKind, Lexer, VariableScope
import jntemplate.evaluator
import jntemplate.runtime
import io

__all__ = ["Tag", "TextTag", "VariableTag", "ValueTag",
           "SetTag", "ReferenceTag", "NullTag", "IncludeTag",
           "FunctionTag", "ForeachTag", "ExpressionTag", "EndTag",
           "ElseifTag", "ElseTag", "IfTag", "LoadTag", "IndexTag",
           "TemplateContext", "TemplateRender", "TemplateParser", "Template"]


class Tag(metaclass=ABCMeta):
    def __init__(self):
        # child tag
        self.children = []
        # first token
        self.first = None
        # last token
        self.last = None

    def __str__(self):
        return self.string()

    @abstractclassmethod
    def execute(self, context):
        pass

    @abstractclassmethod
    def parse(self, context, output):
        pass

    @abstractclassmethod
    def string(self):
        pass

    def boolean(self, context):
        value = self.execute(context)
        return jntemplate.evaluator.calculate_boolean(value)

    def add_child(self, node):
        if (node != None):
            self.children.append(node)


class TextTag(Tag):
    def __init__(self):
        super(TextTag, self).__init__()

    def execute(self, context):
        r = self.string()
        # if context.strip_white_space and r != None:
        #     return r.rstrip()
        return r

    def string(self):
        if self.first == None:
            return None
        return self.first.string()

    def parse(self, context, output):
        if output != None:
            output.write(self.execute(context))


class BaseTag(Tag):
    def __init__(self):
        super(BaseTag, self).__init__()

    def parse(self, context, output):
        if output != None:
            result = self.execute(context)
            if result != None:
                output.write(str(result))

    def string(self):
        if self.last == None or self.first == self.last:
            return self.first.string()
        data = []
        token = self.first
        data.append(token.string())
        while(True):
            token = token.next
            if(token == None or token == self.last):
                break
            data.append(token.string())
        return "".join(data)


class SimpleTag(BaseTag):
    def __init__(self):
        super(SimpleTag, self).__init__()

    @abstractclassmethod
    def execute_for(base_value, context):
        pass


class VariableTag(SimpleTag):
    def __init__(self):
        super(VariableTag, self).__init__()
        self.name = None

    def execute_for(self, base_value, context):
        if base_value == None:
            return None
        if not hasattr(base_value, self.name):
            return None
        return getattr(base_value, self.name)

    def execute(self, context):
        return context.data.get(self.name)


class IndexTag(SimpleTag):
    def __init__(self):
        super(IndexTag, self).__init__()
        self.name = None
        self.key = None

    def execute_for(self, base_value, context):
        return self.execute_index(base_value, self.key)

    def execute(self, context):
        return self.execute_index(context.data.get(self.name), self.key)

    def execute_index(self, data, key):
        if data == None:
            raise Exception("data cannet be null.")
        return data[key]


class ValueTag(BaseTag):
    def __init__(self):
        super(ValueTag, self).__init__()
        self.value = None

    def execute(self, context):
        return self.value

    def parse(self, context, output):
        # output.write(self.string())
        if self.value != None:
            output.write(str(self.value))

    # def string(self):
    #     if self.value == None:
    #         return None
    #     return str(self.value)


class SetTag(BaseTag):
    def __init__(self):
        super(SetTag, self).__init__()
        self.value = None
        self.name = None

    def execute(self, context):
        if self.name != None:
            val = self.value.execute(context)
            if not context.data.chang_value(self.name, val):
                context.data.push(self.name, val)

    def parse(self, context, output):
        self.execute(context)


class ReferenceTag(SimpleTag):
    def __init__(self):
        super(ReferenceTag, self).__init__()

    def execute(self, context):
        if len(self.children) > 0:
            start = 1
            end = len(self.children)
            result = self.children[0].execute(context)
            while start < end:
                if result != None:
                    result = self.children[start].execute_for(result, context)
                start += 1
            return result
        return None

    def execute_for(self, base_value, context):
        if len(self.children) > 0:
            start = 0
            end = len(self.children)
            result = base_value
            while start < end:
                if result != None:
                    result = self.children[start].execute_for(start, context)
                start += 1
            return result
        return None


class NullTag(BaseTag):
    def __init__(self):
        super(NullTag, self).__init__()

    def execute(self, context):
        return None

    def boolean(self, context):
        return False

    def string(self):
        return ""


class BlockTag(BaseTag):
    def __init__(self):
        super(BlockTag, self).__init__()
        self.key = None
        self.content = None

    def execute(self, context):
        render = self._create_render(context)
        return render.render()

    def parse(self, context, output):
        render = self._create_render(context)
        render.io_render(output)

    def _create_render(self, context):
        return TemplateRender(context, self.content)


class LoadTag(BlockTag):
    def __init__(self):
        super(LoadTag, self).__init__()
        self.path = None
        # super().aa()

    def execute(self, context):
        self.load_resource(context)
        super().execute(context)

    def parse(self, context, output):
        self.load_resource(context)
        super().parse(context, output)

    def load_resource(self, context):
        if self.path != None:
            p = str(self.path.execute(context))
            text, full = jntemplate.runtime.loader.load(
                p, context.encoding, context.current_path)
            if full == None:
                self. content = ""
            else:
                self. content = text
        else:
            self. content = ""


class IncludeTag(BaseTag):
    def __init__(self):
        super(IncludeTag, self).__init__()
        self.path = None

    def execute(self, context):
        if self.path != None:
            p = str(self.path.execute(context))
            content, full = jntemplate.runtime.loader.load(
                p, context.encoding, context.current_path)
            return content
        return None


class FunctionTag(SimpleTag):
    def __init__(self):
        super(FunctionTag, self).__init__()
        self.name = None

    def _get_args(self, context):

        arr = []
        for t in self.children:
            arr.append(t.execute(context))
        return arr

    def execute_func(self, func, args):
        if(func == None):
            return None
        if args == None or len(args) == 0:
            return func()
        n = len(args)
        if n == 1:
            return func(args[0])
        if n == 2:
            return func(args[0], args[1])
        if n == 3:
            return func(args[0], args[1], args[2])
        if n == 4:
            return func(args[0], args[1], args[2], args[3])
        if n == 5:
            return func(args[0], args[1], args[2], args[3], args[4])
        if n == 6:
            return func(args[0], args[1], args[2], args[3], args[4], args[5])
        if n == 7:
            return func(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        if n == 8:
            return func(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
        if n == 9:
            return func(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
        if n == 10:
            return func(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])

        raise Exception("too many arguments.")
        # arr = []
        # for i in range(n):
        #     arr.append("args["+str(i)+"]")
        # arr[0] = "func(" + arr[0]
        # arr[n-1] = arr[n-1]+")"
        # return eval(",".join(arr))
        # Object result = context.TempData[this._name];

    def execute(self, context):
        args = self._get_args(context)
        func = context.data.get(self.name)
        return self.execute_func(func, args)

    def execute_for(self, base_value, context):
        if base_value == None or not hasattr(base_value, self.name):
            return None
        args = self._get_args(context)
        func = getattr(base_value, self.name)
        return self.execute_func(func, args)


# class ForTag(SimpleTag):
#     """ like jnt4net"s ForeachTag """

class ForeachTag(BaseTag):
    def __init__(self):
        super(ForeachTag, self).__init__()
        self.name = None
        self.source = None

    def _execute(self, value, context, output):
        if value != None:
            i = 0
            for node in value:
                ctx = context.create_child()
                ctx.data.set("foreachIndex", i)
                ctx.data.set(self.name, node)
                for tag in self.children:
                    tag.parse(ctx, output)
                i += 1

    def execute(self, context):
        with io.StringIO() as output:
            self.parse(context, output)
            result = output.getvalue()
        return result

    def parse(self, context, output):
        if self.source != None:
            self._execute(self.source.execute(context), context, output)


class ExpressionTag(BaseTag):
    def __init__(self):
        super(ExpressionTag, self).__init__()

    def execute(self, context):
        arr = []
        for tag in self.children:
            if isinstance(tag, TextTag):
                arr.append(OperatorElement(tag.first.text))
            else:
                arr.append(tag.execute(context))
        stack = jntemplate.evaluator.get_reverse_polish_notation(arr)
        return jntemplate.evaluator.calculate_reverse_polish_notation(stack)


class EndTag(BaseTag):
    def __init__(self):
        super(EndTag, self).__init__()

    def execute(self, context):
        return None

    def boolean(self, context):
        return False

    def parse(self, context, output):
        pass


class ElseifTag(BaseTag):
    def __init__(self):
        super(ElseifTag, self).__init__()
        self.test = None

    def execute(self, context):
        if len(self.children) == 1:
            return self.children[0].execute(context)
        return self.parse(context)

    def boolean(self, context):
        return self.test.boolean(context)

    def parse(self, context, output):
        with io.StringIO() as output:
            for tag in self.children:
                tag.parse(context, output)
            result = output.getvalue()
        return result


class ElseTag(ElseifTag):
    def __init__(self):
        super(ElseTag, self).__init__()

    def boolean(self, context):
        return True


class IfTag(BaseTag):
    def __init__(self):
        super(IfTag, self).__init__()

    def execute(self, context):
        for tag in self.children:
            if tag.boolean(context):
                return tag.execute(context)
        return None


class TemplateContext(object):

    def __init__(self, data=None):
        if data == None:
            data = VariableScope()
        self.data = data
        self.erros = []
        self.current_path = None
        # Common.utils.ToBoolean(Engine.GetEnvironmentVariable("ThrowErrors"));
        self.throw_errors = True
        # Common.utils.ToBoolean(Engine.GetEnvironmentVariable("StripWhiteSpace"));
        self.strip_white_space = True
        self.encoding = "utf-8"

    def get_last_error(self):
        if len(self.erros) > 0:
            return self.erros[0]
        return None

    def add_error(self, ers):
        self.erros.append(ers)

    def clear_error(self):
        self.erros.clear()

    def create_child(self):
        vs = VariableScope(self.data)
        ctx = TemplateContext(vs)
        ctx.erros = self.erros
        ctx.current_path = self.current_path
        ctx.throw_errors = self.throw_errors
        ctx.strip_white_space = self.strip_white_space
        ctx.encoding = self.encoding
        return ctx


class TemplateRender(object):
    def __init__(self, context, text):
        self.context = context
        self.document = text

    def render(self):
        with io.StringIO() as output:
            self.io_render(output)
            result = output.getvalue()
        return result

    def io_render(self, output):
        # loader
        lexer = Lexer(self.document)
        chars = lexer.parse()
        # output.write
        parser = TemplateParser(chars)
        tags = parser.parser_all()

        for t in tags:
            t.parse(self.context, output)


class TemplateParser(object):
    def __init__(self, collection):
        self.tokens = jntemplate.utils.clear_space_token(collection)
        self.tag = None
        self._index = 0
        self.reset()

    def reset(self):
        self.tag = None
        self._index = 0

    def next(self):
        if self._index < len(self.tokens):
            t = self._read()
            if t != None:
                self.tag = t
                return True
        return False

    def _is_tag_end(self, token):
        if token == None or token.kind == TokenKind.tag_end or token.kind == TokenKind.eof:
            return True
        return False

    def _is_tag_start(self, token):
        if token != None and token.kind == TokenKind.tag_start:
            return True
        return False

    def _read(self):
        if not self._is_tag_start(self.tokens[self._index]):
            t = TextTag()
            t.first = self.tokens[self._index]
            t.last = None
            self._index += 1
            return t

        t1 = self.tokens[self._index]
        t2 = self.tokens[self._index]
        tc = []
        while True:
            self._index += 1
            t2.next = self.tokens[self._index]
            t2 = t2.next
            tc.append(t2)

            if self._is_tag_end(self.tokens[self._index]):
                break
        tc.pop()
        self._index += 1

        tag = self.read(tc)

        if tag != None:
            tag.first = t1
            if len(tag.children) == 0 or tag.last == None or t2.compare(tag.last) > 0:
                tag.last = t2
        return tag

    def read(self, tc):
        if tc == None or len(tc) == 0:
            return None
        return jntemplate.runtime.resolve(self, tc)

    def parser_all(self):
        tags = []
        while self.next():
            tags.append(self.tag)
        return tags


class Template(TemplateRender):
    def __init__(self, text=None, context=None):
        if context == None:
            context = TemplateContext()
        super(Template, self).__init__(context, text)

    def set(self, key, value):
        self.context.data.push(key, value)

    def string(self):
        return self.render()
