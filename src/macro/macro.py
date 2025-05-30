from grienetsiis import invoer_kiezen, STOP

from .categorie import Categorieën, Hoofdcategorieën
from .dag import Dag
from .ingredient import Ingrediënten
from .product import Merken, Producten


def uitvoeren():
    
    while True:
        
        opdracht = invoer_kiezen(
            "HOOFDMENU",
            ["dag invullen", "gegevens bewerken"],
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
                    ["vandaag"],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = "HOOFDMENU",
                    )
                
                if opdracht_dag is STOP:
                    break
                
                elif opdracht_dag == "vandaag":
                    
                    dag = Dag.openen("vandaag")
                    dag.opdracht(terug_naar)
                    dag.opslaan()
        
        elif opdracht == "gegevens bewerken":
            
            terug_naar = "MENU GEGEVENS"
            
            while True:
                
                opdracht_gegevens = invoer_kiezen(
                    "MENU GEGEVENS",
                    ["hoofdcategorieën",
                    "categorieën", "ingrediënten", "producten", "merken"],
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
    
    print("tot ziens")