import datetime as dt
import locale
from pathlib import Path
from typing import Dict, List

from grienetsiis import invoer_kiezen, invoer_validatie, openen_json, ObjectWijzer, STOP

from .macrotype import MacroType, Hoeveelheid
from .product import Producten
from .voedingswaarde import Voedingswaarde


locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

class Dag(MacroType):
    
    BESTANDSMAP:    Path    = Path("gegevens/dagen")
    EXTENSIE:       str     = "dag"
    
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
        if len(self.producten) == 0:
            return f"dag \"{self.dag}\""
        else:
            return f"dag \"{self.dag}\" van {self.voedingswaarde.calorieën}"
    
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
        
        bestandspad = cls.BESTANDSMAP
        if not bestandspad.is_dir():
            bestandspad.mkdir(parents = True)
        
        bestandspad /= f"{datum.year}"
        if not bestandspad.is_dir():
            bestandspad.mkdir()
        
        bestandspad /= f"{datum.strftime("%Y-%m-%d")}.{cls.EXTENSIE}"
        
        if bestandspad.is_file():
            return openen_json(
                bestandspad,
                object_wijzers = [
                    ObjectWijzer(cls.van_json, frozenset(("datum", "producten", "gerechten"))),
                    ObjectWijzer(Hoeveelheid.van_json, Hoeveelheid.VELDEN),
                    ],
                )
        
        else:
            return cls(datum)
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                f"MENU DAG/{f"{self.dag}".upper()}",
                [
                    "toevoegen producten",
                    "toevoegen gerechten",
                    "toon voedingswaarde",
                    "toon producten",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "toevoegen producten":
                
                producten = Producten.openen()
                
                while True:
                    
                    product, eenheid = producten.kiezen_product_eenheid(terug_naar = f"MENU DAG/{f"{self.dag}".upper()}", geef_uuid = False, stoppen = True)
                    
                    if product is STOP:
                        break
                    
                    if eenheid is STOP:
                        continue
                    
                    aantal = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    if product.uuid in self.producten.keys():
                        for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(self.producten[product.uuid]):
                            if hoeveelheid == hoeveelheid_aanwezig:
                                self.producten[product.uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                                break
                        else:
                            self.producten[product.uuid].append(hoeveelheid)
                    else:
                        self.producten[product.uuid] = [hoeveelheid]
                    break
            
            elif opdracht == "toevoegen gerechten":
                ...
            
            elif opdracht == "toon voedingswaarde":
                
                if len(self.producten) == 0:
                    print(f">>> er zijn geen producten voor {self}")
                    continue
                
                print(self.voedingswaarde)
            
            elif opdracht == "toon producten":
                
                if len(self.producten) == 0:
                    print(f">>> er zijn geen producten voor {self}")
                    continue
                
                producten = Producten.openen()
                
                print(f"{"HOEVEELHEID":<17} PRODUCT")
                
                for product_uuid, hoeveelheden in self.producten.items():
                    
                    for hoeveelheid in hoeveelheden:
                    
                        print(f"{f"{hoeveelheid}":<17} {producten[product_uuid].product_naam}")
            
            else:
                ...
            
    @property
    def bestandsnaam(self) -> str:
        return f"{self.datum.year}\\{self.datum.strftime("%Y-%m-%d")}"
    
    @property
    def dag(self) -> str:
        return f"{self.datum.strftime("%A %d %B %Y")}"
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        
        dag_voedingswaarde = Voedingswaarde()
        producten = Producten.openen()
        
        for product_uuid, hoeveelheden in self.producten.items():
            for hoeveelheid in hoeveelheden:
                product_voedingswaarde = producten[product_uuid].bereken_voedingswaarde(hoeveelheid)
                dag_voedingswaarde += product_voedingswaarde
        
        return dag_voedingswaarde