from typing import Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Categorie, Categorieën, Hoofdcategorie
from .ingredient import Ingrediënt, Ingrediënten
from .macrotype import MacroType, MacroTypeDatabank, Eenheid, Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Merk(MacroType):
    
    VELDEN = frozenset(("merk_naam", ))
    
    def __init__(
        self,
        merk_naam: str,
        ) -> "Merk":
        
        self.merk_naam = merk_naam
    
    def __repr__(self) -> str:
        return f"merk \"{self.merk_naam}\""
    
    @classmethod
    def nieuw(cls) -> "Merk":
        
        merk_naam = invoer_validatie("merknaam", str, valideren = True, kleine_letters = True, uitsluiten_leeg = True, stoppen = True)
        if merk_naam is STOP:
            return STOP
        
        return cls(
            merk_naam,
            )

class Merken(MacroTypeDatabank):
    
    BESTANDSNAAM:   str                 = "merken"
    OBJECT_WIJZERS: List[ObjectWijzer]  = [
        ObjectWijzer(Merk.van_json, Merk.VELDEN),
        ]
    
    def opdracht(self):
        
        while True:
            
            if len(self) == 0:
            
                opdracht = invoer_kiezen("MENU GEGEVENS/MERK", ["nieuw merk"], stoppen = True, kies_een = False)
                
                if opdracht is STOP:
                    break
                
                elif opdracht == "nieuw merk":
                    self.nieuw()
            
            else:
                
                opdracht = invoer_kiezen("MENU GEGEVENS/MERK", ["nieuw merk", "weergeven merk"], stoppen = True, kies_een = False)
                
                if opdracht is STOP:
                    break
                
                elif opdracht == "nieuw merk":
                    self.nieuw()
                
                elif opdracht == "weergeven merk":
                    merk_uuid = self.kiezen(kies_bevestiging = False)
                    print()
                    print(self[merk_uuid])
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        merk = Merk.nieuw()
        if merk is STOP:
            return STOP
        
        merk_uuid = str(uuid4())
        self[merk_uuid] = merk
        
        self.opslaan()
        
        return merk_uuid if geef_uuid else merk
    
    def kiezen(
        self,
        kies_bevestiging:   bool    = True,
        geef_uuid:          bool    = True,
        stoppen:            bool    = True,
        ) -> Merk | str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                kies_optie = invoer_kiezen("geen merken aanwezig, maak een nieuw merk", ["nieuw merk"], stoppen = stoppen, kies_een = False)
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(geef_uuid)
            
            else:
                
                kies_optie = invoer_kiezen("merk op naam of maak een nieuwe", ["merknaam", "nieuw merk"], stoppen = stoppen)
                
                if kies_optie is STOP:
                    return STOP
                
                if kies_optie == "merknaam":
                    
                    print("\ngeef een zoekterm op voor een merk")
                    zoekterm = invoer_validatie("zoekterm", str, kleine_letters = True)
                    
                    merken_mogelijk = [merk_uuid for merk_uuid, merk in self.items() if zoekterm in merk.merk_naam]
                    
                    if len(merken_mogelijk) == 0:
                        print(f"\n>>> geen merken gevonden")
                        continue
                    
                    merk_uuid = invoer_kiezen("merk", {merk.merk_naam: merk_uuid for merk_uuid, merk in self.items() if merk_uuid in merken_mogelijk}, stoppen = True)
                    
                    if merk_uuid is STOP:
                        continue
                    
                    if kies_bevestiging: print(f"\n>>> merk \"{self[merk_uuid].merk_naam}\" gekozen")
                    
                    return merk_uuid if geef_uuid else self[merk_uuid]
                
                else:
                    return self.nieuw(geef_uuid)

