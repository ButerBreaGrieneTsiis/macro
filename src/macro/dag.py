import datetime as dt
import locale
from pathlib import Path
from typing import Dict, List

from grienetsiis import invoer_kiezen, invoer_validatie, openen_json, ObjectWijzer, STOP

from .gerecht import Gerechten
from .macrotype import MacroType, Eenheid, Hoeveelheid
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
        elif datum == "aangepast":
            
            jaar = invoer_validatie(
                "jaar",
                int,
                bereik = (1970, dt.datetime.today().year)
                )
            
            maand = invoer_validatie(
                "maand",
                int,
                bereik = (1, 12)
                )
            
            dag = invoer_validatie(
                "dag",
                int,
                bereik = (1, 31)
                )
            
            datum = dt.date(jaar, maand, dag)
        
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
                    "verwijderen producten",
                    "verwijderen gerechten",
                    "aanpassen hoeveelheid producten",
                    "aanpassen porties gerechten",
                    "aanpassen versie gerechten",
                    "weergeef producten",
                    "weergeef gerechten",
                    "weergeef voedingswaarde",
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
                    
                    product_uuid, eenheid = producten.kiezen_product_eenheid(
                        terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                        )
                    
                    if product_uuid is STOP:
                        break
                    
                    if eenheid is STOP:
                        continue
                    
                    aantal = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    if product_uuid in self.producten.keys():
                        for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(self.producten[product_uuid]):
                            if hoeveelheid == hoeveelheid_aanwezig:
                                self.producten[product_uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                                break
                        else:
                            self.producten[product_uuid].append(hoeveelheid)
                    else:
                        self.producten[product_uuid] = [hoeveelheid]
                    
                    print(f"\n>>> {hoeveelheid} toegevoegd van {producten[product_uuid]}")
                    
                    break
            
            elif opdracht == "toevoegen gerechten":
                
                gerechten = Gerechten.openen()
                
                while True:
                    
                    gerecht_uuid, versie_uuid = gerechten.kiezen_gerecht_versie(
                        terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                        )
                    
                    if gerecht_uuid is STOP:
                        break
                    
                    if versie_uuid is STOP:
                        continue
                    
                    eenheid = Eenheid("portie")
                    
                    aantal = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    self.gerechten[gerecht_uuid] = {
                        "versie_uuid": versie_uuid,
                        "hoeveelheid": hoeveelheid,
                        }
                    
                    versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                    print(f"\n>>> {hoeveelheid} toegevoegd van {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
                    
                    break
            
            elif opdracht == "verwijderen producten":
                
                producten = Producten.openen()
                
                product_uuid = invoer_kiezen(
                    "een product om te verwijderen",
                    {producten[product_uuid]: product_uuid for product_uuid in self.producten.keys()},
                    stoppen = True,
                    terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                    )
                
                if product_uuid is STOP:
                    continue
                
                del self.producten[product_uuid]
                
                print(f"\n>>> {producten[product_uuid]} verwijderd")
            
            elif opdracht == "verwijderen gerechten":
                
                gerechten = Gerechten.openen()
                
                gerecht_uuid = invoer_kiezen(
                    "een product om te verwijderen",
                    {gerechten[gerecht_uuid]: gerecht_uuid for gerecht_uuid in self.gerechten.keys()},
                    stoppen = True,
                    terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                    )
                
                if gerecht_uuid is STOP:
                    continue
                
                del self.gerechten[gerecht_uuid]
                
                print(f"\n>>> {gerechten[gerecht_uuid]} verwijderd")
            
            elif opdracht == "aanpassen hoeveelheid producten":
                
                producten = Producten.openen()
                
                kies_optie = invoer_kiezen(
                    "een product om aan te passen",
                    {f"{f"{hoeveelheid}":<17} {producten[product_uuid]}": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.producten.items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                    stoppen = True,
                    terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                product_uuid, ihoeveelheid = kies_optie
                
                eenheid = producten.kiezen_eenheid(
                    terug_naar = f"MENU DAG/{f"{self.dag}".upper()}",
                    product_uuid = product_uuid,
                    )
                
                if eenheid is STOP:
                    continue
                
                aantal = invoer_validatie(
                    f"hoeveel {eenheid.meervoud}",
                    float,
                    )
                
                hoeveelheid = Hoeveelheid(aantal, eenheid)
                
                print(f"\n>>> hoeveelheid {self.producten[product_uuid][ihoeveelheid]} aangepast naar {hoeveelheid}")
                
                self.producten[product_uuid][ihoeveelheid] = hoeveelheid
            
            elif opdracht == "aanpassen porties gerechten":
                ...
            
            elif opdracht == "aanpassen versie gerechten":
                ...
            
            elif opdracht == "weergeef producten":
                
                if len(self.producten) == 0:
                    print(f">>> er zijn geen producten voor {self}")
                    continue
                
                producten = Producten.openen()
                
                print(f"\n     {"HOEVEELHEID":<26} PRODUCT")
                
                for product_uuid, hoeveelheden in self.producten.items():
                    
                    for hoeveelheid in hoeveelheden:
                        
                        print(f"     {f"{hoeveelheid}":<17} {f"({Hoeveelheid(hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid], producten[product_uuid].basis_eenheid)})":<8} {producten[product_uuid]}")
            
            elif opdracht == "weergeef gerechten":
                
                if len(self.gerechten) == 0:
                    print(f"\n>>> er zijn geen gerechten voor {self}")
                    continue
                
                gerechten = Gerechten.openen()
                
                print(f"\n     HOEVEELHEID GERECHT")
                
                for gerecht_uuid, gerecht_dict in self.gerechten.items():
                    
                    versie_uuid = gerecht_dict["versie_uuid"]
                    versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                    
                    print(f"     {f"{gerecht_dict["hoeveelheid"]}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
            
            elif opdracht == "weergeef voedingswaarde":
                
                if len(self.producten) == 0 and len(self.gerechten) == 0:
                    print(f"\n>>> er zijn geen producten of gerechten voor {self}")
                    continue
                
                print(self.voedingswaarde)
        
        return self
        
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
        gerechten = Gerechten.openen()
        
        for product_uuid, hoeveelheden in self.producten.items():
            for hoeveelheid in hoeveelheden:
                product_voedingswaarde = producten[product_uuid].bereken_voedingswaarde(hoeveelheid)
                dag_voedingswaarde += product_voedingswaarde
        
        for gerecht_uuid, gerecht_dict in self.gerechten.items():
            gerecht_voedingswaarde = gerechten[gerecht_uuid].voedingswaarde(gerecht_dict["versie_uuid"]) * gerecht_dict["hoeveelheid"].waarde
            dag_voedingswaarde += gerecht_voedingswaarde
            
        return dag_voedingswaarde