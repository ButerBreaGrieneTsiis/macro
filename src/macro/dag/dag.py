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
    def titel() -> str:
        return f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}"
    
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
    def toevoegen_product() -> commando.Doorgaan:
        
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
    
    @staticmethod
    def weergeven_product() -> commando.Doorgaan:
        
        dag = Dag.selecteren(datum = Dag._HUIDIGE_DAG)
        
        if len(dag.producten) == 0 and len(dag.gerechten) == 0:
            print(f"\n>>> geen producten of gerechten aanwezig om te weergeven")
            return commando.Doorgaan
        
        if len(dag.producten) > 0:
            print("\nlos toegevoegde producten")
            print(f"\n{"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
        
        calorieën_totaal    =   Hoeveelheid(0, Eenheid.KILOCALORIE)
        eiwitten_totaal     =   Hoeveelheid(0, Eenheid.GRAM)
        
        for product_uuid, hoeveelheden in dag.producten.items():
            
            for hoeveelheid in hoeveelheden:
                
                print(f"{f"{hoeveelheid}":<18} {f"{Product.subregister()[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * Product.subregister()[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>9} {f"{Product.subregister()[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * Product.subregister()[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>8} {Product.subregister()[product_uuid]}")
                calorieën_totaal += Product.subregister()[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * Product.subregister()[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
                eiwitten_totaal += Product.subregister()[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * Product.subregister()[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
        
        print(f"\n{"SUBTOTAAL":<18} {f"{calorieën_totaal}":>9} {f"{eiwitten_totaal}":>8} ")
        
        # for gerecht_uuid, versie_dict in self.gerechten.items():
            
        #     for versie_uuid, versie_hoeveelheid  in versie_dict.items():
        #         versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
        #         print(f"\n     {versie_hoeveelheid} van {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
        #         print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                
        #         aantal_porties = gerechten[gerecht_uuid].porties if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid].get("porties", gerechten[gerecht_uuid].porties)
                
        #         for product_uuid, hoeveelheden in gerechten[gerecht_uuid].producten(versie_uuid).items():
            
        #             for hoeveelheid in hoeveelheden:
                        
        #                 print(f"     {f"{hoeveelheid * versie_hoeveelheid.waarde/aantal_porties}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100 * versie_hoeveelheid.waarde/aantal_porties}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100 * versie_hoeveelheid.waarde/aantal_porties}":>8} {producten[product_uuid]}")
                
        #         print(f"\n     {"SUBTOTAAL":<18} {f"{gerechten[gerecht_uuid].voedingswaarde(versie_uuid).calorieën}":>9} {f"{gerechten[gerecht_uuid].voedingswaarde(versie_uuid).eiwitten}":>8} ")
                
        # print(f"\n\n     {"TOTAAL":<18} {f"{self.voedingswaarde.calorieën}":>9} {f"{self.voedingswaarde.eiwitten}":>8}")
        
        return commando.DOORGAAN
        
    @staticmethod
    def veranderen_dag() -> commando.Doorgaan:
        
        opties = {
            dt.date.today(): f"vandaag ({dt.date.today().strftime("%A %d %B %Y")})",
            (dt.date.today() + dt.timedelta(days = 1)): f"morgen ({(dt.date.today() + dt.timedelta(days = 1)).strftime("%A %d %B %Y")})",
            (dt.date.today() + dt.timedelta(days = 2)): f"overmorgen ({(dt.date.today() + dt.timedelta(days = 2)).strftime("%A %d %B %Y")})",
            (dt.date.today() - dt.timedelta(days = 1)): f"gisteren ({(dt.date.today() - dt.timedelta(days = 1)).strftime("%A %d %B %Y")})",
            (dt.date.today() - dt.timedelta(days = 2)): f"eergisteren ({(dt.date.today() - dt.timedelta(days = 2)).strftime("%A %d %B %Y")})",
            "aangepast": f"aangepast ({(dt.date.today() - dt.timedelta(days = 2)).strftime("%A %d %B %Y")})",
            }
        
        datum = kiezen(
            opties = opties,
            tekst_beschrijving = "dag",
            tekst_annuleren = f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}",
            )
        if datum is commando.STOP:
            return commando.DOORGAAN
        
        if datum == "aangepast":
            
            jaar = invoeren(
                tekst_beschrijving = "jaar",
                invoer_type = "int",
                waardes_bereik = (1970, dt.datetime.today().year)
                )
            if jaar is commando.STOP:
                return commando.DOORGAAN
            
            maand = invoeren(
                tekst_beschrijving = "maand",
                invoer_type = "int",
                waardes_bereik = (1, 12)
                )
            if maand is commando.STOP:
                return commando.DOORGAAN
            
            dag = invoeren(
                tekst_beschrijving = "dag",
                invoer_type = "int",
                waardes_bereik = (1, 31)
                )
            if dag is commando.STOP:
                return commando.DOORGAAN
            
            datum = dt.date(jaar, maand, dag)
        
        print(f"\n>>> datum veranderd van \"{Dag._HUIDIGE_DAG}\" naar \"{datum}\"")
        Dag._HUIDIGE_DAG = datum
        return commando.DOORGAAN