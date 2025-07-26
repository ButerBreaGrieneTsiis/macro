from typing import Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Categorie, Categorieën, Hoofdcategorie, Hoofdcategorieën
from .ingredient import Ingrediënt, Ingrediënten
from .macrotype import MacroType, MacroTypeDatabank, Eenheid, Hoeveelheid
from .voedingswaarde import Voedingswaarde


class Merk(MacroType):
    
    VELDEN = frozenset((
        "merk_naam",
        ))
    
    def __init__(
        self,
        merk_naam: str,
        ) -> "Merk":
        
        self.merk_naam = merk_naam
    
    def __repr__(self) -> str:
        return f"merk \"{self.merk_naam}\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ) -> "Merk":
        
        merk_naam = invoer_validatie(
            "merknaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            terug_naar = terug_naar,
            )
        
        return cls(
            merk_naam,
            )
    
    def bewerk(
        self,
        terug_naar: str,
        ):
        
        print(f"\ninvullen nieuwe naam voor {self}")
        merk_naam = invoer_validatie(
            "merknaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        self.merk_naam = merk_naam
        
        return self

class Merken(MacroTypeDatabank):
    
    BESTANDSNAAM:   str                 = "merken"
    OBJECT_WIJZERS: List[ObjectWijzer]  = [
        ObjectWijzer(Merk.van_json, Merk.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                "MENU GEGEVENS/MERK",
                [
                    "nieuw merk",
                    "selecteer en bewerk",
                    "weergeef merken",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
                
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuw merk":
                self.nieuw(terug_naar = "MENU GEGEVENS/MERK")
            
            elif opdracht == "selecteer en bewerk":
                
                merk_uuid = self.kiezen(
                    terug_naar = "MENU GEGEVENS/MERK",
                    uitsluiten_nieuw = True,
                    )
                if merk_uuid is STOP:
                    continue
                
                self[merk_uuid].bewerk(
                    terug_naar = "MENU GEGEVENS/MERK",
                    )
            
            elif opdracht == "weergeef merken":
                
                print()
                for merk in self.lijst:
                    print(f"     {merk}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        merk = Merk.nieuw(terug_naar)
        if merk is STOP:
            return STOP
        
        merk_uuid = str(uuid4())
        self[merk_uuid] = merk
        
        self.opslaan()
        
        return merk_uuid
    
    def kiezen(
        self,
        terug_naar: str,
        uitsluiten_nieuw: bool = False,
        ) -> Merk | str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen merken aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen merken aanwezig, maak een nieuw merk",
                    [
                        "nieuw merk",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(
                        terug_naar,
                        )
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "merk op naam of maak een nieuwe",
                        [
                            "merknaam",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "merk op naam of maak een nieuwe",
                        [
                            "merknaam",
                            "nieuw merk",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                if kies_optie == "merknaam":
                    
                    print("\ngeef een zoekterm op voor een merk")
                    zoekterm = invoer_validatie(
                        "zoekterm",
                        str,
                        kleine_letters = True,
                        )
                    
                    merken_mogelijk = [merk_uuid for merk_uuid, merk in self.items() if zoekterm in merk.merk_naam]
                    
                    if len(merken_mogelijk) == 0:
                        print(f"\n>>> geen merken gevonden")
                        continue
                    
                    merk_uuid = invoer_kiezen(
                        "merk",
                        {self[merk_uuid].merk_naam: merk_uuid for merk_uuid in merken_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if merk_uuid is STOP:
                        continue
                    
                    print(f"\n>>> {self[merk_uuid]} gekozen")
                    
                    return merk_uuid
                
                elif kies_optie == "nieuw merk":
                    return self.nieuw(
                        terug_naar,
                        )

class Product(MacroType):
    
    VELDEN = frozenset((
        "product_naam",
        "merk_uuid",
        "voedingswaarde",
        "basis_eenheid",
        "ingrediënt_uuid",
        "opmerking",
        "eenheden",
        ))
    
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
        return f"product \"{self.product_naam} ({self.merk})\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ) -> "Product":
        
        ingrediënten    = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen(terug_naar)
        
        if ingrediënt_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuw product onder \"{ingrediënten[ingrediënt_uuid]}\"")
        product_naam    = invoer_validatie(
            "productnaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        merken          = Merken.openen()
        merk_uuid       = merken.kiezen(terug_naar)
        
        if merk_uuid is STOP:
            return STOP
        
        opmerking       = invoer_validatie(
            "opmerking",
            str,
            kleine_letters = True,
            )
        basis_eenheid   = Eenheid(invoer_kiezen(
            "eenheid waarvoor voedingswaarden gelden",
            {f"{Hoeveelheid(100, basis_eenheid)}": basis_eenheid for basis_eenheid in Hoeveelheid.BASIS_EENHEDEN},
            ))
        voedingswaarde  = Voedingswaarde.nieuw(basis_eenheid)
        
        return cls(
            product_naam,
            merk_uuid,
            voedingswaarde,
            basis_eenheid,
            ingrediënt_uuid,
            opmerking,
            )
    
    def bewerk(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            print(f"selecteren wat te bewerken")
            
            kies_optie = invoer_kiezen(
                f"MENU {f"{self}".upper()}",
                [
                    "bewerk productnaam",
                    "bewerk merk",
                    "bewerk voedingswaarde",
                    "bewerk eenheden",
                    "bewerk ingrediënt",
                    ],
                kies_een = False,
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                return self
            
            elif kies_optie == "bewerk productnaam":
            
                print(f"\ninvullen nieuwe naam voor {self}")
                product_naam = invoer_validatie(
                    "productnaam",
                    str,
                    valideren = True,
                    kleine_letters = True,
                    uitsluiten_leeg = True,
                    )
                
                self.product_naam = product_naam
            
            elif kies_optie == "bewerk merk":
                
                merken = Merken.openen()
                merk_uuid = merken.kiezen(
                    terug_naar = f"MENU {f"{self}".upper()}",
                    uitsluiten_nieuw = True,
                    )
                
                if merk_uuid is STOP:
                    continue
                
                self.merk_uuid = merk_uuid
            
            elif kies_optie == "bewerk voedingswaarde":
                
                print(f"\nhuidige voedingswaarde voor {Hoeveelheid(100, self.basis_eenheid)}\n")
                print(self.voedingswaarde)
                
                voedingswaarde = Voedingswaarde.nieuw(self.basis_eenheid)
                self.voedingswaarde = voedingswaarde
            
            elif kies_optie == "bewerk eenheden":
                
                self.bewerk_eenheden()
            
            elif kies_optie == "bewerk ingrediënt":
                
                ingrediënten = Ingrediënten.openen()
                ingrediënt_uuid = ingrediënten.kiezen(
                    terug_naar = f"MENU {f"{self}".upper()}",
                    uitsluiten_nieuw = True,
                    )
                
                if ingrediënt_uuid is STOP:
                    continue
                
                self.ingrediënt_uuid = ingrediënt_uuid
        
    def weergeef(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te weergeven")
        
        while True:
        
            kies_optie = invoer_kiezen(
                "veld",
                [
                    "weergeef merk",
                    "weergeef voedingswaarde",
                    "weergeef eenheden",
                    "weergeef hoofdcategorie",
                    "weergeef categorie",
                    "weergeef ingrediënt",
                    ],
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                break
            
            elif kies_optie == "weergeef merk":
                
                print(f"\n     {self.merk}")
            
            elif kies_optie == "weergeef voedingswaarde":
                
                print(f"\nvoedingswaarde voor {Hoeveelheid(100, self.basis_eenheid)}\n")
                print(self.voedingswaarde)
            
            elif kies_optie == "weergeef eenheden":
                
                if len(self.eenheden) == 0:
                    print("\n>>> geen eenheden gedefinieerd")
                else:
                    print(f"\n     EENHEID          HOEVEELHEID CALORIEËN")
                    [print(f"     {f"{Hoeveelheid(1, eenheid)}":<17}{f"{Hoeveelheid(waarde, self.basis_eenheid)}":<11} {self.voedingswaarde.calorieën * waarde / 100.0}") for eenheid, waarde in self.eenheden.items()]
            
            elif kies_optie == "weergeef hoofdcategorie":
                
                print(f"\n     {self.hoofdcategorie}")
            
            elif kies_optie == "weergeef categorie":
                
                print(f"\n     {self.categorie}")
            
            elif kies_optie == "weergeef ingrediënt":
                
                print(f"\n     {self.ingrediënt}")
    
    def bewerk_eenheden(self) -> Eenheid:
        
        eenheid = invoer_kiezen(
            "eenheid",
            {eenheid.enkelvoud: eenheid for eenheid in Eenheid if eenheid not in Hoeveelheid.BASIS_EENHEDEN and eenheid not in Hoeveelheid.ENERGIE_EENHEDEN},
            )
        
        print(f"hoeveel {self.basis_eenheid.meervoud} is \"{Hoeveelheid(1, eenheid)}\"?")
        waarde = invoer_validatie(
            f"hoeveel {self.basis_eenheid.meervoud}",
            int,
            )
        
        if eenheid in self.eenheden:
            if waarde == self.eenheden[eenheid]:
                print(f">>> geen wijziging")
            else: 
                print(f">>> eenheid \"{eenheid.meervoud}\" van {Hoeveelheid(waarde, self.basis_eenheid)} bestaat al, overschrijven?")
                
                if invoer_kiezen(
                    "keuze",
                    {
                        "ja": True,
                        "nee": False,
                        },
                    kies_een = False,
                    ):
                    self.eenheden[eenheid] = waarde
        
        else:
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
    
    BESTANDSNAAM: str = "producten"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Product.van_json, Product.VELDEN),
        ObjectWijzer(Voedingswaarde.van_json, Voedingswaarde.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
        
            opdracht = invoer_kiezen(
                "MENU GEGEVENS/PRODUCT",
                [
                    "nieuw product",
                    "selecteer en bewerk",
                    "selecteer en weergeef",
                    "weergeef producten",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuw product":
                self.nieuw(
                    terug_naar = "MENU GEGEVENS/PRODUCT",
                    )
            
            elif opdracht == "selecteer en bewerk":
                
                product_uuid = self.kiezen_product(
                    terug_naar = "MENU GEGEVENS/PRODUCT",
                    uitsluiten_nieuw = True,
                    )
                if product_uuid is STOP:
                    continue
                
                self[product_uuid].bewerk(
                    terug_naar = "MENU GEGEVENS/PRODUCT",
                    )
            
            elif opdracht == "selecteer en weergeef":
                
                product_uuid = self.kiezen_product(
                    terug_naar = "MENU GEGEVENS/PRODUCT",
                    uitsluiten_nieuw = True,
                    )
                if product_uuid is STOP:
                    continue
                
                self[product_uuid].weergeef(
                    terug_naar = "MENU GEGEVENS/PRODUCT",
                    )
            
            elif opdracht == "weergeef producten":
                
                if len(self) == 0:
                    print("\n>>> geen producten aanwezig")
                    continue
                
                while True:
                    
                    opdracht_weergeef = invoer_kiezen(
                        "MENU GEGEVENS/PRODUCT/WEERGEEF",
                        [
                            "alle producten",
                            "alle producten onder een hoofdcategorie",
                            "alle producten onder een categorie",
                            "alle producten onder een ingrediënt",
                            ],
                        stoppen = True,
                        kies_een = False,
                        terug_naar = "MENU GEGEVENS/PRODUCT",
                        )
                    if opdracht_weergeef is STOP:
                        break
                    
                    elif opdracht_weergeef == "alle producten":
                        
                        print()
                        hoofdcategorieën = Hoofdcategorieën.openen()
                        categorieën = Categorieën.openen()
                        ingrediënten = Ingrediënten.openen()
                        for hoofdcategorie_uuid, hoofdcategorie in hoofdcategorieën.items():
                            print(f"     {hoofdcategorie}")
                            for categorie_uuid, categorie in categorieën.items():
                                if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                                    print(f"       {categorie}")
                                    for ingrediënt_uuid, ingrediënt in ingrediënten.items():
                                        if ingrediënt.categorie_uuid == categorie_uuid:
                                            print(f"         {ingrediënt}")
                                            for product in self.lijst:
                                                if product.ingrediënt_uuid == ingrediënt_uuid:
                                                    print(f"           {product}")
                    
                    elif opdracht_weergeef == "alle producten onder een hoofdcategorie":
                        
                        hoofdcategorieën = Hoofdcategorieën.openen()
                        
                        hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/PRODUCT/WEERGEEF",
                            )
                        
                        if hoofdcategorie_uuid is STOP:
                            continue
                        
                        print()
                        categorieën = Categorieën.openen()
                        ingrediënten = Ingrediënten.openen()
                        for categorie_uuid, categorie in categorieën.items():
                            if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                                print(f"     {categorie}")
                                for ingrediënt_uuid, ingrediënt in ingrediënten.items():
                                    if ingrediënt.categorie_uuid == categorie_uuid:
                                        print(f"       {ingrediënt}")
                                        for product in self.lijst:
                                            if product.ingrediënt_uuid == ingrediënt_uuid:
                                                print(f"         {product}")
                    
                    elif opdracht_weergeef == "alle producten onder een categorie":
                        
                        categorieën = Categorieën.openen()
                        
                        categorie_uuid = categorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/PRODUCT/WEERGEEF",
                            )
                        
                        if categorie_uuid is STOP:
                            continue
                        
                        print()
                        
                        ingrediënten = Ingrediënten.openen()
                        for ingrediënt_uuid, ingrediënt in ingrediënten.items():
                            if ingrediënt.categorie_uuid == categorie_uuid:
                                print(f"     {ingrediënt}")
                                for product in self.lijst:
                                    if product.ingrediënt_uuid == ingrediënt_uuid:
                                        print(f"       {product}")
                    
                    elif opdracht_weergeef == "alle producten onder een ingrediënt":
                        
                        ingrediënten = Ingrediënten.openen()
                        
                        ingrediënt_uuid = ingrediënten.kiezen(
                            terug_naar = "MENU GEGEVENS/PRODUCT/WEERGEEF",
                            )
                        
                        if ingrediënt_uuid is STOP:
                            continue
                        
                        print()
                        
                        for product in self.lijst:
                            if product.ingrediënt_uuid == ingrediënt_uuid:
                                print(f"     {product}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        product = Product.nieuw(terug_naar)
        
        if product is STOP:
            return STOP
        
        if invoer_kiezen(
            "toevoegen nieuwe eenheid",
            {
                "ja": True,
                "nee": False,
                },
            kies_een = False,
            ):
            product.bewerk_eenheden()
        
        product_uuid = str(uuid4())
        self[product_uuid] = product
        
        self.opslaan()
        
        return product_uuid
    
    def nieuwe_eenheid(
        self,
        product_uuid: str = None,
        ):
        
        product_uuid = self.kiezen_product() if product_uuid is None else product_uuid
        eenheid = self[product_uuid].bewerk_eenheden()
        
        self.opslaan()
        
        return eenheid
    
    def kiezen_product(
        self,
        terug_naar: str,
        uitsluiten_nieuw: bool = False,
        ) -> str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen producten aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen producten aanwezig, maak een nieuw product",
                    [
                        "nieuw product",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(
                        terug_naar,
                        )
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "product op naam, ingrediënt of categorie, of maak een nieuwe",
                        [
                            "selecteren product",
                            "zoek op productnaam",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                else:
                    kies_optie = invoer_kiezen(
                        "product op naam, ingrediënt of categorie, of maak een nieuwe",
                        [
                            "selecteren product",
                            "zoek op productnaam",
                            "nieuw product",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "selecteren product":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                        terug_naar,
                        uitsluiten_nieuw = True,
                        )
                    if hoofdcategorie_uuid is STOP:
                        return STOP
                    
                    categorieën = Categorieën.openen()
                    
                    if len([categorie for categorie in categorieën.lijst if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid]) == 0:
                        print(f"\n>>> geen categorieën aanwezig onder {hoofdcategorieën[hoofdcategorie_uuid]}")
                        return STOP
                    
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {f"{categorie}": categorie_uuid for categorie_uuid, categorie in categorieën.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if categorie_uuid is STOP:
                        return STOP
                    
                    ingrediënten = Ingrediënten.openen()
                    
                    if len([ingrediënt for ingrediënt in ingrediënten.lijst if ingrediënt.categorie_uuid == categorie_uuid]) == 0:
                        print(f"\n>>> geen ingrediënten aanwezig onder {categorieën[categorie_uuid]}")
                        return STOP
                    
                    ingrediënt_uuid = invoer_kiezen(
                        "ingrediënt",
                        {f"{ingrediënt}": ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt.categorie_uuid == categorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if ingrediënt_uuid is STOP:
                        return STOP
                    
                    if len([product for product in self.lijst if product.ingrediënt_uuid == ingrediënt_uuid]) == 0:
                        print(f"\n>>> geen producten aanwezig onder {ingrediënten[ingrediënt_uuid]}")
                        return STOP
                    
                    product_uuid = invoer_kiezen(
                        "product",
                        {f"{product}": product_uuid for product_uuid, product in self.items() if product.ingrediënt_uuid == ingrediënt_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if product_uuid is STOP:
                        return STOP
                    
                    print(f"\n>>> {self[product_uuid]} gekozen")
                    
                    return product_uuid
                
                if kies_optie == "zoek op productnaam":
                    
                    print("\ngeef een zoekterm op")
                    
                    zoekterm = invoer_validatie(
                        "productnaam",
                        str,
                        kleine_letters = True,
                        )
                    
                    ingrediënten = Ingrediënten.openen()
                    ingrediënten_mogelijk = ingrediënten.zoeken(zoekterm)
                    producten_mogelijk = self.zoeken(zoekterm)
                    
                    if len(ingrediënten_mogelijk) == 0:
                        if len(producten_mogelijk) == 0:
                            print(f"\n>>> zoekterm \"{zoekterm}\" levert ingrediënten noch producten op")
                            continue
                        else:
                            print(f"\n>>> {len(producten_mogelijk)} product{"en" if len(producten_mogelijk) > 1 else ""} gevonden")
                    else:
                        if len(producten_mogelijk) == 0:
                            print(f"\n>>> {len(ingrediënten_mogelijk)} ingrediënt{"en" if len(ingrediënten_mogelijk) > 1 else ""} gevonden")
                        else:
                            print(f"\n>>> {len(ingrediënten_mogelijk)} ingrediënt{"en" if len(ingrediënten_mogelijk) > 1 else ""} en {len(producten_mogelijk)} product{"en" if len(producten_mogelijk) > 1 else ""} gevonden")
                    
                    uuid = invoer_kiezen(
                        "ingrediënt of product",
                        {ingrediënten[ingrediënt_uuid]: ingrediënt_uuid for ingrediënt_uuid in ingrediënten_mogelijk} | {self[product_uuid]: product_uuid for product_uuid in producten_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if uuid is STOP:
                        continue
                    
                    if uuid in ingrediënten_mogelijk:
                        
                        if len([product for product in self.lijst if product.ingrediënt_uuid == uuid]) == 0:
                            print(f"\n>>> geen producten aanwezig onder {ingrediënten[uuid]}")
                            continue
                        
                        product_uuid = invoer_kiezen(
                            "product",
                            {f"{product}": product_uuid for product_uuid, product in self.items() if product.ingrediënt_uuid == uuid},
                            stoppen = True,
                            terug_naar = terug_naar,
                            )
                        if product_uuid is STOP:
                            return STOP
                    else:
                        product_uuid = uuid
                    
                    print(f"\n>>> {self[product_uuid]} gekozen")
                    
                    return product_uuid
                
                if kies_optie == "nieuw product":
                    return self.nieuw(
                        terug_naar,
                        )
    
    def kiezen_eenheid(
        self,
        terug_naar: str,
        product_uuid: str,
        ) -> Eenheid | Stop:
        
        optie_dict = {
            f"per \"{self[product_uuid].basis_eenheid.meervoud}\"": "basiseenheid"
        } | {
            f"per \"{eenheid.enkelvoud}\"": eenheid for eenheid in self[product_uuid].eenheden.keys()
        } | {
            "nieuwe eenheid": "nieuwe eenheid",
            }
        
        kies_optie = invoer_kiezen(
            "bestaande eenheid of maakt een nieuwe",
            optie_dict,
            stoppen = True,
            terug_naar = terug_naar,
            )
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "nieuwe eenheid":
            eenheid =  self.nieuwe_eenheid(
                product_uuid = product_uuid,
                )
                        
        elif kies_optie == "basiseenheid":
            eenheid = self[product_uuid].basis_eenheid
        
        else:
            eenheid = kies_optie
        
        print(f"\n>>> eenheid \"{eenheid.meervoud}\" gekozen")
        
        return eenheid
    
    def kiezen_product_eenheid(
        self,
        terug_naar: str,
        ) -> Tuple[str | Stop, Eenheid | Stop]:
        
        product_uuid = self.kiezen_product(
            terug_naar = terug_naar,
            )
        
        if product_uuid is STOP:
            return product_uuid, ...
        
        eenheid = self.kiezen_eenheid(
            terug_naar = terug_naar,
            product_uuid = product_uuid,
            )
        
        if eenheid is STOP:
            return product_uuid, eenheid
        
        return product_uuid, eenheid
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [product_uuid for product_uuid, product in self.items() if zoekterm in product.product_naam]