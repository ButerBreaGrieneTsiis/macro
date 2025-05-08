import datetime as dt
from typing import Dict, List

from .hoeveelheid import Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Dag:
    
    def __init__(
        self,
        datum: dt.Date,
        producten: Dict[str, List[Hoeveelheid]] = None,
        ) -> "Dag":
        
        self.datum = datum
        self.producten = Dict() if producten is None else producten
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        ...
    