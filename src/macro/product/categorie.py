"""macro.categorie.categorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.product import Hoofdcategorie


@dataclass
class Categorie(GeregistreerdObject):
    
    categorie_naam: str
    hoofdcategorie_uuid: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"categorie \"{self.categorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU GEGEVENS CATEGORIE",
        geef_id: bool = False,
        ) -> Categorie | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuwe categorie")
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = terug_naar,
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        categorie_naam = invoeren(
            tekst_beschrijving = "categorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if categorie_naam is commando.STOP:
            return commando.DOORGAAN
        
        print(f"\n>>> nieuwe categorie \"{categorie_naam}\" gemaakt")
        
        categorie = cls(
            categorie_naam = categorie_naam,
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            )
        
        if geef_id:
            return getattr(categorie, categorie._ID_VELD)
        return categorie
    
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
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuwe", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU GEGEVENS CATEGORIE",
        ) -> str | commando.Stop | commando.Doorgaan | None:
        
        aantal_categorieën = len(Categorie.subregister())
        
        if aantal_categorieën == 0:
            print(f"\n>>> geen categorieën aanwezig")
            
            if not toestaan_nieuw:
                return None
            
            selectiemethode = "nieuw"
        
        if not selectiemethode:
            
            opties = {}
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw categorie"
            
            if aantal_categorieën > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie"
                opties["zoeken"] = "zoeken op categorienaam"
            
            selectiemethode = kiezen(
                opties = opties,
                tekst_beschrijving = "selectiemethode voor categorie",
                tekst_annuleren = terug_naar,
                )
            if selectiemethode is commando.STOP:
                return commando.STOP
        
        if selectiemethode == "nieuw":
            return Categorie.nieuw(
                terug_naar = terug_naar,
                geef_id = geef_id,
                )
        
        if aantal_categorieën == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            hoofdcategorie_uuid = Hoofdcategorie.selecteren(
                geef_id = True,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
            if hoofdcategorie_uuid is commando.STOP:
                return commando.STOP
            
            return Categorie.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_uuid,
            ).selecteren(
                geef_id = geef_id,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Categorie.subregister().zoeken(
            veld = "categorie_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven(
        terug_naar: str = "terug naar MENU GEGEVENS CATEGORIE",
        ) -> commando.Doorgaan:
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = terug_naar,
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        Categorie.subregister().filter(
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            ).weergeven()
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        categorie_uuid = Categorie.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Categorie.subregister()[categorie_uuid]}\" verwijderd")
        del Categorie.subregister()[categorie_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def bewerken() -> commando.Doorgaan | None:
        
        categorie_uuid = Categorie.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
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
            opties = list(Categorie.velden().keys()),
            tekst_beschrijving = "veld om te bewerken",
            )
    
    @staticmethod
    def velden() -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Categorie.__annotations__.items() if not veld.startswith("_")}