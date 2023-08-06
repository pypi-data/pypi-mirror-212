__all__ = ['BaseHTML', 'NameBaseHTML']

import re

EMPTY = ['area', 'base', 'br', 'col', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

class BaseHTML:	
    def __init__(self, tag: str, **kwargs):
        self._tag: str = tag
        before = kwargs.pop('before', list())
        self._before: list['BaseHTML', str] = before if isinstance(before, list) else [before]
        inner = kwargs.pop('inner', list())
        self._inner: list['BaseHTML', str] = inner if isinstance(inner, list) else [inner]
        after = kwargs.pop('after', list())
        self._after: list['BaseHTML', str] = after if isinstance(after, list) else [after]
        klass = kwargs.pop('klass', list())
        self._klass: list = klass if isinstance(klass, list) else [klass]
        style = kwargs.pop('style', list())
        self._style: list = style if isinstance(style, list) else [style]
        config = kwargs.pop('config', list())
        self._config: list = config if isinstance(config, list) else [config]
        self._kwargs: dict = kwargs
        
    def __str__(self):
        if self.tag in EMPTY:
            return f'{self.before}<{self.tag} {self.attributes}>{self.after}'
        return f'{self.before}<{self.tag} {self.attributes}>{self.inner}</{self.tag}>{self.after}'
    
    @property
    def tag(self):
        return self._tag
        
    @property
    def inner(self):
        return ' '.join([str(i) for i in self._inner if all([i is not None, i != ''])])
        
    @property
    def before(self):
        return ' '.join([str(i) for i in self._before if all([i is not None, i != ''])])
        
    @property
    def after(self):
        return ' '.join([str(i) for i in self._after if all([i is not None, i != ''])])
        
    @property
    def klass(self):
        result = ' '.join([str(i) for i in self._klass if all([i is not None, i != ''])])
        return f'class="{result}"' if result else ''
        
    @property
    def style(self):
        result = '; '.join([str(i) for i in self._style if all([i is not None, i != ''])])
        return f'style="{result}"' if result else ''
        
    @property
    def config(self):
        return ' '.join([str(i) for i in self._config if all([i is not None, i != ''])])
        
    @property
    def attributes(self):
        return re.sub(r'\s+', ' ', f'{self.kwargs} {self.klass} {self.config} {self.style}').strip()
        
    @property
    def kwargs(self):
        return ' '.join([f'{k.replace("_","-")}="{v}"' for k, v in self._kwargs.items() if all([v is not None, v != ''])])

    def addinner(self, *args):
        self._inner.extend(args)
        return self
        
    def addbefore(self, *args):
        self._before.extend(args)
        return self
        
    def addafter(self, *args):
        self._after.extend(args)
        return self
        
    def addklass(self, *args):
        self._klass.extend(args)
        return self
        
    def addstyle(self, *args):
        self._style.extend(args)
        return self
        
    def addconfig(self, *args):
        self._config.extend(args)
        return self
        
    def addkwargs(self, **kwargs):
        self._kwargs.update(kwargs)
        return self


class NameBaseHTML(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__(type(self).__name__.lower(), **kwargs)

