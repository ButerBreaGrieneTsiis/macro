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
                f"MENU DAG {f"{self.dag}".upper()}",
                [
                    "toevoegen producten",
                    "toevoegen gerechten",
                    "verwijderen producten",
                    "verwijderen gerechten",
                    "aanpassen hoeveelheid producten",
                    "aanpassen porties gerechten",
                    "weergeef producten",
                    "weergeef gerechten",
                    "weergeef voedingswaarde",
                    "kopiëren producten van andere dag",
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
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
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
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                    
                    if gerecht_uuid is STOP:
                        break
                    
                    if versie_uuid is STOP:
                        continue
                    
                    eenheid = Eenheid("portie")
                    
                    porties = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(porties, eenheid)
                    
                    if gerecht_uuid in self.gerechten.keys():
                        if versie_uuid in self.gerechten[gerecht_uuid]:
                            self.gerechten[gerecht_uuid][versie_uuid].waarde += porties
                        else:
                            self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid
                    else:
                        self.gerechten[gerecht_uuid] = {}
                        self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid
                    
                    versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                    print(f"\n>>> {hoeveelheid} toegevoegd van {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
                    
                    break
            
            elif opdracht == "verwijderen producten":
                
                if len(self.producten) == 0:
                    print("\n>>> geen producten aanwezig om te verwijderen")
                    continue
                
                producten = Producten.openen()
                
                kies_optie = invoer_kiezen(
                    "een product en hoeveelheid om te verwijderen",
                    {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.producten.items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                    stoppen = True,
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                product_uuid, ihoeveelheid = kies_optie
                
                print(f"\n>>> {self.producten[product_uuid][ihoeveelheid]} van {producten[product_uuid]} verwijderd")
                
                del self.producten[product_uuid][ihoeveelheid]
            
            elif opdracht == "verwijderen gerechten":
                
                if len(self.gerechten) == 0:
                    print("\n>>> geen gerechten aanwezig om te verwijderen")
                    continue
                
                gerechten = Gerechten.openen()
                
                kies_optie = invoer_kiezen(
                    "een gerecht en versie om te verwijderen",
                    {f"{f"{hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")": (gerecht_uuid, versie_uuid) for gerecht_uuid, versie_dict in self.gerechten.items() for versie_uuid, hoeveelheid in versie_dict.items() if (versie_naam := "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"])},
                    stoppen = True,
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                gerecht_uuid, versie_uuid = kies_optie
                
                versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                print(f"\n>>> versie \"{versie_naam}\" van {gerechten[gerecht_uuid]} verwijderd")
                
                del self.gerechten[gerecht_uuid][versie_uuid]
            
            elif opdracht == "aanpassen hoeveelheid producten":
                
                if len(self.producten) == 0:
                    print("\n>>> geen producten aanwezig om de hoeveelheid van aan te passen")
                    continue
                
                producten = Producten.openen()
                
                kies_optie = invoer_kiezen(
                    "een product en hoeveelheid om aan te passen",
                    {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.producten.items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                    stoppen = True,
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                product_uuid, ihoeveelheid = kies_optie
                
                eenheid = producten.kiezen_eenheid(
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
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
                
                if len(self.gerechten) == 0:
                    print("\n>>> geen gerechten aanwezig om het aantal porties van aan te passen")
                    continue
                
                gerechten = Gerechten.openen()
                
                kies_optie = invoer_kiezen(
                    "een gerecht en versie om aan te passen",
                    {f"{f"{hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")": (gerecht_uuid, versie_uuid) for gerecht_uuid, versie_dict in self.gerechten.items() for versie_uuid, hoeveelheid in versie_dict.items() if (versie_naam := "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"])},
                    stoppen = True,
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                gerecht_uuid, versie_uuid = kies_optie
                
                eenheid = Eenheid("portie")
                    
                porties = invoer_validatie(
                    f"hoeveel {eenheid.meervoud}",
                    float,
                    )
                
                hoeveelheid = Hoeveelheid(porties, eenheid)
                
                self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid
            
            elif opdracht == "weergeef producten":
                
                if len(self.producten) == 0 and len(self.gerechten) == 0:
                    print(f"\n>>> geen producten of gerechten aanwezig om te weergeven")
                    continue
                
                producten = Producten.openen()
                gerechten = Gerechten.openen()
                
                if len(self.producten) > 0:
                    print("\n     los toegevoegde producten")
                    print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                
                calorieën_totaal    =   Hoeveelheid(0, Eenheid("kcal"))
                eiwitten_totaal     =   Hoeveelheid(0, Eenheid("g"))
                
                for product_uuid, hoeveelheden in self.producten.items():
                    
                    for hoeveelheid in hoeveelheden:
                        
                        print(f"     {f"{hoeveelheid}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>8} {producten[product_uuid]}")
                        calorieën_totaal += producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
                        eiwitten_totaal += producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
                
                print(f"\n     {"SUBTOTAAL":<18} {f"{calorieën_totaal}":>9} {f"{eiwitten_totaal}":>8} ")
                
                for gerecht_uuid, versie_dict in self.gerechten.items():
                    
                    for versie_uuid, versie_hoeveelheid  in versie_dict.items():
                        versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                        print(f"\n     {versie_hoeveelheid} van {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
                        print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                        
                        aantal_porties = gerechten[gerecht_uuid].porties if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid].get("porties", gerechten[gerecht_uuid].porties)
                        
                        for product_uuid, hoeveelheden in gerechten[gerecht_uuid].producten(versie_uuid).items():
                    
                            for hoeveelheid in hoeveelheden:
                                
                                print(f"     {f"{hoeveelheid * versie_hoeveelheid.waarde/aantal_porties}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100 * versie_hoeveelheid.waarde/aantal_porties}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100 * versie_hoeveelheid.waarde/aantal_porties}":>8} {producten[product_uuid]}")
                        
                        print(f"\n     {"SUBTOTAAL":<18} {f"{gerechten[gerecht_uuid].voedingswaarde(versie_uuid).calorieën}":>9} {f"{gerechten[gerecht_uuid].voedingswaarde(versie_uuid).eiwitten}":>8} ")
                        
                print(f"\n\n     {"TOTAAL":<18} {f"{self.voedingswaarde.calorieën}":>9} {f"{self.voedingswaarde.eiwitten}":>8}")
            
            elif opdracht == "weergeef gerechten":
                
                if len(self.gerechten) == 0:
                    print(f"\n>>> geen gerechten aanwezig om te weergeven")
                    continue
                
                gerechten = Gerechten.openen()
                
                print(f"\n     HOEVEELHEID GERECHT")
                
                for gerecht_uuid, versie_dict in self.gerechten.items():
                    for versie_uuid, versie_hoeveelheid in versie_dict.items():
                        
                        versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
                        
                        print(f"     {f"{versie_hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
            
            elif opdracht == "weergeef voedingswaarde":
                
                if len(self.producten) == 0 and len(self.gerechten) == 0:
                    print(f"\n>>> geen producten of gerechten aanwezig om een voedingswaarde te berekenen")
                    continue
                
                print(f"\n     voedingswaarde voor {self}\n")
                print(self.voedingswaarde)
            
            elif opdracht == "kopiëren producten van andere dag":
                
                if self.datum == dt.date.today() - dt.timedelta(days = 2):
                
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "vandaag",
                            "gisteren",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                elif self.datum == dt.date.today() - dt.timedelta(days = 1):
                
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "vandaag",
                            "eergisteren",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                elif self.datum == dt.date.today():
                    
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "gisteren",
                            "eergisteren",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                elif self.datum == dt.date.today() + dt.timedelta(days = 1):
                    
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "vandaag",
                            "gisteren",
                            "eergisteren",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                elif self.datum == dt.date.today() + dt.timedelta(days = 2):
                    
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "vandaag",
                            "gisteren",
                            "eergisteren",
                            "morgen",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                else:
                    
                    opdracht_dag = invoer_kiezen(
                        "dag om van te kopiëren",
                        [
                            "vandaag",
                            "gisteren",
                            "eergisteren",
                            "morgen",
                            "overmorgen",
                            "aangepast",
                            ],
                        stoppen = True,
                        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                        )
                
                if opdracht_dag is STOP:
                    continue
                
                andere_dag = self.openen(opdracht_dag)
                
                if andere_dag.datum == self.datum:
                    print(f"\n>>> kan niet producten kopiëren van en naar dezelfde dag")
                    continue
                
                if len(andere_dag.producten) == 0:
                    print(f"\n>>> geen producten aanwezig bij {andere_dag}")
                    continue
                
                producten = Producten.openen()
                
                kies_optie = invoer_kiezen(
                    "één of meerdere product(en) om te kopiëren",
                    {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in andere_dag.producten.items() for hoeveelheid in hoeveelheden},
                    stoppen = True,
                    terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
                    meerdere_keuzes = True,
                    )
                
                if kies_optie is STOP:
                    continue
                
                print("")
                for product_uuid, hoeveelheid in kies_optie:
                    
                    if product_uuid in self.producten.keys():
                        for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(self.producten[product_uuid]):
                            if hoeveelheid == hoeveelheid_aanwezig:
                                self.producten[product_uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                                break
                        else:
                            self.producten[product_uuid].append(hoeveelheid)
                    else:
                        self.producten[product_uuid] = [hoeveelheid]
                    
                    print(f">>> {hoeveelheid} toegevoegd van {producten[product_uuid]}")
                
            
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
        
        for gerecht_uuid, versie_dict in self.gerechten.items():
            for versie_uuid, hoeveelheid in versie_dict.items():
                gerecht_voedingswaarde = gerechten[gerecht_uuid].voedingswaarde(versie_uuid) * hoeveelheid.waarde
                dag_voedingswaarde += gerecht_voedingswaarde
        
        return dag_voedingswaarde