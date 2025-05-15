from typing import Dict, List
from uuid import uuid4

from grienetsiis import invoer_kiezen, invoer_validatie

from .categorie import Categorieën
from .hoeveelheid import Eenheid, Hoeveelheid
from .ingredient import Ingrediënten
from .macrotype import ClassMapper, MacroType, MacroTypeDatabank
from .voedingswaarde import Voedingswaarde


class Product(MacroType):
    
    frozenset = frozenset(("product_naam", "merk_naam", "opmerking", "voedingswaarde", "eenheid", "ingrediënt_uuid", "hoeveelheden",))
    
    def __init__(
        self,
        product_naam: str,
        merk_naam: str,
        voedingswaarde: Voedingswaarde,
        eenheid: Eenheid,
        ingrediënt_uuid: str,
        opmerking: str = None,
        hoeveelheden: Dict[Eenheid, float] = None,
        ) -> "Product":
        
        self.product_naam       = product_naam
        self.merk_naam          = merk_naam
        self.opmerking          = opmerking
        self.voedingswaarde     = voedingswaarde
        self.eenheid            = eenheid
        self.ingrediënt_uuid    = ingrediënt_uuid
        self.hoeveelheden       = dict() if hoeveelheden is None else hoeveelheden
    
    def __repr__(self) -> str:
        return f"product \"{self.product_naam} ({self.merk_naam})\"" \
        + f"\nvoedingswaarde per 100 {self.eenheid.enkelvoud}:" \
        + f"\n{self.voedingswaarde}"
    
    @classmethod
    def nieuw(cls) -> "Product":
        
        ingrediënten = Ingrediënten.openen()
        ingrediënt_uuid = ingrediënten.kiezen()
        print(f"\ninvullen gegevens nieuw product onder ingrediënt \"{ingrediënten[ingrediënt_uuid].ingrediënt_naam}\"")
        product_naam = invoer_validatie("productnaam", str, valideren = True, kleine_letters = True)
        merk_naam = invoer_validatie("merknaam", str, valideren = True, kleine_letters = True)
        opmerking = invoer_validatie("opmerking", str, kleine_letters = True)
        eenheid = Eenheid(invoer_kiezen("eenheid", ["g", "ml"]))
        voedingswaarde = Voedingswaarde.nieuw(eenheid)
        
        return cls(
            product_naam,
            merk_naam,
            voedingswaarde,
            eenheid,
            ingrediënt_uuid,
            opmerking,
            )
    
    def toevoegen_hoeveelheid(self):
        
        ...
        
        return self
    
    # def bereken_voedingswaarde(
    #     self,
    #     hoeveelheid: Tuple[float, str],
    #     ) -> Voedingswaarde:
    #     # iets anders voor 100 g/ml?
    #     return deepcopy(self.voedingswaarde) * self.hoeveelheden[hoeveelheid[1]] * hoeveelheid[0]

class Producten(MacroTypeDatabank):
    
    bestandsnaam: str = "producten"
    class_mappers: List[ClassMapper] = [
        ClassMapper(Product.van_json, Product.frozenset),
        ClassMapper(Voedingswaarde.van_json, Voedingswaarde.frozenset),
        ]
    
    def opdracht(self):
        
        while True:
        
            opdracht = invoer_kiezen("opdracht product", ["nieuw product", "nieuwe hoeveelheid", "weergeven product"], stoppen = True)
            
            if not bool(opdracht):
                break
            
            elif opdracht == "nieuw product":
                self.nieuw()
            
            elif opdracht == "nieuwe hoeveelheid":
                self.nieuwe_hoeveelheid()
                
            
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
        
        product_uuid = str(uuid4())
        self[product_uuid] = product
        
        self.opslaan()
        
        return product_uuid if geef_uuid else product
    
    def nieuwe_hoeveelheid(self):
        
        product = self.kiezen(geef_uuid = False)
    
    def kiezen(
        self,
        kies_bevestiging: bool = True,
        geef_uuid: bool =  True,
        ) -> str:
        
        while True:
        
            kies_optie = invoer_kiezen("product op naam of categorie, of maak een nieuwe", ["ingrediëntnaam", "productnaam", "categorie", "nieuw"])
            
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