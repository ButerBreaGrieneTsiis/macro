"""macro.menu.hoofdmenu"""
from grienetsiis.opdrachtprompt import Menu
from grienetsiis.register import Register

from macro.utils import welkomstscherm


hoofdmenu = Menu(
    naam = "HOOFDMENU",
    functie_start = welkomstscherm,
    functie_eind = Register.opslaan,
    )