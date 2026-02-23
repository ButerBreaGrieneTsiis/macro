"""macro.menu.submenus.menu_dag"""
from grienetsiis.opdrachtprompt import Menu

from macro.dag import Dag
from macro.menu import hoofdmenu


menu_dag = Menu(Dag.titel, hoofdmenu)
hoofdmenu.toevoegen_optie(menu_dag, "dag invullen")

menu_dag_product = Menu(lambda: Dag.titel() + " PRODUCTEN", menu_dag)
menu_dag.toevoegen_optie(menu_dag_product, "producten invullen")

menu_dag_product.toevoegen_optie(Dag.toevoegen_product, "toevoegen product")
menu_dag_product.toevoegen_optie(Dag.aanpassen_product, "aanpassen hoeveelheid product")
menu_dag_product.toevoegen_optie(Dag.weergeven_product, "weergeven product")
menu_dag_product.toevoegen_optie(Dag.verwijderen_product, "verwijderen product")
menu_dag_product.toevoegen_optie(Dag.kopiëren_product, "kopiëren producten van andere dag")

menu_dag_gerecht = Menu(lambda: Dag.titel() + " GERECHTEN", menu_dag)
menu_dag.toevoegen_optie(menu_dag_gerecht, "gerechten invullen")

menu_dag_gerecht.toevoegen_optie(Dag.toevoegen_gerecht, "toevoegen gerecht")
# menu_dag_gerecht.toevoegen_optie(Dag.aanpassen_gerecht, "aanpassen porties gerecht")
# menu_dag_gerecht.toevoegen_optie(Dag.weergeven_gerecht, "weergeven gerecht")
menu_dag_gerecht.toevoegen_optie(Dag.verwijderen_gerecht, "verwijderen gerecht")

menu_dag.toevoegen_optie(Dag.weergeven_voedingswaarde, "voedingswaarde weergeven")
menu_dag.toevoegen_optie(Dag.veranderen_dag, "dag veranderen")