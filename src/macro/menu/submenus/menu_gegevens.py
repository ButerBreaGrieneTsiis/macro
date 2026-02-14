"""macro.menu.submenus.menu_gegevens"""
from grienetsiis.opdrachtprompt import Menu

from macro.categorie import Hoofdcategorie, Categorie
from macro.product import Ingrediënt, Merk
from macro.menu import hoofdmenu


menu_gegevens = Menu("MENU GEGEVENS BEWERKEN", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_gegevens, "bewerken gegevens")

Hoofdcategorie.toevoegen_menu(menu_gegevens)
Categorie.toevoegen_menu(menu_gegevens)
Ingrediënt.toevoegen_menu(menu_gegevens)
Merk.toevoegen_menu(menu_gegevens)