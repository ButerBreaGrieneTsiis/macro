"""
macro
"""
from pathlib import Path

from grienetsiis.register import Register

from macro.categorie import Hoofdcategorie


__all__ = [
    "Hoofdcategorie",
    ]

__version__ = "1.0.0-dev"

Register.instellen(
    registratie_methode = "uuid",
    bestandsmap = Path("gegevens"),
    )

Register.registreer_type(
    geregistreerd_type = Hoofdcategorie,
    subregister_naam = "hoofdcategorie",
    bestandsmap = Path("gegevens"),
    bestandsnaam = "hoofdcategorie",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Hoofdcategorie.naar_json,
    ontcijfer_functie_objecten = Hoofdcategorie.van_json,
    )