from typing import Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Categorie, Categorieën, Hoofdcategorie
from .ingredient import Ingrediënt, Ingrediënten
from .macrotype import MacroType, MacroTypeDatabank, Eenheid, Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Product(MacroType):
    
    VELDEN = frozenset(("product_naam", "merk_naam", "voedingswaarde", "basis_eenheid", "ingrediënt_uuid", "opmerking", "eenheden",))
    
    def __init__(
        self,
        product_naam:       str,
        merk_naam:          str,
        voedingswaarde:     Voedingswaarde,
        basis_eenheid:      Eenheid,
        ingrediënt_uuid:    str,
        opmerking:          str                     = None,
        eenheden:           Dict[Eenheid, float]    = None,
        ) -> "Product":
        
        self.product_naam       = product_naam
        self.merk_naam          = merk_naam
        self.opmerking          = opmerking
        self.voedingswaarde     = voedingswaarde
        self.basis_eenheid      = basis_eenheid
        self.ingrediënt_uuid    = ingrediënt_uuid
        self.eenheden           = dict() if eenheden is None else eenheden
    
    def __repr__(self) -> str:
        return f"product \"{self.product_naam} ({self.merk_naam})\"" \
        + f"\nvoedingswaarde per 100 {self.eenheid.enkelvoud}:" \
        + f"\n{self.voedingswaarde}"
    
    @classmethod
    def nieuw(cls) -> "Product":
        
        ingrediënten    = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen()
        print(f"\ninvullen gegevens nieuw product onder ingrediënt \"{ingrediënten[ingrediënt_uuid].ingrediënt_naam}\"")
        product_naam    = invoer_validatie("productnaam", str, valideren = True, kleine_letters = True)
        merk_naam       = invoer_validatie("merknaam", str, valideren = True, kleine_letters = True)
        opmerking       = invoer_validatie("opmerking", str, kleine_letters = True)
        basis_eenheid   = Eenheid(invoer_kiezen("eenheid", ["g", "ml"]))
        voedingswaarde  = Voedingswaarde.nieuw(basis_eenheid)
        
        return cls(
            product_naam,
            merk_naam,
            voedingswaarde,
            basis_eenheid,
            ingrediënt_uuid,
            opmerking,
            )
    
    def nieuwe_eenheid(self) -> Eenheid:
        
        eenheid = invoer_kiezen("eenheid", {Eenheid[eenheid].enkelvoud: Eenheid[eenheid] for eenheid in Eenheid if eenheid not in Eenheid.BASISEENHEDEN})
        
        print(f"hoeveel 100 {self.eenheid.enkelvoud} is 1 {eenheid.enkelvoud}?")
        aantal_ons = invoer_validatie(f"hoeveel 100 {self.eenheid.enkelvoud}", type = float)
        
        print(f">>> eenheid {eenheid.meervoud} toegevoegd van {aantal_ons:.2f} {self.eenheid.enkelvoud}")
        self.eenheden[eenheid.enkelvoud] = aantal_ons
        
        return eenheid
    
    @property
    def ingrediënt(self) -> Ingrediënt:
        ingrediënten = Ingrediënten.openen()
        return ingrediënten[self.ingrediënt_uuid]
    
    @property
    def categorie(self) -> Categorie:
        return self.ingrediënt.categorie
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return self.ingrediënt.categorie.hoofdcategorie
    
