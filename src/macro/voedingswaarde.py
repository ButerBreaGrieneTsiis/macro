from typing import List

from grienetsiis import invoer_validatie, invoer_kiezen

from .macrotype import MacroType


class Voedingswaarde(MacroType):
    
    VELDEN = frozenset(("calorieën", "vetten", "verzadigd", "koolhydraten", "suikers", "eiwitten", "vezels", "zout", ))
    
    CALORIE_PER_GRAM_VET            =   9.0
    CALORIE_PER_GRAM_KOOLHYDRAAT    =   4.0
    CALORIE_PER_GRAM_EIWIT          =   4.0
    KILOJOULE_PER_KILOCALORIE       =   4.184
    
    def __init__(
        self,
        calorieën: int      = 0,
        vetten: int         = 0,
        verzadigd: int      = 0,
        koolhydraten: int   = 0,
        suikers: int        = 0,
        eiwitten: int       = 0,
        vezels: int         = 0,
        zout: int           = 0,
        ) -> "Voedingswaarde":
        
        self.calorieën      =   calorieën
        self.vetten         =   vetten
        self.verzadigd      =   verzadigd
        self.koolhydraten   =   koolhydraten
        self.suikers        =   suikers
        self.eiwitten       =   eiwitten
        self.vezels         =   vezels
        self.zout           =   zout
    
    def __repr__(self):
        
        return (
            f"    {"calorieën":<21}{self.calorieën:>6.0f} kcal\n"
            f"    {f"({int(self.KILOJOULE_PER_KILOCALORIE*self.calorieën)}":>27} kJ)\n"
            f"    {"vetten":<21}{self.vetten/10:>6.1f} g\n"
            f"        {"waarvan verzadigd":<17}{self.verzadigd/10:>6.1f} g\n"
            f"    {"koolydraten":<21}{self.koolhydraten/10:>6.1f} g\n"
            f"        {"waarvan suikers":<17}{self.suikers/10:>6.1f} g\n"
            f"    {"eiwitten":<21}{self.eiwitten/10:>6.1f} g\n"
            f"    {"vezels":<21}{self.vezels/10:>6.1f} g\n"
            f"    {"zout":<21}{self.zout/10:>6.1f} g"
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
    
    def afronden(self):
        
        self.calorieën      =   round(self.calorieën)
        self.vetten         =   round(self.vetten)
        self.verzadigd      =   round(self.verzadigd)
        self.koolhydraten   =   round(self.koolhydraten)
        self.suikers        =   round(self.suikers)
        self.eiwitten       =   round(self.eiwitten)
        self.vezels         =   round(self.vezels)
        self.zout           =   round(self.zout)
        
        return self
    
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