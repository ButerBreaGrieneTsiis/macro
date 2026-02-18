"""macro.categorie.hoofdcategorie_gerecht"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from grienetsiis.opdrachtprompt import invoeren, commando, Menu
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
        
        hoofdcategorie_gerecht = cls(
            hoofdcategorie_naam = hoofdcategorie_naam,
            )
        
        if geef_id:
            return hoofdcategorie_gerecht._id
        return hoofdcategorie_gerecht
    
    # INSTANCE METHODS
    
    def bewerken(self) -> None:
        
        menu_bewerken = Menu(f"MENU BEWERKEN ({f"{self}".upper()})", "MENU HOOFDCATEGORIE GERECHT", blijf_in_menu = True)
        menu_bewerken.toevoegen_optie(self.bewerken_naam, "naam")
        
        menu_bewerken()
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.hoofdcategorie_naam
        hoofdcategorie_naam = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if hoofdcategorie_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
        print(f"\n>>> veld \"hoofdcategorienaam\" veranderd van \"{waarde_oud}\" naar \"{self.hoofdcategorie_naam}\"")
        return commando.DOORGAAN
    
    def inspecteren(self) -> None:
        
        menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{self}".upper()})", "MENU HOOFDCATEGORIE GERECHT", blijf_in_menu = True)
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.hoofdcategorie_naam}"), "naam")
        
        menu_inspectie()
    
    # PROPERTIES
    
    @property
    def velden(self) -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in HoofdcategorieGerecht.__annotations__.items() if not veld.startswith("_")}
    
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
    def selecteren_en_bewerken() -> commando.Doorgaan:
        
        hoofdcategorie_gerecht = HoofdcategorieGerecht.selecteren(
            geef_id = False,
            toestaan_nieuw = False,
            )
        if hoofdcategorie_gerecht is commando.STOP or hoofdcategorie_gerecht is None:
            return commando.DOORGAAN
        
        hoofdcategorie_gerecht.bewerken()
        return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_inspecteren() -> commando.Doorgaan:
        
        hoofdcategorie_gerecht = HoofdcategorieGerecht.selecteren(
            geef_id = False,
            toestaan_nieuw = False,
            )
        if hoofdcategorie_gerecht is commando.STOP or hoofdcategorie_gerecht is None:
            return commando.DOORGAAN
        
        hoofdcategorie_gerecht.inspecteren()
        return commando.DOORGAAN