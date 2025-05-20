import datetime as dt
from pathlib import Path
from typing import Any, Dict, List

from grienetsiis import openen_json, opslaan_json, ObjectWijzer

from .hoeveelheid import Eenheid


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