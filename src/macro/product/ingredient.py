"""macro.product.ingredient"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Dict, Literal

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
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU GEGEVENS INGREDIËNT",
        geef_id: bool = False,
        ) -> Ingrediënt | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw ingrediënt")
        
        categorie_uuid = Categorie.selecteren(terug_naar = terug_naar)
        if categorie_uuid is commando.STOP or categorie_uuid is commando.DOORGAAN or categorie_uuid is None:
            return commando.DOORGAAN
        
        ingrediënt_naam = invoeren(
            tekst_beschrijving = "ingrediëntnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if ingrediënt_naam is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuw ingrediënt \"{ingrediënt_naam}\" gemaakt")
        
        ingrediënt = cls(
            ingrediënt_naam = ingrediënt_naam,
            categorie_uuid = categorie_uuid,
            )
        
        if geef_id:
            return getattr(ingrediënt, ingrediënt._ID_VELD)
        return ingrediënt
    
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
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU GEGEVENS INGREDIËNT",
        ) -> str | commando.Stop | commando.Doorgaan | None:
        
        aantal_ingrediënten = len(Ingrediënt.subregister())
        
        if aantal_ingrediënten == 0:
            print(f"\n>>> geen ingrediënten aanwezig")
            
            if not toestaan_nieuw:
                return None
            
            selectiemethode = "nieuw"
        
        if not selectiemethode:
            
            opties = {}
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw ingrediënt"
            
            if aantal_ingrediënten > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie en categorie"
                opties["zoeken"] = "zoeken op ingrediëntnaam"
            
            selectiemethode = kiezen(
                opties = opties,
                tekst_beschrijving = "selectiemethode voor ingrediënt",
                tekst_annuleren = terug_naar,
                )
            if selectiemethode is commando.STOP:
                return commando.STOP
        
        if selectiemethode == "nieuw":
            return Ingrediënt.nieuw(
                terug_naar = terug_naar,
                geef_id = True,
                )
        
        if aantal_ingrediënten == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            categorie_uuid = Categorie.selecteren(
                toestaan_nieuw = toestaan_nieuw,
                selectiemethode = "selecteren",
                terug_naar = terug_naar,
                )
            if categorie_uuid is commando.STOP:
                return commando.STOP
            
            return Ingrediënt.subregister().filter(
                categorie_uuid = categorie_uuid,
            ).selecteren(
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Ingrediënt.subregister().zoeken(veld = "ingrediënt_naam")
    
    @staticmethod
    def weergeven(
        terug_naar: str = "terug naar MENU GEGEVENS INGREDIËNT",
        ) -> commando.Doorgaan:
        
        categorie_uuid = Categorie.selecteren(
            toestaan_nieuw = False,
            terug_naar = terug_naar,
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        Ingrediënt.subregister().filter(
            categorie_uuid = categorie_uuid,
            ).weergeven()
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
            opties = list(Ingrediënt.velden().keys()),
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
    def velden() -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Ingrediënt.__annotations__.items() if not veld.startswith("_")}