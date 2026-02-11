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
    def nieuw(cls) -> Hoofdcategorie:
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        
        hoofdcategorie_naam = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        return cls(
            hoofdcategorie_naam = hoofdcategorie_naam,
            )
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Hoofdcategorie._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren() -> str:
        return Hoofdcategorie.subregister().selecteren()
    
    @staticmethod
    def weergeven():
        return Hoofdcategorie.subregister().weergeven()
    
    @staticmethod
    def verwijderen():
        return Hoofdcategorie.subregister().verwijderen()
    
    @staticmethod
    def bewerken():
        hoofdcategorie_uuid = Hoofdcategorie.selecteren()
        
        if hoofdcategorie_uuid is commando.STOP:
            return None
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        
        hoofdcategorie_naam = invoeren(
            tekst_beschrijving = "hoofdcategorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        Hoofdcategorie.subregister()[hoofdcategorie_uuid].hoofdcategorie_naam = hoofdcategorie_naam
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_hoofdcategorie = Menu("MENU GEGEVENS HOOFDCATEGORIE", super_menu, False)
        
        super_menu.toevoegen_optie(menu_hoofdcategorie, "menu hoofdcategorie")
        
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.nieuw, "nieuwe hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.bewerken, "bewerken hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.verwijderen, "verwijderen hoofdcategorie")
        menu_hoofdcategorie.toevoegen_optie(Hoofdcategorie.weergeven, "weergeven hoofdcategorie")
        
        return menu_hoofdcategorie