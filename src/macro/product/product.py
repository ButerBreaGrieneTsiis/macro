"""macro.product.product"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.product import Hoofdcategorie, Categorie, Ingrediënt, Merk
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde


@dataclass
class Product(GeregistreerdObject):
    
    product_naam: str
    ingrediënt_uuid: str
    merk_uuid: str
    voedingswaarde: Voedingswaarde
    basis_eenheid: Eenheid
    eenheden: Dict[Eenheid, str] | None = None
    opmerking: str | None = None
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"product \"{self.product_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU PRODUCT",
        geef_id: bool = False,
        ) -> Product | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw product")
        
        ingrediënt_uuid = Ingrediënt.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = terug_naar,
            )
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is commando.DOORGAAN or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        product_naam = invoeren(
            tekst_beschrijving = "productnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if product_naam is commando.STOP:
            return commando.DOORGAAN
        
        merk_uuid = Merk.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = terug_naar,
            )
        if merk_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        opmerking = invoeren(
            tekst_beschrijving = "opmerking",
            invoer_type = "str",
            uitsluiten_leeg = False,
            valideren = False,
            uitvoer_kleine_letters = True,
            )
        if opmerking is commando.STOP:
            return commando.DOORGAAN
        
        basis_eenheid = kiezen(
            opties = {eenheid: Hoeveelheid(100.0, eenheid) for eenheid in Hoeveelheid._BASIS_EENHEDEN},
            tekst_beschrijving = "eenheid waarvoor voedingswaarden gelden",
            )
        if basis_eenheid is commando.STOP:
            return commando.DOORGAAN
        
        voedingswaarde = Voedingswaarde.nieuw(basis_eenheid)
        if voedingswaarde is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuw product \"{product_naam}\" gemaakt")
        
        product = cls(
            product_naam = product_naam,
            ingrediënt_uuid = ingrediënt_uuid,
            merk_uuid = merk_uuid,
            voedingswaarde = voedingswaarde,
            basis_eenheid = basis_eenheid,
            )
    
        if geef_id:
            return getattr(product, product._ID_VELD)
        return product
    
    # INSTANCE METHODS
    
    def bewerken(self) -> None:
        
        menu_bewerken = Menu(f"MENU BEWERKEN ({f"{self}".upper()})", "MENU PRODUCT", blijf_in_menu = True)
        menu_bewerken.toevoegen_optie(self.bewerken_naam, "naam")
        menu_bewerken.toevoegen_optie(self.bewerken_ingrediënt, "ingrediënt")
        menu_bewerken.toevoegen_optie(self.bewerken_merk, "merk")
        # menu_bewerken.toevoegen_optie(self.bewerken_eenheden, "eenheden")
        # menu_bewerken.toevoegen_optie(self.bewerken_voedingswaarde, "voedingswaarde")
        
        menu_bewerken()
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.product_naam
        product_naam = invoeren(
            tekst_beschrijving = "productnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if product_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.product_naam = product_naam
        print(f"\n>>> veld \"productnaam\" veranderd van \"{waarde_oud}\" naar \"{self.product_naam}\"")
        return commando.DOORGAAN
    
    def bewerken_merk(self) -> commando.Doorgaan:
        
        waarde_oud = self.merk
        merk_uuid = Merk.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if merk_uuid is commando.STOP or merk_uuid is None:
            return commando.DOORGAAN
        
        self.merk_uuid = merk_uuid
        print(f"\n>>> veld \"merk\" veranderd van \"{waarde_oud}\" naar \"{self.merk}\"")
        return commando.DOORGAAN
    
    def bewerken_ingrediënt(self) -> commando.Doorgaan:
        
        waarde_oud = self.ingrediënt
        ingrediënt_uuid = Ingrediënt.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        self.ingrediënt_uuid = ingrediënt_uuid
        print(f"\n>>> veld \"ingrediënt\" veranderd van \"{waarde_oud}\" naar \"{self.ingrediënt}\"")
        return commando.DOORGAAN
        
    def inspecteren(self) -> None:
        
        menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{self}".upper()})", "MENU INGREDIËNT", blijf_in_menu = True)
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.product_naam}"), "naam")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.hoofdcategorie}"), "hoofdcategorie")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.categorie}"), "categorie")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.ingrediënt}"), "ingrediënt")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.merk}"), "merk")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.eenheden}"), "eenheden")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.voedingswaarde}"), "voedingswaarde")
        
        menu_inspectie()
    
    # PROPERTIES
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return Hoofdcategorie.subregister()[self.categorie.hoofdcategorie_uuid]
    
    @property
    def categorie(self) -> Categorie:
        return Categorie.subregister()[self.ingrediënt.categorie_uuid]
    
    @property
    def ingrediënt(self) -> Ingrediënt:
        return Ingrediënt.subregister()[self.ingrediënt_uuid]
    
    @property
    def merk(self) -> Merk:
        return Merk.subregister()[self.merk_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Product._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU PRODUCT",
        ) -> str | commando.Stop | None:
        
        aantal_producten = len(Product.subregister())
        
        if aantal_producten == 0:
            print(f"\n>>> geen producten aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
            
            selectiemethode = "nieuw"
            
        if not selectiemethode:
            
            opties = {}
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw product"
            
            if aantal_producten > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie, categorie en ingrediënt"
                opties["zoeken"] = "zoeken op productnaam"
            
            selectiemethode = kiezen(
                opties = opties,
                tekst_beschrijving = "selectiemethode voor product",
                tekst_annuleren = terug_naar,
                )
            if selectiemethode is commando.STOP:
                return commando.STOP
        
        if selectiemethode == "nieuw":
            return Product.nieuw(
                terug_naar = terug_naar,
                geef_id = geef_id,
                )
        
        if aantal_producten == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            ingrediënt_uuid = Ingrediënt.selecteren(
                geef_id = True,
                toestaan_nieuw = toestaan_nieuw,
                selectiemethode = "selecteren",
                terug_naar = terug_naar,
                )
            if ingrediënt_uuid is commando.STOP:
                return commando.STOP
            
            return Product.subregister().filter(
                ingrediënt_uuid = ingrediënt_uuid,
            ).selecteren(
                geef_id = geef_id,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Product.subregister().zoeken(
            veld = "product_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven(
        terug_naar: str = "terug naar MENU PRODUCT",
        ) -> commando.Doorgaan:
        
        ingrediënt_uuid = Ingrediënt.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = terug_naar,
            )
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        Product.subregister().filter(
            ingrediënt_uuid = ingrediënt_uuid,
            ).weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        product_uuid = Product.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if product_uuid is commando.STOP or product_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Product.subregister()[product_uuid]}\" verwijderd")
        del Product.subregister()[product_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_bewerken() -> commando.Doorgaan:
        
        while True:
            
            product = Product.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if product is commando.STOP:
                return commando.DOORGAAN
            if product is None:
                continue
            
            product.bewerken()
            return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_inspecteren() -> commando.Doorgaan:
        
        while True:
            
            product = Product.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if product is commando.STOP:
                return commando.DOORGAAN
            if product is None:
                continue
            
            product.inspecteren()
            return commando.DOORGAAN