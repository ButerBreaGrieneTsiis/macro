from copy import deepcopy
from typing import Any, Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Hoofdcategorie, Categorie, HoofdcategorieënGerecht, CategorieënGerecht
from .macrotype import MacroType, MacroTypeDatabank, Hoeveelheid, Eenheid
from .product import Producten
from .voedingswaarde import Voedingswaarde


class Gerecht(MacroType):
    
    VELDEN = frozenset((
        "gerecht_naam",
        "categorie_uuid",
        "producten_standaard",
        "porties",
        "versies",
        "recept",
        ))
    
    def __init__(
        self,
        gerecht_naam: str,
        categorie_uuid: str,
        producten_standaard: Dict[str, Hoeveelheid],
        porties: int,
        versies: Dict[str, Dict[str, Any]] = None,
        recept: Dict[str, str] = None,
        ) -> "Gerecht":
        
        self.gerecht_naam = gerecht_naam
        self.categorie_uuid = categorie_uuid
        self.producten_standaard = producten_standaard
        self.porties = porties
        self.versies = dict() if versies is None else versies
        self.recept = dict() if recept is None else recept
    
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
        
        gerecht_naam = invoer_validatie(
            "gerechtnaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        producten = Producten.openen()
        
        producten_standaard = {}
        
        while True:
            
            if len(producten_standaard) > 0:
                
                calorieën_totaal    = Hoeveelheid(0, Eenheid("kcal"))
                eiwitten_totaal     = Hoeveelheid(0, Eenheid("g"))
                
                print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                for product_uuid, hoeveelheden in producten_standaard.items():
                    for hoeveelheid in hoeveelheden:
                        print(f"     {f"{hoeveelheid}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>8} {producten[product_uuid]}")
                        calorieën_totaal += producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
                        eiwitten_totaal  += producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100
                
                print(f"\n     {"TOTAAL":<18} {f"{calorieën_totaal}":>9} {f"{eiwitten_totaal}":>8}")
            
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
            
            if product_uuid in producten_standaard.keys():
                for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(producten_standaard[product_uuid]):
                    if hoeveelheid == hoeveelheid_aanwezig:
                        producten_standaard[product_uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                        break
                else:
                    producten_standaard[product_uuid].append(hoeveelheid)
            else:
                producten_standaard[product_uuid] = [hoeveelheid]
        
        if len(producten_standaard) == 0:
            return STOP
        
        porties = invoer_validatie(
            f"hoeveel porties",
            int,
            bereik = (1, 100),
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
            
            print(f"selecteren wat te bewerken")
            
            kies_optie = invoer_kiezen(
                f"MENU {f"{self}".upper()} BEWERK",
                [
                    "bewerk gerechtnaam",
                    "bewerk producten",
                    "bewerk porties",
                    "bewerk versies",
                    "bewerk categorie",
                    "bewerk recept",
                    ],
                kies_een = False,
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                break
            
            elif kies_optie == "bewerk gerechtnaam":
                
                print(f"\ninvullen nieuwe naam voor {self}")
                gerecht_naam = invoer_validatie(
                    "gerechtnaam",
                    str,
                    valideren = True,
                    kleine_letters = True,
                    uitsluiten_leeg = True,
                    )
                
                self.gerecht_naam = gerecht_naam
            
            elif kies_optie == "bewerk producten":
                
                while True:
                    
                    kies_optie_bewerken = invoer_kiezen(
                        f"MENU {f"{self}".upper()} BEWERK PRODUCTEN",
                        [
                            "toevoegen producten",
                            "verwijderen producten",
                            "aanpassen hoeveelheid producten",
                            ],
                        kies_een = False,
                        stoppen = True,
                        terug_naar = f"KLAAR MET BEWERKEN",
                        )
                    
                    if kies_optie_bewerken is STOP:
                        break
                    
                    elif kies_optie_bewerken == "toevoegen producten":
                        
                        producten = Producten.openen()
                        
                        product_uuid, eenheid = producten.kiezen_product_eenheid(
                            terug_naar = f"MENU {f"{self}".upper()} BEWERK PRODUCTEN",
                            )
                        
                        if product_uuid is STOP:
                            continue
                        
                        if eenheid is STOP:
                            continue
                        
                        aantal = invoer_validatie(
                            f"hoeveel {eenheid.meervoud}",
                            float,
                            )
                        
                        hoeveelheid = Hoeveelheid(aantal, eenheid)
                        
                        if product_uuid in self.producten_standaard.keys():
                            for ihoeveelheid_aanwezig, hoeveelheid_aanwezig in enumerate(self.producten_standaard[product_uuid]):
                                if hoeveelheid == hoeveelheid_aanwezig:
                                    self.producten_standaard[product_uuid][ihoeveelheid_aanwezig] = hoeveelheid + hoeveelheid_aanwezig
                                    break
                            else:
                                self.producten_standaard[product_uuid].append(hoeveelheid)
                        else:
                            self.producten_standaard[product_uuid] = [hoeveelheid]
                    
                    elif kies_optie_bewerken == "verwijderen producten":
                        
                        producten = Producten.openen()
                        
                        kies_optie_verwijderen = invoer_kiezen(
                            "een product en hoeveelheid om te verwijderen",
                            {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                            stoppen = True,
                            terug_naar = f"MENU {f"{self}".upper()} BEWERK",
                            )
                        
                        if kies_optie_verwijderen is STOP:
                            continue
                        
                        product_uuid, ihoeveelheid = kies_optie_verwijderen
                        
                        print(f"\n>>> {self.producten_standaard[product_uuid][ihoeveelheid]} van {producten[product_uuid]} verwijderd")
                        
                        del self.producten_standaard[product_uuid][ihoeveelheid]
                    
                    elif kies_optie_bewerken == "aanpassen hoeveelheid producten":
                        
                        producten = Producten.openen()
                        
                        kies_optie_aanpassen = invoer_kiezen(
                            "een product en hoeveelheid om aan te passen",
                            {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                            stoppen = True,
                            terug_naar = f"MENU {f"{self}".upper()} BEWERK",
                            )
                        
                        if kies_optie_aanpassen is STOP:
                            continue
                        
                        product_uuid, ihoeveelheid = kies_optie_aanpassen
                
                        eenheid = producten.kiezen_eenheid(
                            terug_naar = f"MENU {f"{self}".upper()} BEWERK",
                            product_uuid = product_uuid,
                            )
                        
                        if eenheid is STOP:
                            continue
                        
                        aantal = invoer_validatie(
                            f"hoeveel {eenheid.meervoud}",
                            float,
                            )
                        
                        hoeveelheid = Hoeveelheid(aantal, eenheid)
                        
                        print(f"\n>>> hoeveelheid {self.producten_standaard[product_uuid][ihoeveelheid]} aangepast naar {hoeveelheid}")
                        
                        self.producten_standaard[product_uuid][ihoeveelheid] = hoeveelheid
                        
                        print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                
                        for product_uuid, hoeveelheden in self.producten().items():
                            for hoeveelheid in hoeveelheden:
                                print(f"     {f"{hoeveelheid}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>8} {producten[product_uuid]}")
                        
                        aantal_porties = self.porties
                        print(f"\n     {"TOTAAL":<18} {f"{self.voedingswaarde().calorieën*aantal_porties}":>9} {f"{self.voedingswaarde().eiwitten*aantal_porties}":>8} (voor {aantal_porties} porties)")
                        print(f"     {"PER PORTIE":<18} {f"{self.voedingswaarde().calorieën}":>9} {f"{self.voedingswaarde().eiwitten}":>8}")
            
            elif kies_optie == "bewerk categorie":
                
                categorieën_gerecht = CategorieënGerecht.openen()
                categorie_uuid = categorieën_gerecht.kiezen(
                    terug_naar = f"MENU {f"{self}".upper()} BEWERK",
                    )
                
                if categorie_uuid is STOP:
                    continue
                
                self.categorie_uuid = categorie_uuid
            
            elif kies_optie == "bewerk porties":
                
                print(f"\ninvullen aantal porties")
                porties = invoer_validatie(
                    f"hoeveel porties",
                    int,
                    )
                self.porties = porties
            
            elif kies_optie == "bewerk versies":
                
                optie_dict = {
                    f"{versie["versie_naam"]}": versie_uuid for versie_uuid, versie in self.versies.items()
                } | {
                    "nieuwe versie": "nieuwe versie"
                    }
                
                kies_optie = invoer_kiezen(
                    "versie",
                    optie_dict,
                    stoppen = True,
                    terug_naar = f"MENU {f"{self}".upper()} BEWERK",
                    )
                
                if kies_optie is STOP:
                    continue
                
                elif kies_optie == "nieuwe versie":
                    self.nieuwe_versie()
                
                else:
                    
                    versie_uuid = kies_optie
                    producten = Producten.openen()
                    
                    while True:
                        
                        kies_optie_bewerken = invoer_kiezen(
                            f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                            [
                                "toevoegen toevoeging product",
                                "verwijderen toevoeging product",
                                "aanpassen toevoeging product",
                                "toevoegen verwijdering product",
                                "verwijderen verwijdering product",
                                "toevoegen aanpassing hoeveelheid",
                                "verwijderen aanpassing hoeveelheid",
                                "aanpassen aanpassing hoeveelheid",
                                "toevoegen aanpassing aantal porties",
                                "verwijderen aanpassing aantal porties",
                                "aanpassen aanpassing aantal porties",
                                "verwijderen versie",
                                ],
                            kies_een = False,
                            stoppen = True,
                            terug_naar = f"KLAAR MET BEWERKEN",
                            )
                        
                        if kies_optie_bewerken is STOP:
                            break
                        
                        elif kies_optie_bewerken == "toevoegen toevoeging product":
                            
                            product_uuid, eenheid = producten.kiezen_product_eenheid(
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if product_uuid is STOP or eenheid is STOP:
                                continue
                            
                            if product_uuid in self.producten_standaard.keys() and eenheid in [hoeveelheid.eenheid for hoeveelheid in self.producten_standaard[product_uuid]]:
                                print(f">>> eenheid \"{eenheid.meervoud}\" voor {producten[product_uuid]} reeds aanwezig, probeer optie \"aanpassen toevoeging product\"")
                                continue
                            
                            if not "toegevoegd" in self.versies[versie_uuid]:
                                self.versies[versie_uuid]["toegevoegd"] = {}
                            else:
                                if product_uuid in self.versies[versie_uuid]["toegevoegd"].keys() and eenheid in [hoeveelheid.eenheid for hoeveelheid in self.versies[versie_uuid]["toegevoegd"][product_uuid]]:
                                    print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in toevoegingen, probeer toevoeging aan te passen")
                                    continue
                            
                            aantal = invoer_validatie(
                                f"hoeveel {eenheid.meervoud}",
                                float,
                                )
                            
                            hoeveelheid = Hoeveelheid(aantal, eenheid)
                            
                            if product_uuid in self.versies[versie_uuid]["toegevoegd"].keys():
                                self.versies[versie_uuid]["toegevoegd"][product_uuid].append(hoeveelheid)
                            else:
                                self.versies[versie_uuid]["toegevoegd"][product_uuid] = [hoeveelheid]
                            
                            if not "toegevoegd" in self.versies[versie_uuid]:
                                self.versies[versie_uuid]["toegevoegd"] = {}
                            
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} toegevoegd aan toevoegingen")
                        
                        elif kies_optie_bewerken == "verwijderen toevoeging product":
                            
                            if len(self.versies[versie_uuid].get("toegevoegd", {})) == 0:
                                print(f">>> geen toevoegingen om te verwijderen")
                                continue
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om te verwijderen uit toevoegingen",
                                {f"{producten[product_uuid]} ({hoeveelheid})": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.versies[versie_uuid]["toegevoegd"].items() for hoeveelheid in hoeveelheden},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, hoeveelheid = kies_optie
                            
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} verwijderd uit toevoegingen")
                            
                            self.versies[versie_uuid]["toegevoegd"][product_uuid].remove(hoeveelheid)
                            
                            if not bool(self.versies[versie_uuid]["toegevoegd"][product_uuid]):
                                del self.versies[versie_uuid]["toegevoegd"][product_uuid]
                            
                            if not bool(self.versies[versie_uuid]["toegevoegd"]):
                                del self.versies[versie_uuid]["toegevoegd"]
                        
                        elif kies_optie_bewerken == "aanpassen toevoeging product":
                            
                            if len(self.versies[versie_uuid].get("toegevoegd", {})) == 0:
                                print(f">>> geen toevoegingen om de hoeveelheid van aan te passen")
                                continue
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om aan te passen uit toevoegingen",
                                {f"{producten[product_uuid]} ({hoeveelheid})": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.versies[versie_uuid]["toegevoegd"].items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, ihoeveelheid = kies_optie
                            
                            hoeveelheid = self.versies[versie_uuid]["toegevoegd"][product_uuid][ihoeveelheid]
                            
                            aantal = invoer_validatie(
                                f"hoeveel {hoeveelheid.eenheid.meervoud}",
                                float,
                                )
                            
                            hoeveelheid_nieuw = Hoeveelheid(aantal, hoeveelheid.eenheid)
                            
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} aangepast naar {hoeveelheid_nieuw} in toevoegingen")
                            
                            self.versies[versie_uuid]["toegevoegd"][product_uuid][ihoeveelheid] = hoeveelheid_nieuw
                        
                        elif kies_optie_bewerken == "toevoegen verwijdering product":
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om te toe te voegen aan verwijderingen",
                                {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for  hoeveelheid in hoeveelheden},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, hoeveelheid = kies_optie
                            
                            
                            if not "verwijderd" in self.versies[versie_uuid]:
                                self.versies[versie_uuid]["verwijderd"] = {}
                            
                            if product_uuid in self.versies[versie_uuid]["verwijderd"].keys():
                                if hoeveelheid not in self.versies[versie_uuid]["verwijderd"][product_uuid]:
                                    self.versies[versie_uuid]["verwijderd"][product_uuid].append(hoeveelheid)
                                else:
                                    print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in verwijderingen")
                                    continue
                            else:
                                self.versies[versie_uuid]["verwijderd"][product_uuid] = [hoeveelheid]
                                
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} toegevoegd aan verwijderingen")
                        
                        elif kies_optie_bewerken == "verwijderen verwijdering product":
                            
                            if len(self.versies[versie_uuid].get("verwijderd", {})) == 0:
                                print(f">>> geen verwijderingen om te verwijderen")
                                continue
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om te verwijderen uit verwijderingen",
                                {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.versies[versie_uuid]["verwijderd"].items() for hoeveelheid in hoeveelheden},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, hoeveelheid = kies_optie
                            
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} verwijderd uit verwijderingen")
                            
                            self.versies[versie_uuid]["verwijderd"][product_uuid].remove(hoeveelheid)
                            
                            if not bool(self.versies[versie_uuid]["verwijderd"][product_uuid]):
                                del self.versies[versie_uuid]["verwijderd"][product_uuid]
                            
                            if not bool(self.versies[versie_uuid]["verwijderd"]):
                                del self.versies[versie_uuid]["verwijderd"]
                        
                        elif kies_optie_bewerken == "toevoegen aanpassing hoeveelheid":
                            
                            kies_optie = invoer_kiezen(
                                "een product en hoeveelheid om toe te voegen aan aanpassen hoeveelheid",
                                {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for hoeveelheid in hoeveelheden},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, hoeveelheid = kies_optie
                            
                            if not "hoeveelheid" in self.versies[versie_uuid].keys():
                                self.versies[versie_uuid]["hoeveelheid"] = {}
                            
                            if product_uuid in self.versies[versie_uuid]["hoeveelheid"] and hoeveelheid in self.versies[versie_uuid]["hoeveelheid"][product_uuid]:
                                print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in aanpassingen")
                                continue
                            
                            aantal = invoer_validatie(
                                f"hoeveel {hoeveelheid.eenheid.meervoud}",
                                float,
                                )
                            
                            hoeveelheid_nieuw = Hoeveelheid(aantal, hoeveelheid.eenheid)
                            
                            if product_uuid in self.versies[versie_uuid]["hoeveelheid"].keys():
                                self.versies[versie_uuid]["hoeveelheid"][product_uuid].append(hoeveelheid_nieuw)
                            else:
                                self.versies[versie_uuid]["hoeveelheid"][product_uuid] = [hoeveelheid_nieuw]
                            
                            print(f"\n>>> {hoeveelheid} --> {hoeveelheid_nieuw} van {producten[product_uuid]} toegevoegd aan aanpassingen")
                        
                        elif kies_optie_bewerken == "verwijderen aanpassing hoeveelheid":
                            
                            if len(self.versies[versie_uuid].get("hoeveelheid", {})) == 0:
                                print(f">>> geen aanpassing om te verwijderen")
                                continue
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om te verwijderen uit aanpassingen",
                                {f"{producten[product_uuid]} ({hoeveelheid})": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.versies[versie_uuid]["hoeveelheid"].items() for hoeveelheid in hoeveelheden},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, hoeveelheid_nieuw = kies_optie
                            
                            hoeveelheid = next(hoeveelheid for hoeveelheid in self.producten_standaard[product_uuid] if hoeveelheid == hoeveelheid_nieuw)
                            
                            print(f"\n>>> {hoeveelheid} --> {hoeveelheid_nieuw} van {producten[product_uuid]} verwijderd uit aanpassingen")
                            
                            self.versies[versie_uuid]["hoeveelheid"][product_uuid].remove(hoeveelheid)
                            
                            if not bool(self.versies[versie_uuid]["hoeveelheid"][product_uuid]):
                                del self.versies[versie_uuid]["hoeveelheid"][product_uuid]
                            
                            if not bool(self.versies[versie_uuid]["hoeveelheid"]):
                                del self.versies[versie_uuid]["hoeveelheid"]
                        
                        elif kies_optie_bewerken == "aanpassen aanpassing hoeveelheid":
                            
                            if len(self.versies[versie_uuid].get("hoeveelheid", {})) == 0:
                                print(f">>> geen aanpassing om de hoeveelheid van aan te passen")
                                continue
                            
                            kies_optie = invoer_kiezen(
                                "product en hoeveelheid om te verwijderen uit aanpassingen",
                                {f"{producten[product_uuid]} ({hoeveelheid})": (product_uuid, ihoeveelheid) for product_uuid, hoeveelheden in self.versies[versie_uuid]["hoeveelheid"].items() for ihoeveelheid, hoeveelheid in enumerate(hoeveelheden)},
                                stoppen = True,
                                terug_naar = f"MENU VERSIE {f"{self.versies[versie_uuid]["versie_naam"]}".upper()} BEWERK",
                                )
                            
                            if kies_optie is STOP:
                                continue
                            
                            product_uuid, ihoeveelheid = kies_optie
                            
                            hoeveelheid = self.versies[versie_uuid]["hoeveelheid"][product_uuid][ihoeveelheid]
                            
                            aantal = invoer_validatie(
                                f"hoeveel {hoeveelheid.eenheid.meervoud}",
                                float,
                                )
                            
                            hoeveelheid_nieuw = Hoeveelheid(aantal, hoeveelheid.eenheid)
                            
                            print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} aangepast naar {hoeveelheid_nieuw} in toevoegingen")
                            
                            self.versies[versie_uuid]["hoeveelheid"][product_uuid][ihoeveelheid] = hoeveelheid_nieuw
                        
                        elif kies_optie_bewerken == "toevoegen aanpassing aantal porties":
                            
                            if "porties" in self.versies[versie_uuid]:
                                print(f">>> toevoeging aanpassing aantal porties ({self.versies[versie_uuid]["porties"]} reeds aanwezig)")
                                continue
                            
                            porties = invoer_validatie(
                                f"hoeveel porties",
                                int,
                                )
                            
                            self.versies[versie_uuid]["porties"] = porties
                        
                        elif kies_optie_bewerken == "verwijderen aanpassing aantal porties":
                            
                            if "porties" not in self.versies[versie_uuid]:
                                print(f">>> geen aanpassing aantal porties aanwezig)")
                                continue
                            
                            del self.versies[versie_uuid]["porties"]
                        
                        elif kies_optie_bewerken == "aanpassen aanpassing aantal porties":
                            
                            if "porties" not in self.versies[versie_uuid]:
                                print(f">>> geen aanpassing aantal porties aanwezig)")
                                continue
                            
                            porties = invoer_validatie(
                                f"hoeveel porties",
                                int,
                                )
                            
                            self.versies[versie_uuid]["porties"] = porties
                        
                        elif kies_optie_bewerken == "verwijderen versie":
                            
                            print(f">>> versie \"{self.versies[versie_uuid]["versie_naam"]} verwijderd\"")
                            
                            del self.versies[versie_uuid]
                            break
            
            elif kies_optie == "bewerk recept":
                
                if not bool(self.recept):
                    print(f"\n>>> er is geen recept gedefinieerd voor {self}")
                    
                    if self.nieuw_recept() is STOP:
                        continue
                    
                    continue
                
                while True:
                    
                    if len(self.recept["benodigdheden"]) > 0:
                        print("\n     benodigdheden")
                        aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
                        [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                
                    print("\n     stappen")
                    aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
                    [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
                
                    kies_optie = invoer_kiezen(
                        f"MENU {f"{self}".upper()} BEWERK RECEPT",
                        [
                            "bewerk benodigdheden",
                            "bewerk stappen",
                            ],
                        kies_een = False,
                        stoppen = True,
                        terug_naar = "BEWERK RECEPT KLAAR",
                        )
                    
                    if kies_optie is STOP:
                        break
                    
                    elif kies_optie == "bewerk benodigdheden":
                        
                        while True:
                            
                            if len(self.recept["benodigdheden"]) > 0:
                                print("\n     benodigdheden")
                                aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
                                [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                            
                            kies_optie_benodigdheden = invoer_kiezen(
                                f"MENU {f"{self}".upper()} BEWERK RECEPT BENODIGDHEDEN",
                                [
                                    "toevoegen benodigdheid",
                                    "verwijderen benodigdheid",
                                    "aanpassen benodigdheid",
                                    ],
                                kies_een = False,
                                stoppen = True,
                                terug_naar = "BEWERK RECEPT BENODIGHEDEN KLAAR",
                                )
                            
                            if kies_optie_benodigdheden is STOP:
                                break
                            
                            elif kies_optie_benodigdheden == "toevoegen benodigdheid":
                                
                                benodigdheid = invoer_validatie(
                                    "benodigdheid",
                                    str,
                                    kleine_letters = True,
                                    uitsluiten_leeg = True,
                                    )
                                
                                if benodigdheid == "klaar":
                                    continue
                                
                                self.recept["benodigdheden"].append(benodigdheid)
                                
                                print(f"\n>>> benodigdheid \"{benodigdheid}\" toegevoegd van benodigdheden")
                            
                            elif kies_optie_benodigdheden == "verwijderen benodigdheid":
                                
                                ibenodigdheid = invoer_kiezen(
                                    "benodigdheid om te verwijderen",
                                    {f"{benodigdheid}": ibenodigdheid for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"])},
                                    stoppen = True,
                                    terug_naar = "VERWIJDEREN BENODIGHEDEN KLAAR",
                                    )
                                
                                if ibenodigdheid is STOP:
                                    continue
                                
                                print(f"\n>>> benodigdheid \"{self.recept["benodigdheden"][ibenodigdheid]}\" verwijderd van benodigdheden")
                                
                                del self.recept["benodigdheden"][ibenodigdheid]
                            
                            elif kies_optie_benodigdheden == "aanpassen benodigdheid":
                                
                                ibenodigdheid = invoer_kiezen(
                                    "benodigdheid om aan te passen",
                                    {f"{benodigdheid}": ibenodigdheid for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"])},
                                    stoppen = True,
                                    terug_naar = "AANPASSEN BENODIGHEDEN KLAAR",
                                    )
                                
                                if ibenodigdheid is STOP:
                                    continue
                                
                                benodigdheid = invoer_validatie(
                                    "benodigdheid",
                                    str,
                                    kleine_letters = True,
                                    uitsluiten_leeg = True,
                                    )
                                
                                if benodigdheid == "klaar":
                                    continue
                                
                                print(f"\n>>> benodigdheid \"{self.recept["benodigdheden"][ibenodigdheid]}\" aangepast naar \"{benodigdheid}\"")
                                
                                self.recept["benodigdheden"][ibenodigdheid] = benodigdheid
                    
                    elif kies_optie == "bewerk stappen":
                        
                        while True:
                            
                            print("\n     stappen")
                            aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
                            [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
                            
                            kies_optie_stappen = invoer_kiezen(
                                f"MENU {f"{self}".upper()} BEWERK RECEPT STAPPEN",
                                [
                                    "toevoegen stap",
                                    "verwijderen stap",
                                    "aanpassen stap",
                                    ],
                                kies_een = False,
                                stoppen = True,
                                terug_naar = "BEWERK RECEPT STAPPEN KLAAR",
                                )
                            
                            if kies_optie_stappen is STOP:
                                break
                            
                            elif kies_optie_stappen == "toevoegen stap":
                                
                                stap = invoer_validatie(
                                    "stap",
                                    str,
                                    kleine_letters = True,
                                    uitsluiten_leeg = True,
                                    )
                                
                                if stap == "klaar":
                                    continue
                                
                                istap = invoer_kiezen(
                                    "plek waar de stap toegevoegd moet worden",
                                    {
                                        f"voor stap \"{stap}\"": istap for istap, stap in enumerate(self.recept["stappen"])
                                    } | {
                                        "laatste stap": len(self.recept["stappen"])
                                        },
                                    stoppen = True,
                                    terug_naar = "TOEVOEGEN STAPPEN KLAAR",
                                    )
                                
                                if istap is STOP:
                                    continue
                                
                                print(f"\n>>> stap \"{stap}\" toegevoegd van stappen")
                                
                                self.recept["stappen"].insert(istap, stap)
                            
                            elif kies_optie_stappen == "verwijderen stap":
                                
                                istap = invoer_kiezen(
                                    "stap om te verwijderen",
                                    {f"{stap}": istap for istap, stap in enumerate(self.recept["stappen"])},
                                    stoppen = True,
                                    terug_naar = "VERWIJDEREN STAPPEN KLAAR",
                                    )
                                
                                if istap is STOP:
                                    continue
                                
                                print(f"\n>>> stap \"{self.recept["stappen"][istap]}\" verwijderd van stappen")
                                
                                del self.recept["stappen"][istap]
                            
                            elif kies_optie_stappen == "aanpassen stap":
                                
                                istap = invoer_kiezen(
                                    "stap om aan te passen",
                                    {f"{stap}": istap for istap, stap in enumerate(self.recept["stappen"])},
                                    stoppen = True,
                                    terug_naar = "AANPASSEN STAPPEN KLAAR",
                                    )
                                
                                if istap is STOP:
                                    continue
                                
                                stap = invoer_validatie(
                                    "stap",
                                    str,
                                    kleine_letters = True,
                                    uitsluiten_leeg = True,
                                    )
                                
                                if stap == "klaar":
                                    continue
                                
                                print(f"\n>>> stap \"{self.recept["stappen"][istap]}\" aangepast naar \"{stap}\"")
                                
                                self.recept["stappen"][istap] = stap
        
        return self
    
    def weergeef(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te weergeven")
        
        while True:
            
            kies_optie = invoer_kiezen(
                f"MENU {f"{self}".upper()}/WEERGEEF",
                [
                    "weergeef producten",
                    "weergeef voedingswaarde",
                    "weergeef versies",
                    "weergeef recept",
                    ],
                kies_een = False,
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                break
            
            elif kies_optie == "weergeef producten":
                
                versie_uuid = self.kiezen_versie(
                    terug_naar,
                    )
                
                if versie_uuid is STOP:
                    return STOP
                
                producten = Producten.openen()
                
                versie_naam = "standaard" if versie_uuid == "standaard" else self.versies[versie_uuid]["versie_naam"]
                print(f"\n     {self} (versie \"{versie_naam}\")")
                print(f"\n     {"HOEVEELHEID":<18} CALORIEËN EIWITTEN PRODUCT")
                
                for product_uuid, hoeveelheden in self.producten(versie_uuid).items():
                    for hoeveelheid in hoeveelheden:
                        print(f"     {f"{hoeveelheid}":<18} {f"{producten[product_uuid].voedingswaarde.calorieën * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>9} {f"{producten[product_uuid].voedingswaarde.eiwitten * (hoeveelheid.waarde if hoeveelheid.eenheid in Hoeveelheid.BASIS_EENHEDEN else hoeveelheid.waarde * producten[product_uuid].eenheden[hoeveelheid.eenheid]) / 100}":>8} {producten[product_uuid]}")
                
                aantal_porties = self.porties if versie_uuid == "standaard" else self.versies[versie_uuid].get("porties", self.porties)
                print(f"\n     {"TOTAAL":<18} {f"{self.voedingswaarde(versie_uuid).calorieën*aantal_porties}":>9} {f"{self.voedingswaarde(versie_uuid).eiwitten*aantal_porties}":>8} (voor {aantal_porties} porties)")
                print(f"     {"PER PORTIE":<18} {f"{self.voedingswaarde(versie_uuid).calorieën}":>9} {f"{self.voedingswaarde(versie_uuid).eiwitten}":>8}")
            
            elif kies_optie == "weergeef voedingswaarde":
                
                versie_uuid = self.kiezen_versie(
                    terug_naar,
                    )
                
                if versie_uuid is STOP:
                    return STOP
                
                versie_naam = "standaard" if versie_uuid == "standaard" else self.versies[versie_uuid]["versie_naam"]
                aantal_porties = self.porties if versie_uuid == "standaard" else self.versies[versie_uuid].get("porties", self.porties)
                
                print(f"\n     voedingswaarde voor versie \"{versie_naam}\" per portie ({aantal_porties} porties)\n")
                print(self.voedingswaarde(versie_uuid))
            
            elif kies_optie == "weergeef versies":
                
                producten = Producten.openen()
                
                if len(self.versies) == 0:
                    print(">>> er zijn geen versies gedefinieerd")
                
                for versie in self.versies.values():
                    
                    print(f"\n     versie \"{versie["versie_naam"]}\"".upper())
                    
                    if "porties" in versie.keys():
                        print("       porties")
                        print(f"         {self.porties} porties --> {versie["porties"]} porties")
                    
                    if "verwijderd" in versie.keys():
                        print("       verwijderd")
                        for product_uuid, hoeveelheden in versie["verwijderd"].items():
                            for hoeveelheid in hoeveelheden:
                                print(f"         {f"{hoeveelheid}":<18} {producten[product_uuid]}")
                    
                    if "toegevoegd" in versie.keys():
                        print("       toegevoegd")
                        for product_uuid, hoeveelheden in versie["toegevoegd"].items():
                            for hoeveelheid in hoeveelheden:
                                print(f"         {f"{hoeveelheid}":<18} {producten[product_uuid]}")
                    
                    if "hoeveelheid" in versie.keys():
                        print("       hoeveelheid aangepast")
                        for product_uuid, hoeveelheden in versie["hoeveelheid"].items():
                            for hoeveelheid in hoeveelheden:
                                hoeveelheid_oud = next(hoeveelheid_oud for hoeveelheid_oud in self.producten_standaard[product_uuid] if hoeveelheid_oud == hoeveelheid)
                                print(f"         {f"{hoeveelheid_oud}":<18} --> {f"{hoeveelheid}":<18} {producten[product_uuid]}")
            
            elif kies_optie == "weergeef recept":
                
                if not bool(self.recept):
                    print(f"\n>>> er is geen recept gedefinieerd voor {self}")
                    continue
                
                if len(self.recept["benodigdheden"]) > 0:
                    print("\n     benodigdheden")
                    aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
                    [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                
                print("\n     stappen")
                aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
                [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
            
    def kiezen_versie(
        self,
        terug_naar: str,
        ) -> str | Stop:
        
        while True:
            
            if len(self.versies) == 0:
                
                versie_uuid = "standaard"
            
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
                
                else:
                    versie_uuid = kies_optie
            
            return versie_uuid
    
    def nieuwe_versie(
        self,
        ) -> str | Stop:
        
        versie = {}
        
        while True:
            
            if len(versie) > 0:
                
                print("\ntot nu toe aangebrachte wijzigingen voor deze versie\n")
                
                if "porties" in versie.keys():
                    print("       porties")
                    print(f"         {self.porties} porties --> {versie["porties"]} porties")
                
                if "verwijderd" in versie.keys():
                    print("       verwijderd")
                    for product_uuid, hoeveelheden in versie["verwijderd"].items():
                        for hoeveelheid in hoeveelheden:
                            print(f"         {f"{hoeveelheid}":<18} {producten[product_uuid]}")
                
                if "toegevoegd" in versie.keys():
                    print("       toegevoegd")
                    for product_uuid, hoeveelheden in versie["toegevoegd"].items():
                        for hoeveelheid in hoeveelheden:
                            print(f"         {f"{hoeveelheid}":<18} {producten[product_uuid]}")
                
                if "hoeveelheid" in versie.keys():
                    print("       hoeveelheid aangepast")
                    for product_uuid, hoeveelheden in versie["hoeveelheid"].items():
                        for hoeveelheid in hoeveelheden:
                            hoeveelheid_oud = next(hoeveelheid_oud for hoeveelheid_oud in self.producten_standaard[product_uuid] if hoeveelheid_oud == hoeveelheid)
                            print(f"         {f"{hoeveelheid_oud}":<18} --> {f"{hoeveelheid}":<18} {producten[product_uuid]}")
            
            kies_optie = invoer_kiezen(
                f"MENU NIEUWE VERSIE {f"{self}".upper()}",
                [
                    "toevoegen product",
                    "verwijderen product",
                    "aanpassen hoeveelheid product",
                    "aanpassen aantal porties",
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
                    terug_naar = f"MENU NIEUWE VERSIE {f"{self}".upper()}",
                    )
                
                if product_uuid is STOP or eenheid is STOP:
                    continue
                
                if product_uuid in self.producten_standaard.keys() and eenheid in [hoeveelheid.eenheid for hoeveelheid in self.producten_standaard[product_uuid]]:
                    print(f">>> eenheid \"{eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig, probeer een aanpassing")
                    continue
                
                if not "toegevoegd" in versie:
                    versie["toegevoegd"] = {}
                else:
                    if product_uuid in versie["toegevoegd"].keys() and eenheid in [hoeveelheid.eenheid for hoeveelheid in versie["toegevoegd"][product_uuid]]:
                        print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in toevoegingen, probeer toevoeging aan te passen")
                        continue
                
                aantal = invoer_validatie(
                    f"hoeveel {eenheid.meervoud}",
                    float,
                    )
                
                hoeveelheid = Hoeveelheid(aantal, eenheid)
                
                if product_uuid in versie["toegevoegd"].keys():
                    versie["toegevoegd"][product_uuid].append(hoeveelheid)
                else:
                    versie["toegevoegd"][product_uuid] = [hoeveelheid]
                
                print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} toegevoegd aan toevoegingen")
            
            elif kies_optie == "verwijderen product":
                
                kies_optie = invoer_kiezen(
                    "een product en hoeveelheid om te verwijderen",
                    {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for hoeveelheid in hoeveelheden},
                    stoppen = True,
                    terug_naar = f"MENU NIEUWE VERSIE {f"{self}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                product_uuid, hoeveelheid = kies_optie
                
                if not "verwijderd" in versie:
                    versie["verwijderd"] = {}
                
                if product_uuid in versie["verwijderd"].keys():
                    if hoeveelheid not in versie["verwijderd"][product_uuid]:
                        versie["verwijderd"][product_uuid].append(hoeveelheid)
                    else:
                        print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in verwijderingen")
                        continue
                else:
                    versie["verwijderd"][product_uuid] = [hoeveelheid]
                
                print(f"\n>>> {hoeveelheid} van {producten[product_uuid]} toegevoegd aan verwijderingen")
                
            elif kies_optie == "aanpassen hoeveelheid product":
                
                kies_optie = invoer_kiezen(
                    "een product en hoeveelheid om de hoeveelheid van aan te passen",
                    {f"{f"{hoeveelheid}":<18} {producten[product_uuid]}": (product_uuid, hoeveelheid) for product_uuid, hoeveelheden in self.producten_standaard.items() for hoeveelheid in hoeveelheden},
                    stoppen = True,
                    terug_naar = f"MENU NIEUWE VERSIE {f"{self}".upper()}",
                    )
                
                if kies_optie is STOP:
                    continue
                
                product_uuid, hoeveelheid = kies_optie
                
                if not "hoeveelheid" in versie:
                    versie["hoeveelheid"] = {}
                
                if product_uuid in versie["hoeveelheid"] and hoeveelheid in versie["hoeveelheid"][product_uuid]:
                    print(f"\n>>> eenheid \"{hoeveelheid.eenheid.meervoud}\" van {producten[product_uuid]} reeds aanwezig in aanpassingen")
                    continue
                
                aantal = invoer_validatie(
                    f"hoeveel {hoeveelheid.eenheid.meervoud}",
                    float,
                    )
                
                hoeveelheid_nieuw = Hoeveelheid(aantal, hoeveelheid.eenheid)
                
                if product_uuid in versie["hoeveelheid"].keys():
                    versie["hoeveelheid"][product_uuid].append(hoeveelheid_nieuw)
                else:
                    versie["hoeveelheid"][product_uuid] = [hoeveelheid_nieuw]
                
                print(f"\n>>> {hoeveelheid} --> {hoeveelheid_nieuw} van {producten[product_uuid]} toegevoegd aan aanpassingen")
            
            elif kies_optie == "aanpassen aantal porties":
                
                porties = invoer_validatie(
                    f"hoeveel porties",
                    int,
                    )
                
                versie["porties"] = porties
            
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
    
    def nieuw_recept(
        self,
        ) -> None | Stop:
        
        print(f"\n>>> aanmaken nieuwe recept voor {self}")
        
        benodigdheden = []
        stappen = []
        
        if invoer_kiezen(
            "toevoegen benodigdheden",
            {
                "ja": True,
                "nee": False,
                },
            kies_een = False,
            ):
            
            while True:
                
                if len(benodigdheden) > 0:
                    print("\nbenodigdheden")
                    aantal_tekens = len(f"{len(benodigdheden)}") + 1
                    [print(f"     {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(benodigdheden, 1)]
                    print("\nvoer \"klaar\" in om benodigdheden af te ronden")
                
                benodigdheid = invoer_validatie(
                    "benodigdheid",
                    str,
                    kleine_letters = True,
                    uitsluiten_leeg = True,
                    )
                
                if benodigdheid == "klaar":
                    break
                
                benodigdheden.append(benodigdheid)
        
        print("\ntoevoegen stappen van het recept")
        
        while True:
            
            if len(stappen) > 0:
                print("\ntoegevoegde stappen")
                aantal_tekens = len(f"{len(stappen)}") + 1
                [print(f"     {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(stappen, 1)]
                print("\nvoer \"klaar\" in om stappen af te ronden")
            
            stap = invoer_validatie(
                f"stap {len(stappen)+1}",
                str,
                kleine_letters = True,
                uitsluiten_leeg = True,
                )
            
            if stap == "klaar":
                break
            
            stappen.append(stap)
        
        if len(stappen) == 0:
            return STOP
        else:
            self.recept = {
                "benodigdheden": benodigdheden,
                "stappen": stappen,
                }
    
    def producten(
        self,
        versie_uuid: str = "standaard",
        ) -> Dict[str, Hoeveelheid]:
        
        producten = deepcopy(self.producten_standaard)
        
        if versie_uuid != "standaard":
            
            for product_uuid, hoeveelheden in self.versies[versie_uuid].get("toegevoegd", {}).items():
                for hoeveelheid in hoeveelheden:
                    if product_uuid not in producten.keys():
                        producten[product_uuid] = [hoeveelheid]
                    else:
                        producten[product_uuid].append(hoeveelheid)
            
            for product_uuid, hoeveelheden in self.versies[versie_uuid].get("verwijderd", {}).items():
                for hoeveelheid in hoeveelheden:
                    producten[product_uuid].remove(hoeveelheid)
            
            for product_uuid, hoeveelheden in self.versies[versie_uuid].get("hoeveelheid", {}).items():
                for hoeveelheid in hoeveelheden:
                    producten[product_uuid].remove(hoeveelheid)
                    producten[product_uuid].append(hoeveelheid)
        
        return producten
    
    def voedingswaarde(
        self,
        versie_uuid: str = "standaard",
        ) -> Voedingswaarde:
        
        gerecht_voedingswaarde = Voedingswaarde()
        producten = Producten.openen()
        
        for product_uuid, hoeveelheden in self.producten(versie_uuid).items():
            for hoeveelheid in hoeveelheden:
                product_voedingswaarde = producten[product_uuid].bereken_voedingswaarde(hoeveelheid)
                gerecht_voedingswaarde += product_voedingswaarde
        
        aantal_porties = self.porties if versie_uuid == "standaard" else self.versies[versie_uuid].get("porties", self.porties)
        gerecht_voedingswaarde /= aantal_porties
        
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
                
                while True:
                    
                    opdracht_weergeef = invoer_kiezen(
                        "MENU GEGEVENS/GERECHT/WEERGEEF",
                        [
                            "alle gerechten",
                            "alle gerechten onder een hoofdcategorie",
                            "alle gerechten onder een categorie",
                            ],
                        stoppen = True,
                        kies_een = False,
                        terug_naar = "MENU GEGEVENS/GERECHT",
                        )
                    if opdracht_weergeef is STOP:
                        break
                    
                    elif opdracht_weergeef == "alle gerechten":
                        
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
                    
                    elif opdracht_weergeef == "alle gerechten onder een hoofdcategorie":
                        
                        hoofdcategorieën = HoofdcategorieënGerecht.openen()
                        
                        hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/GERECHT/WEERGEEF",
                            )
                        
                        if hoofdcategorie_uuid is STOP:
                            continue
                        
                        print()
                        categorieën = CategorieënGerecht.openen()
                        for categorie_uuid, categorie in categorieën.items():
                            if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                                print(f"     {categorie}")
                                for gerecht in self.lijst:
                                        if gerecht.categorie_uuid == categorie_uuid:
                                            print(f"       {gerecht}")
                    
                    elif opdracht_weergeef == "alle gerechten onder een categorie":
                        
                        categorieën = CategorieënGerecht.openen()
                        
                        categorie_uuid = categorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/GERECHT/WEERGEEF",
                            )
                        
                        if categorie_uuid is STOP:
                            continue
                        
                        print()
                        
                        for gerecht in self.lijst:
                            if gerecht.categorie_uuid == categorie_uuid:
                                print(f"     {gerecht}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        gerecht = Gerecht.nieuw(terug_naar)
        
        if gerecht is STOP:
            return STOP
        
        gerecht_uuid = str(uuid4())
        
        if invoer_kiezen(
            "toevoegen versie",
            {
                "ja": True,
                "nee": False,
                },
            kies_een = False,
            ):
            
            gerecht.nieuwe_versie()
        
        if invoer_kiezen(
            "toevoegen recept",
            {
                "ja": True,
                "nee": False,
                },
            kies_een = False,
            ):
            
            gerecht.nieuw_recept()
        
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
                    
                    if len([categorie for categorie in categorieën_gerecht.lijst if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid]) == 0:
                        print(f"\n>>> geen categorieën aanwezig onder {hoofdcategorieën_gerecht[hoofdcategorie_uuid]}")
                        return STOP
                    
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {f"{categorie}": categorie_uuid for categorie_uuid, categorie in categorieën_gerecht.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if categorie_uuid is STOP:
                        return STOP
                    
                    if len([gerecht for gerecht in self.lijst if gerecht.categorie_uuid == categorie_uuid]) == 0:
                        print(f"\n>>> geen gerechten aanwezig onder {categorieën_gerecht[categorie_uuid]}")
                        return STOP
                    
                    gerecht_uuid = invoer_kiezen(
                        "ingrediënt",
                        {f"{gerecht}": gerecht_uuid for gerecht_uuid, gerecht in self.items() if gerecht.categorie_uuid == categorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if gerecht_uuid is STOP:
                        return STOP
                    
                    print(f"\n>>> {self[gerecht_uuid]} gekozen")
                    
                    return gerecht_uuid
                
                elif kies_optie == "zoek op gerechtnaam":
                        
                    print("\ngeef een gerechtnaam op")
                    
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
                    
                    print(f"\n>>> {self[gerecht_uuid]} gekozen")
                    
                    return gerecht_uuid
                
                if kies_optie == "nieuw gerecht":
                    return self.nieuw(
                        terug_naar,
                        )
    
    def kiezen_versie(
        self,
        terug_naar: str,
        gerecht_uuid: str,
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
        else:
            versie_uuid = kies_optie
        
        versie_naam = "standaard" if kies_optie == "standaard" else self[gerecht_uuid].versies[versie_uuid]["versie_naam"]
        print(f"\n>>> versie \"{versie_naam}\" gekozen")
        
        return versie_uuid
        
    def kiezen_gerecht_versie(
        self,
        terug_naar: str,
        ) -> Tuple[str | Stop, str | Stop]:
        
        gerecht_uuid = self.kiezen_gerecht(
            terug_naar,
            )
        
        if gerecht_uuid is STOP:
            return gerecht_uuid, ...
        
        versie_uuid = self.kiezen_versie(
            terug_naar,
            gerecht_uuid,
            )
        
        if versie_uuid is STOP:
            return gerecht_uuid, versie_uuid
        
        return gerecht_uuid, versie_uuid
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [gerecht_uuid for gerecht_uuid, gerecht in self.items() if zoekterm in gerecht.gerecht_naam]