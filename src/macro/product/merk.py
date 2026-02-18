"""macro.product.merk"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from grienetsiis.opdrachtprompt import invoeren, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject


@dataclass
class Merk(GeregistreerdObject):
    
    merk_naam: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"merk \"{self.merk_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        geef_id: bool = False,
        ) -> Merk | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw merk")
        
        merk_naam = invoeren(
            tekst_beschrijving = "merknaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        if merk_naam is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuw merk \"{merk_naam}\" gemaakt")
        
        merk = cls(
            merk_naam = merk_naam,
            )
        
        if geef_id:
            return merk._id
        return merk
    
    # INSTANCE METHODS
    
    def bewerken(self) -> None:
        
        menu_bewerken = Menu(f"MENU BEWERKEN ({f"{self}".upper()})", "MENU MERK", blijf_in_menu = True)
        menu_bewerken.toevoegen_optie(self.bewerken_naam, "naam")
        
        menu_bewerken()
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.hoofdcategorie_naam
        merk_naam = invoeren(
            tekst_beschrijving = "merknaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if merk_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.merk_naam = merk_naam
        print(f"\n>>> veld \"merknaam\" veranderd van \"{waarde_oud}\" naar \"{self.merk_naam}\"")
        return commando.DOORGAAN
    
    def inspecteren(self) -> None:
        
        menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{self}".upper()})", "MENU MERK", blijf_in_menu = True)
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.merk_naam}"), "naam")
        
        menu_inspectie()
    
    # PROPERTIES
    
    @property
    def velden(self) -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Merk.__annotations__.items() if not veld.startswith("_")}
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Merk._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU GEGEVENS MERK",
        ) -> str | commando.Stop | None:
        
        return Merk.subregister().selecteren(
            geef_id = geef_id,
            toestaan_nieuw = toestaan_nieuw,
            terug_naar = terug_naar,
            )
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Merk.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        merk_uuid = Merk.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if merk_uuid is commando.STOP or merk_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Merk.subregister()[merk_uuid]}\" verwijderd")
        del Merk.subregister()[merk_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_bewerken() -> commando.Doorgaan:
        
        merk = Merk.selecteren(
            geef_id = False,
            toestaan_nieuw = False,
            )
        if merk is commando.STOP or merk is None:
            return commando.DOORGAAN
        
        merk.bewerken()
        return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_inspecteren() -> commando.Doorgaan:
        
        merk = Merk.selecteren(
            geef_id = False,
            toestaan_nieuw = False,
            )
        if merk is commando.STOP or merk is None:
            return commando.DOORGAAN
        
        merk.inspecteren()
        return commando.DOORGAAN