from grienetsiis import invoer_kiezen, STOP

from .categorie import Hoofdcategorieën, Categorieën, HoofdcategorieënGerecht, CategorieënGerecht
from .dag import Dag
from .gerecht import Gerechten
from .ingredient import Ingrediënten
from .product import Merken, Producten


def uitvoeren():
    
    while True:
        
        opdracht = invoer_kiezen(
            "HOOFDMENU",
            [
                "dag invullen",
                "gegevens bewerken",
                ],
            stoppen = True,
            kies_een = False,
            terug_naar = "AFSLUITEN",
            )
        
        if opdracht is STOP:
            break
        
        elif opdracht == "dag invullen":
            
            terug_naar = "MENU DAG"
            
            while True:
                
                opdracht_dag = invoer_kiezen(
                    "MENU DAG",
                    [
                        "vandaag",
                        "gisteren",
                        "eergisteren",
                        "morgen",
                        "overmorgen",
                        "aangepast",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = "HOOFDMENU",
                    )
                
                if opdracht_dag is STOP:
                    break
                
                dag = Dag.openen(opdracht_dag)
                dag.opdracht(terug_naar)
                dag.opslaan()
        
        elif opdracht == "gegevens bewerken":
            
            terug_naar = "MENU GEGEVENS"
            
            while True:
                
                opdracht_gegevens = invoer_kiezen(
                    "MENU GEGEVENS",
                    [
                        "hoofdcategorieën",
                        "categorieën",
                        "ingrediënten",
                        "producten",
                        "merken",
                        "hoofdcategorieën gerechten",
                        "categorieën gerechten",
                        "gerechten",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = "HOOFDMENU",
                    )
                
                if opdracht_gegevens is STOP:
                    break
                
                elif opdracht_gegevens == "hoofdcategorieën":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorieën.opdracht(terug_naar)
                    hoofdcategorieën.opslaan()
                
                elif opdracht_gegevens == "categorieën":
                    
                    categorieën = Categorieën.openen()
                    categorieën.opdracht(terug_naar)
                    categorieën.opslaan()
                
                elif opdracht_gegevens == "ingrediënten":
                    
                    ingrediënten = Ingrediënten.openen()
                    ingrediënten.opdracht(terug_naar)
                    ingrediënten.opslaan()
                
                elif opdracht_gegevens == "producten":
                    
                    producten = Producten.openen()
                    producten.opdracht(terug_naar)
                    producten.opslaan()
                
                elif opdracht_gegevens == "merken":
                    
                    merken = Merken.openen()
                    merken.opdracht(terug_naar)
                    merken.opslaan()
                
                elif opdracht_gegevens == "hoofdcategorieën gerechten":
                    
                    hoofdcategorieën_gerecht = HoofdcategorieënGerecht.openen()
                    hoofdcategorieën_gerecht.opdracht(terug_naar)
                    hoofdcategorieën_gerecht.opslaan()
                
                elif opdracht_gegevens == "categorieën gerechten":
                    
                    categorieën_gerecht = CategorieënGerecht.openen()
                    categorieën_gerecht.opdracht(terug_naar)
                    categorieën_gerecht.opslaan()
                
                elif opdracht_gegevens == "gerechten":
                    
                    gerechten = Gerechten.openen()
                    gerechten.opdracht(terug_naar)
                    gerechten.opslaan()
    
    print("tot ziens")