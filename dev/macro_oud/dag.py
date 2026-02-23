elif opdracht == "toevoegen gerechten":
    
    gerechten = Gerechten.openen()
    
    while True:
        
        gerecht_uuid, versie_uuid = gerechten.kiezen_gerecht_versie(
            terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
            )
        
        if gerecht_uuid is STOP:
            break
        
        if versie_uuid is STOP:
            continue
        
        eenheid = Eenheid("portie")
        
        porties = invoer_validatie(
            f"hoeveel {eenheid.meervoud}",
            float,
            )
        
        hoeveelheid = Hoeveelheid(porties, eenheid)
        
        if gerecht_uuid in self.gerechten.keys():
            if versie_uuid in self.gerechten[gerecht_uuid]:
                self.gerechten[gerecht_uuid][versie_uuid].waarde += porties
            else:
                self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid
        else:
            self.gerechten[gerecht_uuid] = {}
            self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid
        
        versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
        print(f"\n>>> {hoeveelheid} toegevoegd van {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")
        
        break

elif opdracht == "verwijderen gerechten":
    
    if len(self.gerechten) == 0:
        print("\n>>> geen gerechten aanwezig om te verwijderen")
        continue
    
    gerechten = Gerechten.openen()
    
    kies_optie = invoer_kiezen(
        "een gerecht en versie om te verwijderen",
        {f"{f"{hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")": (gerecht_uuid, versie_uuid) for gerecht_uuid, versie_dict in self.gerechten.items() for versie_uuid, hoeveelheid in versie_dict.items() if (versie_naam := "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"])},
        stoppen = True,
        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
        )
    
    if kies_optie is STOP:
        continue
    
    gerecht_uuid, versie_uuid = kies_optie
    
    versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
    print(f"\n>>> versie \"{versie_naam}\" van {gerechten[gerecht_uuid]} verwijderd")
    
    del self.gerechten[gerecht_uuid][versie_uuid]

elif opdracht == "aanpassen porties gerechten":
    
    if len(self.gerechten) == 0:
        print("\n>>> geen gerechten aanwezig om het aantal porties van aan te passen")
        continue
    
    gerechten = Gerechten.openen()
    
    kies_optie = invoer_kiezen(
        "een gerecht en versie om aan te passen",
        {f"{f"{hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")": (gerecht_uuid, versie_uuid) for gerecht_uuid, versie_dict in self.gerechten.items() for versie_uuid, hoeveelheid in versie_dict.items() if (versie_naam := "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"])},
        stoppen = True,
        terug_naar = f"MENU DAG {f"{self.dag}".upper()}",
        )
    
    if kies_optie is STOP:
        continue
    
    gerecht_uuid, versie_uuid = kies_optie
    
    eenheid = Eenheid("portie")
        
    porties = invoer_validatie(
        f"hoeveel {eenheid.meervoud}",
        float,
        )
    
    hoeveelheid = Hoeveelheid(porties, eenheid)
    
    self.gerechten[gerecht_uuid][versie_uuid] = hoeveelheid

elif opdracht == "weergeef gerechten":
    
    if len(self.gerechten) == 0:
        print(f"\n>>> geen gerechten aanwezig om te weergeven")
        continue
    
    gerechten = Gerechten.openen()
    
    print(f"\n     HOEVEELHEID GERECHT")
    
    for gerecht_uuid, versie_dict in self.gerechten.items():
        for versie_uuid, versie_hoeveelheid in versie_dict.items():
            
            versie_naam = "standaard" if versie_uuid == "standaard" else gerechten[gerecht_uuid].versies[versie_uuid]["versie_naam"]
            
            print(f"     {f"{versie_hoeveelheid}":<11} {gerechten[gerecht_uuid]} (versie \"{versie_naam}\")")