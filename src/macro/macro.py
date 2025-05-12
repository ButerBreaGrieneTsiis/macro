from grienetsiis import invoer_kiezen

from .categorie import Categorieën, Hoofdcategorieën
from .ingredient import Ingrediënten
from .product import Producten


def uitvoeren():
    
    while True:
        
        opdracht = invoer_kiezen("opdracht hoofdmenu", ["gegevens"], stoppen = True)
        if not bool(opdracht):
            break
        
        elif opdracht == "gegevens":
            
            while True:
            
                opdracht_gegevens = invoer_kiezen("opdracht gegevens", ["hoofdcategorieën", "categorieën", "ingrediënten", "producten"], stoppen = True)
                if not bool(opdracht_gegevens):
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