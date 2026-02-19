"""macro main entry point"""
from grienetsiis.register import Register

from macro.menu import hoofdmenu
from macro.utils import welkomstscherm

Register.openen()
welkomstscherm()
hoofdmenu()
Register().opslaan()