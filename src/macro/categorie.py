from pathlib import Path
from uuid import uuid4

from grienetsiis import open_json, opslaan_json, invoer_kiezen, invoer_validatie

from .macrotype import MacroType, MacroTypeDatabank


class Hoofdcategorie(MacroType):
    
    frozenset = frozenset(("hoofdcategorie_naam", ))
    
    def __init__(
        self,
        hoofdcategorie_naam: str,
        ) -> "Hoofdcategorie":
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
    
    @classmethod
    def nieuw(cls) -> "Hoofdcategorie":
        
        hoofdcategorie_naam = invoer_validatie("naam", str, valideren = True, kleine_letters = True)
        
        return cls(
            hoofdcategorie_naam
            )

class Categorie(MacroType):
    
    frozenset = frozenset(("categorie_naam", "hoofdcategorie_uuid"))
    
    def __init__(
        self,
        categorie_naam: str,
        hoofdcategorie_uuid: str,
        ) -> "Categorie":
        
        self.categorie_naam = categorie_naam
        self.hoofdcategorie_uuid = hoofdcategorie_uuid
    
    @classmethod
    def nieuw(cls) -> "Categorie":
        
        hoofdcategorieën = Hoofdcategorieën.openen()
        hoofdcategorie_uuid = hoofdcategorieën.kiezen()
        categorie_naam = invoer_validatie("naam", str, valideren = True, kleine_letters = True)
        
        return cls(
            categorie_naam,
            hoofdcategorie_uuid,
            )

class Hoofdcategorieën(MacroTypeDatabank):
    
    bestandsnaam: str = "hoofdcategorieën"
    object = Hoofdcategorie
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht hoofdcategorie", ["nieuwe hoofdcategorie"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuwe hoofdcategorie":
                
                self.nieuw()
            
        return self
    
    def nieuw(self):
        
        hoofdcategorie = Hoofdcategorie.nieuw()
        
        uuid = str(uuid4())
        self[uuid] = hoofdcategorie
        self.opslaan()
        
        return self
    
    def kiezen(self) -> str:
        return invoer_kiezen("hoofdcategorie", {hoofdcategorie.hoofdcategorie_naam: hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items()})

class Categorieën(MacroTypeDatabank):
    
    bestandsnaam: str = "categorieën"
    object = Categorie
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht categorie", ["nieuwe categorie"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuwe categorie":
                
                self.nieuw()
            
        return self
    
    def nieuw(self):
        
        categorie = Categorie.nieuw()
        
        uuid = str(uuid4())
        self[uuid] = categorie
        self.opslaan()
        
        return self
    
    def kiezen(self) -> str:
        
        hoofdcategorieën = Hoofdcategorieën.openen()
        hoofdcategorie_uuid = hoofdcategorieën.kiezen()
        return invoer_kiezen("categorie", {categorie.categorie_naam: categorie_uuid for categorie_uuid, categorie in self.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid})