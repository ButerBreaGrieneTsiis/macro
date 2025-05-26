from typing import Any, Dict, List

from .macrotype import MacroType, MacroTypeDatabank, Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Gerecht(MacroType):
    
    def __init__(
        self,
        gerecht_naam: str,
        categorie_uuid: str, # dezelfde class kan gebruikt worden als voor product
        producten: Dict[str, List[Hoeveelheid]], #  uuid: aantal 100 g/ml
        porties: int,
        recept: str,
        versies: List[Dict[str, Any]], # uitvoeringen van het recept met een dictionary met een naam, [{"versie_naam": "standaard", "toegevoegd": {}, "verwijderd": [], "vervangen": {}, "hoeveelheid": {}}]
        ) -> "Gerecht":
        
        self.gerecht_naam = gerecht_naam
        self.categorie_uuid = categorie_uuid
        self.producten = producten
        self.porties = porties
        self.recept = recept
        self.versies = versies
    
    def __repr__(self):
        ...
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        ...
        
    @property
    def ingrediënten(self) -> Dict[str, str]: # mapping van product_uuid: ingredient_uuid
        
        ...

class Gerechten(MacroTypeDatabank):
    ...