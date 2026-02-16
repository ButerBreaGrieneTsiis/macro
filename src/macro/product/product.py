"""macro.product.product"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Dict, List

from grienetsiis.opdrachtprompt import invoeren, kiezen, Menu, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.categorie import Hoofdcategorie, Categorie
from macro.product import Ingrediënt, Merk
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
    
    _SUBREGISTER_NAAM: ClassVar[str] = "product"
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"product \"{self.product_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU GEGEVENS PRODUCT",
        ) -> Product | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw product")
        
        ingrediënt_uuid = Ingrediënt.selecteren(terug_naar = terug_naar)
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
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
        
        merk_uuid = Merk.selecteren(terug_naar = terug_naar)
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
        
        return cls(
            product_naam = product_naam,
            ingrediënt_uuid = ingrediënt_uuid,
            merk_uuid = merk_uuid,
            voedingswaarde = voedingswaarde,
            basis_eenheid = basis_eenheid,
            )
    
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
    
    # @staticmethod
    # def selecteren(
    #     toestaan_nieuw: bool = True,
    #     terug_naar: str = "terug naar MENU GEGEVENS PRODUCT",
    #     ) -> str | commando.Stop | None:
        
    #     if len(Ingrediënt.subregister()) == 0:
    #         print(f"\n>>> geen product aanwezig")
    #         return None
        
    #     keuze_selecteren = kiezen(
    #         opties = [
    #             "selecteren via categorie",
    #             "selecteren op productnaam",
    #             ],
    #         tekst_beschrijving = "selectiemethode",
    #         tekst_annuleren = terug_naar,
    #         )
        
    #     if keuze_selecteren is commando.STOP:
    #         return commando.STOP
        
    #     if keuze_selecteren == "selecteren via categorie":
            
    #         categorie_uuid = Categorie.selecteren(
    #             toestaan_nieuw = toestaan_nieuw,
    #             terug_naar = terug_naar,
    #             )
            
    #         return Ingrediënt.subregister().filter(
    #             categorie_uuid = categorie_uuid,
    #         ).selecteren(
    #             toestaan_nieuw = toestaan_nieuw,
    #             terug_naar = terug_naar,
    #             )
        
    #     return Ingrediënt.subregister().zoeken(veld = "ingrediënt_naam")
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Product.subregister().weergeven()
        return commando.DOORGAAN
    
    # @staticmethod
    # def verwijderen() -> commando.Doorgaan:
        
    #     ingrediënt_uuid = Ingrediënt.selecteren(toestaan_nieuw = False)
    #     if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
    #         return commando.DOORGAAN
        
    #     print(f">>> \"{Ingrediënt.subregister()[ingrediënt_uuid]}\" verwijderd")
    #     del Ingrediënt.subregister()[ingrediënt_uuid]
    #     return commando.DOORGAAN
    
    # @staticmethod
    # def bewerken() -> commando.Doorgaan | None:
        
    #     ingrediënt_uuid = Ingrediënt.selecteren(toestaan_nieuw = False)
    #     if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
    #         return commando.DOORGAAN
        
    #     veld = Ingrediënt.kiezen_veld()
    #     if veld is commando.STOP:
    #         return commando.DOORGAAN
        
    #     waarde_nieuw = invoeren(
    #         tekst_beschrijving = veld,
    #         invoer_type = Ingrediënt.velden()[veld],
    #         uitsluiten_leeg = True,
    #         valideren = True,
    #         uitvoer_kleine_letters = True,
    #         )
        
    #     if waarde_nieuw is commando.STOP:
    #         return commando.DOORGAAN 
        
    #     waarde_oud = getattr(Ingrediënt.subregister()[ingrediënt_uuid], veld)
        
    #     print(f"\n>>> veld \"{veld}\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
    #     setattr(Ingrediënt.subregister()[ingrediënt_uuid], veld, waarde_nieuw)
    #     return commando.DOORGAAN
    
    # @staticmethod
    # def kiezen_veld() -> str | commando.Stop:
    #     return kiezen(
    #         opties = Ingrediënt.velden(),
    #         tekst_beschrijving = "veld om te bewerken",
    #         )
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_product = Menu("MENU GEGEVENS PRODUCT", super_menu, True)
        
        super_menu.toevoegen_optie(menu_product, "menu product")
        
        menu_product.toevoegen_optie(Product.nieuw, "nieuwe product")
        # menu_product.toevoegen_optie(Product.bewerken, "bewerken product")
        # menu_product.toevoegen_optie(Product.verwijderen, "verwijderen product")
        menu_product.toevoegen_optie(Product.weergeven, "weergeven product")
        
        return menu_product
    
    @staticmethod
    def velden() -> List[str]:
        return [veld for veld in Product.__annotations__ if not veld.startswith("_")]