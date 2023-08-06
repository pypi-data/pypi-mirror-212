
__all__ = ['HTML', 'Head', 'Body', 'Style']

from typing import Union
from .base import *
from .elements import *


class Style(NameBaseHTML):
    
    def __str__(self):
        return "\t\t<style>\n{}\t\t</style>".format(self.inner)
    
    @property
    def attributes(self):
        return ''
    
    @property
    def inner(self):
        return " ".join(["\t\t\t{}\n".format(i) for i in self._inner if not all([i is None, i != ""])])


class Head(BaseHTML):
    def __init__(self, title: str, inner: list[Union[Meta, Link, Script, Style]]):
        super().__init__('head', inner=[Title(title), *inner])
        
    @property
    def attributes(self):
        return ''
        
    @property
    def inner(self):
        return ''.join(["\n\t\t{}".format(i) for i in self._inner]) + '\n\t'

class Body(NameBaseHTML):
    pass


class HTML(BaseHTML):
    def __init__(self, head: Head, body: Body, lang: str = 'pt-BR'):
        super().__init__('html', inner=[head, body], lang=lang)
        
    @property
    def before(self):
        return '<!doctype html>\n'
    
    @property
    def inner(self):
        return ''.join(["\n\t{}".format(i) for i in self._inner]) + '\n'
