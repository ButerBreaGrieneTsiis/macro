"""macro.categorie.hoofdcategorie_gerecht"""
from __future__ import annotations
from dataclasses import dataclass

from grienetsiis.opdrachtprompt import invoeren, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject


@dataclass
class HoofdcategorieGerecht(GeregistreerdObject):
    
    hoofdcategorie_naam: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"hoofdcategorie gerecht \"{self.hoofdcategorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        geef_id: bool = False,
        ) -> HoofdcategorieGerecht | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie gerecht")
        
        hoofdcategorie_naam = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if hoofdcategorie_naam is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuwe hoofdcategorie gerecht \"{hoofdcategorie_naam}\" gemaakt")
        
        hoofdcategorie = cls(
            hoofdcategorie_naam = hoofdcategorie_naam,
            )
        
        if geef_id:
            return getattr(hoofdcategorie, hoofdcategorie._ID_VELD)
        return hoofdcategorie
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[HoofdcategorieGerecht._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU GEGEVENS HOOFDCATEGORIE GERECHT",
        ) -> str | commando.Stop | None:
        
        return HoofdcategorieGerecht.subregister().selecteren(
            geef_id = geef_id,
            toestaan_nieuw = toestaan_nieuw,
            terug_naar = terug_naar,
            )
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        HoofdcategorieGerecht.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid]}\" verwijderd")
        del HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan | None:
        
        hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        print(f"\nbewerken gegevens {HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid]}\n")
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN
        
        waarde_oud = HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid].hoofdcategorie_naam
        
        print(f"\n>>> veld \"hoofdcategorie_naam\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
        HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid].hoofdcategorie_naam = waarde_nieuw
        return commando.DOORGAAN