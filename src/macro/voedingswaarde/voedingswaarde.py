"""macro.voedingswaarde.voedingswaarde"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando
from grienetsiis.types import BasisType

from macro.voedingswaarde import Eenheid, Hoeveelheid


@dataclass
class Voedingswaarde(BasisType):
    
    _calorieën: int = 0
    _vetten: int = 0
    _verzadigd: int = 0
    _koolhydraten: int = 0
    _suikers: int = 0
    _eiwitten: int = 0
    _vezels: int = 0
    _zout: int = 0
    
    _CALORIE_PER_GRAM_VET: ClassVar[float] = 9.0
    _CALORIE_PER_GRAM_KOOLHYDRAAT: ClassVar[float] = 4.0
    _CALORIE_PER_GRAM_EIWIT: ClassVar[float] = 4.0
    _KILOJOULE_PER_KILOCALORIE: ClassVar[float] = 4.184
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        
        return (
            f"{"calorieën":<21}{self.calorieën} ({self.kilojoule})\n"
            f"{"vetten":<21}{f"{self.vetten}":>8}\n"
            f"  {"waarvan verzadigd":<19}{f"{self.verzadigd}":>8}\n"
            f"{"koolydraten":<21}{f"{self.koolhydraten}":>8}\n"
            f"  {"waarvan suikers":<19}{f"{self.suikers}":>8}\n"
            f"{"eiwitten":<21}{f"{self.eiwitten}":>8}\n"
            f"{"vezels":<21}{f"{self.vezels}":>8}\n"
            f"{"zout":<21}{f"{self.zout}":>8}"
            )
    
    def __mul__(
        self,
        factor: float | int,
        ) -> Voedingswaarde:
        
        return Voedingswaarde(
            _calorieën = factor * self._calorieën,
            _vetten = factor * self._vetten,
            _verzadigd = factor * self._verzadigd,
            _koolhydraten = factor * self._koolhydraten,
            _suikers = factor * self._suikers,
            _eiwitten = factor * self._eiwitten,
            _vezels = factor * self._vezels,
            _zout = factor * self._zout,
            )
    
    def __truediv__(
        self,
        factor: float | int,
        ) -> Voedingswaarde:
        
        return Voedingswaarde(
            _calorieën = self._calorieën / factor,
            _vetten = self._vetten / factor,
            _verzadigd = self._verzadigd / factor,
            _koolhydraten = self._koolhydraten / factor,
            _suikers = self._suikers / factor,
            _eiwitten = self._eiwitten / factor,
            _vezels = self._vezels / factor,
            _zout = self._zout / factor,
            )
    
    def __iadd__(
        self,
        ander: Voedingswaarde,
        ) -> Voedingswaarde:
        
        self._calorieën += ander._calorieën
        self._vetten += ander._vetten
        self._verzadigd += ander._verzadigd
        self._koolhydraten += ander._koolhydraten
        self._suikers += ander._suikers
        self._eiwitten += ander._eiwitten
        self._vezels += ander._vezels
        self._zout += ander._zout
        
        return self
    
    def __add__(
        self,
        ander: Voedingswaarde,
        ) -> Voedingswaarde:
        
        return Voedingswaarde(
            _calorieën = self._calorieën + ander._calorieën,
            _vetten = self._vetten + ander._vetten,
            _verzadigd = self._verzadigd + ander._verzadigd,
            _koolhydraten = self._koolhydraten + ander._koolhydraten,
            _suikers = self._suikers + ander._suikers,
            _eiwitten = self._eiwitten + ander._eiwitten,
            _vezels = self._vezels + ander._vezels,
            _zout = self._zout + ander._zout,
            )
    
    # CLASS METHODS
    
    @classmethod
    def nieuw(
        cls,
        basis_eenheid: Eenheid,
        ) -> Voedingswaarde | commando.Stop:
        
        while True:
            
            print(f"\nvul de voedingswaarde in per {Hoeveelheid(100, basis_eenheid)}\n")
            
            calorieën = invoeren(
                tekst_beschrijving = "calorieën",
                invoer_type = "int",
                waardes_bereik = (0, 900),
                )
            if calorieën is commando.STOP:
                return commando.STOP
            
            vetten = invoeren(
                tekst_beschrijving = "vetten",
                invoer_type = "float",
                waardes_bereik = (0.0, 100.0),
                )
            if vetten is commando.STOP:
                return commando.STOP
            
            verzadigd = invoeren(
                tekst_beschrijving = "waarvan verzadigd",
                invoer_type = "float",
                waardes_bereik = (0.0, vetten),
                ) if not vetten == 0.0 else 0.0
            if verzadigd is commando.STOP:
                return commando.STOP
            
            koolhydraten = invoeren(
                tekst_beschrijving = "koolhydraten",
                invoer_type = "float",
                waardes_bereik = (0.0, 100.0),
                )
            if koolhydraten is commando.STOP:
                return commando.STOP
            
            suikers = invoeren(
                tekst_beschrijving = "waarvan suikers",
                invoer_type = "float",
                waardes_bereik = (0.0, koolhydraten),
                ) if not koolhydraten == 0.0 else 0.0
            if suikers is commando.STOP:
                return commando.STOP
            
            eiwitten = invoeren(
                tekst_beschrijving = "eiwitten",
                invoer_type = "float",
                waardes_bereik = (0.0, 100.0),
                )
            if eiwitten is commando.STOP:
                return commando.STOP
            
            vezels = invoeren(
                tekst_beschrijving = "vezels",
                invoer_type = "float",
                waardes_bereik = (0.0, 100.0),
                )
            if vezels is commando.STOP:
                return commando.STOP
            
            zout = invoeren(
                tekst_beschrijving = "zout",
                invoer_type = "float",
                waardes_bereik = (0.0, 100.0),
                )
            if zout is commando.STOP:
                return commando.STOP
            
            calorieën_berekend = vetten * Voedingswaarde._CALORIE_PER_GRAM_VET + koolhydraten * Voedingswaarde._CALORIE_PER_GRAM_KOOLHYDRAAT + eiwitten * Voedingswaarde._CALORIE_PER_GRAM_EIWIT
            
            if (calorieën + calorieën_berekend) > 0 and abs(calorieën - calorieën_berekend) / ((calorieën + calorieën_berekend)/2) > 0.1:
                
                keuze_doorgaan = kiezen(
                    opties = {
                        False: "verschil accepteren",
                        True: "opnieuw invullen",
                        },
                    tekst_beschrijving = f"\ncalorieën ingevuld ({Hoeveelheid(calorieën, Eenheid.KILOCALORIE)}) en berekend ({Hoeveelheid(calorieën_berekend, Eenheid.KILOCALORIE)}) verschillen meer dan 10%",
                    tekst_kies_een = False,
                    tekst_annuleren = "stop",
                    )
                
                if keuze_doorgaan is commando.STOP:
                    return commando.STOP
                if keuze_doorgaan:
                    continue
            
            break
        
        return cls(
            _calorieën = calorieën,
            _vetten = int(10 * vetten),
            _verzadigd = int(10 * verzadigd),
            _koolhydraten = int(10 * koolhydraten),
            _suikers = int(10 * suikers),
            _eiwitten = int(10 * eiwitten),
            _vezels = int(10 * vezels),
            _zout = int(10 * zout),
            )
    
    # PROPERTIES
    
    @property
    def calorieën(self) -> Hoeveelheid:
        return Hoeveelheid(self._calorieën, Eenheid.KILOCALORIE)
    
    @calorieën.setter
    def calorieën(self, waarde: int) -> None:
        self._calorieën = waarde
    
    @property
    def vetten(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._vetten/10, 1), Eenheid.GRAM)
    
    @vetten.setter
    def vetten(self, waarde: float) -> None:
        self._vetten = int(10 * waarde)
    
    @property
    def verzadigd(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._verzadigd/10, 1), Eenheid.GRAM)
    
    @verzadigd.setter
    def verzadigd(self, waarde: float) -> None:
        self._verzadigd = int(10 * waarde)
    
    @property
    def koolhydraten(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._koolhydraten/10, 1), Eenheid.GRAM)
    
    @koolhydraten.setter
    def koolhydraten(self, waarde: float) -> None:
        self._koolhydraten = int(10 * waarde)
    
    @property
    def suikers(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._suikers/10, 1), Eenheid.GRAM)
    
    @suikers.setter
    def suikers(self, waarde: float) -> None:
        self._suikers = int(10 * waarde)
    
    @property
    def eiwitten(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._eiwitten/10, 1), Eenheid.GRAM)
    
    @eiwitten.setter
    def eiwitten(self, waarde: float) -> None:
        self._eiwitten = int(10 * waarde)
    
    @property
    def vezels(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._vezels/10, 1), Eenheid.GRAM)
    
    @vezels.setter
    def vezels(self, waarde: float) -> None:
        self._vezels = int(10 * waarde)
    
    @property
    def zout(self) -> Hoeveelheid:
        return Hoeveelheid(round(self._zout/10, 1), Eenheid.GRAM)
    
    @zout.setter
    def zout(self, waarde: float) -> None:
        self._zout = int(10 * waarde)
    
    @property
    def kilojoule(self) -> Hoeveelheid:
        return Hoeveelheid(Voedingswaarde._KILOJOULE_PER_KILOCALORIE * self._calorieën, Eenheid.KILOJOULE)