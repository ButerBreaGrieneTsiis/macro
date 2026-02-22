"""macro.gerecht.variant"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Literal, TYPE_CHECKING

from grienetsiis.opdrachtprompt import invoeren, kiezen, commando, Menu
from grienetsiis.register import Subregister, Register, GeregistreerdObject
from grienetsiis.types import BasisType

from macro.gerecht import HoofdcategorieGerecht, CategorieGerecht
from macro.product import Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde

if TYPE_CHECKING:
    from macro.gerecht import Gerecht


@dataclass
class Recept(BasisType):
    ...