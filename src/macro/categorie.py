from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie

from .macrotype import ClassMapper, MacroType, MacroTypeDatabank


class Hoofdcategorie(MacroType):
    
    frozenset = frozenset(("hoofdcategorie_naam", ))
    
    def __init__(
        self,
        hoofdcategorie_naam: str,
        ) -> "Hoofdcategorie":
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
    
    def __repr__(self) -> str:
        return f"categorie \"{self.hoofdcategorie_naam}\""
    
    @classmethod
    def nieuw(cls) -> "Hoofdcategorie":
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        hoofdcategorie_naam = invoer_validatie("hoofdcategorienaam", str, valideren = True, kleine_letters = True)
        
        return cls(
            hoofdcategorie_naam
            )

class Categorie(MacroType):
    
    frozenset = frozenset(("categorie_naam", "hoofdcategorie_uuid",))
    
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
    def nieuw(cls) -> "Categorie":
        
        hoofdcategorieën = Hoofdcategorieën.openen()
        hoofdcategorie_uuid = hoofdcategorieën.kiezen()
        
        print(f"\ninvullen gegevens nieuwe categorie onder hoofdcategorie \"{hoofdcategorieën[hoofdcategorie_uuid].hoofdcategorie_naam}\"")
        categorie_naam = invoer_validatie("categorienaam", str, valideren = True, kleine_letters = True)
        
        return cls(
            categorie_naam,
            hoofdcategorie_uuid,
            )
    
    @property
    def hoofdcategorie(self):
        hoofdcategorieën = Hoofdcategorieën.openen()
        return hoofdcategorieën[self.hoofdcategorie_uuid]

class Hoofdcategorieën(MacroTypeDatabank):
    
    bestandsnaam: str = "hoofdcategorieën"
    class_mappers: List[ClassMapper] = [
        ClassMapper(Hoofdcategorie.van_json, Hoofdcategorie.frozenset),
        ]
    
    def opdracht(self):
        
        while True:
            
            opdracht = invoer_kiezen("opdracht hoofdcategorie", ["nieuwe hoofdcategorie"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuwe hoofdcategorie":
                
                self.nieuw()
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        hoofdcategorie = Hoofdcategorie.nieuw()
        
        hoofdcategorie_uuid = str(uuid4())
        self[hoofdcategorie_uuid] = hoofdcategorie
        
        self.opslaan()
        
        return hoofdcategorie_uuid if geef_uuid else hoofdcategorie
    
    def kiezen(
        self,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        ) -> str | Hoofdcategorie:
        
        hoofdcategorie_uuid = invoer_kiezen("hoofdcategorie", {hoofdcategorie.hoofdcategorie_naam: hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items()})
        if kies_bevestiging: print(f"\n>>> hoofdcategorie \"{self[hoofdcategorie_uuid].hoofdcategorie_naam}\" gekozen")
        
        return hoofdcategorie_uuid if geef_uuid else self[hoofdcategorie_uuid]

class Categorieën(MacroTypeDatabank):
    
    bestandsnaam: str = "categorieën"
    class_mappers: List[ClassMapper] = [
        ClassMapper(Categorie.van_json, Categorie.frozenset),
        ]
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht categorie", ["nieuwe categorie"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuwe categorie":
                
                self.nieuw()
            
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        categorie = Categorie.nieuw()
        
        categorie_uuid = str(uuid4())
        self[categorie_uuid] = categorie
        
        self.opslaan()
        
        return categorie_uuid if geef_uuid else categorie
    
    def kiezen(
        self,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        ) -> str | Categorie:
        
        hoofdcategorieën = Hoofdcategorieën.openen()
        hoofdcategorie_uuid = hoofdcategorieën.kiezen()
        
        categorie_uuid = invoer_kiezen("categorie", {categorie.categorie_naam: categorie_uuid for categorie_uuid, categorie in self.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid})
        if kies_bevestiging: print(f"\n>>> categorie \"{self[categorie_uuid].categorie_naam}\" gekozen")
        
        return categorie_uuid if geef_uuid else self[categorie_uuid]