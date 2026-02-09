"""macro.categorie.hoofdcategorie"""
from __future__ import annotations
from dataclasses import dataclass

from grienetsiis.register import GeregistreerdObject


@dataclass
class Hoofdcategorie(GeregistreerdObject):
    
    hoofdcategorie_naam: str