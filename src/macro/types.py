from grienetsiis import invoer_validatie, invoer_kiezen


class MacroType:
    
    ...

class Voedingswaarde(MacroType):
    
    """
    is het nodig om voedinsgswaarde apart te maken voor 
    een los product t.o.v. een totale voedingswaarde voor een dag/recept?
    """
    
    calorie_per_gram_vet            =   9
    calorie_per_gram_koolhydraat    =   4
    calorie_per_gram_eiwit          =   4
    
    def __init__(
        self,
        calorieen:      int = 0,
        vetten:         int = 0,
        verzadigd:      int = 0,
        koolhydraten:   int = 0,
        suikers:        int = 0,
        eiwitten:       int = 0,
        vezels:         int = 0,
        zout:           int = 0,
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
        
        return f"""
            \t{"calorieën":<21}{self.calorieen:>6.0f} kcal
            \t{f"({int(4.184*self.calorieen)}":>27} kJ)
            \t{"vetten":<21}{self.vetten/10:>6.1f} g
            \t\t{"waarvan verzadigd":<17}{self.verzadigd/10:>6.1f} g
            \t{"koolydraten":<21}{self.koolhydraten/10:>6.1f} g
            \t\t{"waarvan suikers":<17}{self.suikers/10:>6.1f} g
            \t{"eiwitten":<21}{self.eiwitten/10:>6.1f} g
            \t{"vezels":<21}{self.vezels/10:>6.1f} g
            \t{"zout":<21}{self.zout/10:>6.1f} g
            """
    
    @classmethod
    def nieuw(cls) -> "Voedingswaarde":
        
        while True:
            
            calorieen = invoer_validatie("calorieën", int, bereik = (0, 900))
            vetten = invoer_validatie("vetten", float, bereik = (0.0, 100.0))
            if not vetten == 0.0:
                verzadigd = invoer_validatie("waarvan verzadigd", float, bereik = (0.0, vetten))
            koolhydraten = invoer_validatie("koolhydraten", float, bereik = (0.0, 100.0))
            if not koolhydraten == 0.0:
                suikers = invoer_validatie("waarvan suikers", float, bereik = (0.0, koolhydraten))
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
            int(10 * vetten),
            int(10 * verzadigd),
            int(10 * koolhydraten),
            int(10 * suikers),
            int(10 * eiwitten),
            int(10 * vezels),
            int(10 * zout),
            )
