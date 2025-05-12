from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie

from .categorie import Categorieën
from .macrotype import MacroType, MacroTypeDatabank

class Ingrediënt(MacroType):
    
    frozenset = frozenset(("ingrediënt_naam", "categorie_uuid"))
    
    def __init__(
        self,
        ingrediënt_naam: str,
        categorie_uuid: str,
        ) -> "Ingrediënt":
        
        self.ingrediënt_naam = ingrediënt_naam
        self.categorie_uuid = categorie_uuid
    
    @classmethod
    def nieuw(cls):
        
        categorieën = Categorieën.openen()
        categorie_uuid = categorieën.kiezen()
        
        ingrediënt_naam = invoer_validatie("naam", str, valideren = True, kleine_letters = True)
        
        return cls(
            ingrediënt_naam,
            categorie_uuid,
            )

class Ingrediënten(MacroTypeDatabank):
    
    bestandsnaam: str = "ingrediënten"
    object = Ingrediënt
    
    def opdracht(self):
        
        while True:
            
            opdracht = invoer_kiezen("opdracht ingrediënt", ["nieuw ingrediënt"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuw ingrediënt":
                
                self.nieuw()
        
        return self
    
    def nieuw(self):
        
        ingrediënt = Ingrediënt.nieuw()
        
        uuid = str(uuid4())
        self[uuid] = ingrediënt
        self.opslaan()
        
        return uuid
    
    def kiezen(self) -> str:
        
        while True:
        
            print("\nkies een ingrediënt op naam of categorie of maak een nieuwe")
            kies_optie = invoer_kiezen("optie", ["naam", "categorie", "nieuw"])
            
            if kies_optie == "naam" or kies_optie == "categorie":
                
                if kies_optie == "naam":
                    print("\ngeef een zoekterm op")
                    zoekterm = invoer_validatie("zoekterm", str, kleine_letters = True)
                    ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if zoekterm in ingrediënt.ingrediënt_naam]
                    if len(ingrediënten_mogelijk) == 0:
                        print(f">>> zoekterm \"{zoekterm}\" levert geen ingrediënten op")
                        continue
                    
                else:
                    categorieën = Categorieën.openen()
                    categorie_uuid = categorieën.kiezen()
                    ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt.categorie_uuid == categorie_uuid]
                    if len(ingrediënten_mogelijk) == 0:
                        print(f">>> geen ingrediënten onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
                        continue
                
                ingrediënt_uuid = invoer_kiezen("ingrediënt", {ingrediënt.ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items()}, stoppen = True)
                
                if not bool(ingrediënt_uuid):
                    continue
                
                print(f"ingrediënt \"{self[ingrediënt_uuid].ingrediënt_naam}\" gekozen")
                
                return ingrediënt_uuid
                        
            else:
                return self.nieuw()