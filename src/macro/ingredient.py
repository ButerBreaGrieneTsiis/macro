from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer

from .categorie import Categorie, Categorieën, Hoofdcategorie
from .macrotype import MacroType, MacroTypeDatabank


class Ingrediënt(MacroType):
    
    velden = frozenset(("ingrediënt_naam", "categorie_uuid",))
    
    def __init__(
        self,
        ingrediënt_naam: str,
        categorie_uuid: str,
        ) -> "Ingrediënt":
        
        self.ingrediënt_naam = ingrediënt_naam
        self.categorie_uuid = categorie_uuid
    
    def __repr__(self) -> "str":
        return f"Ingrediënt {self.ingrediënt_naam}"
    
    @classmethod
    def nieuw(cls):
        
        categorieën = Categorieën.openen()
        categorie_uuid = categorieën.kiezen()
        print(f"\ninvullen gegevens nieuw ingrediënt onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
        ingrediënt_naam = invoer_validatie("ingrediëntnaam", str, valideren = True, kleine_letters = True)
        
        return cls(
            ingrediënt_naam,
            categorie_uuid,
            )
    
    @property
    def categorie(self) -> Categorie:
        categorieën = Categorieën.openen()
        return categorieën[self.categorie_uuid]
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return self.categorie.hoofdcategorie

class Ingrediënten(MacroTypeDatabank):
    
    bestandsnaam: str = "ingrediënten"
    object_wijzers: List[ObjectWijzer] = [
        ObjectWijzer(Ingrediënt.van_json, Ingrediënt.velden),
        ]
    
    def opdracht(self):
        
        while True:
            
            opdracht = invoer_kiezen("opdracht ingrediënt", ["nieuw ingrediënt"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuw ingrediënt":
                self.nieuw()
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        ingrediënt = Ingrediënt.nieuw()
        
        ingrediënt_uuid = str(uuid4())
        self[ingrediënt_uuid] = ingrediënt
        
        self.opslaan()
        
        return ingrediënt_uuid if geef_uuid else ingrediënt
    
    def kiezen(
        self,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        ) -> str | Ingrediënt:
        
        while True:
            
            kies_optie = invoer_kiezen("ingrediënt op naam of categorie, of maak een nieuwe", ["ingrediëntnaam", "categorie", "nieuw"])
            
            if kies_optie == "ingrediëntnaam" or kies_optie == "categorie":
                
                if kies_optie == "ingrediëntnaam":
                    print("\ngeef een zoekterm op")
                    zoekterm = invoer_validatie("ingrediëntnaam", str, kleine_letters = True)
                    ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if zoekterm in ingrediënt.ingrediënt_naam]
                    if len(ingrediënten_mogelijk) == 0:
                        print(f"\n>>> zoekterm \"{zoekterm}\" levert geen ingrediënten op")
                        continue
                
                else:
                    categorieën = Categorieën.openen()
                    categorie_uuid = categorieën.kiezen()
                    ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt.categorie_uuid == categorie_uuid]
                    if len(ingrediënten_mogelijk) == 0:
                        print(f"\n>>> geen ingrediënten onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
                        continue
                
                print(f"\n>>> {len(ingrediënten_mogelijk)} ingrediënt{"en" if len(ingrediënten_mogelijk) > 1 else ""} gevonden")
                ingrediënt_uuid = invoer_kiezen("ingrediënt", {ingrediënt.ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt_uuid in ingrediënten_mogelijk}, stoppen = True)
                
                if not bool(ingrediënt_uuid):
                    continue
                
                if kies_bevestiging: print(f"\n>>> ingrediënt \"{self[ingrediënt_uuid].ingrediënt_naam}\" gekozen")
                
                return ingrediënt_uuid if geef_uuid else self[ingrediënt_uuid]
            
            else:
                return self.nieuw(geef_uuid)