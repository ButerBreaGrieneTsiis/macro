"""macro.menu.submenus.menu_product"""
from grienetsiis.opdrachtprompt import Menu

from macro.product import Hoofdcategorie, Categorie, Ingrediënt, Merk, Product
from macro.menu import hoofdmenu


menu_gegevens = Menu("MENU GEGEVENS PRODUCT", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_gegevens, "gegevens product")

menu_product = Menu("MENU PRODUCT", menu_gegevens, True)
menu_ingrediënt = Menu("MENU INGREDIËNT", menu_gegevens, True)
menu_merk = Menu("MENU MERK", menu_gegevens, True)
menu_categorie = Menu("MENU CATEGORIE", menu_gegevens, True)
menu_hoofdcategorie = Menu("MENU HOOFDCATEGORIE", menu_gegevens, True)

menu_gegevens.toevoegen_optie(menu_product, "producten")
menu_gegevens.toevoegen_optie(menu_ingrediënt, "ingrediënten")
menu_gegevens.toevoegen_optie(menu_merk, "merken")
menu_gegevens.toevoegen_optie(menu_categorie, "categorieën")
menu_gegevens.toevoegen_optie(menu_hoofdcategorie, "hoofdcategorieën")

menu_product.toevoegen_optie(Product.nieuw, "nieuw product")
menu_product.toevoegen_optie(Product.bewerken, "bewerken product")
menu_product.toevoegen_optie(Product.inspecteren, "inspecteren product")
menu_product.toevoegen_optie(Product.weergeven, "weergeven product")
menu_product.toevoegen_optie(Product.verwijderen, "verwijderen product")

menu_ingrediënt.toevoegen_optie(Ingrediënt.nieuw, "nieuwe ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.bewerken, "bewerken ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.inspecteren, "inspecteren ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.weergeven, "weergeven ingrediënt")
menu_ingrediënt.toevoegen_optie(Ingrediënt.verwijderen, "verwijderen ingrediënt")

menu_merk.toevoegen_optie(Merk.nieuw, "nieuwe merk")
menu_merk.toevoegen_optie(Merk.bewerken, "bewerken merk")
menu_merk.toevoegen_optie(Merk.inspecteren, "inspecteren merk")
menu_merk.toevoegen_optie(Merk.weergeven, "weergeven merk")
menu_merk.toevoegen_optie(Merk.verwijderen, "verwijderen merk")

menu_categorie.toevoegen_optie(Categorie.nieuw, "nieuwe categorie")
menu_categorie.toevoegen_optie(Categorie.bewerken, "bewerken categorie")
menu_categorie.toevoegen_optie(Categorie.inspecteren, "inspecteren categorie")
menu_categorie.toevoegen_optie(Categorie.weergeven, "weergeven categorieën")
menu_categorie.toevoegen_optie(Categorie.verwijderen, "verwijderen categorie")

menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.nieuw, "nieuwe hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.bewerken, "bewerken hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.inspecteren, "inspecteren hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.weergeven, "weergeven hoofdcategorie")
menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.verwijderen, "verwijderen hoofdcategorie")