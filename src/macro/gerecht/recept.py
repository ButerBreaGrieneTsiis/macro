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


    # def nieuw_recept(
    #     self,
    #     ) -> None | Stop:
        
    #     print(f"\n>>> aanmaken nieuwe recept voor {self}")
        
    #     benodigdheden = []
    #     stappen = []
        
    #     if invoer_kiezen(
    #         "toevoegen benodigdheden",
    #         {
    #             "ja": True,
    #             "nee": False,
    #             },
    #         kies_een = False,
    #         ):
            
    #         while True:
                
    #             if len(benodigdheden) > 0:
    #                 print("\nbenodigdheden")
    #                 aantal_tekens = len(f"{len(benodigdheden)}") + 1
    #                 [print(f"     {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(benodigdheden, 1)]
    #                 print("\nvoer \"klaar\" in om benodigdheden af te ronden")
                
    #             benodigdheid = invoer_validatie(
    #                 "benodigdheid",
    #                 str,
    #                 kleine_letters = True,
    #                 uitsluiten_leeg = True,
    #                 )
                
    #             if benodigdheid == "klaar":
    #                 break
                
    #             benodigdheden.append(benodigdheid)
        
    #     print("\ntoevoegen stappen van het recept")
        
    #     while True:
            
    #         if len(stappen) > 0:
    #             print("\ntoegevoegde stappen")
    #             aantal_tekens = len(f"{len(stappen)}") + 1
    #             [print(f"     {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(stappen, 1)]
    #             print("\nvoer \"klaar\" in om stappen af te ronden")
            
    #         stap = invoer_validatie(
    #             f"stap {len(stappen)+1}",
    #             str,
    #             kleine_letters = True,
    #             uitsluiten_leeg = True,
    #             )
            
    #         if stap == "klaar":
    #             break
            
    #         stappen.append(stap)
        
    #     if len(stappen) == 0:
    #         return STOP
    #     else:
    #         self.recept = {
    #             "benodigdheden": benodigdheden,
    #             "stappen": stappen,
    #             }


    #         elif kies_optie == "weergeef recept":
                
    #             if not bool(self.recept):
    #                 print(f"\n>>> er is geen recept gedefinieerd voor {self}")
    #                 continue
                
    #             if len(self.recept["benodigdheden"]) > 0:
    #                 print("\n     benodigdheden")
    #                 aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
    #                 [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                
    #             print("\n     stappen")
    #             aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
    #             [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
    
    
    # elif kies_optie == "bewerk recept":
                
    #             if not bool(self.recept):
    #                 print(f"\n>>> er is geen recept gedefinieerd voor {self}")
                    
    #                 if self.nieuw_recept() is STOP:
    #                     continue
                    
    #                 continue
                
    #             while True:
                    
    #                 if len(self.recept["benodigdheden"]) > 0:
    #                     print("\n     benodigdheden")
    #                     aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
    #                     [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                
    #                 print("\n     stappen")
    #                 aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
    #                 [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
                
    #                 kies_optie = invoer_kiezen(
    #                     f"MENU {f"{self}".upper()} BEWERK RECEPT",
    #                     [
    #                         "bewerk benodigdheden",
    #                         "bewerk stappen",
    #                         ],
    #                     kies_een = False,
    #                     stoppen = True,
    #                     terug_naar = "BEWERK RECEPT KLAAR",
    #                     )
                    
    #                 if kies_optie is STOP:
    #                     break
                    
    #                 elif kies_optie == "bewerk benodigdheden":
                        
    #                     while True:
                            
    #                         if len(self.recept["benodigdheden"]) > 0:
    #                             print("\n     benodigdheden")
    #                             aantal_tekens = len(f"{len(self.recept["benodigdheden"])}") + 1
    #                             [print(f"       {f"{ibenodigdheid}.":>{aantal_tekens}} {benodigdheid}") for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"], 1)]
                            
    #                         kies_optie_benodigdheden = invoer_kiezen(
    #                             f"MENU {f"{self}".upper()} BEWERK RECEPT BENODIGDHEDEN",
    #                             [
    #                                 "toevoegen benodigdheid",
    #                                 "verwijderen benodigdheid",
    #                                 "aanpassen benodigdheid",
    #                                 ],
    #                             kies_een = False,
    #                             stoppen = True,
    #                             terug_naar = "BEWERK RECEPT BENODIGHEDEN KLAAR",
    #                             )
                            
    #                         if kies_optie_benodigdheden is STOP:
    #                             break
                            
    #                         elif kies_optie_benodigdheden == "toevoegen benodigdheid":
                                
    #                             benodigdheid = invoer_validatie(
    #                                 "benodigdheid",
    #                                 str,
    #                                 kleine_letters = True,
    #                                 uitsluiten_leeg = True,
    #                                 )
                                
    #                             if benodigdheid == "klaar":
    #                                 continue
                                
    #                             self.recept["benodigdheden"].append(benodigdheid)
                                
    #                             print(f"\n>>> benodigdheid \"{benodigdheid}\" toegevoegd van benodigdheden")
                            
    #                         elif kies_optie_benodigdheden == "verwijderen benodigdheid":
                                
    #                             ibenodigdheid = invoer_kiezen(
    #                                 "benodigdheid om te verwijderen",
    #                                 {f"{benodigdheid}": ibenodigdheid for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"])},
    #                                 stoppen = True,
    #                                 terug_naar = "VERWIJDEREN BENODIGHEDEN KLAAR",
    #                                 )
                                
    #                             if ibenodigdheid is STOP:
    #                                 continue
                                
    #                             print(f"\n>>> benodigdheid \"{self.recept["benodigdheden"][ibenodigdheid]}\" verwijderd van benodigdheden")
                                
    #                             del self.recept["benodigdheden"][ibenodigdheid]
                            
    #                         elif kies_optie_benodigdheden == "aanpassen benodigdheid":
                                
    #                             ibenodigdheid = invoer_kiezen(
    #                                 "benodigdheid om aan te passen",
    #                                 {f"{benodigdheid}": ibenodigdheid for ibenodigdheid, benodigdheid in enumerate(self.recept["benodigdheden"])},
    #                                 stoppen = True,
    #                                 terug_naar = "AANPASSEN BENODIGHEDEN KLAAR",
    #                                 )
                                
    #                             if ibenodigdheid is STOP:
    #                                 continue
                                
    #                             benodigdheid = invoer_validatie(
    #                                 "benodigdheid",
    #                                 str,
    #                                 kleine_letters = True,
    #                                 uitsluiten_leeg = True,
    #                                 )
                                
    #                             if benodigdheid == "klaar":
    #                                 continue
                                
    #                             print(f"\n>>> benodigdheid \"{self.recept["benodigdheden"][ibenodigdheid]}\" aangepast naar \"{benodigdheid}\"")
                                
    #                             self.recept["benodigdheden"][ibenodigdheid] = benodigdheid
                    
    #                 elif kies_optie == "bewerk stappen":
                        
    #                     while True:
                            
    #                         print("\n     stappen")
    #                         aantal_tekens = len(f"{len(self.recept["stappen"])}") + 1
    #                         [print(f"       {f"{istap}.":>{aantal_tekens}} {stap}") for istap, stap in enumerate(self.recept["stappen"], 1)]
                            
    #                         kies_optie_stappen = invoer_kiezen(
    #                             f"MENU {f"{self}".upper()} BEWERK RECEPT STAPPEN",
    #                             [
    #                                 "toevoegen stap",
    #                                 "verwijderen stap",
    #                                 "aanpassen stap",
    #                                 ],
    #                             kies_een = False,
    #                             stoppen = True,
    #                             terug_naar = "BEWERK RECEPT STAPPEN KLAAR",
    #                             )
                            
    #                         if kies_optie_stappen is STOP:
    #                             break
                            
    #                         elif kies_optie_stappen == "toevoegen stap":
                                
    #                             stap = invoer_validatie(
    #                                 "stap",
    #                                 str,
    #                                 kleine_letters = True,
    #                                 uitsluiten_leeg = True,
    #                                 )
                                
    #                             if stap == "klaar":
    #                                 continue
                                
    #                             istap = invoer_kiezen(
    #                                 "plek waar de stap toegevoegd moet worden",
    #                                 {
    #                                     f"voor stap \"{stap}\"": istap for istap, stap in enumerate(self.recept["stappen"])
    #                                 } | {
    #                                     "laatste stap": len(self.recept["stappen"])
    #                                     },
    #                                 stoppen = True,
    #                                 terug_naar = "TOEVOEGEN STAPPEN KLAAR",
    #                                 )
                                
    #                             if istap is STOP:
    #                                 continue
                                
    #                             print(f"\n>>> stap \"{stap}\" toegevoegd van stappen")
                                
    #                             self.recept["stappen"].insert(istap, stap)
                            
    #                         elif kies_optie_stappen == "verwijderen stap":
                                
    #                             istap = invoer_kiezen(
    #                                 "stap om te verwijderen",
    #                                 {f"{stap}": istap for istap, stap in enumerate(self.recept["stappen"])},
    #                                 stoppen = True,
    #                                 terug_naar = "VERWIJDEREN STAPPEN KLAAR",
    #                                 )
                                
    #                             if istap is STOP:
    #                                 continue
                                
    #                             print(f"\n>>> stap \"{self.recept["stappen"][istap]}\" verwijderd van stappen")
                                
    #                             del self.recept["stappen"][istap]
                            
    #                         elif kies_optie_stappen == "aanpassen stap":
                                
    #                             istap = invoer_kiezen(
    #                                 "stap om aan te passen",
    #                                 {f"{stap}": istap for istap, stap in enumerate(self.recept["stappen"])},
    #                                 stoppen = True,
    #                                 terug_naar = "AANPASSEN STAPPEN KLAAR",
    #                                 )
                                
    #                             if istap is STOP:
    #                                 continue
                                
    #                             stap = invoer_validatie(
    #                                 "stap",
    #                                 str,
    #                                 kleine_letters = True,
    #                                 uitsluiten_leeg = True,
    #                                 )
                                
    #                             if stap == "klaar":
    #                                 continue
                                
    #                             print(f"\n>>> stap \"{self.recept["stappen"][istap]}\" aangepast naar \"{stap}\"")
                                
    #                             self.recept["stappen"][istap] = stap