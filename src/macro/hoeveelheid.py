from enum import Enum


class Eenheid(Enum):
    
    STUK        =   "stuk",         "stuks"
    FLES        =   "fles",         "flessen"
    BLIK        =   "blik",         "blikken"
    POT         =   "pot",          "potten"
    PORTIE      =   "portie",       "porties"
    ZAK         =   "zak",          "zakken"
    THEELEPEL   =   "eetlepel",     "eetlepels"
    EETLEPEL    =   "theelepel",    "theelepels"
    PLAK        =   "plak",         "plakken"
    VERPAKKING  =   "verpakking",   "verpakkingen"
    GRAM        =   "g",            "g"
    MILLILITER  =   "ml",           "ml"
    
    # https://stackoverflow.com/questions/75384124/how-to-initialize-named-tuple-in-python-enum
    def __new__(cls, enkelvoud, meervoud):
        veld = object.__new__(cls)
        veld._value_    = enkelvoud
        veld.enkelvoud  = enkelvoud
        veld.meervoud   = meervoud
        return veld

class Hoeveelheid:
    
    def __init__(
        self,
        waarde: float,
        eenheid: Eenheid,
        ) -> "Hoeveelheid":
        
        self.waarde = waarde
        self.eenheid = eenheid
    
    def __repr__(self) -> str:
        
        formaat = ".0f" if self.waarde.is_integer() else ".2f"
        
        if self.waarde == 1.0:
            return f"{self.waarde:{formaat}} {self.eenheid.enkelvoud}"
        else:
            return f"{self.waarde:{formaat}} {self.eenheid.meervoud}"
    
    @classmethod
    def van_tekst(
        cls,
        waarde: float,
        eenheid: str,
        ) -> "Hoeveelheid":
        
        return cls(
            waarde,
            Eenheid(eenheid),
            )