class Producten(MacroTypeDatabank):
    
    BESTANDSNAAM:   str                 = "producten"
    OBJECT_WIJZERS: List[ObjectWijzer]  = [
        ObjectWijzer(Product.van_json, Product.VELDEN),
        ObjectWijzer(Voedingswaarde.van_json, Voedingswaarde.VELDEN),
        ]
    
    def opdracht(self):
        
        while True:
            
            opdracht = invoer_kiezen("opdracht product", ["nieuw product", "nieuwe eenheid", "weergeven product"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuw product":
                self.nieuw()
            
            elif opdracht == "nieuwe eenheid":
                self.nieuwe_eenheid()
            
            elif opdracht == "weergeven product":
                product_uuid = self.kiezen(kies_bevestiging = False)
                print()
                print(self[product_uuid])
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        product = Product.nieuw()
        
        if invoer_kiezen("toevoegen nieuwe eenheid", {"ja": True, "nee": False}, kies_een = False):
            product.nieuwe_eenheid()
        
        product_uuid = str(uuid4())
        self[product_uuid] = product\
        
        self.opslaan()
        
        return product_uuid if geef_uuid else product
    
    def nieuwe_eenheid(
        self,
        product_uuid: str = None,
        ):
        
        product_uuid = self.kiezen_product() if product_uuid is None else product_uuid
        eenheid = self[product_uuid].nieuwe_eenheid()
        
        self.opslaan()
        
        return eenheid
    
    def kiezen_product(
        self,
        kies_bevestiging:   bool    = True,
        geef_uuid:          bool    = True,
        stoppen:            bool    = False,
        ) -> Product | str | Stop:
        
        while True:
            
            kies_optie = invoer_kiezen("product op naam of categorie, of maak een nieuwe", ["productnaam", "ingrediëntnaam", "categorie", "nieuw"], stoppen = stoppen)
            
            if kies_optie is STOP:
                return STOP
            
            if kies_optie == "ingrediëntnaam" or kies_optie == "productnaam" or kies_optie == "categorie":
                
                if kies_optie == "ingrediëntnaam" or kies_optie == "categorie":
                    
                    if kies_optie == "ingrediëntnaam":
                        
                        print("\ngeef een zoekterm op voor een ingrediënt")
                        zoekterm = invoer_validatie("zoekterm", str, kleine_letters = True)
                        
                        ingrediënten = Ingrediënten.openen()
                        ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if zoekterm in ingrediënt.ingrediënt_naam]
                    
                    else:
                        
                        categorieën = Categorieën.openen()
                        categorie_uuid = categorieën.kiezen()
                        
                        ingrediënten = Ingrediënten.openen()
                        ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt.categorie_uuid == categorie_uuid]
                    
                    if len(ingrediënten_mogelijk) == 0:
                        print(f">>> geen ingrediënten gevonden")
                        continue
                    
                    ingrediënt_uuid = invoer_kiezen("ingrediënt", {ingrediënt.ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt_uuid in ingrediënten_mogelijk}, stoppen = True)
                    
                    if not bool(ingrediënt_uuid):
                        continue
                    
                    print(f"\n>>> ingrediënt \"{ingrediënten[ingrediënt_uuid].ingrediënt_naam}\" gekozen")
                    
                    producten_mogelijk = [product_uuid for product_uuid, product in self.items() if product.ingrediënt_uuid == ingrediënt_uuid]
                
                else:
                    
                    print("\ngeef een zoekterm op voor een product")
                    zoekterm = invoer_validatie("zoekterm", str, kleine_letters = True)
                    
                    producten_mogelijk = [product_uuid for product_uuid, product in self.items() if zoekterm in product.product_naam]
                
                if len(producten_mogelijk) == 0:
                    print(f"\n>>> geen producten gevonden")
                    continue
                
                product_uuid = invoer_kiezen("product", {product.product_naam: product_uuid for product_uuid, product in self.items() if product_uuid in producten_mogelijk}, stoppen = True)
                
                if not bool(product_uuid):
                    continue
                
                if kies_bevestiging: print(f"\n>>> product \"{self[product_uuid].product_naam}\" gekozen")
                
                return product_uuid if geef_uuid else self[product_uuid]
            
            else:
                return self.nieuw(geef_uuid)
    
    def kiezen_eenheid(
        self,
        product_uuid:       str,
        kies_bevestiging:   bool    = True,
        stoppen:            bool    = False,
        ) -> Eenheid | Stop:
        
        optie_dict = {"nieuwe eenheid": "nieuwe eenheid", f"eenheid \"{self[product_uuid].eenheid.enkelvoud}\"": "eigen eenheid"} | {f"eenheid \"{eenheid.enkelvoud}\"": eenheid for eenheid in self[product_uuid].eenheden.keys()}
        
        kies_optie = invoer_kiezen("bestaande eenheid of maakt een nieuwe", optie_dict, stoppen = stoppen)
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "nieuwe eenheid":
            eenheid =  self.nieuwe_eenheid(product_uuid)
                        
        elif kies_optie == "eigen eenheid":
            eenheid = self[product_uuid].eenheid
        
        else:
            eenheid = kies_optie
        
        if kies_bevestiging: print(f"\n>>> eenheid \"{eenheid.meervoud}\" gekozen")
        
        return eenheid
        
    def kiezen_product_eenheid(
        self,
        kies_bevestiging:   bool    = True,
        geef_uuid:          bool    = True,
        stoppen:            bool    = False,
        ) -> Tuple[Product | Stop, Eenheid | Stop]:
        
        product_uuid = self.kiezen_product(kies_bevestiging, stoppen)
        
        if product_uuid is STOP:
            return STOP, ...
        
        eenheid = self.kiezen_eenheid(product_uuid, kies_bevestiging, stoppen)
        
        if eenheid is STOP:
            return product_uuid if geef_uuid else self[product_uuid], STOP
        
        return product_uuid if geef_uuid else self[product_uuid], eenheid