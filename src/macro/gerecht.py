from typing import Any, Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Hoofdcategorie, Categorie, HoofdcategorieënGerecht, CategorieënGerecht
from .macrotype import MacroType, MacroTypeDatabank, Hoeveelheid
from .product import Producten
from .voedingswaarde import Voedingswaarde


class Gerecht(MacroType):
    
    VELDEN = frozenset(("gerecht_naam", "categorie_uuid", "producten_standaard", "porties", "versies",))
    
    def __init__(
        self,
        gerecht_naam: str,
        categorie_uuid: str,
        producten_standaard: Dict[str, Hoeveelheid],
        porties: int,
        versies: Dict[str, Dict[str, Any]] = None,
        ) -> "Gerecht":
        
        self.gerecht_naam = gerecht_naam
        self.categorie_uuid = categorie_uuid
        self.producten_standaard = producten_standaard
        self.porties = porties
        self.versies = dict() if versies is None else versies
    
    def __repr__(self):
        return f"gerecht \"{self.gerecht_naam}\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ) -> "Gerecht":
        
        categorieën_gerecht = CategorieënGerecht.openen()
        categorie_uuid = categorieën_gerecht.kiezen(terug_naar)
        
        if categorie_uuid is STOP:
            return STOP
        
        gerecht_naam    = invoer_validatie(
            "gerechtnaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        producten = Producten.openen()
        
        producten_standaard = {}
        
        while True:
            
            product_uuid, eenheid = producten.kiezen_product_eenheid(
                terug_naar = "GERECHT KLAAR",
                )
            
            if product_uuid is STOP:
                break
            
            if eenheid is STOP:
                continue
            
            aantal = invoer_validatie(
                f"hoeveel {eenheid.meervoud}",
                float,
                )
            
            hoeveelheid = Hoeveelheid(aantal, eenheid)
            producten_standaard[product_uuid] = hoeveelheid
        
        porties = invoer_validatie(
            f"hoeveel porties",
            int,
            )
        
        return cls(
            gerecht_naam = gerecht_naam,
            categorie_uuid = categorie_uuid,
            producten_standaard = producten_standaard,
            porties = porties,
            )
    
    def bewerk(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            kies_optie = invoer_kiezen(
                f"MENU {f"{self}".upper()}",
                [
                    "bewerk gerechtnaam",
                    "bewerk producten",
                    "bewerk porties",
                    "bewerk versies",
                    "bewerk categorie",
                    ],
                kies_een = False,
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                return self
            
            ...
    
    def weergeef(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te weergeven")
        
        kies_optie = invoer_kiezen(
            "veld",
            [
                "weergeef producten",
                "weergeef voedingswaarde", # benoem hier ook erbij voor hoeveel porties
                "weergeef versies",
                "weergeef recept",
                ],
            stoppen = True,
            terug_naar = terug_naar,
            )
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "weergeef producten":
            
            producten = Producten.openen()
            
            print(f"     {"HOEVEELHEID":<17} PRODUCT")
            
            for product_uuid, hoeveelheid in self.producten_standaard.items():
                print(f"     {f"{hoeveelheid}":<17} {producten[product_uuid]}")
        
        elif kies_optie == "weergeef voedingswaarde":
            
            versie_uuid = self.kiezen_versie(
                terug_naar,
                )
            
            if versie_uuid is STOP:
                return STOP
            
            versie_naam = "standaard" if versie_uuid == "standaard" else self.versies[versie_uuid]["versie_naam"]
            
            print(f"\nvoedingswaarde voor versie \"{versie_naam}\" per portie ({self.porties} porties)\n")            
            print(self.voedingswaarde(versie_uuid) / self.porties)
    
    def kiezen_versie(
        self,
        terug_naar: str,
        ) -> str | Stop:
        
        while True:
            
            if len(self.versies) == 0:
                
                kies_optie = "standaard"
            
            else:
                
                optie_dict = {
                    "standaard": "standaard"
                } | {
                    f"{versie["versie_naam"]}": versie_uuid for versie_uuid, versie in self.versies.items()
                    }
                
                kies_optie = invoer_kiezen(
                    "versie",
                    optie_dict,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
            
            return kies_optie
    
    def nieuwe_versie(
        self,
        ) -> str | Stop:
        
        versie = {}
        
        while True:
            
            kies_optie = invoer_kiezen(
                f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                [
                    "toevoegen product",
                    "verwijderen product",
                    "vervangen product",
                    "aanpassen hoeveelheid",
                    ],
                kies_een = False,
                stoppen = True,
                terug_naar = "BEWERKINGEN KLAAR",
                )
            
            if kies_optie is STOP:
                break
            
            producten = Producten.openen()
            
            if kies_optie == "toevoegen product":
                
                product_uuid, eenheid = producten.kiezen_product_eenheid(
                    terug_naar = f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                    )
                
                if product_uuid is STOP or eenheid is STOP:
                    continue
                
                if product_uuid in self.producten_standaard.keys():
                    print(f">>> {producten[product_uuid]} reeds aanwezig, kies een andere optie")
                    continue
                
                aantal = invoer_validatie(
                    f"hoeveel {eenheid.meervoud}",
                    float,
                    )
                
                hoeveelheid = Hoeveelheid(aantal, eenheid)
                
                if not "toegevoegd" in versie:
                    versie["toegevoegd"] = {}
                
                versie["toegevoegd"][product_uuid] = hoeveelheid
            
            else:
                
                product_uuid = invoer_kiezen(
                    "product",
                    {f"{producten[product_uuid]} ({hoeveelheid})": product_uuid for product_uuid, hoeveelheid in self.producten_standaard.items()},
                    stoppen = True,
                    terug_naar = f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                    )
                
                if product_uuid is STOP:
                        continue
                
                if kies_optie == "verwijderen product":
                    
                    if not "verwijderd" in versie:
                        versie["verwijderd"] = []
                    
                    if not product_uuid in versie["verwijderd"]:
                        versie["verwijderd"].append(product_uuid)
                
                elif kies_optie == "vervangen product":
                    
                    vervangend_product_uuid = invoer_kiezen(
                        "vervangend product",
                        {f"{vervangend_product}": vervangend_product_uuid for vervangend_product_uuid, vervangend_product in producten.items() if vervangend_product.ingrediënt_uuid == producten[product_uuid].ingrediënt_uuid and vervangend_product_uuid != product_uuid},
                        stoppen = True,
                        terug_naar = f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                        )
                    
                    if vervangend_product_uuid is STOP:
                        continue
                    
                    eenheid = Producten.kiezen_eenheid(
                        terug_naar = f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                        product_uuid = vervangend_product_uuid,
                        )
                    
                    if eenheid is STOP:
                        continue
                    
                    aantal = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    if not "vervangen" in versie:
                        versie["vervangen"] = {}
                    
                    versie["vervangen"][product_uuid] = {
                        "product_uuid": vervangend_product_uuid,
                        "hoeveelheid": hoeveelheid,
                        }
                
                elif kies_optie == "aanpassen hoeveelheid":
                    
                    eenheid = Producten.kiezen_eenheid(
                        terug_naar = f"MENU TOEVOEGEN VERSIE {f"{self}".upper()}",
                        product_uuid = product_uuid,
                        )
                    
                    if eenheid is STOP:
                        continue
                    
                    aantal = invoer_validatie(
                        f"hoeveel {eenheid.meervoud}",
                        float,
                        )
                    
                    hoeveelheid = Hoeveelheid(aantal, eenheid)
                    
                    if not "hoeveelheid" in versie:
                        versie["hoeveelheid"] = {}
                    
                    versie["hoeveelheid"][product_uuid] = {
                        "hoeveelheid": hoeveelheid,
                        }
        
        if not bool(versie):
            return STOP
        
        versie_naam = invoer_validatie(
            "versienaam",
            type = str,
            )
        
        versie_uuid = str(uuid4())
        versie["versie_naam"] = versie_naam
        
        self.versies[versie_uuid] = versie
        
        return versie_uuid
    
    def producten(
        self,
        versie_uuid: str = "standaard",
        ) -> Dict[str, Hoeveelheid]:
        
        producten = self.producten_standaard
        
        if versie_uuid is not "standaard":
            
            for product_uuid, hoeveelheid in self.versies[versie_uuid]["toegevoegd"].items():
                
                producten[product_uuid] = hoeveelheid
            
            for product_uuid in self.versies[versie_uuid]["verwijderd"]:
                
                del producten[product_uuid]
            
            for product_uuid, nieuw in self.versies[versie_uuid]["vervangen"].items():
                
                del producten[product_uuid]
                producten[nieuw["product_uuid"]] = nieuw["hoeveelheid"]
            
            for product_uuid, hoeveelheid in self.versies[versie_uuid]["hoeveelheid"].items():
                
                producten[product_uuid] = hoeveelheid
        
        return producten
    
    def voedingswaarde(
        self,
        versie_uuid: str = "standaard",
        ) -> Voedingswaarde:
        
        gerecht_voedingswaarde = Voedingswaarde()
        producten = Producten.openen()
        
        for product_uuid, hoeveelheid in self.producten(versie_uuid).items():
            product_voedingswaarde = producten[product_uuid].bereken_voedingswaarde(hoeveelheid)
            gerecht_voedingswaarde += product_voedingswaarde
        
        return gerecht_voedingswaarde
    
    @property
    def categorie(self) -> Categorie:
        categorieën = CategorieënGerecht.openen()
        return categorieën[self.categorie_uuid]
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return self.categorie.hoofdcategorie

class Gerechten(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "gerechten"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Gerecht.van_json, Gerecht.VELDEN),
        ObjectWijzer(Hoeveelheid.van_json, Hoeveelheid.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                "MENU GEGEVENS/GERECHT",
                [
                    "nieuw gerecht",
                    "selecteer en bewerk",
                    "selecteer en weergeef",
                    "weergeef gerechten",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuw gerecht":
                self.nieuw(
                    terug_naar = "MENU GEGEVENS/GERECHT",
                    )
            
            elif opdracht == "selecteer en bewerk":
                
                gerecht_uuid = self.kiezen_gerecht(
                    terug_naar = "MENU GEGEVENS/GERECHT",
                    uitsluiten_nieuw = True,
                    )
                if gerecht_uuid is STOP:
                    continue
                
                self[gerecht_uuid].bewerk(
                    terug_naar = "MENU GEGEVENS/GERECHT",
                    )
            
            elif opdracht == "selecteer en weergeef":
                
                gerecht_uuid = self.kiezen_gerecht(
                    terug_naar = "MENU GEGEVENS/GERECHT",
                    uitsluiten_nieuw = True,
                    )
                if gerecht_uuid is STOP:
                    continue
                
                self[gerecht_uuid].weergeef(
                    terug_naar = "MENU GEGEVENS/GERECHT",
                    )
            
            elif opdracht == "weergeef gerechten":
                
                if len(self) == 0:
                    print("\n>>> geen gerechten aanwezig")
                    continue
                
                print()
                hoofdcategorieën = HoofdcategorieënGerecht.openen()
                categorieën = CategorieënGerecht.openen()
                for hoofdcategorie_uuid, hoofdcategorie in hoofdcategorieën.items():
                    print(f"     {hoofdcategorie}")
                    for categorie_uuid, categorie in categorieën.items():
                        if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                            print(f"       {categorie}")
                            for gerecht in self.lijst:
                                if gerecht.categorie_uuid == categorie_uuid:
                                    print(f"         {gerecht}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        gerecht = Gerecht.nieuw(terug_naar)
        
        if gerecht is STOP:
            return STOP
        
        if invoer_kiezen(
            "toevoegen versie",
            {
                "ja": True,
                "nee": False,
                },
            kies_een = False,
            ):
            gerecht.nieuwe_versie(
                terug_naar = terug_naar,
                )
        
        gerecht_uuid = str(uuid4())
        self[gerecht_uuid] = gerecht
        
        self.opslaan()
        
        return gerecht_uuid
    
    def nieuwe_versie(
        self,
        gerecht_uuid: str = None,
        ):
        
        gerecht_uuid = self.kiezen_gerecht() if gerecht_uuid is None else gerecht_uuid
        versie_uuid = self[gerecht_uuid].nieuwe_versie()
        
        self.opslaan()
        
        return versie_uuid
    
    def kiezen_gerecht(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        uitsluiten_nieuw: bool = False,
        ) -> str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen gerechten aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen gerechten aanwezig, maak een nieuw gerecht",
                    [
                        "nieuw gerecht",
                        ],
                    kies_een = False,
                    stoppen = True,
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
                        "gerecht op naam of categorie, of maak een nieuwe",
                        [
                            "selecteren gerecht",
                            "zoek op gerechtnaam",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "gerecht op naam of categorie, of maak een nieuwe",
                        [
                            "selecteren gerecht",
                            "zoek op gerechtnaam",
                            "nieuw gerecht",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "selecteren gerecht":
                    
                    hoofdcategorieën_gerecht = HoofdcategorieënGerecht.openen()
                    hoofdcategorie_uuid = hoofdcategorieën_gerecht.kiezen(
                        terug_naar,
                        uitsluiten_nieuw = True,
                        )
                    if hoofdcategorie_uuid is STOP:
                        return STOP
                    
                    categorieën_gerecht = CategorieënGerecht.openen()
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {f"{categorie}": categorie_uuid for categorie_uuid, categorie in categorieën_gerecht.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if categorie_uuid is STOP:
                        return STOP
                    
                    gerecht_uuid = invoer_kiezen(
                        "ingrediënt",
                        {f"{gerecht}": gerecht_uuid for gerecht_uuid, gerecht in self.items() if gerecht.categorie_uuid == categorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if gerecht_uuid is STOP:
                        return STOP
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[gerecht_uuid]} gekozen")
                    
                    return gerecht_uuid
                
                elif kies_optie == "zoek op gerechtnaam":
                        
                    print("\ngeef een zoekterm op")
                    
                    zoekterm = invoer_validatie(
                        "gerechtnaam",
                        str,
                        kleine_letters = True,
                        )
                    
                    gerechten_mogelijk = self.zoeken(zoekterm)
                    if len(gerechten_mogelijk) == 0:
                        print(f"\n>>> zoekterm \"{zoekterm}\" levert geen gerechten op")
                        continue
                    
                    print(f"\n>>> {len(gerechten_mogelijk)} gerecht{"en" if len(gerechten_mogelijk) > 1 else ""} gevonden")
                    gerecht_uuid = invoer_kiezen(
                        "ingrediënt",
                        {self[gerecht_uuid].gerecht_naam: gerecht_uuid for gerecht_uuid in gerechten_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if gerecht_uuid is STOP:
                        continue
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[gerecht_uuid].gerecht_naam} gekozen")
                    
                    return gerecht_uuid
                
                if kies_optie == "nieuw gerecht":
                    return self.nieuw(
                        terug_naar,
                        )
    
    def kiezen_versie(
        self,
        terug_naar: str,
        gerecht_uuid: str,
        kies_bevestiging: bool = True,
        ) -> str | Stop:
        
        optie_dict = {
            "standaard": "standaard"
        } | {
            f"{versie["versie_naam"]}": versie_uuid for versie_uuid, versie in self[gerecht_uuid].versies.items()
        } | {
            "nieuwe versie": "nieuwe versie"
            }
        
        kies_optie = invoer_kiezen(
            "bestaande versie of maakt een nieuwe",
            optie_dict,
            stoppen = True,
            terug_naar = terug_naar,
            )
        
        if kies_optie is STOP:
            return STOP
        
        elif kies_optie == "nieuwe versie":
            versie_uuid = self.nieuwe_versie(gerecht_uuid)
            if kies_bevestiging: 
                print(f"\n>>> versie \"{self[gerecht_uuid].versies[versie_uuid].versie_naam}\" gekozen")
                        
        else:
            versie_uuid = kies_optie
            if kies_bevestiging: 
                print(f"\n>>> versie \"{kies_optie}\" gekozen")
        
        return versie_uuid
        
    def kiezen_gerecht_versie(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        ) -> Tuple[str | Stop, str | Stop]:
        
        gerecht_uuid = self.kiezen_gerecht(
            terug_naar,
            kies_bevestiging = kies_bevestiging,
            )
        
        if gerecht_uuid is STOP:
            return gerecht_uuid, ...
        
        versie_uuid = self.kiezen_versie(
            terug_naar,
            gerecht_uuid,
            kies_bevestiging = kies_bevestiging,
            )
        
        if versie_uuid is STOP:
            return gerecht_uuid, versie_uuid
        
        return gerecht_uuid, versie_uuid
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [gerecht_uuid for gerecht_uuid, gerecht in self.items() if zoekterm in gerecht.gerecht_naam]