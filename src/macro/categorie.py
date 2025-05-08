from .macrotype import MacroType

from grienetsiis import open_json, opslaan_json


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
    
    bestandsmap: str = "gegevens"
    bestandsnaam: str = "hoofdcategorieën"
    extensie: str = "json"
    
    @classmethod
    def instantiëren(cls):
        cls().opslaan()
        return cls()
    
    @classmethod
    def openen(cls):
        return cls(**open_json(cls.bestandsmap, cls.bestandsnaam, cls.extensie, (Hoofdcategorie, Hoofdcategorie.frozenset, "van_json")))
    
    def opslaan(self):
        opslaan_json(self, self.bestandsmap, self.bestandsnaam, self.extensie)

class Categorieën(dict):
    
    bestandsmap: str = "gegevens"
    bestandsnaam: str = "categorieën"
    extensie: str = "json"
    
    @classmethod
    def instantiëren(cls):
        cls().opslaan()
        return cls()
    
    @classmethod
    def openen(cls):
        return cls(**open_json(cls.bestandsmap, cls.bestandsnaam, cls.extensie, (Categorie, Categorie.frozenset, "van_json")))
    
    def opslaan(self):
        opslaan_json(self, self.bestandsmap, self.bestandsnaam, self.extensie)