"""macro main entry point"""
from grienetsiis.register import Register

from macro.menu import hoofdmenu


Register.openen()
hoofdmenu()
Register().opslaan()