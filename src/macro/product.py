from typing import Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Categorie, Categorieën, Hoofdcategorie, Hoofdcategorieën
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
            stoppen = True,
            terug_naar = terug_naar,
            )
        if merk_naam is STOP:
            return STOP
        
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
                    "toon merken",
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
            
            elif opdracht == "toon merken":
                
                print()
                for merk in self.lijst:
                    print(f"     {merk}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        geef_uuid: bool = True,
        ):
        
        merk = Merk.nieuw(terug_naar)
        if merk is STOP:
            return STOP
        
        merk_uuid = str(uuid4())
        self[merk_uuid] = merk
        
        self.opslaan()
        
        return merk_uuid if geef_uuid else merk
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        geef_uuid: bool = True,
        stoppen: bool = True,
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
                    stoppen = stoppen,
                    kies_een = False,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "merk op naam of maak een nieuwe",
                        [
                            "merknaam",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "merk op naam of maak een nieuwe",
                        [
                            "merknaam",
                            "nieuw merk",
                            ],
                        stoppen = stoppen,
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
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[merk_uuid]} gekozen")
                    
                    return merk_uuid if geef_uuid else self[merk_uuid]
                
                elif kies_optie == "nieuw merk":
                    return self.nieuw(
                        terug_naar,
                        geef_uuid = geef_uuid,
                        )

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
        return f"product \"{self.product_naam} ({self.merk})\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ) -> "Product":
        
        ingrediënten    = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen(terug_naar, stoppen = True)
        
        if ingrediënt_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuw product onder ingrediënt \"{ingrediënten[ingrediënt_uuid].ingrediënt_naam}\"")
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
            
            if kies_optie == "bewerk productnaam":
            
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
                    stoppen = True
                    )
                
                if merk_uuid is STOP:
                    continue
                
                self.merk_uuid = merk_uuid
            
            elif kies_optie == "bewerk voedingswaarde":
                
                voedingswaarde = Voedingswaarde.nieuw()
                self.voedingswaarde = voedingswaarde
            
            elif kies_optie == "bewerk eenheden":
                
                self.bewerk_eenheden()
            
            elif kies_optie == "bewerk ingrediënt":
                
                ingrediënten = Ingrediënten.openen()
                ingrediënt_uuid = ingrediënten.kiezen(
                    terug_naar = f"MENU {f"{self}".upper()}",
                    uitsluiten_nieuw = True,
                    stoppen = True,
                    )
                
                if ingrediënt_uuid is STOP:
                    continue
                
                self.ingrediënt_uuid = ingrediënt_uuid
        
    def weergeef(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te weergeven")
        
        kies_optie = invoer_kiezen(
            "veld",
            [
                "weergeef merk",
                "weergeef voedingswaarde",
                "weergeef eenheden",
                ],
            stoppen = True,
            terug_naar = terug_naar,
            )
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "weergeef merk":
            
            print(self.merk)
        
        elif kies_optie == "weergeef voedingswaarde":
            
            print(self.voedingswaarde)
        
        elif kies_optie == "weergeef eenheden":
            
            if len(self.eenheden) == 0:
                print(">>> geen eenheden gedefinieerd")
            else:
                print(f"     EENHEID     HOEVEELHEID")
                [print(f"     {f"{Hoeveelheid(1, eenheid)}":<12}{Hoeveelheid(waarde, self.basis_eenheid)}") for eenheid, waarde in self.eenheden.items()]
    
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
                    {"ja": True, "nee": False},
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
    
    BESTANDSNAAM:   str                 = "producten"
    OBJECT_WIJZERS: List[ObjectWijzer]  = [
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
                    "toon producten",
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
            
            elif opdracht == "toon producten":
                
                if len(self) == 0:
                    print("\n>>> geen producten aanwezig")
                    continue
                
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
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        geef_uuid: bool = True,
        ):
        
        product = Product.nieuw(terug_naar)
        
        if product is STOP:
            return STOP
        
        if invoer_kiezen(
            "toevoegen nieuwe eenheid",
            {"ja": True, "nee": False},
            kies_een = False,
            ):
            product.bewerk_eenheden()
        
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
        eenheid = self[product_uuid].bewerk_eenheden()
        
        self.opslaan()
        
        return eenheid
    
    def kiezen_product(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        geef_uuid: bool = True,
        stoppen: bool = True,
        uitsluiten_nieuw: bool = False,
        ) -> Product | str | Stop:
        
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
                    stoppen = stoppen,
                    kies_een = False,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                else:
                    return self.nieuw(terug_naar, geef_uuid = geef_uuid)
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "product op naam, ingrediënt of categorie, of maak een nieuwe",
                        [
                            "selecteren product",
                            "zoek op naam",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                else:
                    kies_optie = invoer_kiezen(
                        "product op naam, ingrediënt of categorie, of maak een nieuwe",
                        [
                            "selecteren product",
                            "zoek op naam",
                            "nieuw product",
                            ],
                        stoppen = stoppen,
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
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {f"{categorie}": categorie_uuid for categorie_uuid, categorie in categorieën.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                    if categorie_uuid is STOP:
                        return STOP
                    
                    ingrediënten = Ingrediënten.openen()
                    ingrediënt_uuid = invoer_kiezen(
                        "ingrediënt",
                        {f"{ingrediënt}": ingrediënt_uuid for ingrediënt_uuid, ingrediënt in ingrediënten.items() if ingrediënt.categorie_uuid == categorie_uuid},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                    if ingrediënt_uuid is STOP:
                        return STOP
                    
                    product_uuid = invoer_kiezen(
                        "product",
                        {f"{product}": product_uuid for product_uuid, product in self.items() if product.ingrediënt_uuid == ingrediënt_uuid},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                    if product_uuid is STOP:
                        return STOP
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[product_uuid]} gekozen")
                    
                    return product_uuid if geef_uuid else self[product_uuid]
                
                if kies_optie == "zoek op naam":
                    
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
                        {ingrediënten[ingrediënt_uuid].ingrediënt_naam: ingrediënt_uuid for ingrediënt_uuid in ingrediënten_mogelijk} | {self[product_uuid].product_naam: product_uuid for product_uuid in producten_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if uuid is STOP:
                        continue
                    
                    if uuid in ingrediënten_mogelijk:
                        product_uuid = invoer_kiezen(
                        "product",
                        {f"{product}": product_uuid for product_uuid, product in self.items() if product.ingrediënt_uuid == uuid},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                        if product_uuid is STOP:
                            return STOP
                    else:
                        product_uuid = uuid
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[product_uuid]} gekozen")
                    
                    return product_uuid if geef_uuid else self[product_uuid]
                
                if kies_optie == "nieuw product":
                    return self.nieuw(
                        terug_naar,
                        geef_uuid = geef_uuid,
                        )
    
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
        
        kies_optie = invoer_kiezen(
            "bestaande eenheid of maakt een nieuwe",
            optie_dict,
            stoppen = stoppen,
            )
        
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
        terug_naar: str,
        kies_bevestiging:   bool    = True,
        geef_uuid:          bool    = True,
        stoppen:            bool    = True,
        ) -> Tuple[Product | Stop, Eenheid | Stop]:
        
        product_uuid = self.kiezen_product(terug_naar, kies_bevestiging = kies_bevestiging, stoppen = stoppen)
        
        if product_uuid is STOP:
            return STOP, ...
        
        eenheid = self.kiezen_eenheid(terug_naar, product_uuid, kies_bevestiging = kies_bevestiging, stoppen = stoppen)
        
        if eenheid is STOP:
            return product_uuid if geef_uuid else self[product_uuid], STOP
        
        return product_uuid if geef_uuid else self[product_uuid], eenheid
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [product_uuid for product_uuid, product in self.items() if zoekterm in product.product_naam]