class Product(MacroType):
    
    VELDEN = frozenset(("product_naam", "merk_uuid", "voedingswaarde", "basis_eenheid", "ingrediënt_uuid", "opmerking", "eenheden",))
    
    def __init__(
        self,
        product_naam:       str,
        merk_uuid:          str,
        voedingswaarde:     Voedingswaarde,
        basis_eenheid:      Eenheid,
        ingrediënt_uuid:    str,
        opmerking:          str                 = None,
        eenheden:           Dict[Eenheid, int]  = None,
        ) -> "Product":
        
        self.product_naam       = product_naam
        self.merk_uuid          = merk_uuid
        self.opmerking          = opmerking
        self.voedingswaarde     = voedingswaarde
        self.basis_eenheid      = basis_eenheid
        self.ingrediënt_uuid    = ingrediënt_uuid
        self.eenheden           = dict() if eenheden is None else eenheden
    
    def __repr__(self) -> str:
        return f"product \"{self.product_naam} ({self.merk})\"" \
        + f"\nmet eenheden" \
        + "\n".join([f"    {f"{Hoeveelheid(1, eenheid)}":<12}: {Hoeveelheid(waarde, self.basis_eenheid)}" for eenheid, waarde in self.eenheden.items()]) \
        + f"\nvoedingswaarde per {Hoeveelheid(100, self.basis_eenheid)}:" \
        + f"\n{self.voedingswaarde}"
    
    @classmethod
    def nieuw(cls) -> "Product":
        
        ingrediënten    = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen(stoppen = True)
        
        if ingrediënt_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuw product onder ingrediënt \"{ingrediënten[ingrediënt_uuid].ingrediënt_naam}\"")
        product_naam    = invoer_validatie("productnaam", str, valideren = True, kleine_letters = True, uitsluiten_leeg = True)
        merken          = Merken.openen()
        merk_uuid       = merken.kiezen()
        
        if merk_uuid is STOP:
            return STOP
        
        opmerking       = invoer_validatie("opmerking", str, kleine_letters = True)
        basis_eenheid   = Eenheid(invoer_kiezen("eenheid waarvoor voedingswaarden gelden", {f"{Hoeveelheid(100, basis_eenheid)}": basis_eenheid for basis_eenheid in Hoeveelheid.BASIS_EENHEDEN}))
        voedingswaarde  = Voedingswaarde.nieuw(basis_eenheid)
        
        return cls(
            product_naam,
            merk_uuid,
            voedingswaarde,
            basis_eenheid,
            ingrediënt_uuid,
            opmerking,
            )
    
    def nieuwe_eenheid(self) -> Eenheid:
        # TE DOEN: check toevoegen voor overschrijven
        eenheid = invoer_kiezen("eenheid", {eenheid.enkelvoud: eenheid for eenheid in Eenheid if eenheid not in Hoeveelheid.BASIS_EENHEDEN and eenheid not in Hoeveelheid.ENERGIE_EENHEDEN})
        
        print(f"hoeveel {self.basis_eenheid.meervoud} is \"{Hoeveelheid(1, eenheid)}\"?")
        waarde = invoer_validatie(f"hoeveel {self.basis_eenheid.meervoud}", type = int)
        
        print(f">>> eenheid \"{eenheid.meervoud}\" toegevoegd van {Hoeveelheid(waarde, self.basis_eenheid)}")
        self.eenheden[eenheid] = waarde
        
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
    
    @property
    def merk(self) -> Merk:
        merken = Merken.openen()
        return merken[self.merk_uuid]
    
    def bereken_voedingswaarde(
        self,
        hoeveelheid: Hoeveelheid,
        ) -> Voedingswaarde:
        
        return self.voedingswaarde * (hoeveelheid.waarde/100.0) * (1.0 if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else self.eenheden[hoeveelheid.eenheid])

