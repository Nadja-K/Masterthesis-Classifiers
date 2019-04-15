## False negatives (für threshold 0.5)
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------ 
0.0                            bodense                        120 lz                         Bodensee                       LZ_120  
0.08333333333333333            Onychophoren                   Stummelfüßer                   Onychophoren                   Stummelfüßer 
0.18181818181818182            stammsitz                      burg habsburg                  Stammsitz                      Habsburg_(Burg) 
0.2222222222222222             octavian                       augustus                       Octavian                       Augustus  
0.25                           US Armee                       Streitkräfte Vereinigten Staaten US-Armee                       Streitkräfte_der_Vereinigten_Staaten
0.27586206896551724            zweitstimm                     bundestagswahlrecht            Zweitstimmen                   Bundestagswahlrecht    
0.3076923076923077             repulsion                      ekel                           Repulsion                      Ekel  
0.3333333333333333             klimawandel                    global erwarm                  Klimawandel                    Globale_Erwärmung
0.375                          135 kc tankflugzeug            135 boeing kc                  KC-135-Tankflugzeug            Boeing_KC-135   
0.4444444444444444             Erderwärmungsgeschwindigkeit   Erwärmung Globale              Erderwärmungsgeschwindigkeit   Globale_Erwärmung     
0.4444444444444444             175 paragraph                  175 §                          Paragraph 175                  §_175
0.4666666666666667             135 kc stratotank              135 boeing kc                  KC-135 Stratotanker            Boeing_KC-135 
0.47058823529411764            tulpenzwiebelspekulation       tulpenmani                     Tulpenzwiebelspekulation       Tulpenmanie     
0.48                           Norden                         Norden Ostfriesland            Norden                         Norden_(Ostfriesland)    
```

## False positives  (für threshold 0.5)
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------ 
0.5                            theophyllin                    edessa theophilos              Theophyllin                    Theophilos_von_Edessa 
0.5                            malaria                        moalv                          Malaria                        Moälven 
0.5365853658536586             kronach rosenberg              burggrafschaft friedberg       Rosenberg in Kronach           Burggrafschaft_Friedberg  
0.5384615384615384             klost muri                     klost oelinghaus               Klöster Muri                   Kloster_Oelinghausen  
0.5925925925925926             Neandertaler                   Wandermenagerie                Neandertaler                   Wandermenagerie 
0.64                           philosoph lehr                 phyllosphar                    philosophische Lehre           Phyllosphäre 
0.6666666666666666             segl                           sl                             Seglern                        Schloss_Ludwigslust 
0.72                           schonhaus                      schopenhauerhaus               Schönhauser Allee              Schopenhauerhaus 
...
1.0                            blut                           blut                           Blüten                         Blut        
1.0                            go                             go                             Go                             Oecusse_(Gemeinde)   
```

## True positives (für threshold 0.5)
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------ 
0.56                           Senatoren                      Senat Frankreich               Senatoren                      Senat_(Frankreich) 
0.6153846153846154             Hochofenemissionen             Hochofen                       Hochofenemissionen             Hochofen  
0.75                           Brauer                         Brauer Max                     Brauer                         Max_Brauer
0.7647058823529411             harbig rudolf stadion          harbig rudolf                  Rudolf-Harbig-Stadion          Rudolf_Harbig
0.7647058823529411             Französische Senat             Frankreich Senat               Französische Senat             Senat_(Frankreich)      
0.7878787878787878             harbig rudolf strass           harbig rudolf                  Rudolf-Harbig-Straße           Rudolf_Harbig
0.8                            arm heinrich thema             arm heinrich                   Armer-Heinrich-Thema           Der_arme_Heinrich  
0.8                            god of seri war                god of war                     God-of-War-Serie               God_of_War
0.8484848484848485             selt wasserschlauch            wasserschlauch                 Seltene Wasserschlauch         Wasserschläuche 
0.9032258064516129             wasserschlauchart              wasserschlauch                 Wasserschlaucharten            Wasserschläuche 
1.0                            fragil syndrom x               fragil syndrom x               Fragiles-X-Syndrome            Fragiles-X-Syndrom   
1.0                            god of                         god of                         God of War                     God_of_War
1.0                            hochof                         hochof                         Hochöfen                       Hochofen
1.0                            hochof                         hochof                         Hochofens                      Hochofen 
```

## True negatives (für threshold 0.5)
```
Similarity                     Refactored mention             Refactored entity              Original mention               Original entity               
------------------------------------------------------------------------------------------------------------------------------------------------------ 
0.2                            siebdruck                      enzyklopadi                    Siebdruck                      Enzyklopädie 
0.20689655172413793            Adams John                     Friedrich Nietzsche            John Adams                     Friedrich_Nietzsche 
0.25                           pavian                         friedrich nietzsch             Pavianen                       Friedrich_Nietzsche  
0.2777777777777778             intercityexperimental          galilei galileo                InterCityExperimental          Galileo_Galilei
0.32                           fletch klass                   erwarm global                  Fletcher-Klasse                Globale_Erwärmung
0.34285714285714286            de enzinas francisco           galilei galileo                Francisco de Enzinas           Galileo_Galilei 
0.34782608695652173            stufentheori                   enzyklopadi                    Stufentheorie                  Enzyklopädie 
0.375                          senat                          enzyklopadi                    Senat                          Enzyklopädie 
0.42857142857142855            margaret valois                erwarm global                  Margarete von Valois           Globale_Erwärmung      
0.4375                         First Nations                  Friedrich Nietzsche            First Nations                  Friedrich_Nietzsche
0.45714285714285713            wien zentralfriedhof           galilei galileo                Wiener Zentralfriedhof         Galileo_Galilei   
```

-----------------------------------------

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
