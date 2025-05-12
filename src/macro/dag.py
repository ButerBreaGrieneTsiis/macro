import datetime as dt
from typing import Dict, List

from .hoeveelheid import Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Dag:
    
    def __init__(
        self,
        datum: dt.Date,
        producten: Dict[str, List[Hoeveelheid]] = None,
        gerechten: Dict[str, Hoeveelheid] = None,
        ) -> "Dag":
        
        self.datum = datum
        self.producten = dict() if producten is None else producten
        self.gerechten = dict() if gerechten is None else gerechten
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        ...
    