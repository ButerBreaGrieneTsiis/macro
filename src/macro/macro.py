from grienetsiis import open_json, opslaan_json, invoer_kiezen

from .categorie import Categorieën, Hoofdcategorieën


class Databank:
    
    def __init__(
        self,
        categorieën: Categorieën,
        hoofdcategorieën: Hoofdcategorieën,
        ) -> "Databank":
        
        self.categorieën        =   categorieën
        self.hoofdcategorieën   =   hoofdcategorieën
    
    @classmethod
    def openen(cls) -> "Databank":
        
        return cls(
            Categorieën.openen(),
            Hoofdcategorieën.openen(),
            )
    
    def opslaan(self) -> None:
        
        self.categorieën.opslaan()
        self.hoofdcategorieën.opslaan()

def uitvoeren():
    
    databank = Databank.openen()
    
    while True:
        
        opdracht = invoer_kiezen("opdracht", ["gegevens"], stoppen = True)
        if not bool(opdracht):
            break
        
        elif opdracht == "gegevens":
            
            while True:
            
                opdracht_gegevens = invoer_kiezen("opdracht", ["hoofdcategorieën", "categorieën"], stoppen = True)
                if not bool(opdracht_gegevens):
                    break
                
                elif opdracht_gegevens == "hoofdcategorieën":
                    databank.hoofdcategorieën.opdracht()
                
                elif opdracht_gegevens == "categorieën":
                    databank.categorieën.opdracht(databank.hoofdcategorieën)
            
    
    databank.opslaan()