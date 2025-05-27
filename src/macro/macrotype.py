import datetime as dt
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

from grienetsiis import openen_json, opslaan_json, ObjectWijzer


class MacroType:
    
    ENCODER_DICT: Dict[str, str] = {
        "Dag": "naar_json",
        "Hoeveelheid": "naar_json",
        }
    
    @classmethod
    def van_json(
        cls,
        **dict,
        ) -> "MacroType":
        
        if "eenheid" in dict.keys():
            dict["eenheid"] = Eenheid(dict["eenheid"])
            
        if "basis_eenheid" in dict.keys():
            dict["basis_eenheid"] = Eenheid(dict["basis_eenheid"])
        
        if "eenheden" in dict.keys():
            for eenheid in list(dict["eenheden"].keys()):
                dict["eenheden"][Eenheid(eenheid)] =  dict["eenheden"].pop(eenheid)
        
        if "datum" in dict.keys():
            dict["datum"] = dt.datetime.strptime(dict["datum"], "%Y-%m-%d").date()
        
        return cls(**dict)
    
    def naar_json(self) -> Dict[str, Any]:
        
        dict_naar_json = {}
        
        for veld_sleutel, veld_waarde in self.__dict__.items():
            
            # alle velden uitsluiten die standaardwaardes hebben; nutteloos om op te slaan
            if veld_waarde is None:
                continue
            elif isinstance(veld_waarde, bool) and not veld_waarde:
                continue
            elif isinstance(veld_waarde, list) and len(veld_waarde) == 0:
                continue
            elif isinstance(veld_waarde, dict) and not bool(veld_waarde):
                continue
            elif isinstance(veld_waarde, str) and veld_waarde == "":
                continue
            elif isinstance(veld_waarde, int) and veld_waarde == 0:
                continue
            elif veld_sleutel == "_uuid":
                continue
            
            # overige velden deserialiseren
            elif isinstance(veld_waarde, dict) and all(isinstance(veld_subsleutel, Eenheid) for veld_subsleutel in veld_waarde.keys()):
                dict_naar_json[veld_sleutel] = {}
                for veld_subsleutel, veld_subwaarde in veld_waarde.items():
                    dict_naar_json[veld_sleutel][veld_subsleutel.value] = veld_subwaarde
            elif isinstance(veld_sleutel, Eenheid):
                dict_naar_json[veld_sleutel.value] = veld_waarde
            elif isinstance(veld_waarde, Eenheid):
                dict_naar_json[veld_sleutel] = veld_waarde.value
            elif isinstance(veld_waarde, Hoeveelheid):
                dict_naar_json[veld_waarde.eenheid.value] = veld_waarde.waarde
            elif isinstance(veld_waarde, dt.date):
                dict_naar_json[veld_sleutel] = veld_waarde.strftime("%Y-%m-%d")
            
            # alle overige velden toevoegen
            else:
                dict_naar_json[veld_sleutel] = veld_waarde
        
        return dict_naar_json
    
    def opslaan(self) -> None:
        bestandspad = self.BESTANDSMAP / f"{self.bestandsnaam}.{self.EXTENSIE}"
        
        opslaan_json(self, bestandspad, encoder_dict = self.ENCODER_DICT)
    
    @property
    def uuid(self):
        return self._uuid
    
    @uuid.setter
    def uuid(self, waarde):
        self._uuid = waarde

class MacroTypeDatabank(dict):
    
    BESTANDSMAP:    Path = Path("gegevens")
    EXTENSIE:       str = "json"
    ENCODER_DICT:   Dict[str, str] = {
        "Voedingswaarde":   "naar_json",
        "Hoofdcategorie":   "naar_json",
        "Categorie":        "naar_json",
        "Ingrediënt":       "naar_json",
        "Product":          "naar_json",
        "Gerecht":          "naar_json",
        }
    
    @classmethod
    def openen(cls) -> "MacroTypeDatabank":
        
        if not cls.BESTANDSMAP.is_dir():
            cls.BESTANDSMAP.mkdir()
        
        bestandspad = cls.BESTANDSMAP / f"{cls.BESTANDSNAAM}.{cls.EXTENSIE}"
        
        if bestandspad.is_file():
            def toevoegen_uuid(macrotype, uuid): 
                macrotype.uuid = uuid
                return macrotype
            
            return cls(**{uuid: toevoegen_uuid(macrotype, uuid) for uuid, macrotype in openen_json(
                bestandspad,
                object_wijzers = cls.OBJECT_WIJZERS,
                ).items()})
        else:
            return cls()
    
    def opslaan(self) -> None:
        bestandspad = self.BESTANDSMAP / f"{self.BESTANDSNAAM}.{self.EXTENSIE}"
        
        opslaan_json(self, bestandspad, encoder_dict = self.ENCODER_DICT)
    
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
    KILOJOULE   =   "kJ",           "kJ"
    
    # https://stackoverflow.com/questions/75384124/how-to-initialize-named-tuple-in-python-enum
    def __new__(cls, enkelvoud, meervoud):
        veld = object.__new__(cls)
        veld._value_    = enkelvoud
        veld.enkelvoud  = enkelvoud
        veld.meervoud   = meervoud
        return veld

class Hoeveelheid(MacroType):
    
    VELDEN              = frozenset(("waarde", "eenheid", ))
    BASIS_EENHEDEN      = [Eenheid["GRAM"], Eenheid["MILLILITER"]]
    ENERGIE_EENHEDEN    = [Eenheid["KILOCALORIE"], Eenheid["KILOJOULE"]]
    
    def __init__(
        self,
        waarde: float,
        eenheid: Eenheid,
        ) -> "Hoeveelheid":
        
        self.waarde = waarde
        self.eenheid = eenheid
    
    def __repr__(self) -> str:
        
        vermenigvuldiger = 100.0 if self.eenheid in self.BASIS_EENHEDEN else 1.0
        
        formaat = ".0f" if self.waarde.is_integer() or self.eenheid in self.BASIS_EENHEDEN else ".2f"
        
        if self.waarde == 1.0:
            return f"{self.waarde*vermenigvuldiger:{formaat}} {self.eenheid.enkelvoud}"
        else:
            return f"{self.waarde*vermenigvuldiger:{formaat}} {self.eenheid.meervoud}"
    
    def __add__(self, ander) -> "Hoeveelheid":
        return Hoeveelheid(self.waarde + ander.waarde, self.eenheid)
    
    def __eq__(self, ander) -> bool:
        return self.eenheid == ander.eenheid