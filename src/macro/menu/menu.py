"""macro.menu.menu"""
from grienetsiis.opdrachtprompt import Menu
from grienetsiis.register import Register

from macro.categorie import Hoofdcategorie


Register.openen()

# HOOFDMENU
hoofdmenu = Menu("HOOFDMENU")


# MENU INVULLEN
menu_invullen = Menu("MENU DAG INVULLEN", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_invullen, "invullen dag")

# MENU GEGEVENS
menu_gegevens = Menu("MENU GEGEVENS BEWERKEN", hoofdmenu)
hoofdmenu.toevoegen_optie(menu_gegevens, "bewerken gegevens")

# MENU GEGEVENS - HOOFDCATEGORIE
menu_hoofdcategorie = Menu("MENU GEGEVENS HOOFDCATEGORIE", menu_gegevens)
menu_gegevens.toevoegen_optie(menu_hoofdcategorie, "bewerken hoofdcategorie")

menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.nieuw, "nieuwe hoofdcategorie")
# menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.bewerken, "bewerken hoofdcategorie")
# menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.weergeef, "weergeven hoofdcategorie")

if __name__ == "__main__":
    hoofdmenu()