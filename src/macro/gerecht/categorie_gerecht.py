"""macro.categorie.categorie_gerecht"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject

from macro.gerecht import HoofdcategorieGerecht


@dataclass
class CategorieGerecht(GeregistreerdObject):
    
    categorie_naam: str
    hoofdcategorie_uuid: str
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"categorie gerecht \"{self.categorie_naam}\""
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str = "terug naar MENU CATEGORIE GERECHT",
        geef_id: bool = False,
        hoofdcategorie_uuid: str | None = None,
        ) -> CategorieGerecht | commando.Doorgaan:
        
        print("\ninvullen gegevens nieuwe categorie gerecht")
        
        if hoofdcategorie_uuid is None:
            hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
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
        
        print(f"\n>>> nieuwe categorie gerecht \"{categorie_naam}\" gemaakt")
        
        categorie_gerecht = cls(
            categorie_naam = categorie_naam,
            hoofdcategorie_uuid = hoofdcategorie_uuid,
            )
        
        if geef_id:
            return categorie_gerecht._id
        return categorie_gerecht
    
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
        
        waarde_oud = self.hoofdcategorie_gerecht
        hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = True,
            terug_naar = f"MENU BEWERKEN ({f"{self}".upper()})",
            )
        if hoofdcategorie_uuid is commando.STOP or hoofdcategorie_uuid is None:
            return commando.DOORGAAN
        
        self.hoofdcategorie_uuid = hoofdcategorie_uuid
        print(f"\n>>> veld \"hoofdcategorie\" veranderd van \"{waarde_oud}\" naar \"{self.hoofdcategorie_gerecht}\"")
        return commando.DOORGAAN
    
    # PROPERTIES
    
    @property
    def hoofdcategorie_gerecht(self) -> HoofdcategorieGerecht:
        return HoofdcategorieGerecht.subregister()[self.hoofdcategorie_uuid]
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register[CategorieGerecht._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        terug_naar: str = "terug naar MENU CATEGORIE GERECHT",
        ) -> str | commando.Stop | commando.Doorgaan | None:
        
        aantal_categorieën = len(CategorieGerecht.subregister())
        
        if aantal_categorieën == 0:
            print("\n>>> geen categorieën gerecht aanwezig")
            
            if not toestaan_nieuw:
                return commando.STOP
            
            selectiemethode = "nieuw"
        
        if not selectiemethode:
            
            opties = {}
            
            if aantal_categorieën > 0:
                opties["selecteren"] = "selecteren via hoofdcategorie gerecht"
                opties["zoeken"] = "zoeken op categorienaam"
            
            if toestaan_nieuw:
                opties["nieuw"] = "nieuw categorie gerecht"
            
            selectiemethode = kiezen(
                opties = opties,
                tekst_beschrijving = "selectiemethode voor categorie gerecht",
                tekst_annuleren = terug_naar,
                )
            if selectiemethode is commando.STOP:
                return commando.STOP
        
        if selectiemethode == "nieuw":
            return CategorieGerecht.nieuw(
                terug_naar = terug_naar,
                geef_id = geef_id,
                )
        
        if aantal_categorieën == 0:
            return None
        
        if selectiemethode == "selecteren":
            
            hoofdcategorie_uuid = HoofdcategorieGerecht.selecteren(
                geef_id = True,
                toestaan_nieuw = toestaan_nieuw,
                terug_naar = terug_naar,
                )
            if hoofdcategorie_uuid is commando.STOP:
                return commando.STOP
            categoriën = CategorieGerecht.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_uuid,
                )
            
            if len(categoriën) > 0:
                return categoriën.selecteren(
                    geef_id = geef_id,
                    toestaan_nieuw = toestaan_nieuw,
                    terug_naar = terug_naar,
                    )
            
            if toestaan_nieuw:
                hoofdcategorie = HoofdcategorieGerecht.subregister()[hoofdcategorie_uuid]
                print(f"\n>>> geen categoriën aanwezig voor {hoofdcategorie}")
                
                return CategorieGerecht.nieuw(
                    terug_naar = terug_naar,
                    geef_id = geef_id,
                    hoofdcategorie_uuid = hoofdcategorie_uuid,
                    )
            
            return None
        
        print()
        return CategorieGerecht.subregister().zoeken(
            veld = "categorie_naam",
            veld_exact_overeenkomend = False,
            geef_id = geef_id,
            )
    
    @staticmethod
    def weergeven_alle() -> commando.Stop:
        
        print()
        
        for hoofdcategorie_gerecht_uuid, hoofdcategorie_gerecht in HoofdcategorieGerecht.subregister().items():
            
            print(hoofdcategorie_gerecht)
            
            for categorie_gerecht in CategorieGerecht.subregister().filter(
                hoofdcategorie_uuid = hoofdcategorie_gerecht_uuid,
                ).lijst:
                
                print(f"  {categorie_gerecht}")
        
        return commando.STOP
    
    @staticmethod
    def weergeven_voor_hoofdcategorie() -> commando.Doorgaan | commando.Stop:
        
        hoofdcategorie_gerecht_uuid = HoofdcategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            terug_naar = "terug naar MENU CATEGORIE GERECHT",
            )
        if hoofdcategorie_gerecht_uuid is commando.STOP or hoofdcategorie_gerecht_uuid is None:
            return commando.DOORGAAN
        
        CategorieGerecht.subregister().filter(
            hoofdcategorie_uuid = hoofdcategorie_gerecht_uuid,
            ).weergeven()
        
        return commando.STOP
    
    @staticmethod
    def bewerken() -> commando.Doorgaan:
        
        while True:
            
            categorie_gerecht = CategorieGerecht.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if categorie_gerecht is commando.STOP:
                return commando.DOORGAAN
            if categorie_gerecht is None:
                continue
            
            menu_bewerken = Menu(f"MENU BEWERKEN ({f"{categorie_gerecht}".upper()})", "MENU CATEGORIE GERECHT", blijf_in_menu = True)
            menu_bewerken.toevoegen_optie(categorie_gerecht.bewerken_naam, "naam")
            menu_bewerken.toevoegen_optie(categorie_gerecht.bewerken_hoofdcategorie, "hoofdcategorie")
            
            menu_bewerken()
            
            return commando.DOORGAAN
    
    @staticmethod
    def inspecteren() -> commando.Doorgaan:
        
        while True:
            
            categorie_gerecht = CategorieGerecht.selecteren(
                geef_id = False,
                toestaan_nieuw = False,
                )
            if categorie_gerecht is commando.STOP:
                return commando.DOORGAAN
            if categorie_gerecht is None:
                continue
            
            menu_inspectie = Menu(f"MENU INSPECTEREN ({f"{categorie_gerecht}".upper()})", "MENU CATEGORIE GERECHT", blijf_in_menu = True)
            menu_inspectie.toevoegen_optie(lambda: print(f"\nnaam voor {categorie_gerecht}:\n>>> {categorie_gerecht.categorie_naam}"), "naam")
            menu_inspectie.toevoegen_optie(lambda: print(f"\nhoofdcategorie voor {categorie_gerecht}:\n>>> {categorie_gerecht.hoofdcategorie}"), "hoofdcategorie")
            
            menu_inspectie()
            
            return commando.DOORGAAN
    
    @staticmethod
    def weergeven() -> commando.Doorgaan:
        
        menu_weergeven = Menu("MENU WEERGEVEN CATEGORIE GERECHT", "MENU CATEGORIE GERECHT", blijf_in_menu = True)
        menu_weergeven.toevoegen_optie(CategorieGerecht.weergeven_alle, "alle categorieën")
        menu_weergeven.toevoegen_optie(CategorieGerecht.weergeven_voor_hoofdcategorie, "categorieën voor hoofdcategorie")
        
        menu_weergeven()
        
        return commando.DOORGAAN
    
    @staticmethod
    def verwijderen() -> commando.Doorgaan:
        
        categorie_uuid = CategorieGerecht.selecteren(
            geef_id = True,
            toestaan_nieuw = False,
            )
        if categorie_uuid is commando.STOP or categorie_uuid is None:
            return commando.DOORGAAN
        
        print(f">>> \"{CategorieGerecht.subregister()[categorie_uuid]}\" verwijderd")
        del CategorieGerecht.subregister()[categorie_uuid]
        return commando.DOORGAAN