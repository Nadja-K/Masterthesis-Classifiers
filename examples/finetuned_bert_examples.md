## (leftover) false negatives
-> Note: only FN that were FN in the original Bert

### #Mixed small

#### Mixed large

#### Geraete small

#### Geraete large

#### Excellent


## Improvements over the unfinetuned Bert model
-> Note: only TP that were FN in the original Bert

### #Mixed small

#### Mixed large

#### Geraete small

#### Geraete large

#### Excellent
```
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
TP         |Abrams-Kampfpanzer                                 |M1_Abrams                                          |Knapp 8000 schwere Abrams-Kampfpanzer bilden sowohl bei Army als auch beim Marine Corps das Rückgrat der Panzerbrigaden, die Ursprungsbeschaffung des relativ schweren Bradley-Schützenpanzers ist noch nicht abgeschlossen und wird durch den veralteten M113 ergänzt.
TP         |achten Kinofilm                                    |Star_Trek:_Der_erste_Kontakt                       |Darüber hinaus hatte er als Holodeck-Charakter einen Cameo-Auftritt im achten Kinofilm .                                                                                                                                                                        
TP         |Alkangehalt                                        |Alkane                                             |Die Spülgasteere zeichnen sich durch einen hohen Alkangehalt (Paraffine) aus.                                                                                                                                                                                   
TP         |anzeigepflichtigen Tierseuchen                     |Tierseuche                                         |Bei Tieren kommen aber auch tödliche Erkrankungen mit Beteiligung des Zentralnervensystems vor, wie die Enzephalomyelitiden der Pferde, deren Krankheitsbilder zu den anzeigepflichtigen Tierseuchen gehören.                                                   
TP         |Erreger der Cholera                                |Vibrio_cholerae                                    |Diese Bakterien bezeichnete er als Erreger der Cholera, obwohl ihm nach seinen eigenen Maßstäben der Nachweis nicht gelungen war: Er hatte vergeblich versucht, Tiere mit der Krankheit zu infizieren.                                                          
TP         |frühmenschliche                                    |Stammesgeschichte_des_Menschen                     |Es ist an zahlreichen Fundstellen des Indischen Subkontinentes nachgewiesen, so u.a. aus den Ablagerungen des Flusses Narmada, wo auch bedeutende frühmenschliche Fossilien entdeckt wurden.                                                                    
TP         |gescheiterten Ballonfahrt                          |Andrées_Polarexpedition_von_1897                   |Knut Hjalmar Ferdinand Frænkel (* 14. Februar 1870 in Karlstad; † Oktober 1897 auf Kvitøya, Svalbard) war ein schwedischer Ingenieur und Entdeckungsreisender, der an der gescheiterten Ballonfahrt von Salomon August Andrée teilnahm.                         
TP         |gescheiterten Expedition                           |Andrées_Polarexpedition_von_1897                   |Bekannt wurde dieses Giles-Land (oder Kvitøya, wie es heute heißt) durch die Entdeckung der dort endgültig gescheiterten Expedition von Salomon August Andrée, der 1897 von Virgohamna auf Danskøya aus zusammen mit zwei Begleitern mit dem Wasserstoffballon Örnen nach Norden fuhr.
TP         |Geschichte des Tennis                              |Geschichte_des_Tennis                              |Eine ausführliche Beschreibung seiner Entstehung findet sich in der Geschichte des Tennis.                                                                                                                                                                      
TP         |Herzdruckmassage                                   |Herz-Lungen-Wiederbelebung                         |Ein Mensch, der sich in diesem Zustand befindet, kann unter Umständen durch Herzdruckmassage und Beatmung wiederbelebt (reanimiert) werden.                                                                                                                     
TP         |Herzdruckmassage                                   |Herz-Lungen-Wiederbelebung                         |Um ein Herunterfallen oder -rutschen der Folie zu verhindern (z.b. bei im Wechsel mit der Atemspende durchgeführter Herzdruckmassage) werden Gummizüge links und rechts am Rand der Folie über die Ohren des Patienten gezogen (im Bild rechts ist nur der linke Gummizug zu sehen).
TP         |Krustenflechten                                    |Flechte                                            |Die Sandsteinfelsen selbst weisen einen leichten Bewuchs mit Krustenflechten auf.                                                                                                                                                                               
TP         |Menschwerdung                                      |Stammesgeschichte_des_Menschen                     |Diese Hochrechnung beginnt mit zwei Menschen im Jahr 50.000 v. Chr., während man heute annimmt, dass die Menschwerdung bereits vor 200.000 Jahren oder früher in die Entstehung des modernen Menschen gemündet hat.                                             
TP         |Perserfeldzug                                      |Römisch-Persische_Kriege                           |Pupienus plante offenbar einen Perserfeldzug, während Balbinus gegen die Germanen ziehen wollte.                                                                                                                                                                
TP         |Pyramide seines Vorgängers                         |Sahure-Pyramide                                    |Neferirkare baute seine Pyramide etwa 200 m südwestlich der Pyramide seines Vorgängers und Vaters Sahure als zweite Pyramide der Nekropole von Abusir.                                                                                                          
TP         |Rhinozeroshörnern                                  |Nashörner                                          |So entstand 1955 die Kopie und das Bild Peintre paranoïaque-critique de la Dentellière de Vermeer (deutsch: Paranoisch-kritisches Gemälde der Spitzenklöpplerin von Vermeer), in dem er das Gemälde in Form von Rhinozeroshörnern explodieren lässt.            
TP         |Schischyphusch                                     |Schischyphusch_oder_Der_Kellner_meines_Onkels      |Häufig steigert Borchert die Intensität seiner Sätze durch das Stilmittel der Klimax, gelegentlich schwächt er sie durch die Antiklimax ab, so etwa in der unterschiedlichen Charakterisierung der beiden Hauptfiguren in Schischyphusch: „Mein Onkel, Säufer, Sänger, Gewaltmensch, Witzereißer, Zotenflüsterer, Verführer, kurzzungiger sprühender, sprudelnder, spuckender Anbeter von Frauen und Kognak.“ Dagegen der Kellner: „Tausendmal im Gartenlokal an jedem Tisch einen Zentimeter in sich hineingekrochen, geduckt, geschrumpft.“ Zur Hervorhebung setzt Borchert Alliterationen ein.
TP         |Selbstporträt mit Palette                          |Selbstporträt_mit_Palette_(Manet)                  |Zu den ersten Erwerbungen gehörten weiterhin Gemälde des Impressionismus wie das Selbstporträt mit Palette von Édouard Manet, ein 1906 entstandenes Seerosenbild von Claude Monet und eine Skulptur einer Balletttänzerin von Edgar Degas.                      

```


