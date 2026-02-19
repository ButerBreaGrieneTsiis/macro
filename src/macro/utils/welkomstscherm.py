from macro._version import __version__


def welkomstscherm():
    
    welkomst_tekst = f"""
`7MMM.     ,MMF'                                  
  MMMb    dPMM                                    
  M YM   ,M MM   ,6"Yb.  ,p6"bo `7Mb,od8 ,pW"Wq.  
  M  Mb  M' MM  8)   MM 6M'  OO   MM' "'6W'   `Wb 
  M  YM.P'  MM   ,pm9MM 8M        MM    8M     M8 
  M  `YM'   MM  8M   MM YM.    ,  MM    YA.   ,A9 
.JML. `'  .JMML.`Moo9^Yo.YMbmd' .JMML.   `Ybmd9'  
{f"versie {__version__}":>50}"""
    
    print(welkomst_tekst)