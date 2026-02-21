"""macro.categorie.hoofdcategorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from grienetsiis.opdrachtprompt import invoeren, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject


@dataclass
class Hoofdcategorie(GeregistreerdObject):
    
    hoofdcategorie_naam: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"hoofdcategorie \"{self.hoofdcategorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        geef_id: bool = False,
        ) -> Hoofdcategorie | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        
        hoofdcategorie_naam = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if hoofdcategorie_naam is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuwe hoofdcategorie \"{hoofdcategorie_naam}\" gemaakt")
        
        hoofdcategorie = cls(
            hoofdcategorie_naam = hoofdcategorie_naam,
            )
        
        if geef_id:
            return hoofdcategorie._id
        return hoofdcategorie
    
    # INSTANCE METHODS
    
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
    
    # PROPERTIES
    
    @property
    def velden(self) -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Hoofdcategorie.__annotations__.items() if not veld.startswith("_")}
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register[Hoofdcategorie._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU HOOFDCATEGORIE",
        ) -> str | commando.Stop | None:
        
        return Hoofdcategorie.subregister().selecteren(
            geef_id = geef_id,
            toestaan_nieuw = toestaan_nieuw,
            terug_naar = terug_naar,
            )
    
    @staticmethod
    def weergeven_alle() -> commando.Stop:
        
        print("\nALLE HOOFDCATEGORIEËN:\n")
        
        Hoofdcategorie.subregister().weergeven()
        return commando.STOP
    
    @staticmethod
    def bewerken() -> commando.Doorgaan:
        
        while True:
            
            hoofdcategorie = Hoofdcategorie.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if hoofdcategorie is commando.STOP or hoofdcategorie is None:
                return commando.DOORGAAN
            
            menu_bewerken = Menu(f"MENU BEWERKEN ({f"{hoofdcategorie}".upper()})", "MENU HOOFDCATEGORIE PRODUCT", blijf_in_menu = True)
            menu_bewerken.toevoegen_optie(hoofdcategorie.bewerken_naam, "naam")
            
            menu_bewerken()
        
            return commando.DOORGAAN
    
    @staticmethod
    def inspecteren() -> commando.Doorgaan:
        
        while True:
            
            hoofdcategorie = Hoofdcategorie.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if hoofdcategorie is commando.STOP or hoofdcategorie is None:
                return commando.DOORGAAN
            
            menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{hoofdcategorie}".upper()})", "MENU HOOFDCATEGORIE PRODUCT", blijf_in_menu = True)
            menu_inspectie.toevoegen_optie(lambda: print(f"\nnaam voor {hoofdcategorie}:\n>>> {hoofdcategorie.hoofdcategorie_naam}"), "naam")
            
            menu_inspectie()
            
            return commando.DOORGAAN
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Hoofdcategorie.weergeven_alle()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Hoofdcategorie.subregister()[hoofdcategorie_uuid]}\" verwijderd")
        del Hoofdcategorie.subregister()[hoofdcategorie_uuid]
        return commando.DOORGAAN