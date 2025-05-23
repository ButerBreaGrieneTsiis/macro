import datetime as dt
import locale
from pathlib import Path
from typing import Dict, List

from grienetsiis import invoer_kiezen, invoer_validatie, openen_json, ObjectWijzer, STOP

from .hoeveelheid import Hoeveelheid
from .macrotype import MacroType
from .product import Producten
from .voedingswaarde import Voedingswaarde


locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

class Dag(MacroType):
    
    bestandsmap:    Path                = Path("gegevens\\dagen")
    extensie:       str                 = "dag"
    
    def __init__(
        self,
        datum:      dt.date,
        producten:  Dict[str, List[Hoeveelheid]]    = None,
        gerechten:  Dict[str, Hoeveelheid]          = None,
        ) -> "Dag":
        
        self.datum = datum
        self.producten = dict() if producten is None else producten
        self.gerechten = dict() if gerechten is None else gerechten
    
    def __repr__(self) -> str:
        return f"dag {self.dag} van {self.voedingswaarde.calorieën}"
    
    @classmethod
    def openen(
        cls,
        datum: str | dt.date,
        ) -> "Dag":
        
        if isinstance(datum, str):
            if datum == "vandaag":
                datum = dt.date.today()
            elif datum == "morgen":
                datum = dt.date.today() + dt.timedelta(days = 1)
            elif datum == "overmorgen":
                datum = dt.date.today() + dt.timedelta(days = 2)
            elif datum == "gisteren":
                datum = dt.date.today() - dt.timedelta(days = 1)
            elif datum == "eergisteren":
                datum = dt.date.today() - dt.timedelta(days = 2)
        
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
                object_wijzers = [ObjectWijzer(cls.van_json, frozenset(("datum", "producten", "gerechten")))],
                )
        
        else:
            return cls(datum)
    
    def opdracht(self):
        
        while True:
            
            opdracht = invoer_kiezen(f"opdracht {self.dag}", ["toevoegen producten", "toevoegen gerechten","toon voedingswaarde", "toon producten"], stoppen = True)
            
            if opdracht is STOP:
                break
            
            elif opdracht == "toevoegen producten":
                
                producten = Producten.openen()
                
                while True:
                    
                    product, eenheid = producten.kiezen_product_eenheid(geef_uuid = False, stoppen = True)
                    
                    if product is STOP:
                        break
                    
                    if eenheid is STOP:
                        continue
                    
                    aantal = invoer_validatie(f"hoeveel {eenheid.meervoud}", float)
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    # nog een check schrijven of de eenheid reeds bestaat -> dan hoeveelheden sommeren -> Hoeveelheid.__add__() maken?
                    if product.uuid in self.producten.keys():
                        self.producten[product.uuid].append(hoeveelheid)
                    else:
                        self.producten[product.uuid] = [hoeveelheid]
                    print(self.producten)
                    break
            
            elif opdracht == "toevoegen gerechten":
                ...
            
            elif opdracht == "toon voedingswaarde":
                ...
            
            else:
                ...
            
    @property
    def bestandsnaam(self) -> str:
        return f"{self.datum.year}\\{self.datum.strftime("%Y-%m-%d")}"
    
    @property
    def dag(self) -> str:
        return f"{self.datum.strftime("%A %d %B %Y")}"
    
    # @property
    # def voedingswaarde(self) -> Voedingswaarde:
        
    #     dag_voedingswaarde = Voedingswaarde()
    #     producten = Producten.openen()
        
    #     for product_uuid, hoeveelheden in self.producten.items():
    #         for hoeveelheid in hoeveelheden:
    #             product_voedingswaarde = producten[product_uuid].voedingswaarde * hoeveelheid.aantal * producten[product_uuid].eenheden[hoeveelheid.eenheid]
    #             dag_voedingswaarde += product_voedingswaarde