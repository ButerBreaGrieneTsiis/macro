from copy import deepcopy
from typing import Any, Dict, List, Tuple

from grienetsiis import invoer_validatie, invoer_kiezen

from .hoeveelheid import Eenheid, Hoeveelheid
from .macrotype import MacroType
from .voedingswaarde import Voedingswaarde

class Ingredient(MacroType):
    
    def __init__(
        self,
        ingredient_naam: str,
        categorie_uuid: str,
        # producten_uuid: List[str] = None, # maken bij het inlezen, niet opslaan
        ) -> "Ingredient":
        
        self.ingredient_naam = ingredient_naam
        self.categorie_uuid = categorie_uuid

class Product(MacroType):
    
    def __init__(
        self,
        product_naam: str,
        merk_naam: str,
        opmerking: str,
        voedingswaarde: Voedingswaarde,
        eenheid: Eenheid,
        ingredient_uuid: str,
        hoeveelheden: Dict[Eenheid, float] = None,
        ) -> "Product":
        
        self.product_naam       = product_naam
        self.merk_naam          = merk_naam
        self.opmerking          = opmerking
        self.voedingswaarde     = voedingswaarde
        self.eenheid            = eenheid
        self.ingredient_uuid    = ingredient_uuid
        self.hoeveelheden       = dict() if hoeveelheden is None else hoeveelheden
    
    def __repr__(self) -> str:
        return f"Product \"{self.product_naam} ({self.merk_naam})\""
    
    @classmethod
    def nieuw(
        cls,
        ingredient_uuid: str,
        ) -> "Product":
        
        product_naam = invoer_validatie("productnaam", str, valideren = True)
        merk_naam = invoer_validatie("merknaam", str, valideren = True)
        opmerking = invoer_validatie("opmerking", str)
        eenheid = Eenheid(invoer_kiezen("eenheid", ["g", "ml"]))
        voedingswaarde = Voedingswaarde.nieuw(eenheid)
        
        return cls(
            product_naam,
            merk_naam,
            opmerking,
            voedingswaarde,
            eenheid,
            ingredient_uuid,
            )
    
    def toevoegen_hoeveelheid(self):
        
        ...
        
        return self
    
    # def bereken_voedingswaarde(
    #     self,
    #     hoeveelheid: Tuple[float, str],
    #     ) -> Voedingswaarde:
    #     # iets anders voor 100 g/ml?
    #     return deepcopy(self.voedingswaarde) * self.hoeveelheden[hoeveelheid[1]] * hoeveelheid[0]