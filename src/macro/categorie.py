from pathlib import Path
from uuid import uuid4

from grienetsiis import open_json, opslaan_json, invoer_kiezen, invoer_validatie

from .macrotype import MacroType


class Hoofdcategorie(MacroType):
    
    def __init__(
        self,
        hoofdcategorie_naam: str,
        ) -> "Hoofdcategorie":
        
        self.hoofdcategorie_naam = hoofdcategorie_naam

class Categorie(MacroType):
    
    frozenset = frozenset(("categorie_naam", "hoofdcategorie_uuid"))
    
    def __init__(
        self,
        categorie_naam: str,
        hoofdcategorie_uuid: str,
        ) -> "Categorie":
        
        self.categorie_naam = categorie_naam
        self.hoofdcategorie_uuid = hoofdcategorie_uuid

class Hoofdcategorieën(dict):
    
    bestandsmap:    str = "gegevens"
    bestandsnaam:   str = "hoofdcategorieën"
    extensie:       str = "json"
    
    @classmethod
    def openen(cls):
        bestandspad = Path(f"{cls.bestandsmap}\\{cls.bestandsnaam}.{cls.extensie}")
        if bestandspad.is_file():
            return cls(**open_json(cls.bestandsmap, cls.bestandsnaam, cls.extensie, (Hoofdcategorie, Hoofdcategorie.frozenset, "van_json")))
        else:
            return cls()
    
    def opslaan(self):
        opslaan_json(self, self.bestandsmap, self.bestandsnaam, self.extensie)
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht", ["toevoegen"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "toevoegen":
                
                self.toevoegen()
            
        return self
    
    def toevoegen(self):
        
        hoofdcategorie_naam = invoer_validatie("naam", str, valideren = True)
        hoofdcategorie = Hoofdcategorie(hoofdcategorie_naam)
        
        uuid = str(uuid4())
        self[uuid] = hoofdcategorie
        
        return self
    
    def kiezen(self) -> str:
        return invoer_kiezen("hoofdcategorie", {hoofdcategorie.hoofdcategorie_naam: hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items()})

class Categorieën(dict):
    
    bestandsmap:    str = "gegevens"
    bestandsnaam:   str = "categorieën"
    extensie:       str = "json"
    
    @classmethod
    def openen(cls):
        bestandspad = Path(f"{cls.bestandsmap}\\{cls.bestandsnaam}.{cls.extensie}")
        if bestandspad.is_file():
            return cls(**open_json(cls.bestandsmap, cls.bestandsnaam, cls.extensie, (Categorie, Categorie.frozenset, "van_json")))
        else:
            return cls()
    
    def opslaan(self):
        opslaan_json(self, self.bestandsmap, self.bestandsnaam, self.extensie)
    
    def opdracht(self, hoofdcategorieën):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht", ["toevoegen"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "toevoegen":
                
                self.toevoegen(hoofdcategorieën)
            
        return self
    
    def toevoegen(self, hoofdcategorieën):
        
        categorie_naam = invoer_validatie("naam", str, valideren = True)
        hoofdcategorie_uuid = hoofdcategorieën.kiezen()
        
        categorie = Categorie(categorie_naam, hoofdcategorie_uuid)
        
        uuid = str(uuid4())
        self[uuid] = categorie
        
        return self