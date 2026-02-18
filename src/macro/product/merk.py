"""macro.product.merk"""
from __future__ import annotations
from dataclasses import dataclass

from grienetsiis.opdrachtprompt import invoeren, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject


@dataclass
class Merk(GeregistreerdObject):
    
    merk_naam: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"merk \"{self.merk_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(cls) -> Merk | commando.Doorgaan:
        
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
        
        return cls(
            merk_naam = merk_naam,
            )
    
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
    def bewerken() -> commando.Doorgaan | None:
        
        merk_uuid = Merk.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if merk_uuid is commando.STOP or merk_uuid is None:
            return commando.DOORGAAN
        
        print(f"\nbewerken gegevens {Merk.subregister()[merk_uuid]}\n")
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = "merknaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN
        
        waarde_oud = Merk.subregister()[merk_uuid].merk_naam
        
        print(f"\n>>> veld \"merk_naam\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
        Merk.subregister()[merk_uuid].merk_naam = waarde_nieuw
        return commando.DOORGAAN