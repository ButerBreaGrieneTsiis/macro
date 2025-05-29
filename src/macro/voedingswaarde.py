from typing import Dict

from grienetsiis import invoer_validatie, invoer_kiezen

from .macrotype import Hoeveelheid, Eenheid


class Voedingswaarde:
    
    VELDEN = frozenset(("calorieën", "vetten", "verzadigd", "koolhydraten", "suikers", "eiwitten", "vezels", "zout", ))
    
    CALORIE_PER_GRAM_VET            =   9.0
    CALORIE_PER_GRAM_KOOLHYDRAAT    =   4.0
    CALORIE_PER_GRAM_EIWIT          =   4.0
    KILOJOULE_PER_KILOCALORIE       =   4.184
    
    def __init__(
        self,
        calorieën: Hoeveelheid      = None,
        vetten: Hoeveelheid         = None,
        verzadigd: Hoeveelheid      = None,
        koolhydraten: Hoeveelheid   = None,
        suikers: Hoeveelheid        = None,
        eiwitten: Hoeveelheid       = None,
        vezels: Hoeveelheid         = None,
        zout: Hoeveelheid           = None,
        ) -> "Voedingswaarde":
        
        self.calorieën    = calorieën    if calorieën    is not None else Hoeveelheid(0.0, Eenheid("kcal"))
        self.vetten       = vetten       if vetten       is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.verzadigd    = verzadigd    if verzadigd    is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.koolhydraten = koolhydraten if koolhydraten is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.suikers      = suikers      if suikers      is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.eiwitten     = eiwitten     if eiwitten     is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.vezels       = vezels       if vezels       is not None else Hoeveelheid(0.0, Eenheid("g"))
        self.zout         = zout         if zout         is not None else Hoeveelheid(0.0, Eenheid("g"))
    
    def __repr__(self):
        
        return (
            f"    {"calorieën":<21}{self.calorieën} ({self.kilojoule})\n"
            f"    {"vetten":<21}{self.vetten}\n"
            f"      {"waarvan verzadigd":<19}{self.verzadigd}\n"
            f"    {"koolydraten":<21}{self.koolhydraten}\n"
            f"      {"waarvan suikers":<19}{self.suikers}\n"
            f"    {"eiwitten":<21}{self.eiwitten}\n"
            f"    {"vezels":<21}{self.vezels}\n"
            f"    {"zout":<21}{self.zout}"
            )
    
    def __mul__(
        self,
        factor: float | int,
        ) -> "Voedingswaarde":
        
        return Voedingswaarde(
            factor * self.calorieën,
            factor * self.vetten,
            factor * self.verzadigd,
            factor * self.koolhydraten,
            factor * self.suikers,
            factor * self.eiwitten,
            factor * self.vezels,
            factor * self.zout,
            )
    
    def __iadd__(
        self,
        ander: "Voedingswaarde",
        ) -> "Voedingswaarde":
        
        self.calorieën      += ander.calorieën
        self.vetten         += ander.vetten
        self.verzadigd      += ander.verzadigd
        self.koolhydraten   += ander.koolhydraten
        self.suikers        += ander.suikers
        self.eiwitten       += ander.eiwitten
        self.vezels         += ander.vezels
        self.zout           += ander.zout
        
        return self
    
    def __add__(
        self,
        ander: "Voedingswaarde",
        ) -> "Voedingswaarde":
        
        return Voedingswaarde(
            self.calorieën      + ander.calorieën,
            self.vetten         + ander.vetten,
            self.verzadigd      + ander.verzadigd,
            self.koolhydraten   + ander.koolhydraten,
            self.suikers        + ander.suikers,
            self.eiwitten       + ander.eiwitten,
            self.vezels         + ander.vezels,
            self.zout           + ander.zout,
            )
    
    @classmethod
    def van_json(
        cls,
        **dict,
        ) -> "Voedingswaarde":
        
        for sleutel in list(dict.keys()):
            if sleutel == "calorieën":
                dict["calorieën"] = Hoeveelheid(dict["calorieën"], Eenheid("kcal"))
            else:
                dict[sleutel] = Hoeveelheid(dict[sleutel]/10, Eenheid("g"))
        
        return cls(**dict)
    
    def naar_json(self) -> Dict[str, int]:
        
        dict_naar_json = {}
        
        for veld_sleutel, veld_waarde in self.__dict__.items():
            
            if veld_waarde == 0.0:
                continue
            
            dict_naar_json[veld_sleutel] = int(round(10 * veld_waarde.waarde))
        
        return dict_naar_json
    
    @classmethod
    def nieuw(
        cls,
        basis_eenheid,
        ) -> "Voedingswaarde":
        
        while True:
            
            print(f"vul de voedingswaarde in per 100 {basis_eenheid.enkelvoud}")
            
            calorieën = invoer_validatie("calorieën", int, bereik = (0, 900))
            vetten = invoer_validatie("vetten", float, bereik = (0.0, 100.0))
            verzadigd = invoer_validatie("waarvan verzadigd", float, bereik = (0.0, vetten)) if not vetten == 0.0 else 0
            koolhydraten = invoer_validatie("koolhydraten", float, bereik = (0.0, 100.0))
            suikers = invoer_validatie("waarvan suikers", float, bereik = (0.0, koolhydraten)) if not koolhydraten == 0.0 else 0
            eiwitten = invoer_validatie("eiwitten", float, bereik = (0.0, 100.0))
            vezels = invoer_validatie("vezels", float, bereik = (0.0, 100.0))
            zout = invoer_validatie("zout", float, bereik = (0.0, 100.0))
            
            calorieën_berekend = vetten * cls.CALORIE_PER_GRAM_VET + koolhydraten * cls.CALORIE_PER_GRAM_KOOLHYDRAAT + eiwitten * cls.CALORIE_PER_GRAM_EIWIT
            
            if abs(calorieën - calorieën_berekend) / ((calorieën + calorieën_berekend)/2) > 0.1:
                print(f"calorieën ingevuld ({calorieën} kcal) en berekend ({calorieën_berekend} kcal) verschillen meer dan 10%")
                if invoer_kiezen("doorgaan", {"ja": False, "nee": True}):
                    continue
            
            break
        
        return cls(
            calorieën,
            int(round(10 * vetten)),
            int(round(10 * verzadigd)),
            int(round(10 * koolhydraten)),
            int(round(10 * suikers)),
            int(round(10 * eiwitten)),
            int(round(10 * vezels)),
            int(round(10 * zout)),
            )
    
    @property
    def kilojoule(self) -> Hoeveelheid:
        return Hoeveelheid(self.KILOJOULE_PER_KILOCALORIE*self.calorieën.waarde, Eenheid("kJ"))