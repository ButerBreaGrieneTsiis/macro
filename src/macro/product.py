from typing import Dict
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie

from .hoeveelheid import Eenheid, Hoeveelheid
from .ingredient import Ingrediënten
from .macrotype import MacroType, MacroTypeDatabank
from .voedingswaarde import Voedingswaarde


class Product(MacroType):
    
    frozenset = frozenset(("product_naam", "merk_naam", "opmerking", "voedingswaarde", "eenheid", "ingrediënt_uuid", "hoeveelheden"))
    
    def __init__(
        self,
        product_naam: str,
        merk_naam: str,
        voedingswaarde: Voedingswaarde,
        eenheid: Eenheid,
        ingrediënt_uuid: str,
        opmerking: str = None,
        hoeveelheden: Dict[Eenheid, float] = None,
        ) -> "Product":
        
        self.product_naam       = product_naam
        self.merk_naam          = merk_naam
        self.opmerking          = opmerking
        self.voedingswaarde     = voedingswaarde
        self.eenheid            = eenheid
        self.ingrediënt_uuid    = ingrediënt_uuid
        self.hoeveelheden       = dict() if hoeveelheden is None else hoeveelheden
    
    def __repr__(self) -> str:
        return f"Product \"{self.product_naam} ({self.merk_naam})\""
    
    @classmethod
    def nieuw(cls) -> "Product":
        
        ingrediënten = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen()
        product_naam = invoer_validatie("productnaam", str, valideren = True, kleine_letters = True)
        merk_naam = invoer_validatie("merknaam", str, valideren = True, kleine_letters = True)
        opmerking = invoer_validatie("opmerking", str, kleine_letters = True)
        eenheid = Eenheid(invoer_kiezen("eenheid", ["g", "ml"]))
        voedingswaarde = Voedingswaarde.nieuw(eenheid)
        
        return cls(
            product_naam,
            merk_naam,
            voedingswaarde,
            eenheid,
            ingrediënt_uuid,
            opmerking,
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

class Producten(MacroTypeDatabank):
    
    bestandsnaam: str = "producten"
    object = Product
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht product", ["nieuw product"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuw product":
                
                self.nieuw()
                
        return self
    
    def nieuw(self):
        
        product = Product.nieuw()
        
        uuid = str(uuid4())
        self[uuid] = product
        self.opslaan()
        
        return self