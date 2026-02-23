"""macro.register"""
from pathlib import Path

from grienetsiis.json import Ontcijferaar, Vercijferaar
from grienetsiis.register import Register

from macro._version import __version__
from macro.gerecht import HoofdcategorieGerecht, CategorieGerecht, Variant, Gerecht
from macro.product import Hoofdcategorie, Categorie, Ingrediënt, Merk, Product
from macro.voedingswaarde import Eenheid, Hoeveelheid, Voedingswaarde
from macro.dag import Dag


def registreren(openen: bool = True) -> None:
    
    Register.instellen(
        bestandsmap = Path("gegevens"),
        bestandsmap_kopie = Path("gegevens//kopie"),
        )
    
    ENUMS = {
        "Eenheid": Eenheid,
        }
    
    Register.registreer_type(
        geregistreerd_type = Hoofdcategorie,
        subregister_naam = "hoofdcategorie",
        bestandsmap = Path("gegevens/product"),
        bestandsnaam = "hoofdcategorie",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Hoofdcategorie.naar_json,
        ontcijfer_functie_objecten = Hoofdcategorie.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = HoofdcategorieGerecht,
        subregister_naam = "hoofdcategorie_gerecht",
        bestandsmap = Path("gegevens/gerecht"),
        bestandsnaam = "hoofdcategorie_gerecht",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = HoofdcategorieGerecht.naar_json,
        ontcijfer_functie_objecten = HoofdcategorieGerecht.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = Categorie,
        subregister_naam = "categorie",
        bestandsmap = Path("gegevens/product"),
        bestandsnaam = "categorie",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Categorie.naar_json,
        ontcijfer_functie_objecten = Categorie.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = CategorieGerecht,
        subregister_naam = "categorie_gerecht",
        bestandsmap = Path("gegevens/gerecht"),
        bestandsnaam = "categorie_gerecht",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = CategorieGerecht.naar_json,
        ontcijfer_functie_objecten = CategorieGerecht.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = Ingrediënt,
        subregister_naam = "ingrediënt",
        bestandsmap = Path("gegevens/product"),
        bestandsnaam = "ingrediënt",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Ingrediënt.naar_json,
        ontcijfer_functie_objecten = Ingrediënt.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = Merk,
        subregister_naam = "merk",
        bestandsmap = Path("gegevens/product"),
        bestandsnaam = "merk",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Merk.naar_json,
        ontcijfer_functie_objecten = Merk.van_json,
        )
    
    Register.registreer_type(
        geregistreerd_type = Product,
        subregister_naam = "product",
        bestandsmap = Path("gegevens/product"),
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
    
    Register.registreer_type(
        geregistreerd_type = Gerecht,
        subregister_naam = "gerecht",
        bestandsmap = Path("gegevens/gerecht"),
        bestandsnaam = "gerecht",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Gerecht.naar_json,
        ontcijfer_functie_objecten = Gerecht.van_json,
        vercijfer_functie_subobjecten = [
            Vercijferaar(
                class_naam = "Variant",
                vercijfer_functie_naam = "naar_json",
                ),
            ],
        ontcijfer_functie_subobjecten = [
            Ontcijferaar(
                velden = frozenset((
                    "variant_naam",
                    "toevoeging",
                    "aanpassing",
                    "verwijdering",
                    "porties",
                    )),
                ontcijfer_functie = Variant.van_json,
                ),
            ],
        )
    
    Register.registreer_type(
        geregistreerd_type = Dag,
        subregister_naam = "dag",
        registratie_methode = "property",
        opslaan = "instantie",
        bestandsmap = Path("gegevens/dagen"),
        bestandsnaam = "dag",
        vercijfer_methode = "functie",
        vercijfer_functie_objecten = Dag.naar_json,
        ontcijfer_functie_objecten = Dag.van_json,
        )
    
    if openen: Register.openen()