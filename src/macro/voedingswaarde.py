from typing import List

from grienetsiis import invoer_validatie, invoer_kiezen

from .macrotype import MacroType


class Voedingswaarde(MacroType):
    
    calorie_per_gram_vet            =   9
    calorie_per_gram_koolhydraat    =   4
    calorie_per_gram_eiwit          =   4
    kilojoule_per_kilocalorie       =   4.184
    
    def __init__(
        self,
        calorieen: int      = 0,
        vetten: int         = 0,
        verzadigd: int      = 0,
        koolhydraten: int   = 0,
        suikers: int        = 0,
        eiwitten: int       = 0,
        vezels: int         = 0,
        zout: int           = 0,
        ) -> "Voedingswaarde":
        
        self.calorieen      =   calorieen
        self.vetten         =   vetten
        self.verzadigd      =   verzadigd
        self.koolhydraten   =   koolhydraten
        self.suikers        =   suikers
        self.eiwitten       =   eiwitten
        self.vezels         =   vezels
        self.zout           =   zout
    
    def __repr__(self):
        
        return (
            f"\t{"calorieën":<21}{self.calorieen:>6.0f} kcal\n"
            f"\t{f"({int(self.kilojoule_per_kilocalorie*self.calorieen)}":>27} kJ)\n"
            f"\t{"vetten":<21}{self.vetten/10:>6.1f} g\n"
            f"\t\t{"waarvan verzadigd":<17}{self.verzadigd/10:>6.1f} g\n"
            f"\t{"koolydraten":<21}{self.koolhydraten/10:>6.1f} g\n"
            f"\t\t{"waarvan suikers":<17}{self.suikers/10:>6.1f} g\n"
            f"\t{"eiwitten":<21}{self.eiwitten/10:>6.1f} g\n"
            f"\t{"vezels":<21}{self.vezels/10:>6.1f} g\n"
            f"\t{"zout":<21}{self.zout/10:>6.1f} g"
            )
    
    def __mul__(
        self,
        factor,
        ) -> "Voedingswaarde":
        
        ...
    
    @classmethod
    def nieuw(
        cls,
        eenheid,
        ) -> "Voedingswaarde":
        
        while True:
            
            print(f"vul de voedingswaarde in per 100 {eenheid.enkelvoud}")
            
            calorieen = invoer_validatie("calorieën", int, bereik = (0, 900))
            vetten = invoer_validatie("vetten", float, bereik = (0.0, 100.0))
            verzadigd = invoer_validatie("waarvan verzadigd", float, bereik = (0.0, vetten)) if not vetten == 0.0 else 0
            koolhydraten = invoer_validatie("koolhydraten", float, bereik = (0.0, 100.0))
            suikers = invoer_validatie("waarvan suikers", float, bereik = (0.0, koolhydraten)) if not koolhydraten == 0.0 else 0
            eiwitten = invoer_validatie("eiwitten", float, bereik = (0.0, 100.0))
            vezels = invoer_validatie("vezels", float, bereik = (0.0, 100.0))
            zout = invoer_validatie("zout", float, bereik = (0.0, 100.0))
            
            calorieen_berekend = vetten * cls.calorie_per_gram_vet + koolhydraten * cls.calorie_per_gram_koolhydraat + eiwitten * cls.calorie_per_gram_eiwit
            
            if abs(calorieen - calorieen_berekend) / ((calorieen + calorieen_berekend)/2) > 0.1:
                print(f"calorieën ingevuld ({calorieen} kcal) en berekend ({calorieen_berekend} kcal) verschillen meer dan 10%")
                if invoer_kiezen("doorgaan", {"ja": False, "nee": True}):
                    continue
            
            break
        
        return cls(
            calorieen,
            int(round(10 * vetten)),
            int(round(10 * verzadigd)),
            int(round(10 * koolhydraten)),
            int(round(10 * suikers)),
            int(round(10 * eiwitten)),
            int(round(10 * vezels)),
            int(round(10 * zout)),
            )
    
    @classmethod
    def van_json(
        cls,
        *lijst: List[int],
        ) -> "Voedingswaarde":
        
        return cls(*lijst)
    
    def naar_json(self) -> List[int]:
        return [
            self.calorieen,
            self.vetten,
            self.verzadigd,
            self.koolhydraten,
            self.suikers,
            self.eiwitten,
            self.vezels,
            self.zout,
            ]