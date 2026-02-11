"""macro.categorie.categorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

from grienetsiis.opdrachtprompt import invoeren, Menu, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from .hoofdcategorie import Hoofdcategorie


@dataclass
class Categorie(GeregistreerdObject):
    
    categorie_naam: str
    hoofdcategorie_uuid: str
    
    _SUBREGISTER_NAAM: ClassVar[str] = "categorie"
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"categorie \"{self.categorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(cls) -> Categorie:
        
        print(f"\ninvullen gegevens nieuwe categorie")
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren()
        
        categorie_naam = invoeren(
            tekst_beschrijving = "categorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        return cls(
            categorie_naam = categorie_naam,
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            )
    
    # PROPERTIES
    
    @property
    def hoofdcategorie(self):
        return Hoofdcategorie.subregister()[self.hoofdcategorie_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_categorie = Menu("MENU GEGEVENS CATEGORIE", super_menu, False)
        
        super_menu.toevoegen_optie(menu_categorie, "menu categorie")
        
        menu_categorie.toevoegen_optie(Categorie.nieuw, "nieuwe categorie")
        # menu_categorie.toevoegen_optie(Categorie.bewerken, "bewerken categorie")
        # menu_categorie.toevoegen_optie(Categorie.verwijderen, "verwijderen categorie")
        # menu_categorie.toevoegen_optie(Categorie.weergeven, "weergeven categorie")
        
        return menu_categorie