from grienetsiis import invoer_kiezen, STOP


from ._version import __version__
from .categorie import Hoofdcategorieën, Categorieën, HoofdcategorieënGerecht, CategorieënGerecht
from .dag import Dag
from .gerecht import Gerechten
from .ingredient import Ingrediënten
from .product import Merken, Producten


def welkomstscherm():
    
    print(f"""
`7MMM.     ,MMF'                                  
  MMMb    dPMM                                    
  M YM   ,M MM   ,6"Yb.  ,p6"bo `7Mb,od8 ,pW"Wq.  
  M  Mb  M' MM  8)   MM 6M'  OO   MM' "'6W'   `Wb 
  M  YM.P'  MM   ,pm9MM 8M        MM    8M     M8 
  M  `YM'   MM  8M   MM YM.    ,  MM    YA.   ,A9 
.JML. `'  .JMML.`Moo9^Yo.YMbmd' .JMML.   `Ybmd9'  
                                     versie {__version__}""")

def uitvoeren():
    
    welkomstscherm()
    
    while True:
        
        opdracht = invoer_kiezen(
            "HOOFDMENU",
            [
                "dag invullen",
                "gegevens bewerken",
                ],
            stoppen = True,
            kies_een = False,
            terug_naar = "AFSLUITEN",
            )
        
        if opdracht is STOP:
            break
        
        elif opdracht == "dag invullen":
            
            terug_naar = "MENU DAG"
            
            while True:
                
                opdracht_dag = invoer_kiezen(
                    "MENU DAG",
                    [
                        "vandaag",
                        "gisteren",
                        "eergisteren",
                        "morgen",
                        "overmorgen",
                        "aangepast",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = "HOOFDMENU",
                    )
                
                if opdracht_dag is STOP:
                    break
                
                dag = Dag.openen(opdracht_dag)
                dag.opdracht(terug_naar)
                dag.opslaan()
        
        elif opdracht == "gegevens bewerken":
            
            terug_naar = "MENU GEGEVENS"
            
            while True:
                
                opdracht_gegevens = invoer_kiezen(
                    "MENU GEGEVENS",
                    [
                        "producten",
                        "ingrediënten",
                        "gerechten",
                        "merken",
                        "hoofdcategorieën producten",
                        "categorieën producten",
                        "hoofdcategorieën gerechten",
                        "categorieën gerechten",
                        "kopie gegevens",
                        ],
                    stoppen = True,
                    kies_een = False,
                    terug_naar = "HOOFDMENU",
                    )
                
                if opdracht_gegevens is STOP:
                    break
                
                elif opdracht_gegevens == "hoofdcategorieën producten":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorieën.opdracht(terug_naar)
                    hoofdcategorieën.opslaan()
                
                elif opdracht_gegevens == "categorieën producten":
                    
                    categorieën = Categorieën.openen()
                    categorieën.opdracht(terug_naar)
                    categorieën.opslaan()
                
                elif opdracht_gegevens == "ingrediënten":
                    
                    ingrediënten = Ingrediënten.openen()
                    ingrediënten.opdracht(terug_naar)
                    ingrediënten.opslaan()
                
                elif opdracht_gegevens == "producten":
                    
                    producten = Producten.openen()
                    producten.opdracht(terug_naar)
                    producten.opslaan()
                
                elif opdracht_gegevens == "merken":
                    
                    merken = Merken.openen()
                    merken.opdracht(terug_naar)
                    merken.opslaan()
                
                elif opdracht_gegevens == "hoofdcategorieën gerechten":
                    
                    hoofdcategorieën_gerecht = HoofdcategorieënGerecht.openen()
                    hoofdcategorieën_gerecht.opdracht(terug_naar)
                    hoofdcategorieën_gerecht.opslaan()
                
                elif opdracht_gegevens == "categorieën gerechten":
                    
                    categorieën_gerecht = CategorieënGerecht.openen()
                    categorieën_gerecht.opdracht(terug_naar)
                    categorieën_gerecht.opslaan()
                
                elif opdracht_gegevens == "gerechten":
                    
                    gerechten = Gerechten.openen()
                    gerechten.opdracht(terug_naar)
                    gerechten.opslaan()
                
                elif opdracht_gegevens == "kopie gegevens":
                    
                    hoofdcategorieën = Hoofdcategorieën.openen()
                    hoofdcategorieën.kopie_opslaan()
                    categorieën = Categorieën.openen()
                    categorieën.kopie_opslaan()
                    ingrediënten = Ingrediënten.openen()
                    ingrediënten.kopie_opslaan()
                    producten = Producten.openen()
                    producten.kopie_opslaan()
                    merken = Merken.openen()
                    merken.kopie_opslaan()
                    hoofdcategorieën_gerecht = HoofdcategorieënGerecht.openen()
                    hoofdcategorieën_gerecht.kopie_opslaan()
                    categorieën_gerecht = CategorieënGerecht.openen()
                    categorieën_gerecht.kopie_opslaan()
                    gerechten = Gerechten.openen()
                    gerechten.kopie_opslaan()
                    
                    print(f"\nkopie van gegevens gemaakt")
    
    print("tot ziens")