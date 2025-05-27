from grienetsiis import invoer_kiezen, STOP

from .categorie import Categorieën, Hoofdcategorieën
from .dag import Dag
from .ingredient import Ingrediënten
from .product import Merken, Producten


def uitvoeren():
    
    while True:
        
        opdracht = invoer_kiezen("opdracht hoofdmenu", ["invullen dag", "gegevens bewerken"], stoppen = True)
        
        if opdracht is STOP:
            break
        
        elif opdracht == "invullen dag":
            
            while True:
                
                opdracht_dag = invoer_kiezen("invullen dag", ["vandaag"], stoppen = True)
                
                if opdracht_dag is STOP:
                    break
                
                elif opdracht_dag == "vandaag":
                    
                    dag = Dag.openen("vandaag")
                    dag.opdracht()
                    dag.opslaan()
        
        elif opdracht == "gegevens bewerken":
            
            while True:
                
                opdracht_gegevens = invoer_kiezen("opdracht gegevens", ["hoofdcategorieën", "categorieën", "ingrediënten", "producten", "merken"], stoppen = True)
                
                if opdracht_gegevens is STOP:
                    break
                
                elif opdracht_gegevens == "hoofdcategorieën":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorieën.opdracht()
                    hoofdcategorieën.opslaan()
                
                elif opdracht_gegevens == "categorieën":
                    
                    categorieën = Categorieën.openen()
                    categorieën.opdracht()
                    categorieën.opslaan()
                
                elif opdracht_gegevens == "ingrediënten":
                    
                    ingrediënten = Ingrediënten.openen()
                    ingrediënten.opdracht()
                    ingrediënten.opslaan()
                
                elif opdracht_gegevens == "producten":
                    
                    producten = Producten.openen()
                    producten.opdracht()
                    producten.opslaan()
                
                elif opdracht_gegevens == "merken":
                    
                    merken = Merken.openen()
                    merken.opdracht()
                    merken.opslaan()
    
    print("tot ziens")