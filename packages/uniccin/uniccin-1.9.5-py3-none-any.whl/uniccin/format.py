# SPDX-License-Identifier: MIT
"""Formatting."""

from collections.abc import Iterable

import uniccin.uc

class UniFormat:
    """Allows a character to be passed to str.format_map()."""

    alias = {
        'id': 'identifier',
        'utf-8': 'utf8',
        'utf-16': 'utf16',
        'v': 'ordinal',
        'x': 'hexadecimal',
    }

    def __init__(self, c: str, eol: str = '\n') -> None:
        self.c = c
        self.v = ord(c)
        self.eol = eol

    def __getitem__(self, key: str) -> str:
        k = key.lower()
        if (a := self.alias.get(k)):
            k = a
        if k.startswith('u') and k[1 :].isdigit():
            return uniccin.uc.u(self.c, digits=int(k[1 :]))
        if k == 'utf8':
            r = uniccin.uc.utf8(self.c)
            return repr(r) if key.isupper() else list_to_hex(r, 2)
        if k == 'utf16':
            r = uniccin.uc.utf16(self.c)
            return repr(r) if key.isupper() else list_to_hex(r, 4)
        if k in ('nfc', 'nfkc', 'nfd', 'nfkd'):
            v = uniccin.uc.normalize(self.c, k)
            return v if key.isupper() else ', '.join(
                uniccin.uc.name(c, '?') for c in v)
        if key == 'eol':
            return self.eol
        if k in uniccin.uc.PROPERTIES:
            return str(uniccin.uc.PROPERTIES[k](self.c, ''))
        raise KeyError(key)

def list_to_hex(i: Iterable[int], w: int = 2) -> str:
    """Return a string of hexadecimal numbers from a list of integers."""
    return ' '.join(f'{x:0{w}X}' for x in i)
