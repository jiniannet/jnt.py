# -*- coding: utf-8 -*-
__version__ = '0.1 dev'

from jntemplate.engine import configure, set_loder, \
    create_context, create, load, get_environment_variable, \
    set_environment_variable
from jntemplate.loaders import BaseLoader, FileLoader
from jntemplate.core import Template

#from jntemplate.engine import TokenKind
