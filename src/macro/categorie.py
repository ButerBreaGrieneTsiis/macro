from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP

from .macrotype import MacroType, MacroTypeDatabank


class Hoofdcategorie(MacroType):
    
    VELDEN = frozenset(("hoofdcategorie_naam", ))
    
    def __init__(
        self,
        hoofdcategorie_naam: str,
        ) -> "Hoofdcategorie":
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
    
    def __repr__(self) -> str:
        return f"hoofdcategorie \"{self.hoofdcategorie_naam}\""
    
    @classmethod
    def nieuw(cls) -> "Hoofdcategorie":
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        hoofdcategorie_naam = invoer_validatie("hoofdcategorienaam", str, valideren = True, kleine_letters = True, uitsluiten_leeg = True)
        
        return cls(
            hoofdcategorie_naam
            )

class Categorie(MacroType):
    
    VELDEN = frozenset(("categorie_naam", "hoofdcategorie_uuid",))
    
    def __init__(
        self,
        categorie_naam: str,
        hoofdcategorie_uuid: str,
        ) -> "Categorie":
        
        self.categorie_naam = categorie_naam
        self.hoofdcategorie_uuid = hoofdcategorie_uuid
    
    def __repr__(self) -> str:
        return f"categorie \"{self.categorie_naam}\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ) -> "Categorie":
        
        hoofdcategorieën = Hoofdcategorieën.openen()
        hoofdcategorie_uuid = hoofdcategorieën.kiezen(terug_naar)
        
        if hoofdcategorie_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuwe categorie onder hoofdcategorie \"{hoofdcategorieën[hoofdcategorie_uuid].hoofdcategorie_naam}\"")
        categorie_naam = invoer_validatie("categorienaam", str, valideren = True, kleine_letters = True, uitsluiten_leeg = True)
        
        return cls(
            categorie_naam,
            hoofdcategorie_uuid,
            )
    
    @property
    def hoofdcategorie(self):
        hoofdcategorieën = Hoofdcategorieën.openen()
        return hoofdcategorieën[self.hoofdcategorie_uuid]

class Hoofdcategorieën(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "hoofdcategorieën"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Hoofdcategorie.van_json, Hoofdcategorie.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen("MENU GEGEVENS/HOOFDCATEGORIE", ["nieuwe hoofdcategorie"], stoppen = True, kies_een = False, terug_naar = terug_naar)
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuwe hoofdcategorie":
                
                self.nieuw()
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        hoofdcategorie = Hoofdcategorie.nieuw()
        
        if hoofdcategorie is STOP:
            return STOP
        
        hoofdcategorie_uuid = str(uuid4())
        self[hoofdcategorie_uuid] = hoofdcategorie
        
        self.opslaan()
        
        return hoofdcategorie_uuid if geef_uuid else hoofdcategorie
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        stoppen: bool = True,
        ) -> str | Hoofdcategorie:
        
        while True:
            
            if len(self) == 0:
            
                kies_optie = invoer_kiezen("geen hoofdcategorieën aanwezig, maak een nieuwe hoofdcategorie", ["nieuwe hoofdcategorie"], kies_een = False, stoppen = stoppen, terug_naar = terug_naar)
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(geef_uuid = geef_uuid)
            
            else:
                
                kies_optie = invoer_kiezen("bestaande hoofdcategorie of maak een nieuwe", ["zoek op hoofdcategorie", "nieuwe hoofdcategorie"], stoppen = stoppen, terug_naar = terug_naar)
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "zoek op hoofdcategorie":
                    
                    hoofdcategorie_uuid = invoer_kiezen("hoofdcategorie", {hoofdcategorie.hoofdcategorie_naam: hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items()})
                    if kies_bevestiging: print(f"\n>>> hoofdcategorie \"{self[hoofdcategorie_uuid].hoofdcategorie_naam}\" gekozen")
                    
                    return hoofdcategorie_uuid if geef_uuid else self[hoofdcategorie_uuid]
                
                else:
                    return self.nieuw(geef_uuid = geef_uuid)

class Categorieën(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "categorieën"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Categorie.van_json, Categorie.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
        
            opdracht = invoer_kiezen("MENU GEGEVENS/CATEGORIE", ["nieuwe categorie"], stoppen = True, kies_een = False, terug_naar = terug_naar)
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuwe categorie":
                
                self.nieuw(terug_naar = "MENU GEGEVENS/CATEGORIE")
            
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        geef_uuid: bool = True,
        ):
        
        categorie = Categorie.nieuw(terug_naar)
        if categorie is STOP:
            return STOP
        
        categorie_uuid = str(uuid4())
        self[categorie_uuid] = categorie
        
        self.opslaan()
        
        return categorie_uuid if geef_uuid else categorie
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        stoppen: bool = True,
        ) -> str | Categorie:
        
        while True:
            if len(self) == 0:
            
                kies_optie = invoer_kiezen("geen categorieën aanwezig, maak een nieuwe categorie", ["nieuwe categorie"], kies_een = False, stoppen = stoppen, terug_naar = terug_naar)
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)
            
            else:
                
                kies_optie = invoer_kiezen("bestaande categorie of maak een nieuwe", ["zoek op hoofdcategorie", "nieuwe categorie"], stoppen = stoppen, terug_naar = terug_naar)
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "zoek op categorie":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorie_uuid = hoofdcategorieën.kiezen()
                    
                    categorie_uuid = invoer_kiezen("categorie", {categorie.categorie_naam: categorie_uuid for categorie_uuid, categorie in self.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid}, stoppen = stoppen, terug_naar = terug_naar)
                    if categorie_uuid is STOP:
                        return STOP
                    
                    if kies_bevestiging: print(f"\n>>> categorie \"{self[categorie_uuid].categorie_naam}\" gekozen")
                    
                    return categorie_uuid if geef_uuid else self[categorie_uuid]
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)