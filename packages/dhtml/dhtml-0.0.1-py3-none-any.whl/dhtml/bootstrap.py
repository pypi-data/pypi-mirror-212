from __future__ import annotations

__all__ = ['NavBar', 'UlNav', 'NavItem', 'NavLink']

from typing import Union
from .base import *
from .elements import *


class NavBar(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__('nav', **kwargs)
        self.addklass('navbar')
        
        
class UlNav(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__('ul', **kwargs)
        self.addklass('nav')
        
    @classmethod
    def from_list(cls, items: list[Union[dict, NavLink]]):
        links = list()
        for item in items:
            if isinstance(item, NavLink):
                links.append(item)
            elif isinstance(item, dict):
                links.append(NavLink(**item))
        return cls(inner=[NavItem(inner=i) for i in links])
        
        
class NavItem(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__('li', **kwargs)
        self.addklass('nav-item')
        
        
class NavLink(BaseHTML):
    def __init__(self, **kwargs):
        super().__init__('a', **kwargs)
        self.addklass('nav-link')
        