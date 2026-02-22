"""macro.menu.submenus.menu_gerecht"""
from grienetsiis.opdrachtprompt import Menu

from macro.gerecht import  HoofdcategorieGerecht, CategorieGerecht, Gerecht
from macro.menu import hoofdmenu


menu_gegevens = Menu("MENU GEGEVENS GERECHT", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_gegevens, "gegevens gerecht")

menu_gerecht = Menu("MENU GERECHT", menu_gegevens, True)
menu_categorie = Menu("MENU CATEGORIE", menu_gegevens, True)
menu_hoofdcategorie = Menu("MENU HOOFDCATEGORIE", menu_gegevens, True)

menu_gegevens.toevoegen_optie(menu_gerecht, "gerechten")
menu_gegevens.toevoegen_optie(menu_categorie, "categorieën")
menu_gegevens.toevoegen_optie(menu_hoofdcategorie, "hoofdcategorieën")

menu_gerecht.toevoegen_optie(Gerecht.nieuw, "nieuw gerecht")
menu_gerecht.toevoegen_optie(Gerecht.bewerken, "bewerken gerecht")
menu_gerecht.toevoegen_optie(Gerecht.inspecteren, "inspecteren gerecht")
menu_gerecht.toevoegen_optie(Gerecht.weergeven, "weergeven gerecht")
menu_gerecht.toevoegen_optie(Gerecht.verwijderen, "verwijderen gerecht")

menu_categorie.toevoegen_optie(CategorieGerecht.nieuw, "nieuwe categorie")
menu_categorie.toevoegen_optie(CategorieGerecht.bewerken, "bewerken categorie")
menu_categorie.toevoegen_optie(CategorieGerecht.inspecteren, "inspecteren categorie")
menu_categorie.toevoegen_optie(CategorieGerecht.weergeven, "weergeven categorie")
menu_categorie.toevoegen_optie(CategorieGerecht.verwijderen, "verwijderen categorie")

menu_hoofdcategorie.toevoegen_optie(HoofdcategorieGerecht.nieuw, "nieuwe hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(HoofdcategorieGerecht.bewerken, "bewerken hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(HoofdcategorieGerecht.inspecteren, "inspecteren hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(HoofdcategorieGerecht.weergeven, "weergeven hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(HoofdcategorieGerecht.verwijderen, "verwijderen hoofdcategorie")