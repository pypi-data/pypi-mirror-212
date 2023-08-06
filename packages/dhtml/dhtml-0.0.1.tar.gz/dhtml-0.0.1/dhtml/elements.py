__all__ = ['Anchor', 'Div', 'Link', 'Meta', 'Header', 'Footer', 'Main', 'Nav', 'Ul', 'Ol', 'Li',
           'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Script', 'Title']

from .base import *


class Anchor(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__('a', **kwargs)
        

class Div(NameBaseHTML):
    pass


class Link(NameBaseHTML):
    pass


class Meta(NameBaseHTML):
    pass


class Main(NameBaseHTML):
    pass


class Title(NameBaseHTML):
    def __init__(self, inner: str):
        super().__init__(inner=[inner])
        
    def __str__(self):
        return f'<title>{self.inner}</title>'


class Footer(NameBaseHTML):
    pass


class Nav(NameBaseHTML):
    pass


class Ul(NameBaseHTML):
    pass


class Ol(NameBaseHTML):
    pass


class Li(NameBaseHTML):
    pass


class H1(NameBaseHTML):
    pass


class H2(NameBaseHTML):
    pass


class H3(NameBaseHTML):
    pass


class H4(NameBaseHTML):
    pass


class H5(NameBaseHTML):
    pass


class H6(NameBaseHTML):
    pass


class Header(NameBaseHTML):
    pass


class Script(NameBaseHTML):
    pass


