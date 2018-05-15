# -*- coding: utf-8 -*-
# cache
# tag_resolver
# resource_directories
from jntemplate.nodes import Token, FlagMode, TokenKind, VariableScope, Lexer
from jntemplate.core import TextTag, TemplateContext, Template
from jntemplate.loaders import FileLoader, BaseLoader
import jntemplate.defaults
from jntemplate.parsers import BooleanParser, NumberParser, EleseParser,\
    EndParser, VariableParser, StringParser, ForeachParser, VariableParser,\
    SetParser, IfParser, ElseifParser, LoadParser, IncludeParser, FunctionParser, \
    ComplexParser, VariableParser, IndexParser
import jntemplate.runtime

__all__ = ["configure", "set_loder", "create_context",
           "create", "load", "get_environment_variable",
           "set_environment_variable"]

def configure(**conf):
    _init_default_resolver()
    jntemplate.runtime.environment.update(jntemplate.defaults.engine_conf) 
    if "data" in conf and isinstance(conf["data"], VariableScope):
        jntemplate.runtime.data = conf["data"]
        del conf["data"]
    if "loader" in conf and isinstance(conf["loader"], BaseLoader):
        jntemplate.runtime.loader = conf["loader"]
        del conf["loader"]

    jntemplate.runtime.environment.update(conf)
    if jntemplate.runtime.loader == None:
        jntemplate.runtime.loader = FileLoader()


def set_loder(loader):
    jntemplate.runtime.loader = loader


def create_context():
    if jntemplate.runtime.data == None:
        ctx = TemplateContext()
    ctx = TemplateContext(jntemplate.runtime.data)
    encoding = get_environment_variable("encoding")
    if encoding != None and encoding != "":
        ctx.encoding = encoding
    return ctx


def create(text):
    return Template(text, create_context())


def load(path, ctx=None):
    if ctx == None:
        ctx = create_context()
    html, full = jntemplate.runtime.loader.load(path, ctx.encoding)
    if full != None:
        ctx.current_path = jntemplate.runtime.loader.get_directory(full)
    else:
        raise Exception("Cannot find \"%s\"." % path)
    return Template(html, ctx)


def get_environment_variable(name):
    return jntemplate.runtime._get_environment_variable(name)


def set_environment_variable(name,  value): 
    jntemplate.runtime._set_environment_variable(name,  value)


def _init_default_resolver():
    jntemplate.runtime.resolver.clear()
    jntemplate.runtime.resolver.append(BooleanParser())
    jntemplate.runtime.resolver.append(NumberParser())
    jntemplate.runtime.resolver.append(EleseParser())
    jntemplate.runtime.resolver.append(EndParser())
    jntemplate.runtime.resolver.append(VariableParser())
    jntemplate.runtime.resolver.append(IndexParser())
    jntemplate.runtime.resolver.append(StringParser())
    jntemplate.runtime.resolver.append(ForeachParser())
    # resolver.append(VariableParser())
    jntemplate.runtime.resolver.append(SetParser())
    jntemplate.runtime.resolver.append(IfParser())
    jntemplate.runtime.resolver.append(ElseifParser())
    # resolver.append(LoadParser())
    jntemplate.runtime.resolver.append(IncludeParser())
    jntemplate.runtime.resolver.append(FunctionParser())
    jntemplate.runtime.resolver.append(ComplexParser())
    # resolver.append(VariableParser())
