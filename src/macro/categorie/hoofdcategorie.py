"""macro.categorie.hoofdcategorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

from grienetsiis.opdrachtprompt import invoeren, Menu, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject


@dataclass
class Hoofdcategorie(GeregistreerdObject):
    
    hoofdcategorie_naam: str
    
    _SUBREGISTER_NAAM: ClassVar[str] = "hoofdcategorie"
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"hoofdcategorie \"{self.hoofdcategorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(cls) -> Hoofdcategorie | commando.Doorgaan:
        
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
        
        return cls(
            hoofdcategorie_naam = hoofdcategorie_naam,
            )
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Hoofdcategorie._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU GEGEVENS HOOFDCATEGORIE",
        ) -> str | commando.Stop | None:
        
        return Hoofdcategorie.subregister().selecteren(
            geef_id = True,
            toestaan_nieuw = toestaan_nieuw,
            terug_naar = terug_naar,
            )
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Hoofdcategorie.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(toestaan_nieuw = False)
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Hoofdcategorie.subregister()[hoofdcategorie_uuid]}\" verwijderd")
        del Hoofdcategorie.subregister()[hoofdcategorie_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan | None:
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(toestaan_nieuw = False)
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        print(f"\nbewerken gegevens {Hoofdcategorie.subregister()[hoofdcategorie_uuid]}\n")
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN
        
        waarde_oud = Hoofdcategorie.subregister()[hoofdcategorie_uuid].hoofdcategorie_naam
        
        print(f"\n>>> veld \"hoofdcategorie_naam\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
        Hoofdcategorie.subregister()[hoofdcategorie_uuid].hoofdcategorie_naam = waarde_nieuw
        return commando.DOORGAAN
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_hoofdcategorie = Menu("MENU GEGEVENS HOOFDCATEGORIE", super_menu, True)
        
        super_menu.toevoegen_optie(menu_hoofdcategorie, "menu hoofdcategorie")
        
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.nieuw, "nieuwe hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.bewerken, "bewerken hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.verwijderen, "verwijderen hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.weergeven, "weergeven hoofdcategorie")
        
        return menu_hoofdcategorie