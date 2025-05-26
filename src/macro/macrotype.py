import datetime as dt
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from grienetsiis import openen_json, opslaan_json, ObjectWijzer


class MacroType:
    
    encoder_dict:   Dict[str, str] = {
        "Dag": "naar_json",
        }
    
    @classmethod
    def van_json(
        cls,
        **dict,
        ) -> "MacroType":
        
        if "eenheid" in dict.keys():
            dict["eenheid"] = Eenheid(dict["eenheid"])
        
        # for eenheid in Eenheid._member_names_:
        #     print(Eenheid[eenheid].enkelvoud, dict.keys())
        #     if Eenheid[eenheid].enkelvoud in dict.keys():
        #         dict[Eenheid[eenheid]] = dict.pop(Eenheid[eenheid].enkelvoud)
        
        if "eenheden" in dict.keys():
            for eenheid in list(dict["eenheden"].keys()):
                dict["eenheden"][Eenheid(eenheid)] =  dict["eenheden"].pop(eenheid)
                
        if "datum" in dict.keys():
            dict["datum"] = dt.datetime.strptime(dict["datum"], "%Y-%m-%d").date()
        
        return cls(**dict)
    
    def naar_json(self) -> Dict[str, Any]:
        
        dict_naar_json = {}
        
        for veld, waarde in self.__dict__.items():
            
            # alle velden uitsluiten die standaardwaardes hebben; nutteloos om op te slaan
            if waarde is None:
                continue
            elif isinstance(waarde, bool) and not waarde:
                continue
            elif isinstance(waarde, list) and len(waarde) == 0:
                continue
            elif isinstance(waarde, dict) and not bool(waarde):
                continue
            elif isinstance(waarde, str) and waarde == "":
                continue
            elif isinstance(waarde, int) and waarde == 0:
                continue
            elif isinstance(waarde, Eenheid):
                dict_naar_json[veld] = waarde.value
            elif isinstance(waarde, Hoeveelheid):
                print(waarde)
                dict_naar_json[waarde.eenheid.value] = waarde.waarde
                print(dict_naar_json)
            elif isinstance(waarde, dt.date):
                dict_naar_json[veld] = waarde.strftime("%Y-%m-%d")
            elif veld == "_uuid":
                continue
            else:
                dict_naar_json[veld] = waarde
        
        return dict_naar_json
    
    def opslaan(self) -> None:
        bestandspad = self.bestandsmap / f"{self.bestandsnaam}.{self.extensie}"
        
        opslaan_json(self, bestandspad, encoder_dict = self.encoder_dict)
    
    @property
    def uuid(self):
        return self._uuid
    
    @uuid.setter
    def uuid(self, waarde):
        self._uuid = waarde

class MacroTypeDatabank(dict):
    
    bestandsmap:    Path = Path("gegevens")
    extensie:       str = "json"
    encoder_dict:   Dict[str, str] = {
        "Voedingswaarde":   "naar_json",
        "Hoofdcategorie":   "naar_json",
        "Categorie":        "naar_json",
        "Ingrediënt":       "naar_json",
        "Product":          "naar_json",
        "Gerecht":          "naar_json",
        }
    
    @classmethod
    def openen(cls) -> "MacroTypeDatabank":
        
        if not cls.bestandsmap.is_dir():
            cls.bestandsmap.mkdir()
        
        bestandspad = cls.bestandsmap / f"{cls.bestandsnaam}.{cls.extensie}"
        
        if bestandspad.is_file():
            def toevoegen_uuid(macrotype, uuid): 
                macrotype.uuid = uuid
                return macrotype
            
            return cls(**{uuid: toevoegen_uuid(macrotype, uuid) for uuid, macrotype in openen_json(
                bestandspad,
                object_wijzers = cls.object_wijzers,
                ).items()})
        else:
            return cls()
    
    def opslaan(self) -> None:
        bestandspad = self.bestandsmap / f"{self.bestandsnaam}.{self.extensie}"
        
        opslaan_json(self, bestandspad, encoder_dict = self.encoder_dict)
    
    @property
    def lijst(self) -> List[MacroType]:
        return list(self.values())

class Eenheid(Enum):
    
    STUK        =   "stuk",         "stuks"
    FLES        =   "fles",         "flessen"
    BLIK        =   "blik",         "blikken"
    POT         =   "pot",          "potten"
    PORTIE      =   "portie",       "porties"
    ZAK         =   "zak",          "zakken"
    THEELEPEL   =   "eetlepel",     "eetlepels"
    EETLEPEL    =   "theelepel",    "theelepels"
    PLAK        =   "plak",         "plakken"
    VERPAKKING  =   "verpakking",   "verpakkingen"
    GRAM        =   "g",            "g"
    MILLILITER  =   "ml",           "ml"
    KILOCALORIE =   "kcal",         "kcal"
    
    # https://stackoverflow.com/questions/75384124/how-to-initialize-named-tuple-in-python-enum
    def __new__(cls, enkelvoud, meervoud):
        veld = object.__new__(cls)
        veld._value_    = enkelvoud
        veld.enkelvoud  = enkelvoud
        veld.meervoud   = meervoud
        return veld

class Hoeveelheid(MacroType):
    
    def __init__(
        self,
        waarde: float,
        eenheid: Eenheid,
        ) -> "Hoeveelheid":
        
        self.waarde = waarde
        self.eenheid = eenheid
    
    def __repr__(self) -> str:
        
        formaat = ".0f" if self.waarde.is_integer() else ".2f"
        
        if self.waarde == 1.0:
            return f"{self.waarde:{formaat}} {self.eenheid.enkelvoud}"
        else:
            return f"{self.waarde:{formaat}} {self.eenheid.meervoud}"
    # VERDERGAAN MET HOEVEELHEID.NAAR_JSON/VAN_JSON
    
    # hoeveelheid naar_json -> "eenheid": waarde als sleutel-waarde paar
    
    # @classmethod
    # def van_tekst(
    #     cls,
    #     waarde: float,
    #     eenheid: str,
    #     ) -> "Hoeveelheid":
        
    #     return cls(
    #         waarde,
    #         Eenheid(eenheid),
    #         )