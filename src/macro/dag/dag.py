"""macro.dag.dag"""
from __future__ import annotations
from calendar import monthrange
from dataclasses import dataclass
import datetime as dt
import locale
from typing import ClassVar, Dict, List, Tuple

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.product import Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde


locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")

@dataclass
class Dag(GeregistreerdObject):
    
    datum: dt.date
    producten: Dict[str, Dict[str, float]] | None = None
    gerechten: Dict[str, Hoeveelheid] | None = None
    
    _HUIDIGE_DAG: ClassVar[dt.date] = dt.date.today()
    
    # DUNDER METHODS
    
    def __post_init__(self) -> None:
        if self.producten is None:
            self.producten = {}
        if self.gerechten is None:
            self.gerechten = {}
    
    def __repr__(self) -> str:
        if len(self.producten) == 0:
            return f"dag \"{self.dag}\""
        else:
            return f"dag \"{self.dag}\" van {self.voedingswaarde.calorieën}"
    
    # INSTANCE METHODS
    
    def selecteren_product(
        self,
        terug_naar: str,
        tekst_beschrijving: str,
        geef_id: bool = True,
        geef_enum: bool = True,
        keuze_meerdere: bool = False,
        ) -> Tuple[str | Product, str | Eenheid] | List[Tuple[str | Product, str | Eenheid]] | commando.Stop:
        
        opties_product = {(product_uuid, eenheid_enkelvoud): f"{f"{Hoeveelheid(waarde, Eenheid.van_enkelvoud(eenheid_enkelvoud))}":<18} {Product.subregister()[product_uuid]}" for product_uuid, hoeveelheden in self.producten.items() for eenheid_enkelvoud, waarde in hoeveelheden.items()}
        
        keuze_product = kiezen(
            opties = opties_product,
            tekst_beschrijving = tekst_beschrijving,
            tekst_annuleren = terug_naar,
            keuze_meerdere = keuze_meerdere,
            )
        if keuze_product is commando.STOP:
            return commando.STOP
        
        if not keuze_meerdere:
            
            product_uuid = keuze_product[0]
            eenheid_enkelvoud = keuze_product[1]
            
            return (
                product_uuid if geef_id else Product.subregister()[product_uuid],
                Eenheid.van_enkelvoud(eenheid_enkelvoud) if geef_enum else eenheid_enkelvoud,
                )
        
        lijst = []
        
        for product_uuid, eenheid_enkelvoud in keuze_product:
            
            lijst.append((
                product_uuid if geef_id else Product.subregister()[product_uuid],
                Eenheid.van_enkelvoud(eenheid_enkelvoud) if geef_enum else eenheid_enkelvoud,
                ))
        
        return lijst
    
    def selecteren_gerecht(self) -> Tuple[str, str] | commando.Stop:
        ...
    
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
    
    @property
    def voedingswaarde(self) -> Voedingswaarde:
        
        dag_voedingswaarde = Voedingswaarde()
        
        for product_uuid, hoeveelheden in self.producten.items():
            
            product = Product.subregister()[product_uuid]
            
            for eenheid_enkelvoud, waarde in hoeveelheden.items():
                
                eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                hoeveelheid = Hoeveelheid(waarde, eenheid)
                
                product_voedingswaarde = product.bereken_voedingswaarde(hoeveelheid)
                dag_voedingswaarde += product_voedingswaarde
        
        # for gerecht_uuid, versie_dict in self.gerechten.items():
        #     for versie_uuid, hoeveelheid in versie_dict.items():
        #         gerecht_voedingswaarde = Gerecht.subregister()[gerecht_uuid].voedingswaarde(versie_uuid) * hoeveelheid.waarde
        #         dag_voedingswaarde += gerecht_voedingswaarde
        
        return dag_voedingswaarde
    
    # STATIC METHODS
    
    @staticmethod
    def titel() -> str:
        return f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}"
    
    @staticmethod
    def subregister() -> Subregister:
        return Register[Dag._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren_dag(
        datum: dt.date = dt.date.today(),
        ) -> str | commando.Stop | None:
        
        datum_tekst = datum.strftime("%Y-%m-%d")
        
        if datum_tekst in Dag.subregister():
            return Dag.subregister()[datum_tekst]
        
        else:
            
            if datum_tekst in Dag.subregister().geregistreerde_instanties:
                return Register.openen_instantie(
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
    def selecteren_datum(
        vandaag: bool = True,
        morgen: bool = True,
        overmorgen: bool = True,
        gisteren: bool = True,
        eergisteren: bool = True,
        aangepast: bool = True,
        ) -> dt.date | commando.Stop:
        
        opties = {}
        
        if vandaag: opties[dt.date.today()] = f"vandaag ({dt.date.today().strftime("%A %d %B %Y")})"
        if morgen: opties[dt.date.today() + dt.timedelta(days = 1)] = f"morgen ({(dt.date.today() + dt.timedelta(days = 1)).strftime("%A %d %B %Y")})"
        if overmorgen: opties[dt.date.today() + dt.timedelta(days = 2)] = f"overmorgen ({(dt.date.today() + dt.timedelta(days = 2)).strftime("%A %d %B %Y")})"
        if gisteren: opties[dt.date.today() - dt.timedelta(days = 1)] = f"gisteren ({(dt.date.today() - dt.timedelta(days = 1)).strftime("%A %d %B %Y")})"
        if eergisteren: opties[dt.date.today() - dt.timedelta(days = 2)] = f"eergisteren ({(dt.date.today() - dt.timedelta(days = 2)).strftime("%A %d %B %Y")})"
        if aangepast: opties["aangepast"] = f"aangepast ({(dt.date.today() - dt.timedelta(days = 2)).strftime("%A %d %B %Y")})"
        
        keuze_datum = kiezen(
            opties = opties,
            tekst_beschrijving = "dag",
            tekst_annuleren = f"MENU DAG {Dag._HUIDIGE_DAG.strftime("%A %d %B %Y").upper()}",
            )
        if keuze_datum is commando.STOP:
            return commando.STOP
        
        if keuze_datum != "aangepast":
            return keuze_datum
        
        jaar = invoeren(
            tekst_beschrijving = "jaar",
            invoer_type = "int",
            waardes_bereik = (1970, dt.datetime.today().year)
            )
        if jaar is commando.STOP:
            return commando.STOP
        
        maand = invoeren(
            tekst_beschrijving = "maand",
            invoer_type = "int",
            waardes_bereik = (1, 12)
            )
        if maand is commando.STOP:
            return commando.STOP
        
        dag = invoeren(
            tekst_beschrijving = "dag",
            invoer_type = "int",
            waardes_bereik = (1, monthrange(jaar, maand)[1])
            )
        if dag is commando.STOP:
            return commando.STOP
        
        return dt.date(jaar, maand, dag)
    
    @staticmethod
    def toevoegen_product() -> commando.Doorgaan:
        
        dag = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        
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
                geef_enum = True,
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
            
            if product_uuid in dag.producten.keys():
                for eenheid_aanwezig in dag.producten[product_uuid]:
                    if eenheid.enkelvoud == eenheid_aanwezig:
                        dag.producten[product_uuid][eenheid.enkelvoud] += waarde
                        break
                else:
                    dag.producten[product_uuid][eenheid.enkelvoud] = waarde
            else:
                dag.producten[product_uuid] = {eenheid.enkelvoud: waarde}
            
            print(f"\n>>> {hoeveelheid} toegevoegd van {product}")
    
    @staticmethod
    def toevoegen_gerecht() -> commando.Doorgaan:
        ...
    
    @staticmethod
    def aanpassen_product() -> commando.Doorgaan:
        
        dag = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        
        if len(dag.producten) == 0:
            print(f"\n>>> geen producten aanwezig om de hoeveelheid van aan te passen")
            return commando.Doorgaan
        
        keuze_product = dag.selecteren_product(
            terug_naar = Dag.titel(),
            tekst_beschrijving = "een product en hoeveelheid om aan te passen",
            geef_id = True,
            geef_enum = True,
            keuze_meerdere = False,
            )
        if keuze_product is commando.STOP:
            return commando.Doorgaan
        
        product_uuid, eenheid_oud = keuze_product
        product = Product.subregister()[product_uuid]
        
        eenheid_nieuw = product.selecteren_eenheid(
            terug_naar = Dag.titel(),
            geef_enum = True,
            toestaan_nieuw = True,
            )
        if eenheid_nieuw is commando.STOP:
            return commando.Doorgaan
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = f"hoeveel {eenheid_nieuw.meervoud}",
            invoer_type = "float",
            )
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN
        
        waarde_oud = dag.producten[product_uuid][eenheid_oud.enkelvoud]
        hoeveelheid_oud = Hoeveelheid(waarde_oud, eenheid_oud)
        
        hoeveelheid_nieuw = Hoeveelheid(waarde_nieuw, eenheid_nieuw)
        
        print(f"\n>>> hoeveelheid {hoeveelheid_oud} aangepast naar {hoeveelheid_nieuw}")
        
        if eenheid_nieuw.enkelvoud in dag.producten[product_uuid]:
            if eenheid_nieuw.enkelvoud != eenheid_oud.enkelvoud:
                dag.producten[product_uuid][eenheid_nieuw.enkelvoud] += waarde_nieuw
                del dag.producten[product_uuid][eenheid_oud.enkelvoud]
            else:
                dag.producten[product_uuid][eenheid_nieuw.enkelvoud] = waarde_nieuw
        else:
            dag.producten[product_uuid][eenheid_nieuw.enkelvoud] = waarde_nieuw
        
        return commando.DOORGAAN
    
    @staticmethod
    def aanpassen_gerecht() -> commando.Doorgaan:
        ...
    
    @staticmethod
    def weergeven_product() -> commando.Doorgaan:
        
        dag = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        
        if len(dag.producten) == 0 and len(dag.gerechten) == 0:
            print(f"\n>>> geen producten of gerechten aanwezig om te weergeven")
            return commando.Doorgaan
        
        if len(dag.producten) > 0:
            print("\nlos toegevoegde producten")
            print(f"\n{"HOEVEELHEID":<20} CALORIEËN EIWITTEN PRODUCT")
        
        calorieën_totaal    =   Hoeveelheid(0, Eenheid.KILOCALORIE)
        eiwitten_totaal     =   Hoeveelheid(0, Eenheid.GRAM)
        
        for product_uuid, hoeveelheden in dag.producten.items():
            
            product = Product.subregister()[product_uuid]
            
            for eenheid_enkelvoud, waarde in hoeveelheden.items():
                
                eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                hoeveelheid = Hoeveelheid(waarde, eenheid)
                
                print(f"{f"{hoeveelheid}":<19} {f"{product.voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>10} {f"{product.voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>8} {product}")
                calorieën_totaal += product.voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100
                eiwitten_totaal += product.voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100
        
        print(f"\n{"SUBTOTAAL":<19} {f"{calorieën_totaal}":>10} {f"{eiwitten_totaal}":>8} ")
        
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
    def weergeven_gerecht() -> commando.Doorgaan:
        ...
    
    @staticmethod
    def weergeven_voedingswaarde() -> commando.Doorgaan:
        
        dag = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        
        if len(dag.producten) == 0 and len(dag.gerechten) == 0:
            print(f"\n>>> geen producten of gerechten aanwezig om voedingswaarde voor te berekenen")
            return commando.Doorgaan
        
        print(f"\nvoedingswaarde voor {dag}\n")
        print(dag.voedingswaarde)
    
    @staticmethod
    def verwijderen_product() -> commando.Doorgaan:
        
        dag = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        
        if len(dag.producten) == 0:
            print(f"\n>>> geen producten aanwezig om te verwijderen")
            return commando.Doorgaan
        
        product_selectie = dag.selecteren_product(
            terug_naar = Dag.titel(),
            tekst_beschrijving = "een product en hoeveelheid om te verwijderen",
            geef_id = True,
            geef_enum = True,
            )
        if product_selectie is commando.STOP:
            return commando.Doorgaan
        
        product_uuid, eenheid = product_selectie
        product = Product.subregister()[product_uuid]
        
        hoeveelheid = Hoeveelheid(dag.producten[product_uuid][eenheid.enkelvoud], eenheid)
        
        print(f"\n>>> hoeveelheid {hoeveelheid} van {product} verwijderd")
        
        del dag.producten[product_uuid][eenheid.enkelvoud]
        
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen_gerecht() -> commando.Doorgaan:
        ...
    
    @staticmethod
    def kopiëren_product() -> commando.Doorgaan:
        
        datum_ander = Dag.selecteren_datum(
            vandaag = Dag._HUIDIGE_DAG != dt.date.today(),
            morgen = False,
            overmorgen = False,
            gisteren = Dag._HUIDIGE_DAG != dt.date.today() - dt.timedelta(days = 1),
            eergisteren = Dag._HUIDIGE_DAG != dt.date.today() - dt.timedelta(days = 2),
            )
        if datum_ander is commando.STOP:
            return commando.DOORGAAN
        
        dag_huidig = Dag.selecteren_dag(datum = Dag._HUIDIGE_DAG)
        dag_ander = Dag.selecteren_dag(datum = datum_ander)
        
        if len(dag_ander.producten) == 0:
            print(f"\n>>> geen producten aanwezig bij {dag_ander}")
            return commando.Doorgaan
        
        keuze_producten = dag_ander.selecteren_product(
            terug_naar = Dag.titel(),
            tekst_beschrijving = "één of meerdere product(en) om te kopiëren",
            geef_id = True,
            geef_enum = True,
            keuze_meerdere = True,
            )
        if keuze_producten is commando.STOP:
            return commando.Doorgaan
        
        print("")
        for product_uuid, eenheid in keuze_producten:
            
            waarde = dag_ander.producten[product_uuid][eenheid.enkelvoud]
            hoeveelheid = Hoeveelheid(waarde, eenheid)
            
            product = Product.subregister()[product_uuid]
            
            if product_uuid in dag_huidig.producten.keys():
                for eenheid_huidig in dag_huidig.producten[product_uuid].keys():
                    if eenheid.enkelvoud == eenheid_huidig:
                        dag_huidig.producten[product_uuid][eenheid.enkelvoud] += waarde
                        break
                else:
                    dag_huidig.producten[product_uuid][eenheid.enkelvoud] = waarde
            else:
                dag_huidig.producten[product_uuid] = {eenheid.enkelvoud: waarde}
            
            print(f">>> {hoeveelheid} toegevoegd van {product}")
    
    @staticmethod
    def veranderen_dag() -> commando.Doorgaan:
        
        datum = Dag.selecteren_datum()
        if datum is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> datum veranderd van \"{Dag._HUIDIGE_DAG}\" naar \"{datum}\"")
        Dag._HUIDIGE_DAG = datum
        return commando.DOORGAAN