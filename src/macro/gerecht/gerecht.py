"""macro.gerecht.gerecht"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal, Tuple

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.gerecht import HoofdcategorieGerecht, CategorieGerecht, Variant, Recept
from macro.product import Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde


@dataclass
class Gerecht(GeregistreerdObject):
    
    gerecht_naam: str
    categorie_uuid: str
    producten_standaard: Dict[str, Dict[str, int]]
    porties: int
    varianten: Dict[str, Variant] | None = None
    recept: Recept | None = None
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"gerecht \"{self.gerecht_naam}\""
    
    def __post_init__(self) -> None:
        if self.varianten is None:
            self.varianten = {}
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU GERECHT",
        geef_id: bool = False,
        ) -> Gerecht | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw gerecht")
        
        categorie_uuid = CategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = terug_naar,
            )
        if categorie_uuid is commando.STOP or categorie_uuid is commando.DOORGAAN or categorie_uuid is None:
            return commando.DOORGAAN
        
        gerecht_naam = invoeren(
            tekst_beschrijving = "gerechtnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if gerecht_naam is commando.STOP:
            return commando.DOORGAAN
        
        producten_standaard = {}
        
        while True:
            
            if len(producten_standaard) > 0:
                
                calorieën_totaal = Hoeveelheid(0, Eenheid.KILOCALORIE)
                eiwitten_totaal = Hoeveelheid(0, Eenheid.GRAM)
                
                print(f"\n{"HOEVEELHEID":<20} CALORIEËN EIWITTEN PRODUCT")
                for product_uuid, hoeveelheden in producten_standaard.items():
                    
                    product = Product.subregister()[product_uuid]
                    
                    for eenheid_enkelvoud, waarde in hoeveelheden.items():
                        
                        eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                        hoeveelheid = Hoeveelheid(waarde, eenheid)
                        
                        print(f"{f"{hoeveelheid}":<19} {f"{product.voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>10} {f"{product.voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>8} {product}")
                        calorieën_totaal += product.voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100
                        eiwitten_totaal  += product.voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100
                
                print(f"\n{"TOTAAL":<19} {f"{calorieën_totaal}":>10} {f"{eiwitten_totaal}":>8}")
            
            product = Product.selecteren(
                geef_id = False,
                toestaan_nieuw = True,
                terug_naar = f"AFRONDEN GERECHT {gerecht_naam.upper()}",
                )
            if product is commando.STOP:
                break
            if product is None:
                continue
            
            eenheid = product.selecteren_eenheid(
                terug_naar = terug_naar,
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
            
            if product_uuid in producten_standaard.keys():
                for eenheid_aanwezig in producten_standaard[product_uuid]:
                    if eenheid.enkelvoud == eenheid_aanwezig:
                        producten_standaard[product_uuid][eenheid.enkelvoud] += waarde
                        break
                else:
                    producten_standaard[product_uuid][eenheid.enkelvoud] = waarde
            else:
                producten_standaard[product_uuid] = {eenheid.enkelvoud: waarde}
            
            print(f"\n>>> {hoeveelheid} toegevoegd van {product}")
        
        if len(producten_standaard) == 0:
            return commando.DOORGAAN
        
        porties = invoeren(
            tekst_beschrijving = f"hoeveel porties",
            invoer_type = "int",
            waardes_bereik = (1, 100),
            )
        if porties is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuw gerecht \"{gerecht_naam}\" gemaakt")
        
        gerecht = cls(
            gerecht_naam = gerecht_naam,
            categorie_uuid = categorie_uuid,
            producten_standaard = producten_standaard,
            porties = porties,
            )
    
        if geef_id:
            return gerecht._id
        return gerecht
    
    # INSTANCE METHODS
    
    def selecteren_product(
        self,
        terug_naar: str,
        tekst_beschrijving: str,
        geef_id: bool = True,
        geef_enum: bool = True,
        ) -> Tuple[str | Product, str | Eenheid] | commando.Stop:
        
        opties_product = {(product_uuid, eenheid_enkelvoud): f"{f"{Hoeveelheid(waarde, Eenheid.van_enkelvoud(eenheid_enkelvoud))}":<19} {Product.subregister()[product_uuid]}" for product_uuid, hoeveelheden in self.producten_standaard.items() for eenheid_enkelvoud, waarde in hoeveelheden.items()}
        
        keuze_product = kiezen(
            opties = opties_product,
            tekst_beschrijving = tekst_beschrijving,
            tekst_annuleren = terug_naar,
            )
        if keuze_product is commando.STOP:
            return commando.STOP
        
        product_uuid = keuze_product[0]
        eenheid_enkelvoud = keuze_product[1]
        
        return (
            product_uuid if geef_id else Product.subregister()[product_uuid],
            Eenheid.van_enkelvoud(eenheid_enkelvoud) if geef_enum else eenheid_enkelvoud,
            )
    
    def selecteren_variant(
        self,
        terug_naar: str,
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        ) -> Variant | str | commando.Stop:
        
        aantal_varianten = len(self.varianten)
        
        if aantal_varianten == 0:
            print(f"\n>>> geen varianten aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
        
        opties_varianten = {variant_uuid: f"{variant}" for variant_uuid, variant in self.varianten.items()}
        
        if toestaan_nieuw:
            opties_varianten |= {"nieuw": "nieuwe variant"}
        
        keuze_variant = kiezen(
            opties = opties_varianten,
            tekst_beschrijving = "variant",
            tekst_annuleren = terug_naar,
            )
        if keuze_variant is commando.STOP:
            return commando.STOP
        
        if keuze_variant == "nieuw":
            variant_uuid = Variant.nieuw(
                terug_naar = terug_naar,
                gerecht = self,
                geef_id = True,
                )
            if variant_uuid is commando.DOORGAAN:
                return commando.STOP
        else:
            variant_uuid = keuze_variant
        
        if geef_id:
            return variant_uuid
        return self.varianten[variant_uuid]
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.gerecht_naam
        gerecht_naam = invoeren(
            tekst_beschrijving = "gerechtnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if gerecht_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.gerecht_naam = gerecht_naam
        print(f"\n>>> veld \"gerechtnaam\" veranderd van \"{waarde_oud}\" naar \"{self.gerecht_naam}\"")
        return commando.DOORGAAN
    
    def bewerken_categorie(self) -> commando.Doorgaan:
        
        waarde_oud = self.categorie
        categorie_uuid = CategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        self.categorie_uuid = categorie_uuid
        print(f"\n>>> veld \"categorie\" veranderd van \"{waarde_oud}\" naar \"{self.categorie}\"")
        return commando.DOORGAAN
    
    def bewerken_producten(self) -> commando.Doorgaan:
        
        menu_bewerken_producten = Menu(f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})", f"MENU BEWERKEN ({f"{self}".upper()})", blijf_in_menu = True)
        menu_bewerken_producten.toevoegen_optie(self.bewerken_producten_toevoegen, "toevoegen producten")
        menu_bewerken_producten.toevoegen_optie(self.bewerken_producten_aanpassen, "aanpassen hoeveelheid producten")
        menu_bewerken_producten.toevoegen_optie(self.bewerken_producten_verwijderen, "verwijderen producten")
        menu_bewerken_producten.toevoegen_optie(self.inspecteren_producten, "inspecteren producten")
        
        menu_bewerken_producten()
        
        return commando.DOORGAAN
    
    def bewerken_producten_toevoegen(self) -> commando.Doorgaan:
        
        product = Product.selecteren(
            geef_id = False,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})",
            )
        if product is commando.STOP or product is None:
            return commando.DOORGAAN
        
        eenheid = product.selecteren_eenheid(
            terug_naar = f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})",
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
        
        if product_uuid in self.producten_standaard.keys():
            for eenheid_aanwezig in self.producten_standaard[product_uuid]:
                if eenheid.enkelvoud == eenheid_aanwezig:
                    self.producten_standaard[product_uuid][eenheid.enkelvoud] += waarde
                    break
            else:
                self.producten_standaard[product_uuid][eenheid.enkelvoud] = waarde
        else:
            self.producten_standaard[product_uuid] = {eenheid.enkelvoud: waarde}
        
        print(f"\n>>> {hoeveelheid} toegevoegd van {product}")
    
    def bewerken_producten_aanpassen(self) -> commando.Doorgaan:
        
        if len(self.producten_standaard) == 0:
            print(f"\n>>> geen producten aanwezig om de hoeveelheid van aan te passen")
            return commando.Doorgaan
        
        keuze_product = self.selecteren_product(
            terug_naar = f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})",
            tekst_beschrijving = "een product en hoeveelheid om aan te passen",
            geef_id = True,
            geef_enum = True,
            )
        if keuze_product is commando.STOP:
            return commando.Doorgaan
        
        product_uuid, eenheid_oud = keuze_product
        product = Product.subregister()[product_uuid]
        
        eenheid_nieuw = product.selecteren_eenheid(
            terug_naar = f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})",
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
        
        waarde_oud = self.producten_standaard[product_uuid][eenheid_oud.enkelvoud]
        hoeveelheid_oud = Hoeveelheid(waarde_oud, eenheid_oud)
        
        hoeveelheid_nieuw = Hoeveelheid(waarde_nieuw, eenheid_nieuw)
        
        print(f"\n>>> hoeveelheid {hoeveelheid_oud} aangepast naar {hoeveelheid_nieuw}")
        
        if eenheid_nieuw.enkelvoud in self.producten_standaard[product_uuid]:
            if eenheid_nieuw.enkelvoud != eenheid_oud.enkelvoud:
                self.producten_standaard[product_uuid][eenheid_nieuw.enkelvoud] += waarde_nieuw
                del self.producten_standaard[product_uuid][eenheid_oud.enkelvoud]
            else:
                self.producten_standaard[product_uuid][eenheid_nieuw.enkelvoud] = waarde_nieuw
        else:
            self.producten_standaard[product_uuid][eenheid_nieuw.enkelvoud] = waarde_nieuw
        
        return commando.DOORGAAN
    
    def bewerken_producten_verwijderen(self) -> commando.Doorgaan:
        
        if len(self.producten_standaard) == 0:
            print(f"\n>>> geen producten aanwezig om te verwijderen")
            return commando.Doorgaan
        
        product_selectie = self.selecteren_product(
            terug_naar = f"MENU BEWERKEN PRODUCTEN ({f"{self}".upper()})",
            tekst_beschrijving = "een product en hoeveelheid om te verwijderen",
            geef_id = True,
            geef_enum = True,
            )
        if product_selectie is commando.STOP:
            return commando.Doorgaan
        
        product_uuid, eenheid = product_selectie
        product = Product.subregister()[product_uuid]
        
        hoeveelheid = Hoeveelheid(self.producten_standaard[product_uuid][eenheid.enkelvoud], eenheid)
        
        print(f"\n>>> hoeveelheid {hoeveelheid} van {product} verwijderd")
        
        del self.producten_standaard[product_uuid][eenheid.enkelvoud]
        
        return commando.DOORGAAN
    
    def bewerken_porties(self) -> commando.Doorgaan:
        
        waarde_oud = self.porties
        porties = invoeren(
            tekst_beschrijving = f"hoeveel porties",
            invoer_type = "int",
            waardes_bereik = (1, 100),
            )
        if porties is commando.STOP:
            return commando.DOORGAAN
        
        self.porties = porties
        print(f"\n>>> veld \"porties\" veranderd van \"{waarde_oud}\" naar \"{self.porties}\"")
        return commando.DOORGAAN
    
    def bewerken_varianten(self) -> commando.Doorgaan:
        
        menu_bewerken_varianten = Menu(f"MENU BEWERKEN VARIANTEN ({f"{self}".upper()})", f"MENU BEWERKEN ({f"{self}".upper()})", blijf_in_menu = True)
        menu_bewerken_varianten.toevoegen_optie(self.bewerken_variant_nieuw, "nieuwe variant")
        menu_bewerken_varianten.toevoegen_optie(self.bewerken_variant_bewerken, "bewerken variant")
        menu_bewerken_varianten.toevoegen_optie(self.bewerken_variant_verwijderen, "verwijderen variant")
        
        menu_bewerken_varianten()
        
        return commando.DOORGAAN
    
    def bewerken_variant_nieuw(self) -> commando.Doorgaan:
        
        variant = Variant.nieuw(
            terug_naar = f"MENU BEWERKEN VARIANTEN ({f"{self}".upper()})",
            gerecht = self,
            geef_id = False,
            )
        if variant is commando.DOORGAAN:
            return commando.STOP
        
        return commando.DOORGAAN
        
    def bewerken_variant_bewerken(self) -> commando.Doorgaan:
        
        variant = self.selecteren_variant(
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            geef_id = False,
            toestaan_nieuw = False,
            )
        if variant is commando.STOP:
            return commando.DOORGAAN
        
        variant.bewerken(
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            gerecht = self,
            )
        
        return commando.DOORGAAN
    
    def bewerken_variant_verwijderen(self) -> commando.Doorgaan:
        
        variant_uuid = self.selecteren_variant(
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            geef_id = True,
            toestaan_nieuw = False,
            )
        if variant_uuid is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> {self.varianten[variant_uuid]} van {self} verwijderd")
        
        del self.varianten[variant_uuid]
        
        return commando.DOORGAAN
    
    def bewerken_recept(self) -> commando.Doorgaan: ... # TODO
    
    def inspecteren_varianten(self) -> None:
        
        variant_uuid = self.selecteren_variant(
            terug_naar = f"MENU INSPECTEREN ({f"{self}".upper()})",
            geef_id = True,
            toestaan_nieuw = False,
            )
        if variant_uuid is commando.STOP:
            return commando.DOORGAAN
        
        variant = self.varianten[variant_uuid]
        
        inspecteer_opties = [
            "toevoegingen",
            "verwijderingen",
            "aanpassingen",
            "porties",
            "resulterende producten",
            "resulterende voedingswaarde",
            ]
        
        while True:
        
            keuze_bewerken = kiezen(
                opties = inspecteer_opties,
                tekst_beschrijving = f"MENU INSPECTEREN VARIANT ({f"{variant}".upper()})",
                tekst_annuleren = f"MENU INSPECTEREN ({f"{self}".upper()})",
                )
            
            if keuze_bewerken is commando.STOP:
                return commando.DOORGAAN
            
            elif keuze_bewerken == "toevoegingen":
                variant.inspecteren_toevoeging()
            
            elif keuze_bewerken == "verwijderingen":
                variant.inspecteren_verwijdering()
            
            elif keuze_bewerken == "aanpassingen":
                variant.inspecteren_aanpassing(gerecht = self)
            
            elif keuze_bewerken == "porties":
                variant.inspecteren_porties()
            
            elif keuze_bewerken == "resulterende producten":
                self.inspecteren_producten(variant_uuid = variant_uuid)
            
            elif keuze_bewerken == "resulterende voedingswaarde":
                self.inspecteren_voedingswaarde(variant_uuid = variant_uuid)
    
    def inspecteren_producten(
        self,
        variant_uuid: str = "standaard",
        ) -> None:
        
        producten = self.producten(variant_uuid = variant_uuid)
        
        variant_naam = "standaard"
        print(f"\n{self} (variant \"{variant_naam}\")")
        print(f"\n{"HOEVEELHEID":<20} CALORIEËN EIWITTEN PRODUCT")
        
        for product_uuid, hoeveelheden in producten.items():
            
            product = Product.subregister()[product_uuid]
            
            for eenheid_enkelvoud, waarde in hoeveelheden.items():
            
                eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                hoeveelheid = Hoeveelheid(waarde, eenheid)
                print(f"{f"{hoeveelheid}":<19} {f"{product.voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>10} {f"{product.voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid._BASIS_EENHEDEN else hoeveelheid.waarde * product.eenheden[eenheid_enkelvoud]) / 100}":>8} {product}")
        
        aantal_porties = self.porties
        print(f"\n{"TOTAAL":<19} {f"{self.bereken_voedingswaarde().calorieën*aantal_porties}":>10} {f"{self.bereken_voedingswaarde().eiwitten*aantal_porties}":>8} (voor {aantal_porties} porties)")
        print(f"{"PER PORTIE":<19} {f"{self.bereken_voedingswaarde().calorieën}":>10} {f"{self.bereken_voedingswaarde().eiwitten}":>8}")
    
    def inspecteren_voedingswaarde(
        self,
        variant_uuid: str = "standaard",
        ) -> None:
        
        voedingswaarde = self.bereken_voedingswaarde(variant_uuid = variant_uuid)
        
        if variant_uuid == "standaard":
            print(f"\nvoedingswaarde voor {self} per portie ({self.porties} porties):\n\n{voedingswaarde}")
        
        else:
            variant = self.varianten[variant_uuid]
            aantal_porties = variant.porties if variant.porties else self.porties
            print(f"\nvoedingswaarde voor {variant} van {self} per portie ({aantal_porties} porties):\n\n{voedingswaarde}")
    
    def producten(
        self,
        variant_uuid: str = "standaard",
        ) -> Dict[str, Dict[str, float]]:
        
        producten = {**self.producten_standaard}
        
        if variant_uuid != "standaard":
            
            for product_uuid, hoeveelheden in self.varianten[variant_uuid].toevoeging.items():
                for eenheid_enkelvoud, waarde in hoeveelheden.items():
                    if product_uuid not in producten.keys():
                        producten[product_uuid] = {eenheid_enkelvoud: waarde}
                    else:
                        producten[product_uuid][eenheid_enkelvoud] = waarde
            
            for product_uuid, hoeveelheden in self.varianten[variant_uuid].verwijdering.items():
                for eenheid_enkelvoud in hoeveelheden:
                    del producten[product_uuid][eenheid_enkelvoud]
            
            for product_uuid, hoeveelheden in self.varianten[variant_uuid].aanpassing.items():
                for eenheid_enkelvoud, waarde in hoeveelheden.items():
                    producten[product_uuid][eenheid_enkelvoud] = waarde
        
        return producten
    
    def bereken_voedingswaarde(
        self,
        variant_uuid: str = "standaard",
        ) -> Voedingswaarde:
        
        producten = self.producten(variant_uuid = variant_uuid)
        
        gerecht_voedingswaarde = Voedingswaarde()
        
        for product_uuid, hoeveelheden in producten.items():
            
            product = Product.subregister()[product_uuid]
            
            for eenheid_enkelvoud, waarde in hoeveelheden.items():
            
                eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                hoeveelheid = Hoeveelheid(waarde, eenheid)
                
                product_voedingswaarde = product.bereken_voedingswaarde(hoeveelheid)
                gerecht_voedingswaarde += product_voedingswaarde
        
        aantal_porties = self.porties
        gerecht_voedingswaarde /= aantal_porties
        
        return gerecht_voedingswaarde
    
    # PROPERTIES
    
    @property
    def hoofdcategorie(self) -> HoofdcategorieGerecht:
        return HoofdcategorieGerecht.subregister()[self.categorie.hoofdcategorie_uuid]
    
    @property
    def categorie(self) -> CategorieGerecht:
        return CategorieGerecht.subregister()[self.categorie_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register[Gerecht._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU GERECHT",
        ) -> str | commando.Stop | None:
        
        aantal_gerechten = len(Gerecht.subregister())
        
        if aantal_gerechten == 0:
            print(f"\n>>> geen gerechten aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
            
            selectiemethode = "nieuw"
            
        if not selectiemethode:
            
            opties = {}
            
            if aantal_gerechten > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie en categorie"
                opties["zoeken"] = "zoeken op gerechtnaam"
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw gerecht"
            
            selectiemethode = kiezen(
                opties = opties,
                tekst_beschrijving = "selectiemethode voor gerecht",
                tekst_annuleren = terug_naar,
                )
            if selectiemethode is commando.STOP:
                return commando.STOP
        
        if selectiemethode == "nieuw":
            return Gerecht.nieuw(
                terug_naar = terug_naar,
                geef_id = geef_id,
                )
        
        if aantal_gerechten == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            categorie_uuid = CategorieGerecht.selecteren(
                geef_id = True,
                toestaan_nieuw = toestaan_nieuw,
                selectiemethode = "selecteren",
                terug_naar = terug_naar,
                )
            if categorie_uuid is commando.STOP:
                return commando.STOP
            
            return Gerecht.subregister().filter(
                categorie_uuid = categorie_uuid,
            ).selecteren(
                geef_id = geef_id,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        print()
        return Gerecht.subregister().zoeken(
            veld = "gerecht_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven_alle() -> commando.Stop:
        
        print("\nALLE GERECHTEN:\n")
        
        for hoofdcategorie_uuid, hoofdcategorie in HoofdcategorieGerecht.subregister().items():
            
            print(hoofdcategorie)
            
            for categorie_uuid, categorie in CategorieGerecht.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_uuid,
                ).items():
                
                print(f"  {categorie}")
                
                for gerecht in Gerecht.subregister().filter(
                    categorie_uuid = categorie_uuid,
                    ).lijst:
                    
                    print(f"    {gerecht}")
        
        return commando.STOP
    
    @staticmethod
    def weergeven_voor_hoofdcategorie() -> commando.Doorgaan | commando.Stop:
        
        hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = "terug naar MENU GERECHT",
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        hoofdcategorie = HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid]
        print(f"\nALLE GERECHTEN VOOR {f"{hoofdcategorie}".upper()}:\n")
        
        for categorie_uuid, categorie in CategorieGerecht.subregister().filter(
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            ).items():
            
            print(f"{categorie}")
            
            for gerecht in Gerecht.subregister().filter(
                categorie_uuid = categorie_uuid,
                ).lijst:
                
                print(f"  {gerecht}")
        
        return commando.STOP
    
    @staticmethod
    def weergeven_voor_categorie() -> commando.Doorgaan | commando.Stop:
        
        categorie_uuid = CategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = "terug naar MENU GERECHT",
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        categorie = CategorieGerecht.subregister()[categorie_uuid]
        print(f"\nALLE GERECHTEN VOOR {f"{categorie}".upper()}:\n")
        
        for gerecht in Gerecht.subregister().filter(
            categorie_uuid = categorie_uuid,
            ).lijst:
            
            print(f"{gerecht}")
        
        return commando.STOP
    
    @staticmethod
    def bewerken() -> commando.Doorgaan:
        
        while True:
            
            gerecht: Gerecht = Gerecht.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if gerecht is commando.STOP:
                return commando.DOORGAAN
            if gerecht is None:
                continue
            
            menu_bewerken = Menu(f"MENU BEWERKEN ({f"{gerecht}".upper()})", "MENU GERECHT", blijf_in_menu = True)
            menu_bewerken.toevoegen_optie(gerecht.bewerken_naam, "naam")
            menu_bewerken.toevoegen_optie(gerecht.bewerken_categorie, "categorie")
            menu_bewerken.toevoegen_optie(gerecht.bewerken_producten, "producten")
            menu_bewerken.toevoegen_optie(gerecht.bewerken_porties, "porties")
            menu_bewerken.toevoegen_optie(gerecht.bewerken_varianten, "varianten")
            menu_bewerken.toevoegen_optie(gerecht.bewerken_recept, "recept")
            
            menu_bewerken()
        
            return commando.DOORGAAN
    
    @staticmethod
    def inspecteren() -> commando.Doorgaan:
        
        while True:
            
            gerecht: Gerecht = Gerecht.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if gerecht is commando.STOP:
                return commando.DOORGAAN
            if gerecht is None:
                continue
            
            menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{gerecht}".upper()})", "MENU GERECHT", blijf_in_menu = True)
            menu_inspectie.toevoegen_optie(lambda: print(f"\nnaam voor {gerecht}:\n>>> {gerecht.gerecht_naam}"), "naam")
            menu_inspectie.toevoegen_optie(lambda: print(f"\nhoofdcategorie voor {gerecht}:\n>>> {gerecht.hoofdcategorie}"), "hoofdcategorie")
            menu_inspectie.toevoegen_optie(lambda: print(f"\ncategorie voor {gerecht}:\n>>> {gerecht.categorie}"), "categorie")
            menu_inspectie.toevoegen_optie(gerecht.inspecteren_producten, "producten")
            menu_inspectie.toevoegen_optie(gerecht.inspecteren_voedingswaarde, "voedingswaarde")
            menu_inspectie.toevoegen_optie(gerecht.inspecteren_varianten, "varianten")
            menu_inspectie.toevoegen_optie(lambda: print(f"\nrecept voor {gerecht}:\n>>> {gerecht.recept}"), "recept")
            
            menu_inspectie()
            
            return commando.DOORGAAN
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        
        menu_weergeven = Menu(f"MENU WEERGEVEN GERECHT", "MENU GERECHT", blijf_in_menu = True)
        menu_weergeven.toevoegen_optie(Gerecht.weergeven_alle, "alle gerechten")
        menu_weergeven.toevoegen_optie(Gerecht.weergeven_voor_hoofdcategorie, "gerechten voor hoofdcategorie")
        menu_weergeven.toevoegen_optie(Gerecht.weergeven_voor_categorie, "gerechten voor categorie")
        
        menu_weergeven()
        
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        gerecht_uuid = Gerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if gerecht_uuid is commando.STOP or gerecht_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Gerecht.subregister()[gerecht_uuid]}\" verwijderd")
        del Gerecht.subregister()[gerecht_uuid]
        return commando.DOORGAAN