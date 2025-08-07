from typing import List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie, ObjectWijzer, STOP, Stop

from .categorie import Categorie, Categorieën, Hoofdcategorie, Hoofdcategorieën
from .macrotype import MacroType, MacroTypeDatabank


class Ingrediënt(MacroType):
    
    VELDEN = frozenset((
        "ingrediënt_naam",
        "categorie_uuid",
        ))
    
    def __init__(
        self,
        ingrediënt_naam: str,
        categorie_uuid: str,
        ) -> "Ingrediënt":
        
        self.ingrediënt_naam = ingrediënt_naam
        self.categorie_uuid = categorie_uuid
    
    def __repr__(self) -> "str":
        return f"ingrediënt \"{self.ingrediënt_naam}\""
    
    @classmethod
    def nieuw(
        cls,
        terug_naar: str,
        ):
        
        categorieën = Categorieën.openen()
        categorie_uuid = categorieën.kiezen(
            terug_naar,
            )
        if categorie_uuid is STOP:
            return STOP
        
        print(f"\ninvullen gegevens nieuw ingrediënt onder categorie \"{categorieën[categorie_uuid].categorie_naam}\"")
        ingrediënt_naam = invoer_validatie(
            "ingrediëntnaam",
            str,
            valideren = True,
            kleine_letters = True,
            uitsluiten_leeg = True,
            )
        
        return cls(
            ingrediënt_naam,
            categorie_uuid,
            )
    
    def bewerk(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            print(f"selecteren wat te bewerken")
            
            kies_optie = invoer_kiezen(
                "veld",
                [
                    "bewerk ingrediëntnaam",
                    "bewerk categorie",
                    ],
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                return self
            
            elif kies_optie == "bewerk ingrediëntnaam":
            
                print(f"\ninvullen nieuwe naam voor {self}")
                ingrediënt_naam = invoer_validatie(
                    "ingrediëntnaam",
                    str,
                    valideren = True,
                    kleine_letters = True,
                    uitsluiten_leeg = True,
                    )
                
                self.ingrediënt_naam = ingrediënt_naam
            
            elif kies_optie == "bewerk categorie":
                
                categorieën = Categorieën.openen()
                categorie_uuid = categorieën.kiezen(
                    terug_naar = terug_naar,
                    uitsluiten_nieuw = True,
                    )
                
                if categorie_uuid is STOP:
                    return
                
                self.categorie_uuid = categorie_uuid
    
    def weergeef(
        self,
        terug_naar: str,
        ):
        
        print(f"selecteren wat te weergeven")
        
        while True:
        
            kies_optie = invoer_kiezen(
                "veld",
                [
                    "weergeef hoofdcategorie",
                    "weergeef categorie",
                    ],
                stoppen = True,
                terug_naar = terug_naar,
                )
            
            if kies_optie is STOP:
                break
            
            elif kies_optie == "weergeef hoofdcategorie":
                
                print(f"\n     {self.hoofdcategorie}")
            
            elif kies_optie == "weergeef categorie":
                
                print(f"\n     {self.categorie}")
    
    @property
    def categorie(self) -> Categorie:
        categorieën = Categorieën.openen()
        return categorieën[self.categorie_uuid]
    
    @property
    def hoofdcategorie(self) -> Hoofdcategorie:
        return self.categorie.hoofdcategorie

class Ingrediënten(MacroTypeDatabank):
    
    BESTANDSNAAM: str = "ingrediënten"
    OBJECT_WIJZERS: List[ObjectWijzer] = [
        ObjectWijzer(Ingrediënt.van_json, Ingrediënt.VELDEN),
        ]
    
    def opdracht(
        self,
        terug_naar: str,
        ):
        
        while True:
            
            opdracht = invoer_kiezen(
                "MENU GEGEVENS/INGREDIËNT",
                [
                    "nieuw ingrediënt",
                    "selecteer en bewerk",
                    "selecteer en weergeef",
                    "weergeef ingrediënten",
                    ],
                stoppen = True,
                kies_een = False,
                terug_naar = terug_naar,
                )
            
            if opdracht is STOP:
                break
            
            elif opdracht == "nieuw ingrediënt":
                self.nieuw(
                    terug_naar = "MENU GEGEVENS/INGREDIËNT",
                    )
            
            elif opdracht == "selecteer en bewerk":
                
                ingrediënt_uuid = self.kiezen(
                    terug_naar = "MENU GEGEVENS/INGREDIËNT",
                    uitsluiten_nieuw = True,
                    )
                if ingrediënt_uuid is STOP:
                    continue
                
                self[ingrediënt_uuid].bewerk(
                    terug_naar = "MENU GEGEVENS/INGREDIËNT",
                    )
            
            elif opdracht == "selecteer en weergeef":
                
                ingrediënt_uuid = self.kiezen(
                    terug_naar = "MENU GEGEVENS/INGREDIËNT",
                    uitsluiten_nieuw = True,
                    )
                if ingrediënt_uuid is STOP:
                    continue
                
                self[ingrediënt_uuid].weergeef(
                    terug_naar = "MENU GEGEVENS/INGREDIËNT",
                    )
            
            elif opdracht == "weergeef ingrediënten":
                
                if len(self) == 0:
                    print("\n>>> geen ingrediënten aanwezig")
                    continue
                
                while True:
                    
                    opdracht_weergeef = invoer_kiezen(
                        "MENU GEGEVENS/INGREDIËNT/WEERGEEF",
                        [
                            "alle ingrediënten",
                            "alle ingrediënten onder een hoofdcategorie",
                            "alle ingrediënten onder een categorie",
                            ],
                        stoppen = True,
                        kies_een = False,
                        terug_naar = "MENU GEGEVENS/INGREDIËNT",
                        )
                    if opdracht_weergeef is STOP:
                        break
                    
                    elif opdracht_weergeef == "alle ingrediënten":
                        
                        print()
                        hoofdcategorieën = Hoofdcategorieën.openen()
                        categorieën = Categorieën.openen()
                        for hoofdcategorie_uuid, hoofdcategorie in hoofdcategorieën.items():
                            print(f"     {hoofdcategorie}")
                            for categorie_uuid, categorie in categorieën.items():
                                if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                                    print(f"       {categorie}")
                                    for ingrediënt in self.lijst:
                                        if ingrediënt.categorie_uuid == categorie_uuid:
                                            print(f"         {ingrediënt}")
                    
                    elif opdracht_weergeef == "alle ingrediënten onder een hoofdcategorie":
                        
                        hoofdcategorieën = Hoofdcategorieën.openen()
                        
                        hoofdcategorie_uuid = hoofdcategorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/INGREDIËNT/WEERGEEF",
                            )
                        
                        if hoofdcategorie_uuid is STOP:
                            continue
                        
                        print()
                        categorieën = Categorieën.openen()
                        for categorie_uuid, categorie in categorieën.items():
                            if categorie.hoofdcategorie_uuid == hoofdcategorie_uuid:
                                print(f"     {categorie}")
                                for ingrediënt in self.lijst:
                                    if ingrediënt.categorie_uuid == categorie_uuid:
                                        print(f"       {ingrediënt}")
                    
                    elif opdracht_weergeef == "alle ingrediënten onder een categorie":
                        
                        categorieën = Categorieën.openen()
                        
                        categorie_uuid = categorieën.kiezen(
                            terug_naar = "MENU GEGEVENS/INGREDIËNT/WEERGEEF",
                            )
                        
                        if categorie_uuid is STOP:
                            continue
                        
                        print()
                        
                        for ingrediënt in self.lijst:
                            if ingrediënt.categorie_uuid == categorie_uuid:
                                print(f"     {ingrediënt}")
        
        return self
    
    def nieuw(
        self,
        terug_naar: str,
        ):
        
        ingrediënt = Ingrediënt.nieuw(
            terug_naar,
            )
        if ingrediënt is STOP:
            return STOP
        
        ingrediënt_uuid = str(uuid4())
        self[ingrediënt_uuid] = ingrediënt
        
        self.opslaan()
        
        return ingrediënt_uuid
    
    def kiezen(
        self,
        terug_naar: str,
        uitsluiten_nieuw: bool = False,
        ) -> str | Stop:
        
        while True:
            
            if len(self) == 0:
                
                if uitsluiten_nieuw:
                    print("\n>>> geen ingrediënten aanwezig om te selecteren")
                    return STOP
                
                kies_optie = invoer_kiezen(
                    "geen ingrediënten aanwezig, maak een nieuw ingrediënt",
                    [
                        "nieuw ingrediënt",
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
                        "ingrediënt op naam of categorie, of maak een nieuwe",
                        [
                            "selecteren ingrediënt",
                            "zoek op ingrediëntnaam",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                else:
                    kies_optie = invoer_kiezen(
                        "ingrediënt op naam of categorie, of maak een nieuwe",
                        [
                            "selecteren ingrediënt",
                            "zoek op ingrediëntnaam",
                            "nieuw ingrediënt",
                            ],
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                
                if kies_optie is STOP:
                    return STOP
                
                elif kies_optie == "selecteren ingrediënt":
                    
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
                    
                    if len([ingrediënt for ingrediënt in self.lijst if ingrediënt.categorie_uuid == categorie_uuid]) == 0:
                        print(f"\n>>> geen ingrediënten aanwezig onder {categorieën[categorie_uuid]}")
                        return STOP
                    
                    ingrediënt_uuid = invoer_kiezen(
                        "ingrediënt",
                        {f"{ingrediënt}": ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if ingrediënt.categorie_uuid == categorie_uuid},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    if ingrediënt_uuid is STOP:
                        return STOP
                    
                    print(f"\n>>> {self[ingrediënt_uuid]} gekozen")
                    
                    return ingrediënt_uuid
                
                elif kies_optie == "zoek op ingrediëntnaam":
                        
                    print("\ngeef een ingrediëntnaam op")
                    
                    zoekterm = invoer_validatie(
                        "ingrediëntnaam",
                        str,
                        kleine_letters = True,
                        )
                    
                    ingrediënten_mogelijk = self.zoeken(zoekterm)
                    if len(ingrediënten_mogelijk) == 0:
                        print(f"\n>>> zoekterm \"{zoekterm}\" levert geen ingrediënten op")
                        continue
                    
                    print(f"\n>>> {len(ingrediënten_mogelijk)} ingrediënt{"en" if len(ingrediënten_mogelijk) > 1 else ""} gevonden")
                    ingrediënt_uuid = invoer_kiezen(
                        "ingrediënt",
                        {self[ingrediënt_uuid]: ingrediënt_uuid for ingrediënt_uuid in ingrediënten_mogelijk},
                        stoppen = True,
                        terug_naar = terug_naar,
                        )
                    
                    if ingrediënt_uuid is STOP:
                        continue
                    
                    print(f"\n>>> {self[ingrediënt_uuid]} gekozen")
                    
                    return ingrediënt_uuid
                
                if kies_optie == "nieuw ingrediënt":
                    return self.nieuw(
                        terug_naar,
                        )
    
    def zoeken(
        self,
        zoekterm: str,
        ) -> List[str]:
        
        return [ingrediënt_uuid for ingrediënt_uuid, ingrediënt in self.items() if zoekterm in ingrediënt.ingrediënt_naam]