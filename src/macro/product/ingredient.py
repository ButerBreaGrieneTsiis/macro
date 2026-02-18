"""macro.product.ingredient"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.product import Hoofdcategorie, Categorie


@dataclass
class Ingrediënt(GeregistreerdObject):
    
    ingrediënt_naam: str
    categorie_uuid: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"ingrediënt \"{self.ingrediënt_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU INGREDIËNT",
        geef_id: bool = False,
        ) -> Ingrediënt | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuw ingrediënt")
        
        categorie_uuid = Categorie.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = terug_naar,
            )
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
            return ingrediënt._id
        return ingrediënt
    
    # INSTANCE METHODS
    
    def bewerken(self) -> None:
        
        menu_bewerken = Menu(f"MENU BEWERKEN ({f"{self}".upper()})", "MENU INGREDIËNT", blijf_in_menu = True)
        menu_bewerken.toevoegen_optie(self.bewerken_naam, "naam")
        menu_bewerken.toevoegen_optie(self.bewerken_categorie, "categorie")
        
        menu_bewerken()
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.ingrediënt_naam
        ingrediënt_naam = invoeren(
            tekst_beschrijving = "ingrediëntnaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if ingrediënt_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.ingrediënt_naam = ingrediënt_naam
        print(f"\n>>> veld \"ingrediëntnaam\" veranderd van \"{waarde_oud}\" naar \"{self.ingrediënt_naam}\"")
        return commando.DOORGAAN
    
    def bewerken_categorie(self) -> commando.Doorgaan:
        
        waarde_oud = self.categorie
        categorie_uuid = Categorie.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        self.categorie_uuid = categorie_uuid
        print(f"\n>>> veld \"categorie\" veranderd van \"{waarde_oud}\" naar \"{self.categorie}\"")
        return commando.DOORGAAN
        
    def inspecteren(self) -> None:
        
        menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{self}".upper()})", "MENU INGREDIËNT", blijf_in_menu = True)
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.ingrediënt_naam}"), "naam")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.hoofdcategorie}"), "hoofdcategorie")
        menu_inspectie.toevoegen_optie(lambda: print(f"\n>>> {self.categorie}"), "categorie")
        
        menu_inspectie()
    
    # PROPERTIES
    
    @property
    def velden(self) -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Ingrediënt.__annotations__.items() if not veld.startswith("_")}
    
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
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU INGREDIËNT",
        ) -> str | commando.Stop | commando.Doorgaan | None:
        
        aantal_ingrediënten = len(Ingrediënt.subregister())
        
        if aantal_ingrediënten == 0:
            print(f"\n>>> geen ingrediënten aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
            
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
                geef_id = geef_id,
                )
        
        if aantal_ingrediënten == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            categorie_uuid = Categorie.selecteren(
                geef_id = True,
                toestaan_nieuw = toestaan_nieuw,
                selectiemethode = "selecteren",
                terug_naar = terug_naar,
                )
            if categorie_uuid is commando.STOP:
                return commando.STOP
            
            return Ingrediënt.subregister().filter(
                categorie_uuid = categorie_uuid,
            ).selecteren(
                geef_id = geef_id,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
        
        return Ingrediënt.subregister().zoeken(
            veld = "ingrediënt_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven(
        terug_naar: str = "terug naar MENU INGREDIËNT",
        ) -> commando.Doorgaan:
        
        categorie_uuid = Categorie.selecteren(
            geef_id = True,
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
        
        ingrediënt_uuid = Ingrediënt.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if ingrediënt_uuid is commando.STOP or ingrediënt_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{Ingrediënt.subregister()[ingrediënt_uuid]}\" verwijderd")
        del Ingrediënt.subregister()[ingrediënt_uuid]
        return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_bewerken() -> commando.Doorgaan:
        
        while True:
            
            ingrediënt = Ingrediënt.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if ingrediënt is commando.STOP:
                return commando.DOORGAAN
            if ingrediënt is None:
                continue
        
            ingrediënt.bewerken()
            return commando.DOORGAAN
    
    @staticmethod
    def selecteren_en_inspecteren() -> commando.Doorgaan:
        
        while True:
            
            ingrediënt = Ingrediënt.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if ingrediënt is commando.STOP:
                return commando.DOORGAAN
            if ingrediënt is None:
                continue
            
            ingrediënt.inspecteren()
            return commando.DOORGAAN