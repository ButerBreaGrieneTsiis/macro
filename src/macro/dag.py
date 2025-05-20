import datetime as dt
from pathlib import Path
from typing import Dict, List

from grienetsiis import openen_json, ObjectWijzer

from .hoeveelheid import Hoeveelheid
from .macrotype import MacroType
from .voedingswaarde import Voedingswaarde


class Dag(MacroType):
    
    bestandsmap: Path = Path("gegevens\\dagen")
    extensie: str = "dag"
    object_wijzers: List[ObjectWijzer] = [
        ObjectWijzer(MacroType.van_json, frozenset(("datum", "producten", "gerechten"))),
        ]
    
    def __init__(
        self,
        datum: dt.date,
        producten: Dict[str, List[Hoeveelheid]] = None,
        gerechten: Dict[str, Hoeveelheid] = None,
        ) -> "Dag":
        
        self.datum = datum
        self.producten = dict() if producten is None else producten
        self.gerechten = dict() if gerechten is None else gerechten
    
    def __repr__(self) -> str:
        return ""
    
    @classmethod
    def openen(
        cls,
        datum: str | dt.date,
        ) -> "Dag":
        
        datum = dt.date.today() if datum == "vandaag" else datum
        
        bestandspad = cls.bestandsmap
        if not bestandspad.is_dir():
            bestandspad.mkdir()
        
        bestandspad /= f"{datum.year}"
        if not bestandspad.is_dir():
            bestandspad.mkdir()
        
        bestandspad /= f"{datum.strftime("%Y-%m-%d")}.{cls.extensie}"
        
        if bestandspad.is_file():
            
            return openen_json(
                bestandspad,
                object_wijzers = cls.object_wijzers,
                )
        
        else:
            return cls(datum)
    
    def opdracht(self):
        
        ...
    
    @property
    def bestandsnaam(self) -> str:
        return f"{self.datum.year}\\{self.datum.strftime("%Y-%m-%d")}"
        
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        ...
    