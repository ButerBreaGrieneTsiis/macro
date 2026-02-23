from copy import deepcopy
from typing import Any, Dict, List, Tuple
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Hoofdcategorie, Categorie, HoofdcategorieënGerecht, CategorieënGerecht
from .macrotype import MacroType, MacroTypeDatabank, Hoeveelheid, Eenheid
from .product import Producten
from .voedingswaarde import Voedingswaarde


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