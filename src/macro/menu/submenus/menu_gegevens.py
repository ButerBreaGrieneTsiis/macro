"""macro.menu.submenus.menu_gegevens"""
from grienetsiis.opdrachtprompt import Menu

from macro.gerecht import  HoofdcategorieGerecht, CategorieGerecht
from macro.product import Hoofdcategorie, Categorie, Ingrediënt, Merk, Product
from macro.menu import hoofdmenu


menu_gegevens = Menu("MENU GEGEVENS BEWERKEN", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_gegevens, "bewerken gegevens")

menu_product = Menu("MENU GEGEVENS PRODUCT", menu_gegevens, True)
menu_ingrediënt = Menu("MENU GEGEVENS INGREDIËNT", menu_gegevens, True)
# gerecht
menu_merk = Menu("MENU GEGEVENS MERK", menu_gegevens, True)
menu_hoofdcategorie = Menu("MENU GEGEVENS HOOFDCATEGORIE PRODUCT", menu_gegevens, True)
menu_categorie = Menu("MENU GEGEVENS CATEGORIE PRODUCT", menu_gegevens, True)
menu_hoofdcategorie_gerecht = Menu("MENU GEGEVENS HOOFDCATEGORIE GERECHT", menu_gegevens, True)
menu_categorie_gerecht = Menu("MENU GEGEVENS CATEGORIE GERECHT", menu_gegevens, True)

menu_gegevens.toevoegen_optie(menu_product, "menu product")
menu_gegevens.toevoegen_optie(menu_categorie, "menu categorie")
menu_gegevens.toevoegen_optie(menu_ingrediënt, "menu ingrediënt")
# gerecht
menu_gegevens.toevoegen_optie(menu_merk, "menu merk")
menu_gegevens.toevoegen_optie(menu_hoofdcategorie, "menu hoofdcategorie")
menu_gegevens.toevoegen_optie(menu_hoofdcategorie_gerecht, "menu hoofdcategorie gerecht")
menu_gegevens.toevoegen_optie(menu_categorie_gerecht, "menu categorie gerecht")

menu_product.toevoegen_optie(Product.nieuw, "nieuw product")
menu_product.toevoegen_optie(Product.bewerken, "bewerken product")
menu_product.toevoegen_optie(Product.verwijderen, "verwijderen product")
menu_product.toevoegen_optie(Product.weergeven, "weergeven product")

menu_ingrediënt.toevoegen_optie(Ingrediënt.nieuw, "nieuwe ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.bewerken, "bewerken ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.verwijderen, "verwijderen ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.weergeven, "weergeven ingrediënt")

menu_merk.toevoegen_optie(Merk.nieuw, "nieuwe merk")
menu_merk.toevoegen_optie(Merk.bewerken, "bewerken merk")
menu_merk.toevoegen_optie(Merk.verwijderen, "verwijderen merk")
menu_merk.toevoegen_optie(Merk.weergeven, "weergeven merk")

menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.nieuw, "nieuwe hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.bewerken, "bewerken hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.verwijderen, "verwijderen hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.weergeven, "weergeven hoofdcategorie")

menu_categorie.toevoegen_optie(Categorie.nieuw, "nieuwe categorie")
menu_categorie.toevoegen_optie(Categorie.bewerken, "bewerken categorie")
menu_categorie.toevoegen_optie(Categorie.verwijderen, "verwijderen categorie")
menu_categorie.toevoegen_optie(Categorie.weergeven, "weergeven categorie")

menu_hoofdcategorie_gerecht.toevoegen_optie(HoofdcategorieGerecht.nieuw, "nieuwe hoofdcategorie gerecht")
menu_hoofdcategorie_gerecht.toevoegen_optie(HoofdcategorieGerecht.bewerken, "bewerken hoofdcategorie gerecht")
menu_hoofdcategorie_gerecht.toevoegen_optie(HoofdcategorieGerecht.verwijderen, "verwijderen hoofdcategorie gerecht")
menu_hoofdcategorie_gerecht.toevoegen_optie(HoofdcategorieGerecht.weergeven, "weergeven hoofdcategorie gerecht")

menu_categorie_gerecht.toevoegen_optie(CategorieGerecht.nieuw, "nieuwe categorie gerecht")
menu_categorie_gerecht.toevoegen_optie(CategorieGerecht.bewerken, "bewerken categorie gerecht")
menu_categorie_gerecht.toevoegen_optie(CategorieGerecht.verwijderen, "verwijderen categorie gerecht")
menu_categorie_gerecht.toevoegen_optie(CategorieGerecht.weergeven, "weergeven categorie gerecht")