## Deteriorations over the unfinetuned Bert model
-> Note: only FN that were TP in the original Bert
-> Nearest neighbor sentences raussuchen hierfür (beispielhaft)

### #Mixed small

#### Mixed large

#### Geraete small

#### Geraete large

#### Excellent
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
FN         |anzeigepflichtige Tierseuche                       |Tierseuche                                         |Die Erkrankung ist eine anzeigepflichtige Tierseuche.                                                                                                                                                                                                           
FN         |Aufteilung seines Vermögens                        |Fürstenenteignung                                  |Das Haus Hohenzollern behielt es nach dem Vertrag mit dem Freistaat Preußen über die Aufteilung seines Vermögens vom 6. Oktober 1926 im Eigentum.                                                                                                               
FN         |Dali’s Mustache                                    |Dali’s_Mustache                                    |Halsman und Dalí veröffentlichten als Ergebnis ihrer Zusammenarbeit 1954 das Buch Dali’s Mustache, das 28 unterschiedliche Fotos seines Schnurrbarts zeigt.                                                                                                     
FN         |Darbepoetin                                        |Erythropoetin                                      |Allerdings konnte in der Dopingkontrolle bei ihr die Verwendung von Darbepoetin nachgewiesen werden.                                                                                                                                                            
FN         |Die Betrogene                                      |Die_Betrogene                                      |Eine entscheidende Szene aus Thomas Manns Erzählung Die Betrogene spielt im Schloss Benrath, das hier den Namen Holterhof trägt.                                                                                                                                
FN         |Herzmassage                                        |Herz-Lungen-Wiederbelebung                         |Nach einem Auftritt am 26. September 2015 erlitt Gruber einen Herzstillstand, den er dank prompter Herzmassage durch seinen Kollegen Puntigam und rasch abfolgender Rettungskette überlebte.                                                                    
FN         |Hooke-Element                                      |Robert_Hooke                                       |In der Rheologie ist die lineare Elastizität neben der Plastizität und der Viskosität eine der drei Grundeigenschaften und wird in den rheologischen Modellen durch eine Feder, das Hooke-Element, dargestellt.                                                 
FN         |Johannisberg bei Jena-Lobeda                       |Johannisberg_(Jena-Lobeda)                         |Mehrere Rettungs- und Forschungsgraben wurden im weiteren Umfeld von Jena durchgeführt, wobei sich Schrickel besonders dem Neolithikum und Neumann der vorrömischen Eisenzeit und dem Mittelalter widmete, unter anderem der Wüstung Gumprechtsdorf im ehemaligen Staatsforst Klosterlausnitz (1952–1953), der Entstehung der mittelalterlichen Städte Jena und Lobeda (1953–1956), dem bronzezeitlichen und frühmittelalterlichen Burgwall auf dem Johannisberg bei Jena-Lobeda (1957, 1959) und der Burg bzw. dem Peterskloster in Saalfeld (1964).
FN         |Kelten                                             |Keltische_Religion                                 |Eine nachträgliche Beeinflussung könnte sich durch den kulturellen und wirtschaftlichen Kontakt mit den Kelten, Balten, Slawen und (spät) auch den Römern ergeben haben.                                                                                        
FN         |Machtkämpfen der 1990er Jahre                      |Afghanischer_Bürgerkrieg_(1989–2001)               |In den Machtkämpfen der 1990er Jahre verlor er sein Amt, konnte es aber 1996 noch einmal für wenige Wochen zurückgewinnen.                                                                                                                                      
FN         |Melankoli                                          |Melancholie_(Munch)                                |Edvard Munch malt die erste Version seines Gemäldes Melankoli als Bestandteil seines Lebensfrieses .                                                                                                                                                            
FN         |Münster Unserer Lieben Frau                        |Konstanzer_Münster                                 |Konstanz: Im Münster Unserer Lieben Frau befindet sich ein Heiliges Grab in der 940 erbauten Mauritiusrotunde: um 1260 als frühgotischer zwölfeckiger Sandsteinbau errichtet.                                                                                   
FN         |Nimrod-Expedition                                  |Nimrod-Expedition                                  |Der Erhalt der am Cape Royds während der Nimrod-Expedition errichteten Hütte, die in Neuseeland als internationales Kulturerbe angesehen wird, liegt in den Händen des New Zealand Antarctic Heritage Trust.                                                    
FN         |Percy Ernst Schramm                                |Percy_Ernst_Schramm                                |Percy Ernst Schramm (1894–1970), Historiker.                                                                                                                                                                                                                    
FN         |seuchenartige                                      |Tierseuche                                         |Die Geflügelcholera ist eine durch Pasteurella multocida hervorgerufene seuchenartige bakterielle Infektionskrankheit der Vögel.                                                                                                                                
FN         |Staurohr                                           |Pitotrohr                                          |Diese wird aus statischem und dynamischem Druck am Staurohr des Fahrtmessers ermittelt.                                                                                                                                                                         
FN         |Taunus- und Wetteraulimes                          |Obergermanisch-Raetischer_Limes                    |In der Folge entstanden die Grenzbefestigungen des Taunus- und Wetteraulimes.                                                                                                                                                                                   
FN         |Tempel- und Klosteranlage                          |Höhlentempel_in_Asien                              |Karla (auch Karli) ist eine aus dem Granitgestein des Dekkan-Plateaus (Indien) herausgeschälte buddhistische Tempel- und Klosteranlage aus der Zeit zwischen dem 2. vorchristlichen und dem 2./3.                                                               
FN         |U-Bahn-Bau                                         |U-Bahn_Berlin                                      |Er war in den Jahren 1927 bis 1929 im Rahmen eines Notstandsprogramms durch Ablagerung von Hausmüll und Aushub vom Straßen- und U-Bahn-Bau entstanden und wurde von 1952 bis 1954 durch Trümmer und Schutt um zehn Meter erhöht.                                
FN         |U-Bahn                                             |U-Bahn_Berlin                                      |Dann führt die Straßentrasse zwischen Gleimviertel und Helmholtzkiez rund 900 Meter weiter bis zur Ringbahn, wo sich der S-Bahnhof Schönhauser Allee mit der gleichnamigen Station der U-Bahn befindet.                                                         
FN         |Überfunktion                                       |Hyperthyreose                                      |Die Schilddrüse ist Ausgangspunkt für zahlreiche Erkrankungen, die unter anderem zu Störungen des Hormonstoffwechsels führen und eine Unter- oder Überfunktion der Schilddrüse (Hypothyreose bzw. Hyperthyreose) hervorrufen können.                            
FN         |Vormenschen                                        |Stammesgeschichte_des_Menschen                     |Auch über das Zahlenverständnis oder gar die mathematischen Fähigkeiten der Vormenschen und der frühen, nicht-schriftlichen Kulturen ist nichts bekannt.                                                                                                        
FN         |X V                                                |Sächsische_X_V                                     |Mit der Vorgängergattung X V hatten sie nur wenig gemeinsam.                                                                                                                                                                                                    
```

## Comparison to the token-level classifier


## Comparison to the rule-based classifier

