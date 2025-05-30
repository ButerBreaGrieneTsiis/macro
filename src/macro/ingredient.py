from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP

from .categorie import Categorie, Categorieën, Hoofdcategorie
from .macrotype import MacroType, MacroTypeDatabank


class Ingrediënt(MacroType):
    
    VELDEN = frozenset(("ingrediënt_naam", "categorie_uuid",))
    
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
    def nieuw(
        cls,
        terug_naar: str,
        ):
        
        categorieën = Categorieën.openen()
        categorie_uuid = categorieën.kiezen(terug_naar)
        if categorie_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuw ingrediënt onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
        ingrediënt_naam = invoer_validatie(
            "ingrediëntnaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
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
    
    BESTANDSNAAM: str = "ingrediënten"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Ingrediënt.van_json, Ingrediënt.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                "MENU GEGEVENS/INGREDIËNT",
                ["nieuw ingrediënt"],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuw ingrediënt":
                self.nieuw(terug_naar = "MENU GEGEVENS/INGREDIËNT")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        geef_uuid: bool = True,
        ):
        
        ingrediënt = Ingrediënt.nieuw(terug_naar)
        if ingrediënt is STOP:
            return STOP
        
        ingrediënt_uuid = str(uuid4())
        self[ingrediënt_uuid] = ingrediënt
        
        self.opslaan()
        
        return ingrediënt_uuid if geef_uuid else ingrediënt
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        stoppen: bool = False,
        ) -> str | Ingrediënt:
        
        while True:
            
            if len(self) == 0:
                
                kies_optie = invoer_kiezen(
                    "geen ingrediënten aanwezig, maak een nieuw ingrediënt",
                    ["nieuw ingrediënt"],
                    kies_een = False,
                    stoppen = stoppen,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)
            
            else:
            
                kies_optie = invoer_kiezen(
                    "ingrediënt op naam of categorie, of maak een nieuwe",
                    ["zoek op ingrediëntnaam", "zoek op categorie", "nieuw ingrediënt"],
                    stoppen = stoppen,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "zoek op ingrediëntnaam" or kies_optie == "zoek op categorie":
                    
                    if kies_optie == "zoek op ingrediëntnaam":
                        print("\ngeef een zoekterm op")
                        zoekterm = invoer_validatie(
                            "ingrediëntnaam",
                            str,
                            kleine_letters = True,
                            )
                        ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if zoekterm in ingrediënt.ingrediënt_naam]
                        if len(ingrediënten_mogelijk) == 0:
                            print(f"\n>>> zoekterm \"{zoekterm}\" levert geen ingrediënten op")
                            continue
                    
                    else:
                        categorieën = Categorieën.openen()
                        categorie_uuid = categorieën.kiezen(terug_naar)
                        
                        if categorie_uuid is STOP:
                            return STOP
                        
                        ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt.categorie_uuid == categorie_uuid]
                        if len(ingrediënten_mogelijk) == 0:
                            print(f"\n>>> geen ingrediënten onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
                            continue
                    
                    print(f"\n>>> {len(ingrediënten_mogelijk)} ingrediënt{"en" if len(ingrediënten_mogelijk) > 1 else ""} gevonden")
                    ingrediënt_uuid = invoer_kiezen(
                        "ingrediënt",
                        {ingrediënt.ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt_uuid in ingrediënten_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if ingrediënt_uuid is STOP:
                        continue
                    
                    if kies_bevestiging: print(f"\n>>> ingrediënt \"{self[ingrediënt_uuid].ingrediënt_naam}\" gekozen")
                    
                    return ingrediënt_uuid if geef_uuid else self[ingrediënt_uuid]
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)