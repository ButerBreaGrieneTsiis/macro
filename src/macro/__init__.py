"""
macro
"""
from ._version import __version__
from .register import registreren


registreren()


__all__ = [
    __version__,
    ]