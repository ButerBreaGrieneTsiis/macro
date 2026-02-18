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
        terug_naar: str = "terug naar MENU MERK",
        ) -> str | commando.Stop | None:
        
        return Merk.subregister().selecteren(
            geef_id = geef_id,
            toestaan_nieuw = toestaan_nieuw,
            terug_naar = terug_naar,
            )
    
    @staticmethod
    def weergeven_alle() -> commando.Doorgaan:
        Merk.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan:
        
        while True:
            
            merk = Merk.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if merk is commando.STOP:
                return commando.DOORGAAN
            if merk is None:
                continue
            
            menu_bewerken = Menu(f"MENU BEWERKEN ({f"{merk}".upper()})", "MENU MERK", blijf_in_menu = True)
            menu_bewerken.toevoegen_optie(merk.bewerken_naam, "naam")
            
            menu_bewerken()
            
            return commando.DOORGAAN
    
    @staticmethod
    def inspecteren() -> commando.Doorgaan:
        
        while True:
            
            merk = Merk.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if merk is commando.STOP:
                return commando.DOORGAAN
            if merk is None:
                continue
            
            menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{merk}".upper()})", "MENU MERK", blijf_in_menu = True)
            menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {merk.merk_naam}"), "naam")
            
            menu_inspectie()
            
            return commando.DOORGAAN
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Merk.weergeven_alle()
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