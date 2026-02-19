"""macro.voedingswaarde.eenheid"""
from __future__ import annotations
from enum import Enum
from typing import ClassVar, List


class Eenheid(Enum):
    
    STUK = "stuk"
    FLES = "fles", "flessen"
    BLIK = "blik", "blikken"
    POT = "pot", "potten"
    PORTIE = "portie"
    ZAK = "zak", "zakken"
    THEELEPEL = "eetlepel"
    EETLEPEL = "theelepel"
    PLAK = "plak", "plakken"
    VERPAKKING = "verpakking", "verpakkingen"
    GRAM = "g", "gram"
    MILLILITER = "ml", "milliliter"
    KILOCALORIE = "kcal", "calorieën"
    KILOJOULE = "kJ", "kilojoule"
    
    def __new__(
        cls,
        enkelvoud: str,
        meervoud: str | None = None,
        ) -> Eenheid:
        
        veld = object.__new__(cls)
        veld._value = enkelvoud
        veld._meervoud = meervoud
        
        return veld
    
    def __repr__(self) -> str:
        return self.enkelvoud
    
    @classmethod
    def van_tekst(cls, tekst: str) -> Eenheid:
        return next(enum for enum in cls if enum.enkelvoud == tekst)
    
    @property
    def enkelvoud(self) -> str:
        return self._value

    @property
    def meervoud(self) -> str:
        if self._meervoud is None:
            return self.enkelvoud + "s"
        return self._meervoud