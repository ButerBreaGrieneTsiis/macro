"""macro.dag.dag"""
from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import locale
from typing import ClassVar, Dict, List, Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, Menu, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject
from grienetsiis.types import BasisType

from macro.product import Hoofdcategorie, Categorie, Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde


locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

@dataclass
class Dag(GeregistreerdObject):
    
    datum: dt.date
    producten: Dict[str, List[Hoeveelheid]] | None = None
    gerechten: Dict[str, Hoeveelheid] | None = None
    
    _HUIDIGE_DAG: ClassVar[dt.date] = dt.date.today()
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        if len(self.producten) == 0:
            return f"dag \"{self.dag}\""
        else:
            return f"dag \"{self.dag}\" van {self.voedingswaarde.calorieën}"
    
    # PROPERTIES
    
    @property
    def _id(self) -> str:
        return self.datum.strftime("%Y-%m-%d")
    
    @property
    def bestandsnaam(self) -> str:
        return f"{self.datum.year}\\{self.datum.strftime("%Y-%m-%d")}"
    
    @property
    def dag(self) -> str:
        return f"{self.datum.strftime("%A %d %B %Y")}"
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Dag._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        datum: dt.date = dt.date.today(),
        ) -> str | commando.Stop | None:
        
        datum_tekst = datum.strftime("%Y-%m-%d")
        
        if datum_tekst in Dag.subregister():
            return Dag.subregister()[datum_tekst]
        
        else:
            
            if datum_tekst in Dag.subregister().geregistreerde_instanties:
                return Register().openen_instantie(
                    subregister_naam = Dag._SUBREGISTER_NAAM,
                    id = datum_tekst,
                    )
            
            else:
                return Dag(
                    datum = Dag._HUIDIGE_DAG,
                    producten = {},
                    gerechten = {},
                    )
    
    @staticmethod
    def toevoegen_product():
        
        dag = Dag.selecteren(datum = Dag._HUIDIGE_DAG)
        
        while True:
            
            product = Product.selecteren(
                geef_id = False,
                toestaan_nieuw = True,
                terug_naar = f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}",
                )
            if product is commando.STOP:
                return commando.DOORGAAN
            if product is None:
                continue
            
            eenheid = product.selecteren_eenheid(
                terug_naar = f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}",
                toestaan_nieuw = True,
                )
            if eenheid is commando.STOP:
                return commando.DOORGAAN
            
            waarde = invoeren(
                tekst_beschrijving = f"hoeveel {eenheid.meervoud}",
                invoer_type = "float",
                )
            if waarde is commando.STOP:
                return commando.DOORGAAN
            
            hoeveelheid = Hoeveelheid(waarde, eenheid)
            
            product_uuid = product._id
            
            if dag.producten is None:
                dag.producten = {}
            
            if product_uuid in dag.producten.keys():
                for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(dag.producten[product_uuid]):
                    if hoeveelheid.eenheid == hoeveelheid_aanwezig.eenheid:
                        dag.producten[product_uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                        break
                else:
                    dag.producten[product_uuid].append(hoeveelheid)
            else:
                dag.producten[product_uuid] = [hoeveelheid]
            
            print(f"\n>>> {hoeveelheid} toegevoegd van {product}")