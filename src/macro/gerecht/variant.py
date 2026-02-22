"""macro.gerecht.variant"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal, TYPE_CHECKING

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject
from grienetsiis.types import BasisType

from macro.gerecht import HoofdcategorieGerecht, CategorieGerecht
from macro.product import Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde

if TYPE_CHECKING:
    from macro.gerecht import Gerecht


@dataclass
class Variant(BasisType):
    
    variant_naam: str
    toevoeging: Dict[str, Dict[str, float]] | None = None
    aanpassing: Dict[str, Dict[str, float]] | None = None
    verwijdering: Dict[str, List[str]] | None = None
    porties: int | None = None
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        return f"variant \"{self.variant_naam}\""
    
    def __post_init__(self) -> None:
        if self.toevoeging is None:
            self.toevoeging = {}
        if self.aanpassing is None:
            self.aanpassing = {}
        if self.verwijdering is None:
            self.verwijdering = []
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        gerecht: Gerecht,
        geef_id: bool = False,
        ) -> Variant | commando.Doorgaan:
        
        print(f"\ninvullen gegevens nieuwe variant")
        
        variant_naam = invoeren(
            tekst_beschrijving = "variant",
            invoer_type = "str",
            uitsluiten_leeg = True,
            valideren = True,
            uitvoer_kleine_letters = True,
            )
        if variant_naam is commando.STOP:
            return commando.DOORGAAN
        
        variant = cls(
            variant_naam = variant_naam,
            )
        
        variant.bewerken(
            terug_naar = terug_naar,
            gerecht = gerecht,
            )
        
        print(f"\n>>> nieuwe variant \"{variant_naam}\" gemaakt")
        
        if geef_id:
            return variant._id
        return variant
    
    # INSTANCE METHODS
    
    def bewerken(
        self,
        terug_naar: str,
        gerecht: Gerecht,
        ) -> commando.Doorgaan:
        
        menu_bewerken_variant = Menu(f"MENU BEWERKEN VARIANT ({f"{self}".upper()})", terug_naar, blijf_in_menu = True)
        menu_bewerken_variant.toevoegen_optie(self.bewerken_producten_toevoegen, "toevoegen producten")
        menu_bewerken_variant.toevoegen_optie(self.bewerken_producten_aanpassen, "aanpassen hoeveelheid producten")
        menu_bewerken_variant.toevoegen_optie(self.bewerken_producten_aanpassen, "verwijderen producten")
        menu_bewerken_variant.toevoegen_optie(self.inspecteren_producten, "inspecteren producten")
        
        menu_bewerken_variant()
        
        return commando.DOORGAAN
    
    def bewerken_producten_toevoegen(): ...
    def bewerken_producten_aanpassen(): ...
    def bewerken_producten_aanpassen(): ...
    
    def inspecteren_producten() -> None:
        
        ...
    
    # PROPERTIES
    
    # STATIC METHODS
    
    @staticmethod
    def subregister() -> Subregister:
        return Register[Variant._SUBREGISTER_NAAM]
    
    @staticmethod
    def selecteren(
        terug_naar: str,
        geef_id: bool = True,
        toestaan_nieuw: bool = True,
        selectiemethode: Literal["nieuw", "selecteren", "zoeken"] | None = None,
        ) -> Variant | str | commando.Stop | None:
        
        ...