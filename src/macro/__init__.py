"""
macro
"""
from pathlib import Path

from grienetsiis.json import Ontcijferaar, Vercijferaar
from grienetsiis.register import Register

from macro.categorie import Hoofdcategorie, HoofdcategorieGerecht, Categorie, CategorieGerecht
from macro.product import Ingrediënt, Merk, Product
from macro.voedingswaarde import Eenheid, Voedingswaarde


__version__ = "1.0.0-dev"

ENUMS = {
    "Eenheid": Eenheid,
    }

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
    geregistreerd_type = HoofdcategorieGerecht,
    subregister_naam = HoofdcategorieGerecht._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "hoofdcategorie_gerecht",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = HoofdcategorieGerecht.naar_json,
    ontcijfer_functie_objecten = HoofdcategorieGerecht.van_json,
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
    geregistreerd_type = CategorieGerecht,
    subregister_naam = CategorieGerecht._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "categorie_gerecht",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = CategorieGerecht.naar_json,
    ontcijfer_functie_objecten = CategorieGerecht.van_json,
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
Register.registreer_type(
    geregistreerd_type = Merk,
    subregister_naam = Merk._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "merk",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Merk.naar_json,
    ontcijfer_functie_objecten = Merk.van_json,
    )
Register.registreer_type(
    geregistreerd_type = Product,
    subregister_naam = Product._SUBREGISTER_NAAM,
    bestandsmap = Path("gegevens"),
    bestandsnaam = "product",
    vercijfer_methode = "functie",
    vercijfer_functie_objecten = Product.naar_json,
    ontcijfer_functie_objecten = Product.van_json,
    vercijfer_functie_subobjecten = [
        Vercijferaar(
            class_naam = "Voedingswaarde",
            vercijfer_functie_naam = "naar_json",
            ),
        ],
    ontcijfer_functie_subobjecten = [
        Ontcijferaar(
            velden = frozenset((
                "_calorieën",
                "_vetten",
                "_verzadigd",
                "_koolhydraten",
                "_suikers",
                "_eiwitten",
                "_vezels",
                "_zout",
                )),
            ontcijfer_functie = Voedingswaarde.van_json,
            ),
        ],
    enums = ENUMS,
    )