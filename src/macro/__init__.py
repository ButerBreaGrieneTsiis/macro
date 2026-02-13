"""
macro
"""
from pathlib import Path

from grienetsiis.register import Register

from macro.categorie import Hoofdcategorie, Categorie
from macro.product import Ingrediënt


__version__ = "1.0.0-dev"

Register.instellen(
    registratie_methode = "uuid",
    bestandsmap = Path("gegevens"),
    )

Register.registreer_type(
    geregistreerd_type = Hoofdcategorie,
    subregister_naam = Hoofdcategorie._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "hoofdcategorie",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Hoofdcategorie.naar_json,
    ontcijfer_functie_objecten = Hoofdcategorie.van_json,
    )
Register.registreer_type(
    geregistreerd_type = Categorie,
    subregister_naam = Categorie._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "categorie",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Categorie.naar_json,
    ontcijfer_functie_objecten = Categorie.van_json,
    )
Register.registreer_type(
    geregistreerd_type = Ingrediënt,
    subregister_naam = Ingrediënt._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "ingrediënt",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Ingrediënt.naar_json,
    ontcijfer_functie_objecten = Ingrediënt.van_json,
    )