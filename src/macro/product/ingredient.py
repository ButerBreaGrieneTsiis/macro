"""macro.product.ingredient"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, List

from grienetsiis.opdrachtprompt import invoeren, kiezen, Menu, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.categorie import Hoofdcategorie, Categorie


@dataclass
class Ingrediënt(GeregistreerdObject):
    
    ingrediënt_naam: str
    categorie_uuid: str
    
    _SUBREGISTER_NAAM: ClassVar[str] = "ingrediënt"
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"ingrediënt \"{self.ingrediënt_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(cls) -> Ingrediënt | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw ingrediënt")
        
        categorie_uuid = Categorie.selecteren()
        
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        ingrediënt_naam = invoeren(
            tekst_beschrijving = "ingrediëntnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        print(f"\n>>> nieuw ingrediënt \"{ingrediënt_naam}\" gemaakt")
        
        return cls(
            ingrediënt_naam = ingrediënt_naam,
            categorie_uuid = categorie_uuid,
            )
    
    # PROPERTIES
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return Hoofdcategorie.subregister()[self.categorie.hoofdcategorie_uuid]
    
    @property
    def categorie(self) -> Categorie:
        return Categorie.subregister()[self.categorie_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register()[Ingrediënt._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        toestaan_nieuw: bool = True,
        terug_naar: str = "terug naar MENU GEGEVENS INGREDIËNT",
        ) -> str | commando.Stop | None:
        
        if len(Ingrediënt.subregister()) == 0:
            print(f"\n>>> geen ingrediënt aanwezig")
            return None
        
        keuze_selecteren = kiezen(
            opties = [
                "selecteren via categorie",
                "selecteren op ingrediëntnaam",
                ],
            tekst_beschrijving = "selectiemethode",
            tekst_annuleren = terug_naar,
            )
        
        if keuze_selecteren is commando.STOP:
            return commando.STOP
        
        if keuze_selecteren == "selecteren via categorie":
            
            categorie_uuid = Categorie.selecteren(
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
            
            return Ingrediënt.subregister().filter(
                categorie_uuid = categorie_uuid,
            ).selecteren(
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Ingrediënt.subregister().zoeken(veld = "ingrediënt_naam")
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        Ingrediënt.subregister().weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        ingrediënt_uuid = Ingrediënt.selecteren(toestaan_nieuw = False)
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Ingrediënt.subregister()[ingrediënt_uuid]}\" verwijderd")
        del Ingrediënt.subregister()[ingrediënt_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan | None:
        
        ingrediënt_uuid = Ingrediënt.selecteren(toestaan_nieuw = False)
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        veld = Ingrediënt.kiezen_veld()
        if veld is commando.STOP:
            return commando.DOORGAAN
        
        waarde_nieuw = invoeren(
            tekst_beschrijving = veld,
            invoer_type = Ingrediënt.velden()[veld],
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        
        if waarde_nieuw is commando.STOP:
            return commando.DOORGAAN 
        
        waarde_oud = getattr(Ingrediënt.subregister()[ingrediënt_uuid], veld)
        
        print(f"\n>>> veld \"{veld}\" veranderd van \"{waarde_oud}\" naar \"{waarde_nieuw}\"")
        setattr(Ingrediënt.subregister()[ingrediënt_uuid], veld, waarde_nieuw)
        return commando.DOORGAAN
    
    @staticmethod
    def kiezen_veld() -> str | commando.Stop:
        return kiezen(
            opties = Ingrediënt.velden(),
            tekst_beschrijving = "veld om te bewerken",
            )
    
    @staticmethod
    def toevoegen_menu(super_menu: Menu) -> Menu:
        
        menu_ingrediënt = Menu("MENU GEGEVENS INGREDIËNT", super_menu, True)
        
        super_menu.toevoegen_optie(menu_ingrediënt, "menu ingrediënt")
        
        menu_ingrediënt.toevoegen_optie(Ingrediënt.nieuw, "nieuwe ingrediënt")
        menu_ingrediënt.toevoegen_optie(Ingrediënt.bewerken, "bewerken ingrediënt")
        menu_ingrediënt.toevoegen_optie(Ingrediënt.verwijderen, "verwijderen ingrediënt")
        menu_ingrediënt.toevoegen_optie(Ingrediënt.weergeven, "weergeven ingrediënt")
        
        return menu_ingrediënt
    
    @staticmethod
    def velden() -> List[str]:
        return [veld for veld in Ingrediënt.__annotations__ if not veld.startswith("_")]