class Producten(MacroTypeDatabank):
    
    BESTANDSNAAM:   str                 = "producten"
    OBJECT_WIJZERS: List[ObjectWijzer]  = [
        ObjectWijzer(Product.van_json, Product.VELDEN),
        ObjectWijzer(Voedingswaarde.van_json, Voedingswaarde.VELDEN),
        ]
    
    def opdracht(self):
        
        while True:
            
            if len(self) == 0:
                opdracht = invoer_kiezen("MENU GEGEVENS/PRODUCT", ["nieuw product"], stoppen = True, kies_een = False)
            
                if opdracht is STOP:
                    break
                
                elif opdracht == "nieuw product":
                    self.nieuw()
                
            else:
                opdracht = invoer_kiezen("MENU GEGEVENS/PRODUCT", ["nieuw product", "nieuwe eenheid", "weergeven product"], stoppen = True, kies_een = False)
                
                if opdracht is STOP:
                    break
                
                elif opdracht == "nieuw product":
                    self.nieuw()
                
                elif opdracht == "nieuwe eenheid":
                    self.nieuwe_eenheid()
                
                elif opdracht == "weergeven product":
                    product = self.kiezen_product(kies_bevestiging = False, geef_uuid = False)
                    print()
                    print(product)
        
        return self
    
    def nieuw(
        self,
        geef_uuid: bool = True,
        ):
        
        product = Product.nieuw()
        
        if product is STOP:
            return STOP
        
        if invoer_kiezen("toevoegen nieuwe eenheid", {"ja": True, "nee": False}, kies_een = False):
            product.nieuwe_eenheid()
        
        product_uuid = str(uuid4())
        product.uuid = product_uuid
        self[product_uuid] = product
        
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
        stoppen:            bool    = True,
        ) -> Product | str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                kies_optie = invoer_kiezen("geen producten aanwezig, maak een nieuw product", ["nieuw product"], stoppen = stoppen, kies_een = False)
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(geef_uuid)
            
            else:
            
                kies_optie = invoer_kiezen("product op naam, ingrediënt of categorie, of maak een nieuwe", ["zoek op productnaam", "zoek op ingrediëntnaam", "zoek op categorie", "nieuw product"], stoppen = stoppen)
                
                if kies_optie is STOP:
                    return STOP
                
                if kies_optie == "zoek op ingrediëntnaam" or kies_optie == "zoek op productnaam" or kies_optie == "zoek op categorie":
                    
                    if kies_optie == "zoek op ingrediëntnaam" or kies_optie == "zoek op categorie":
                        
                        if kies_optie == "zoek op ingrediëntnaam":
                            
                            print("\ngeef een zoekterm op voor een ingrediënt")
                            zoekterm = invoer_validatie("zoekterm", str, kleine_letters = True)
                            
                            ingrediënten = Ingrediënten.openen()
                            ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if zoekterm in ingrediënt.ingrediënt_naam]
                        
                        else:
                            
                            categorieën = Categorieën.openen()
                            categorie_uuid = categorieën.kiezen()
                            
                            if categorie_uuid is STOP:
                                STOP
                            
                            ingrediënten = Ingrediënten.openen()
                            ingrediënten_mogelijk = [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt.categorie_uuid == categorie_uuid]
                        
                        if len(ingrediënten_mogelijk) == 0:
                            print(f">>> geen ingrediënten gevonden")
                            continue
                        
                        ingrediënt_uuid = invoer_kiezen("ingrediënt", {ingrediënt.ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt_uuid in ingrediënten_mogelijk}, stoppen = True)
                        
                        if ingrediënt_uuid is STOP:
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
                    
                    if product_uuid is STOP:
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
        
        optie_dict = {
            f"per \"{self[product_uuid].basis_eenheid.meervoud}\"": "basiseenheid"
        } | {
            f"per \"{eenheid.enkelvoud}\"": eenheid for eenheid in self[product_uuid].eenheden.keys()
        } | {
            "nieuwe eenheid": "nieuwe eenheid",
            }
        
        kies_optie = invoer_kiezen("bestaande eenheid of maakt een nieuwe", optie_dict, stoppen = stoppen)
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "nieuwe eenheid":
            eenheid =  self.nieuwe_eenheid(product_uuid)
                        
        elif kies_optie == "basiseenheid":
            eenheid = self[product_uuid].basis_eenheid
        
        else:
            eenheid = kies_optie
        
        if kies_bevestiging: print(f"\n>>> eenheid \"{eenheid.meervoud}\" gekozen")
        
        return eenheid
    
    def kiezen_product_eenheid(
        self,
        kies_bevestiging:   bool    = True,
        geef_uuid:          bool    = True,
        stoppen:            bool    = True,
        ) -> Tuple[Product | Stop, Eenheid | Stop]:
        
        product_uuid = self.kiezen_product(kies_bevestiging, stoppen)
        
        if product_uuid is STOP:
            return STOP, ...
        
        eenheid = self.kiezen_eenheid(product_uuid, kies_bevestiging, stoppen)
        
        if eenheid is STOP:
            return product_uuid if geef_uuid else self[product_uuid], STOP
        
        return product_uuid if geef_uuid else self[product_uuid], eenheid