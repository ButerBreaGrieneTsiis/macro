from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP

from .macrotype import MacroType, MacroTypeDatabank


class Hoofdcategorie(MacroType):
    
    VELDEN = frozenset((
        "hoofdcategorie_naam",
        ))
    
    def __init__(
        self,
        hoofdcategorie_naam: str,
        ) -> "Hoofdcategorie":
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
    
    def __repr__(self) -> str:
        return f"hoofdcategorie \"{self.hoofdcategorie_naam}\""
    
    @classmethod
    def nieuw(cls) -> "Hoofdcategorie":
        
        print(f"\ninvullen gegevens nieuwe hoofdcategorie")
        hoofdcategorie_naam = invoer_validatie(
            "hoofdcategorienaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        return cls(
            hoofdcategorie_naam
            )
    
    def bewerk(self):
        
        print(f"\ninvullen nieuwe naam voor {self}")
        hoofdcategorie_naam = invoer_validatie(
            "hoofdcategorienaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        self.hoofdcategorie_naam = hoofdcategorie_naam
        
        return self

class Categorie(MacroType):
    
    VELDEN = frozenset((
        "categorie_naam",
        "hoofdcategorie_uuid",
        ))
    
    def __init__(
        self,
        categorie_naam: str,
        hoofdcategorie_uuid: str,
        ) -> "Categorie":
        
        self.categorie_naam = categorie_naam
        self.hoofdcategorie_uuid = hoofdcategorie_uuid
    
    def __repr__(self) -> str:
        return f"categorie \"{self.categorie_naam}\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        hoofdcategorieën,
        ) -> "Categorie":
        
        hoofdcategorie_uuid = hoofdcategorieën.kiezen(terug_naar)
        
        if hoofdcategorie_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuwe categorie onder hoofdcategorie \"{hoofdcategorieën[hoofdcategorie_uuid].hoofdcategorie_naam}\"")
        categorie_naam = invoer_validatie(
            "categorienaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        return cls(
            categorie_naam,
            hoofdcategorie_uuid,
            )
    
    def bewerk(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te bewerken")
        
        kies_optie = invoer_kiezen(
            "veld",
            [
                "bewerk categorienaam",
                "bewerk hoofdcategorie",
                ],
            stoppen = True,
            terug_naar = terug_naar,
            )
        
        if kies_optie is STOP:
            return
        
        if kies_optie == "bewerk categorienaam":
        
            print(f"\ninvullen nieuwe naam voor {self}")
            categorie_naam = invoer_validatie(
                "categorienaam",
                str,
                valideren = True,
                kleine_letters = True,
                uitsluiten_leeg = True,
                )
            
            self.categorie_naam = categorie_naam
        
        elif kies_optie == "bewerk hoofdcategorie":
            
            hoofdcategorieën = Hoofdcategorieën.openen()
            hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                terug_naar = terug_naar,
                uitsluiten_nieuw = True,
                )
            
            if hoofdcategorie_uuid is STOP:
                return
            
            self.hoofdcategorie_uuid = hoofdcategorie_uuid
        
        return self
        
    @property
    def hoofdcategorie(self):
        hoofdcategorieën = Hoofdcategorieën.openen()
        return hoofdcategorieën[self.hoofdcategorie_uuid]

