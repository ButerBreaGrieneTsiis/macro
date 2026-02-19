"""macro.menu.submenus.menu_dag"""
from grienetsiis.opdrachtprompt import Menu

from macro.dag import Dag
from macro.menu import hoofdmenu


menu_dag = Menu(Dag.titel, hoofdmenu)
hoofdmenu.toevoegen_optie(menu_dag, "invullen dag")

menu_dag.toevoegen_optie(Dag.toevoegen_product, "toevoegen product")
# menu_dag.toevoegen_optie(Dag.toevoegen_gerecht, "toevoegen gerecht")
# menu_dag.toevoegen_optie(Dag.aanpassen_product, "aanpassen hoeveelheid product")
# menu_dag.toevoegen_optie(Dag.aanpassen_gerecht, "aanpassen porties gerecht")
menu_dag.toevoegen_optie(Dag.weergeven_product, "weergeven product")
# menu_dag.toevoegen_optie(Dag.weergeven_gerecht, "weergeven gerecht")
menu_dag.toevoegen_optie(Dag.weergeven_voedingswaarde, "weergeven voedingswaarde")
# menu_dag.toevoegen_optie(Dag.verwijderen_product, "verwijderen product")
# menu_dag.toevoegen_optie(Dag.verwijderen_gerecht, "verwijderen gerecht")
# menu_dag.toevoegen_optie(Dag.kopiëren, "kopiëren producten van andere dag")
menu_dag.toevoegen_optie(Dag.veranderen_dag, "veranderen van dag")