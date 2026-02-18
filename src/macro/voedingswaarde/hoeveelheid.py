"""macro.voedingswaarde.hoeveelheid"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, List

from grienetsiis.gereedschap import formatteer_getal

from macro.voedingswaarde import Eenheid


@dataclass
class Hoeveelheid:
    
    waarde: float
    eenheid: Eenheid
    
    _BASIS_EENHEDEN: ClassVar[List[Eenheid]] = [
        Eenheid.GRAM,
        Eenheid.MILLILITER,
        ]
    _ENERGIE_EENHEDEN: ClassVar[List[Eenheid]] = [
        Eenheid.KILOCALORIE,
        Eenheid.KILOJOULE,
        ]
    
    # DUNDER METHODS
    
    def __repr__(self) -> str:
        
        if self.waarde == 1.0 or self.eenheid in Hoeveelheid._BASIS_EENHEDEN or self.eenheid in Hoeveelheid._ENERGIE_EENHEDEN:
            eenheid = self.eenheid.enkelvoud
        else:
            eenheid = self.eenheid.meervoud
        
        if self.eenheid in Hoeveelheid._ENERGIE_EENHEDEN:
            aantal_decimalen = 0
            decimalen_automatisch = False
        elif self.eenheid in Hoeveelheid._BASIS_EENHEDEN:
            aantal_decimalen = 1
            decimalen_automatisch = False
        else:
            aantal_decimalen = 3
            decimalen_automatisch = True
        
        return formatteer_getal(
            getal = self.waarde,
            decimalen_automatisch = decimalen_automatisch,
            decimalen = aantal_decimalen,
            suffix = eenheid
            )
    
    def __add__(
        self,
        ander: Hoeveelheid,
        ) -> Hoeveelheid:
        
        return Hoeveelheid(self.waarde + ander.waarde, self.eenheid)
    
    def __mul__(
        self,
        factor: float | int,
        ) -> Hoeveelheid:
        
        return Hoeveelheid(
            self.waarde * factor,
            self.eenheid,
            )
    
    def __rmul__(
        self,
        factor: float | int,
        ) -> Hoeveelheid:
        
        return Hoeveelheid(
            self.waarde * factor,
            self.eenheid,
            )
    
    def __truediv__(
        self,
        factor: float | int,
        ) -> Hoeveelheid:
        
        return Hoeveelheid(
            self.waarde / factor,
            self.eenheid,
            )
    
    def __iadd__(
        self,
        ander: Hoeveelheid,
        ) -> Hoeveelheid:
        
        self.waarde += ander.waarde
        
        return self