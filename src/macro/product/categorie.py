"""macro.categorie.categorie"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
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
        terug_naar: str = "terug naar MENU CATEGORIE PRODUCT",
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
            return categorie._id
        return categorie
    
    # INSTANCE METHODS
    
    def bewerken_naam(self) -> commando.Doorgaan:
        
        waarde_oud = self.categorie_naam
        categorie_naam = invoeren(
            tekst_beschrijving = "categorienaam",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if categorie_naam is commando.STOP:
            return commando.DOORGAAN
        
        self.categorie_naam = categorie_naam
        print(f"\n>>> veld \"categorienaam\" veranderd van \"{waarde_oud}\" naar \"{self.categorie_naam}\"")
        return commando.DOORGAAN
    
    def bewerken_hoofdcategorie(self) -> commando.Doorgaan:
        
        waarde_oud = self.hoofdcategorie
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        self.hoofdcategorie_uuid = hoofdcategorie_uuid
        print(f"\n>>> veld \"hoofdcategorie\" veranderd van \"{waarde_oud}\" naar \"{self.hoofdcategorie}\"")
        return commando.DOORGAAN
    
    # PROPERTIES
    
    @property
    def velden(self) -> Dict[str, str]:
        return {veld: veld_type for veld, veld_type in Categorie.__annotations__.items() if not veld.startswith("_")}
    
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
        terug_naar: str = "terug naar MENU CATEGORIE PRODUCT",
        ) -> str | commando.Stop | commando.Doorgaan | None:
        
        aantal_categorieën = len(Categorie.subregister())
        
        if aantal_categorieën == 0:
            print(f"\n>>> geen categorieën aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
            
            selectiemethode = "nieuw"
        
        if not selectiemethode:
            
            opties = {}
            
            if aantal_categorieën > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie"
                opties["zoeken"] = "zoeken op categorienaam"
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw categorie"
            
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
        
        print()
        return Categorie.subregister().zoeken(
            veld = "categorie_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven_alle() -> commando.Stop:
        
        print("\nALLE CATEGORIEËN:\n")
        
        for hoofdcategorie_uuid, hoofdcategorie in Hoofdcategorie.subregister().items():
            
            print(hoofdcategorie)
            
            for categorie in Categorie.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_uuid,
                ).lijst:
                
                print(f"  {categorie}")
        
        return commando.STOP
    
    @staticmethod
    def weergeven_voor_hoofdcategorie() -> commando.Doorgaan | commando.Stop:
        
        hoofdcategorie_uuid = Hoofdcategorie.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = "terug naar MENU CATEGORIE PRODUCT",
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        hoofdcategorie = Hoofdcategorie.subregister()[hoofdcategorie_uuid]
        print(f"\nALLE CATEGORIEËN VOOR {f"{hoofdcategorie}".upper()}:\n")
        
        Categorie.subregister().filter(
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            ).weergeven()
        
        return commando.STOP
    
    @staticmethod
    def bewerken() -> commando.Doorgaan:
        
        while True:
            
            categorie = Categorie.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if categorie is commando.STOP:
                return commando.DOORGAAN
            if categorie is None:
                continue
            
            menu_bewerken = Menu(f"MENU BEWERKEN ({f"{categorie}".upper()})", "MENU CATEGORIE PRODUCT", blijf_in_menu = True)
            menu_bewerken.toevoegen_optie(categorie.bewerken_naam, "naam")
            menu_bewerken.toevoegen_optie(categorie.bewerken_hoofdcategorie, "hoofdcategorie")
            
            menu_bewerken()
            
            return commando.DOORGAAN
    
    @staticmethod
    def inspecteren() -> commando.Doorgaan:
        
        while True:
            
            categorie = Categorie.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if categorie is commando.STOP:
                return commando.DOORGAAN
            if categorie is None:
                continue
            
            menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{categorie}".upper()})", "MENU CATEGORIE PRODUCT", blijf_in_menu = True)
            menu_inspectie.toevoegen_optie(lambda: print(f"\nnaam voor {categorie}:\n>>> {categorie.categorie_naam}"), "naam")
            menu_inspectie.toevoegen_optie(lambda: print(f"\nhoofdcategorie voor {categorie}:\n>>> {categorie.hoofdcategorie}"), "hoofdcategorie")
            
            menu_inspectie()
            
            return commando.DOORGAAN
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        
        menu_weergeven = Menu(f"MENU WEERGEVEN CATEGORIE PRODUCT", "MENU CATEGORIE PRODUCT", blijf_in_menu = True)
        menu_weergeven.toevoegen_optie(Categorie.weergeven_alle, "alle categorieën")
        menu_weergeven.toevoegen_optie(Categorie.weergeven_voor_hoofdcategorie, "categorieën voor hoofdcategorie")
        
        menu_weergeven()
        
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