"""macro.gerecht.variant"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING
from uuid import uuid4

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando
from grienetsiis.types import BasisType

from macro.product import Product
from macro.voedingswaarde import Eenheid, Hoeveelheid

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
            self.verwijdering = {}
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        gerecht: Gerecht,
        geef_id: bool = False,
        ) -> Variant | commando.Doorgaan:
        
        print("\ninvullen gegevens nieuwe variant")
        
        variant_naam = invoeren(
            tekst_beschrijving = "variantnaam",
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
        
        variant_uuid = str(uuid4())
        gerecht.varianten[variant_uuid] = variant
        
        print(f"\n>>> nieuwe variant \"{variant_naam}\" gemaakt")
        
        if geef_id:
            return variant_uuid
        return variant
    
    # INSTANCE METHODS
    
    def bewerken(
        self,
        terug_naar: str,
        gerecht: Gerecht,
        ) -> commando.Doorgaan:
        
        bewerk_opties = [
            "toevoegen toevoeging product",
            "verwijderen toevoeging product", # TODO
            "toevoegen verwijdering product", # TODO
            "verwijderen verwijdering product", # TODO
            "toevoegen aanpassing hoeveelheid", # TODO
            "verwijderen aanpassing hoeveelheid", # TODO
            "toevoegen aanpassing aantal porties", # TODO
            "verwijderen aanpassing aantal porties", # TODO
            "inspecteren", # TODO
            ]
        
        while True:
        
            keuze_bewerken = kiezen(
                opties = bewerk_opties,
                tekst_beschrijving = f"MENU BEWERKEN VARIANT ({f"{self}".upper()})",
                tekst_annuleren = f"AFRONDEN VARIANT ({f"{self}".upper()})",
                )
            
            if keuze_bewerken is commando.STOP:
                return commando.DOORGAAN
            
            if keuze_bewerken == "toevoegen toevoeging product":
                
                product = Product.selecteren(
                    geef_id = False,
                    toestaan_nieuw = True,
                    terug_naar = f"MENU BEWERKEN VARIANT ({f"{self}".upper()})",
                    )
                if product is commando.STOP or product is None:
                    continue
                
                eenheid = product.selecteren_eenheid(
                    terug_naar = f"MENU BEWERKEN VARIANT ({f"{self}".upper()})",
                    geef_enum = True,
                    toestaan_nieuw = True,
                    )
                if eenheid is commando.STOP:
                    continue
                
                product_uuid = product._id
                
                if product_uuid in gerecht.producten_standaard.keys() and eenheid.enkelvoud in [eenheid_enkelvoud for eenheid_enkelvoud in gerecht.producten_standaard[product_uuid]]:
                    print(f">>> eenheid \"{eenheid.meervoud}\" voor {product} reeds aanwezig, probeer optie \"aanpassen toevoeging product\"")
                    continue
                
                if product_uuid in self.toevoeging.keys() and eenheid.enkelvoud in [eenheid_enkelvoud for eenheid_enkelvoud in self.toevoeging[product_uuid]]:
                    print(f"\n>>> eenheid \"{eenheid.meervoud}\" van {product} reeds aanwezig in toevoegingen, probeer toevoeging aan te passen")
                    continue
                
                waarde = invoeren(
                    tekst_beschrijving = f"hoeveel {eenheid.meervoud}",
                    invoer_type = "float",
                    )
                if waarde is commando.STOP:
                    return commando.DOORGAAN
                
                hoeveelheid = Hoeveelheid(waarde, eenheid)
                
                if product_uuid in self.toevoeging.keys():
                    self.toevoeging[product_uuid][eenheid.enkelvoud] = waarde
                else:
                    self.toevoeging[product_uuid] = {eenheid.enkelvoud: waarde}
                
                print(f"\n>>> {hoeveelheid} van {product} toegevoegd aan toevoegingen")
            
            if keuze_bewerken == "inspecteren":
                
                self.inspecteren(gerecht = gerecht)
            
    def inspecteren(
        self,
        gerecht: Gerecht,
        ) -> None:
        
        self.inspecteren_toevoeging()
        self.inspecteren_verwijdering()
        self.inspecteren_aanpassing(gerecht = gerecht)
        self.inspecteren_porties()
    
    def inspecteren_toevoeging(self) -> None:
        
        if self.toevoeging:
            
            print(f"\ntoevoegingen voor {self}:\n")
            for product_uuid, hoeveelheden in self.toevoeging.items():
                
                product = Product.subregister()[product_uuid]
                
                for eenheid_enkelvoud, waarde in hoeveelheden.items():
                    
                    eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                    hoeveelheid = Hoeveelheid(waarde, eenheid)
                    print(f">>> {f"{hoeveelheid}":<19} {product}")
        else:
            print(f"\n{self} bevat geen toevoegingen")
    
    def inspecteren_verwijdering(self) -> None:
        
        if self.verwijdering:
            
            print(f"\nverwijderingen voor {self}:\n")
            for product_uuid, hoeveelheden in self.verwijdering.items():
                
                product = Product.subregister()[product_uuid]
                
                for eenheid_enkelvoud, waarde in hoeveelheden.items():
                    
                    eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                    hoeveelheid = Hoeveelheid(waarde, eenheid)
                    print(f">>> {f"{hoeveelheid}":<19} {product}")
        else:
            print(f"\n{self} bevat geen verwijderingen")
    
    def inspecteren_aanpassing(
        self,
        gerecht: Gerecht,
        ) -> None:
        
        if self.aanpassing:
            
            print(f"\naanpassingen voor {self}:\n")
            for product_uuid, hoeveelheden in self.aanpassing.items():
                
                product = Product.subregister()[product_uuid]
                
                for eenheid_enkelvoud, waarde in hoeveelheden.items():
                    
                    eenheid = Eenheid.van_enkelvoud(eenheid_enkelvoud)
                    hoeveelheid = Hoeveelheid(waarde, eenheid)
                    waarde_oud = gerecht.producten_standaard[product_uuid][eenheid_enkelvoud]
                    hoeveelheid_oud = Hoeveelheid(waarde_oud, eenheid)
                    print(f">>> {f"{hoeveelheid_oud}":<19} --> {f"{hoeveelheid}":<19} {product}")
        else:
            print(f"\n{self} bevat geen aanpassingen")
    
    def inspecteren_porties(self) -> None:
        if self.porties:
            print(f"\nporties voor {self}:\n>>> {self.porties}")
        else:
            print(f"\n{self} bevat geen wijzigingen voor aantal porties")