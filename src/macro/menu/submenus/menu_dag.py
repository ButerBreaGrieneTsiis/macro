"""macro.menu.submenus.menu_dag"""
from grienetsiis.opdrachtprompt import Menu

from macro.menu import hoofdmenu


menu_dag = Menu("MENU DAG INVULLEN", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_dag, "invullen dag")