class Hoofdcategorieën(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "hoofdcategorieën"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Hoofdcategorie.van_json, Hoofdcategorie.VELDEN),
        ]
    MENU: str = "MENU GEGEVENS/HOOFDCATEGORIE"
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                self.MENU,
                [
                    "nieuwe hoofdcategorie",
                    "selecteren en bewerken",
                    "toon hoofdcategorieën",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuwe hoofdcategorie":
                
                self.nieuw()
            
            elif opdracht == "selecteren en bewerken":
                
                hoofdcategorie_uuid = self.kiezen(
                    terug_naar = self.MENU,
                    uitsluiten_nieuw = True,
                    )
                if hoofdcategorie_uuid is STOP:
                    continue
                
                self[hoofdcategorie_uuid].bewerk()
            
            elif opdracht == "toon hoofdcategorieën":
                
                if len(self) == 0:
                    print("\n>>> geen hoofdcategorieën aanwezig")
                    continue
                print("")
                print(self)
            
        return self
    
    def nieuw(self):
        
        hoofdcategorie = Hoofdcategorie.nieuw()
        
        if hoofdcategorie is STOP:
            return STOP
        
        hoofdcategorie_uuid = str(uuid4())
        self[hoofdcategorie_uuid] = hoofdcategorie
        
        self.opslaan()
        
        return hoofdcategorie_uuid
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        stoppen: bool = True,
        uitsluiten_nieuw: bool = False,
        ) -> str | Hoofdcategorie:
        
        while True:
            
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen hoofdcategorieën aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen hoofdcategorieën aanwezig, maak een nieuwe hoofdcategorie",
                    [
                        "nieuwe hoofdcategorie",
                        ],
                    kies_een = False,
                    stoppen = stoppen,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                if kies_optie == "nieuwe hoofdcategorie":
                    return self.nieuw()
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "bestaande hoofdcategorie of maak een nieuwe",
                        [
                            "selecteren hoofdcategorie",
                            "zoek op hoofdcategorienaam",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "bestaande hoofdcategorie of maak een nieuwe",
                        [
                            "selecteren hoofdcategorie",
                            "zoek op hoofdcategorienaam",
                            "nieuwe hoofdcategorie",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "selecteren hoofdcategorie":
                    
                    hoofdcategorie_uuid = invoer_kiezen(
                        "hoofdcategorie",
                        {f"{hoofdcategorie}": hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items()},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                    
                    if hoofdcategorie_uuid is STOP: 
                        continue
                    
                    if kies_bevestiging: 
                        print(f"\n>>> {self[hoofdcategorie_uuid]} gekozen")
                    
                    return hoofdcategorie_uuid
                
                elif kies_optie == "zoek op hoofdcategorienaam":
                    
                    print("\ngeef een zoekterm op")
                    
                    zoekterm = invoer_validatie(
                        "hoofdcategorienaam",
                        str,
                        kleine_letters = True,
                        )
                    
                    hoofdcategorieën_mogelijk = self.zoeken(zoekterm)
                    if len(hoofdcategorieën_mogelijk) == 0:
                        print(f"\n>>> zoekterm \"{zoekterm}\" levert geen hoofdcategorieën op")
                        continue
                    
                    print(f"\n>>> {len(hoofdcategorieën_mogelijk)} hoofdcategorie{"ën" if len(hoofdcategorieën_mogelijk) > 1 else ""} gevonden")
                    hoofdcategorie_uuid = invoer_kiezen(
                        "hoofdcategorie",
                        {self[hoofdcategorie_uuid].hoofdcategorie_naam: hoofdcategorie_uuid for hoofdcategorie_uuid in hoofdcategorieën_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if hoofdcategorie_uuid is STOP:
                        continue
                    
                    if kies_bevestiging: 
                        print(f"\n>>> {self[hoofdcategorie_uuid]} gekozen")
                    
                    return hoofdcategorie_uuid
                
                if kies_optie == "nieuwe hoofdcategorie":
                    return self.nieuw()
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [hoofdcategorie_uuid for hoofdcategorie_uuid, hoofdcategorie in self.items() if zoekterm in hoofdcategorie.hoofdcategorie_naam]
        
class Categorieën(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "categorieën"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Categorie.van_json, Categorie.VELDEN),
        ]
    HOOFDCATEGORIEËN = Hoofdcategorieën
    MENU: str = "MENU GEGEVENS/HOOFDCATEGORIE"
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                self.MENU,
                [
                    "nieuwe categorie",
                    "selecteer en bewerk",
                    "toon categorieën",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuwe categorie":
                
                self.nieuw(
                    terug_naar = self.MENU,
                    )
            
            elif opdracht == "selecteer en bewerk":
                
                categorie_uuid = self.kiezen(
                    terug_naar = self.MENU,
                    uitsluiten_nieuw = True,
                    )
                if categorie_uuid is STOP:
                    continue
                
                self[categorie_uuid].bewerk(
                    terug_naar = self.MENU,
                    )
            
            elif opdracht == "toon categorieën":
                
                if len(self) == 0:
                    print("\n>>> geen categorieën aanwezig")
                    continue
                
                print()
                hoofdcategorieën = self.HOOFDCATEGORIEËN.openen()
                for hoofdcategorie_uuid, hoofdcategorie in hoofdcategorieën.items():
                    print(f"     {hoofdcategorie}")
                    for categorie in self.lijst:
                        if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                            print(f"       {categorie}")
            
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        hoofdcategorieën = self.HOOFDCATEGORIEËN.openen()
        
        categorie = Categorie.nieuw(
            terug_naar,
            hoofdcategorieën,
            )
        if categorie is STOP:
            return STOP
        
        categorie_uuid = str(uuid4())
        self[categorie_uuid] = categorie
        
        self.opslaan()
        
        return categorie_uuid
    
    def kiezen(
        self,
        terug_naar: str,
        kies_bevestiging: bool = True,
        stoppen: bool = True,
        uitsluiten_nieuw: bool = False,
        ) -> str | Categorie:
        
        while True:
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen categorieën aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen categorieën aanwezig, maak een nieuwe categorie",
                    [
                        "nieuwe categorie",
                        ],
                    kies_een = False,
                    stoppen = stoppen,
                    terug_naar = terug_naar,
                    )
                
                if kies_optie is STOP:
                    return STOP
                
                if kies_optie == "nieuwe categorie":
                    return self.nieuw(
                        terug_naar,
                        )
            
            else:
                
                if uitsluiten_nieuw:
                    kies_optie = invoer_kiezen(
                        "bestaande hoofdcategorie of maak een nieuwe",
                        [
                            "selecteren hoofdcategorie",
                            "zoek op categorienaam",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "bestaande categorie of maak een nieuwe",
                        [
                            "selecteren categorie",
                            "zoek op categorienaam",
                            "nieuwe categorie",
                            ],
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "selecteren categorie":
                    
                    hoofdcategorieën = self.HOOFDCATEGORIEËN.openen()
                    hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                        terug_naar,
                        uitsluiten_nieuw = True,
                        )
                    if hoofdcategorie_uuid is STOP:
                        return STOP
                    
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {f"{categorie}": categorie_uuid for categorie_uuid, categorie in self.items() if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid},
                        stoppen = stoppen,
                        terug_naar = terug_naar,
                        )
                    if categorie_uuid is STOP:
                        return STOP
                    
                    if kies_bevestiging:
                        print(f"\n>>> {self[categorie_uuid]} gekozen")
                    
                    return categorie_uuid
                
                elif kies_optie == "zoek op categorienaam":
                    
                    print("\ngeef een zoekterm op")
                    
                    zoekterm = invoer_validatie(
                        "categorienaam",
                        str,
                        kleine_letters = True,
                        )
                    
                    categorieën_mogelijk = self.zoeken(zoekterm)
                    if len(categorieën_mogelijk) == 0:
                        print(f"\n>>> zoekterm \"{zoekterm}\" levert geen categorieën op")
                        continue
                    
                    print(f"\n>>> {len(categorieën_mogelijk)} categorie{"ën" if len(categorieën_mogelijk) > 1 else ""} gevonden")
                    categorie_uuid = invoer_kiezen(
                        "categorie",
                        {self[categorie_uuid].categorie_naam: categorie_uuid for categorie_uuid in categorieën_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if categorie_uuid is STOP:
                        continue
                    
                    if kies_bevestiging: 
                        print(f"\n>>> {self[categorie_uuid]} gekozen")
                    
                
                elif kies_optie == "nieuwe categorie":
                    return self.nieuw(
                        terug_naar,
                        )
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [categorie_uuid for categorie_uuid, categorie in self.items() if zoekterm in categorie.categorie_naam]

class HoofdcategorieënGerecht(Hoofdcategorieën):
    
    BESTANDSNAAM: str = "hoofdcategorieën_gerecht"
    MENU: str = "MENU GEGEVENS/HOOFDCATEGORIE GERECHT"

class CategorieënGerecht(Categorieën):
    
    BESTANDSNAAM: str = "categorieën_gerecht"
    HOOFDCATEGORIEËN = HoofdcategorieënGerecht
    MENU: str = "MENU GEGEVENS/CATEGORIE GERECHT"