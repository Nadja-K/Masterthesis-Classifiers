## Statistiken
* TP: 3483
* Total: 5050
* 68.97% entities were classified correctly.

## Beispiele bei denen die Regeln geholfen haben
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------ 
0.5333333333333333             all gurtel van                 strahlungsgurtel               Van-Allen-Gürtel               Strahlungsgürtel              
0.5833333333333334             sakular                        astronomi sakular              säkular                        Säkular_(Astronomie)          
0.6666666666666666             fleck                          sternfleck                     Flecken                        Sternfleck                    
0.6896551724137931             stellar objekt                 astronom objekt                stellaren Objekten             Astronomisches_Objekt         
0.7222222222222222             grand hypothes tack            grand modell tack              Hypothese des Grand Tack       Grand-Tack-Modell             
0.7222222222222222             dunkl zeitalt                  dunkl kosmologi zeitalt        Dunklen Zeitalter              Dunkles_Zeitalter_(Kosmologie)
0.75                           fusion                         kernfusion                     Fusion                         Kernfusion                    
0.7567567567567568             Titius Bode „Gesetz“           Titius Bode Reihe              Titius-Bode-„Gesetz“           Titius-Bode-Reihe             
0.8125                         horizontalast stern            horizontalast                  Horizontalast-Sterne           Horizontalast                 
0.8181818181818182             astrophysikal                  astrophys                      astrophysikalische             Astrophysik                   
0.8181818181818182             astrophysikal                  astrophys                      astrophysikalischen            Astrophysik                   
0.8484848484848485             common envelop phas            common envelop                 Common-Envelope-Phase          Common_Envelope               
0.875                          quadrat                        quadratur                      quadratische                   Quadratur                     
0.9655172413793104             Neutronensterne                Neutronenstern                 Neutronensterne                Neutronenstern                
0.9655172413793104             Neutronensterns                Neutronenstern                 Neutronensterns                Neutronenstern                                
...
1.0                            deep extrem field hubbl        deep extrem field hubbl        Hubble Extreme Deep Field      Hubble_Extreme_Deep_Field     
1.0                            mittelpunktsgleich             mittelpunktsgleich             Mittelpunktsgleichungen        Mittelpunktsgleichung         
1.0                            bi ellipt transf               bi ellipt transf               bi-elliptischer Transfer       Bi-elliptischer_Transfer      
1.0                            strahlungsgurtel               strahlungsgurtel               Strahlungsgürtels              Strahlungsgürtel              
1.0                            dark energy survey             dark energy survey             Dark Energy Survey             Dark_Energy_Survey                                 
```

## Beispiele mit niedriger Similarity
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------
0.0                            aufbau                         kosmologi                      Aufbau                         Kosmologie
0.09090909090909091            schwerefeld                    gravitation                    Schwerefeld                    Gravitation                   
0.23529411764705882            Himmelskörper                  Astronomisches Objekt          Himmelskörper                  Astronomisches_Objekt         
0.3076923076923077             anziehungskraft                gravitation                    Anziehungskraft                Gravitation                   
0.3333333333333333             am himmel                      astronom objekt                am Himmel                      Astronomisches_Objekt         
0.41379310344827586            objekt weltall                 astronom objekt                Objekte im Weltall             Astronomisches_Objekt         
0.5714285714285714             objekt                         astronom objekt                Objekt                         Astronomisches_Objekt         
```

## Beispiele für 'wörter tauschen'
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------
0.4444444444444444             Bahnknoten                     Astronomie Knoten              Bahnknoten                     Knoten_(Astronomie)           
0.5789473684210527             radioemission sonn             radioastronomi solar           Radioemissionen der Sonne      Solare_Radioastronomie        
0.6285714285714286             Gezeiten Vorhersage            Gezeitenrechnung               Vorhersage von Gezeiten        Gezeitenrechnung              
0.7368421052631579             bzw fruhling herbstpunkt       fruhlingspunkt                 Frühlings- bzw. Herbstpunkts   Frühlingspunkt         
0.7804878048780488             Gezeiten Vorausberechnung      Gezeitenrechnung               Vorausberechnung der Gezeiten  Gezeitenrechnung              
0.972972972972973              inflation kosmolog             inflation kosmologi            kosmologischen Inflation       Inflation_(Kosmologie)        
```

##Abkürzungen
* Erster Chunk: falsche Abkürzungen
* Zweiter Chunk: richtige Abkürzungen
* Dritter Chunk: alles dazwischen

Anmerkungen: die Wörter mit den falschen Abkürzungen haben tatsächlich auch i.d.R. niedrige similarity Values, Wörter 
mit korrekten Abkürzungen haben i.d.R. höhere similarity Values.
Insgesamt gibt es aber nicht allzu viele Fälle, in denen tatsächlich eine Abkürzung vorkommt. 
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------
0.2857142857142857             e                              eklipt                         Erdbahnebene                   Ekliptik                      
0.2857142857142857             a                              erdnah                         Apogäum-                       Erdnähe                       
0.3076923076923077             ausgedehnt                     edu                            ausgedehnt                     Expansion_des_Universums      
0.4                            jet                            aj                             Jet                            Jet_(Astronomie)              
0.4                            jet                            aj                             Jet                            Jet_(Astronomie)              
0.4                            imf                            mu                             IMF                            Ursprüngliche_Massenfunktion  
0.4444444444444444             apogaum                        aa                             Apogäum                        Apsis_(Astronomie)            
0.4444444444444444             prograd                        rr                             prograd                        Rechtläufig_und_rückläufig    
0.5                            rot                            r                              Rot-                           Rotverschiebung               
...
0.5454545454545454             ii poss                        opss                           POSS-II                        Palomar_Observatory_Sky_Survey
0.5714285714285714             λcdm                           clm                            ΛCDM                           Lambda-CDM-Modell             
0.625                          flrw metrik                    flrwm                          FLRW Metriken                  Friedmann-Lemaître-Robertson-Walker-Metrik
0.6666666666666666             sorc                           srace                          SORCE                          Solar_Radiation_and_Climate_Experiment
0.8571428571428571             ads                            adrs                           AdS                            Anti-de-Sitter-Raum           
...
0.5                            l1                             lp                             L1                             Lagrange-Punkte               
0.6666666666666666             s                              ps                             s-                             S-Prozess                     
```
