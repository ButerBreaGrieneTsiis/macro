"""macro.categorie.categorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, List

from grienetsiis.opdrachtprompt import invoeren, kiezen, Menu, commando
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
    def nieuw(cls) -> Categorie | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuwe categorie")
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren()
        
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        categorie_naam = invoeren(
            tekst_beschrijving = "categorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        print(f"\n>>> nieuwe categorie \"{categorie_naam}\" gemaakt")
        
        return cls(
            categorie_naam = categorie_naam,
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            )
    
    # PROPERTIES
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return Hoofdcategorie.subregister()[self.hoofdcategorie_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Categorie._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU GEGEVENS CATEGORIE",
        ) -> str | commando.Stop | None:
        
        if len(Categorie.subregister()) == 0:
            print(f"\n>>> geen categorie aanwezig")
            return None
        
        keuze_selecteren = kiezen(
            opties = [
                "selecteren via hoofdcategorie",
                "selecteren op categorienaam",
                ],
            tekst_beschrijving = "selectiemethode",
            tekst_annuleren = terug_naar,
            )
        
        if keuze_selecteren is commando.STOP:
            return commando.STOP
        
        if keuze_selecteren == "selecteren via hoofdcategorie":
            hoofdcategorie_uuid = Hoofdcategorie.selecteren(
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
            return Categorie.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_uuid,
            ).selecteren(
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Categorie.subregister().zoeken(veld = "categorie_naam")
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Categorie.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        categorie_uuid = Categorie.selecteren(toestaan_nieuw = False)
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Categorie.subregister()[categorie_uuid]}\" verwijderd")
        del Categorie.subregister()[categorie_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan | None:
        
        categorie_uuid = Categorie.selecteren(toestaan_nieuw = False)
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        veld = Categorie.kiezen_veld()
        if veld is commando.STOP:
            return commando.DOORGAAN
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = veld,
            invoer_type = Categorie.velden()[veld],
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN 
        
        waarde_oud = getattr(Categorie.subregister()[categorie_uuid], veld)
        
        print(f"\n>>> veld \"{veld}\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
        setattr(Categorie.subregister()[categorie_uuid], veld, waarde_nieuw)
        return commando.DOORGAAN
    
    @staticmethod
    def kiezen_veld() -> str | commando.Stop:
        return kiezen(
            opties = Categorie.velden(),
            tekst_beschrijving = "veld om te bewerken",
            )
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_categorie = Menu("MENU GEGEVENS CATEGORIE", super_menu, False)
        
        super_menu.toevoegen_optie(menu_categorie, "menu categorie")
        
        menu_categorie.toevoegen_optie(Categorie.nieuw, "nieuwe categorie")
        menu_categorie.toevoegen_optie(Categorie.bewerken, "bewerken categorie")
        menu_categorie.toevoegen_optie(Categorie.verwijderen, "verwijderen categorie")
        menu_categorie.toevoegen_optie(Categorie.weergeven, "weergeven categorie")
        
        return menu_categorie
    
    @staticmethod
    def velden() -> List[str]:
        return [veld for veld in Categorie.__annotations__ if not veld.startswith("_")]