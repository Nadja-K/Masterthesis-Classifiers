# Table of Contents
1. [General notes and remarks to the reults of the experiments](#general-notes-and-remarks-to-the-results-of-the-experiments)
2. [Comparison to the unfinedtuned Bert model](#comparison-to-the-unfinetuned-bert-model)
3. [Comparison to the token-level classifier](#comparison-to-the-token-level-classifier)
4. [Comparison to the rule-based classifier](#comparison-to-the-rule-based-classifier)


## General notes and remarks to the results of the experiments
* It is logical that the (finetuned/original) bert model fails for some of the samples that the rule-based and token-level classifier classified successfully. The reason for this are the context-sentences that are used for the annoy nearest neighbor search. It is entirely possible that the context sentences of an entity simply did not contain any sentence that was remotely similar to a query sentence, leading to a FN classification because a context-sentence of a different entity might me more similar.
* Quite a few of new FN samples seem to be rather trivial cases that should easily be covered by the rule-based classifier



## Comparison to the unfinetuned Bert model
### (leftover) false negatives
-> Note: only FN that were FN in the original Bert

#### Mixed small
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------

``` 

#### Mixed large
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------

``` 

#### Geraete small
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------

``` 

#### Geraete large
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------

``` 

#### Excellent
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------

``` 


### Improvements over the unfinetuned Bert model
-> Note: only TP that were FN in the original Bert

#### Mixed small
- Num new TP samples: 241

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
TP         |Thurella                                           |Thurella                                           |Dazu gehören der Getränkehersteller Thurella, die Vermögensverwaltungsgesellschaft Schroders, der Uhrenhersteller Alfex, die Augenoptikerkette Visilab und die Sportfachhandelsgruppe Intersport .                                                              
TP         |Thurgauer Kantonalbank                             |Thurgauer_Kantonalbank                             |Mehrere kantonale Einrichtungen haben hier wegen der zentraleren geographischen Lage gegenüber Frauenfeld, dem Hauptort des Kantons, ihren Sitz, so die Thurgauer Kantonalbank und das Thurgauer Verwaltungsgericht.                                            
TP         |Thurgauer Kantonalbank                             |Thurgauer_Kantonalbank                             |Zu den Reformen gehörten die Volkswahl des Regierungsrates, die Gründung der Thurgauer Kantonalbank und die Unvereinbarkeit verschiedener Ämter.                                                                                                                
TP         |Thut, Kurt                                         |Kurt_Thut                                          |Thut, Kurt (1931–2011), Schweizer Innenarchitekt.                                                                                                                                                                                                               
TP         |TMX Group                                          |Toronto_Stock_Exchange                             |Die TMX Group, welche die Torontoer Börse und die Montreal Exchange betreibt, hat ihren Hauptsitz ebenfalls im Financial District.                                                                                                                              
TP         |Tōbu-Bahngesellschaft                              |Tōbu_Tetsudō                                       |Der Turm steht auf dem Gelände eines alten Rangierbahnhofes der Tōbu-Bahngesellschaft, die den Hauptteil der damals geschätzten Gesamtkosten von circa 60 Milliarden Yen, umgerechnet rund 460 Millionen Euro, übernehmen wollte.                               
TP         |Traugott Vogel                                     |Traugott_Vogel                                     |Dort war er oft in Gesellschaft von weiteren Zürcher Literaten und Kulturschaffenden anzutreffen, etwa dem Literaturprofessor Fritz Ernst, dem Literaturkritiker Bernhard Diebold, seinem Freund Traugott Vogel oder Rudolf Jakob Humm.                         
TP         |TSX                                                |Toronto_Stock_Exchange                             |CanWest Global Communications (TSX: CGS; NYSE: CWG) war ein international tätiger Medienkonzern aus Kanada und einer der größten des Landes.                                                                                                                    
TP         |UK-Freistellung                                    |Reklamierung                                       |Armeekorps (Berlin) versetzt, was einer UK-Freistellung vom Fronteinsatz zugunsten seiner Dienstgeschäfte in der NS-Auslandsorganisation gleichkam.                                                                                                             
TP         |Unipetrol                                          |Unipetrol                                          |In Brüx (damals Reichsgau Sudetenland) wurde die Sudetenländische Bergbau AG gegründet und bei Maltheuern nördlich von Brüx errichtete die Sudetenländische Treibstoffwerke AG mit Sitz Oberleutensdorf ein Hydrierwerk (heute Unipetrol RPA – Raffinerie, Petrochemie, Agrochemie), um aus der geförderten Kohle synthetisches Benzin herzustellen.
TP         |Unipetrol                                          |Unipetrol                                          |Nördlich davon errichtete in der Gemarkung Maltheuern die mit Mehrheitsbeteiligung der SUBAG entstandene Sudetenländische Treibstoffwerke AG (STW) Oberleutensdorf ein Hydrierwerk (heute Unipetrol RPA – Raffinerie, Petrochemie, Agrochemie), um durch Kohleverflüssigung Benzin sowie Diesel- und Heizöl herzustellen.
...
``` 

#### Mixed large
- Num new TP samples: 1727

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
TP         |Wojciech Młynarski                                 |Wojciech_Młynarski                                 |Warszawa Główna war häufig Thema in polnischen Filmen, so auch in einem Lied von Wojciech Młynarski („Niedziela na Głównym“).                                                                                                                                   
TP         |Wolfgang Lesowsky                                  |Wolfgang_Lesowsky                                  |Fernseh-Dokumentation, Österreich, 1994, 45 Min., Regie: Wolfgang Lesowsky, Produktion: Leopold Museum, Atelier Corinne Hochwarter, Forum Film, (englisch, deutsch), zu Schieles Stationen in Wien, Neulengbach, Krumau, Tulln.                                 
TP         |Wolfgang Neff                                      |Wolfgang_Neff                                      |Wolfgang Neff (1875–1936), österreichischer Schauspieler, Theaterregisseur und Filmregisseur.                                                                                                                                                                   
TP         |Wolfgang Neff                                      |Wolfgang_Neff                                      |Wolfgang Neff (1875–nach 1936), österreichischer Schauspieler, Theaterregisseur und Filmregisseur.                                                                                                                                                              
TP         |Wolf Nöhren                                        |Wolf_Nöhren                                        |Für die Bühnenarchitektur arbeitete Biolek mit Dieter Flimm und Wolf Nöhren zusammen.                                                                                                                                                                           
TP         |Wolf Nöhren                                        |Wolf_Nöhren                                        |In dieser Zeit entstand auch die Freundschaft mit seinem Kollegen Wolf Nöhren.                                                                                                                                                                                  
TP         |Women Accepted for Volunteer Emergency Service (WAVES) |WAVES                                              |In den weiblichen Organisationen – wie Women’s Army Corps (WAC) und Women Accepted for Volunteer Emergency Service (WAVES) –, in denen während des Zweiten Weltkrieges 275.000 Frauen dienten, entstand eine blühende lesbische Subkultur.                      
TP         |Wsewolod Witaljewitsch Wischnewski                 |Wsewolod_Witaljewitsch_Wischnewski                 |Wsewolod Witaljewitsch Wischnewski (1900–1951), sowjetischer Schriftsteller.                                                                                                                                                                                    
TP         |Wuchtgeschosse                                     |Wuchtgeschoss                                      |Obwohl der Churchill zu den am schwersten gepanzerten Fahrzeugen in den Kämpfen um die Normandie gehörte, war er dennoch durch Wuchtgeschosse aus modernen 75- und 88-mm- Kanonen, selbst an der am besten gepanzerten Frontseite, verwundbar.                  
TP         |Würth-Konzerns                                     |Würth-Gruppe                                       |Swiridoff war unter anderem von 1971 bis 1991 Chefredakteur und Herausgeber der Firmenzeitung Würth Report des weltweit agierenden Würth-Konzerns .                                                                                                             
TP         |Württembergische Bodensee-Dampfschiffgesellschaft  |Friedrichshafener_Dampfbootgesellschaft            |Um Abläufe und Organisation der Schifftransporte besser zu kontrollieren, wurde 1854 die 30 Jahre zuvor gegründete Württembergische Bodensee-Dampfschiffgesellschaft verstaatlicht und der Staatsbahn unterstellt.                                              
...
``` 

#### Geraete small
- Num new TP samples: 70

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
TP         |Kurbelantriebs                                     |Handkurbel                                         |Bei der Fuldaseilbahn Beiseförth wird mittels eines Kurbelantriebs ein Seilbahnkorb per Muskelkraft als Fährenersatz (ähnlich einer Schwebefähre) über den Fluss bewegt.                                                                                        
TP         |Leistungsaufnahme                                  |CPU-Leistungsaufnahme                              |Aufgrund ihrer geringen Leistungsaufnahme kommen ARM-Prozessoren vor allem in eingebetteten Systemen, wie Mobiltelefonen, PDAs und Routern zum Einsatz.                                                                                                         
TP         |Lenkstange                                         |Lenkstange                                         |Dabei wurde die Lenkstange nach hinten gezogen und bewegte damit einen mit Zahnrädern versehenen Quadranten (Viertelkreis), der ein Zahnrad drehte, das auf die vordere Nabe wirkte.                                                                            
TP         |Maschinenfabrik Rieter und Co.                     |Rieter                                             |Danach absolvierte er eine Lehre als Maschinentechniker bei Trindler & Knobel in Flums und trat 1879 eine Stelle in der Maschinenfabrik Rieter und Co.                                                                                                          
TP         |Monsterroller                                      |Monsterroller                                      |Die Höhendifferenz aller Strecken beträgt 350 m. Monsterroller, spezialisierte Downhill- und Freeridebikes sowie die zugehörige Schutzausrüstung werden zum Verleih angeboten.                                                                                  
TP         |Morseübungsgeräte                                  |Schreibtelegraf                                    |Die ersten Produkte sind unter anderem Morseübungsgeräte für die britische und belgische Armee.                                                                                                                                                                 
TP         |MTD (Unternehmen)                                  |MTD_(Unternehmen)                                  |MTD (Unternehmen), ein Hersteller von motorisierten Gartengeräten.                                                                                                                                                                                              
TP         |Mundbinde                                          |Phorbeia                                           |Das Spiel – vermutlich mit Zirkularatmung, wie es bei den traditionellen Instrumenten des Mittelmeerraums und in Asien bis heute begegnet – wurde durch eine Mundbinde (griechisch phorbeia, lateinisch capistrum) unterstützt.                                 
TP         |Okuliermesser                                      |Okuliermesser                                      |Bei der eigentlichen Okulation wird das Auge mit dem Okuliermesser flach aus dem Edelreis herausgeschnitten, in einer Länge von ca. 1–2 cm bei Rosen und ca. 2–4 cm bei Obst.                                                                                   
TP         |Peter Falk (Ingenieur)                             |Peter_Falk_(Ingenieur)                             |Peter Falk (Ingenieur) (* 1932), deutscher Ingenieur.                                                                                                                                                                                                           
TP         |pipeline                                           |Pipeline                                           |Hinüber führen eine Gaspipeline und eine 110-kV-Hochspannungsleitung.                                                                                                                                                                                           
TP         |Planar                                             |Planar_(Objektiv)                                  |Planar 2/80 mm (äquivalent ca. 50 mm KB).                                                                                                                                                                                                                       
TP         |Planars                                            |Planar_(Objektiv)                                  |Das Pancolar kann als Abwandlung des Planars verstanden werden.                                                                                                                                                                                                 
TP         |Queuespitze                                        |Queue_(Billard)                                    |Die Billardkreide wird auf die Pomeranze an der Queuespitze aufgetragen.                                                                                                                                                                                        
...
``` 

#### Geraete large
- Num new TP samples: 3176

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
TP         |Achim Kaufmann                                     |Achim_Kaufmann                                     |Eine feste Zusammenarbeit verbindet ihn auch mit dem Pianisten Achim Kaufmann.                                                                                                                                                                                  
TP         |Achim Mohné                                        |Achim_Mohné                                        |Achim Mohné (* 1964), Künstler.                                                                                                                                                                                                                                 
TP         |Ack van Rooyen                                     |Ack_van_Rooyen                                     |Er arbeitete dabei mit verschiedenen Solisten der populären Musik, des Jazz und der Klassik wie beispielsweise Gitte Hænning, Wencke Myhre, Bill Ramsey, Klaus Doldinger, Paul Kuhn, Campino, Heino, Rex Gildo, Ack van Rooyen, Deborah Sasson oder Ruth Hohmann zusammen.
TP         |Ack van Rooyen                                     |Ack_van_Rooyen                                     |Hiseman und Thompson gehörten 1976 neben Volker Kriegel, Albert Mangelsdorff, Eberhard Weber, Ian Carr, Charlie Mariano und Ack van Rooyen zu den ersten Mitgliedern des von Wolfgang Dauner gegründeten United Jazz + Rock Ensemble .                          
TP         |Adelhard Roidinger                                 |Adelhard_Roidinger                                 |Während der Gymnasialzeit begann er das Jazzseminar bei Adelhard Roidinger am Linzer Brucknerkonservatorium sowie nach der Matura Volkswirtschaftslehre an der Kepler Universität Linz zu studieren, gab aber beide Studien für ein Leben zunächst als Musiker auf.
TP         |Adelheid-Kreuz                                     |Adelheid-Kreuz                                     |Die letzten Mönche übersiedelten auf Umwegen mit Kunstschätzen, darunter dem Adelheid-Kreuz sowie den Gebeinen von 12 Habsburgern zum Stift St. Paul im Lavanttal in Kärnten.                                                                                   
TP         |Admiral Kornilow                                   |Admiral_Kornilow                                   |Im Jahr 1885 wurde Reitzenstein Minenoffizier des Kreuzers Admiral Kornilow .                                                                                                                                                                                   
TP         |Adolf Odkolek von Újezd                            |Adolf_Odkolek_von_Újezd                            |Selbstlademechanismen, die nach diesem Prinzip arbeiten, erschienen ab etwa 1890 bei Maschinengewehren wie dem Colt Modell 1895 von John Moses Browning, dem Hotchkiss M1914 von Benjamin Hotchkiss auf der Basis der Erfindung des Österreichers Adolf Odkolek von Újezd, dem Lewis Gun von Colonel Isaac Lewis und einigen anderen Konstruktionen.
TP         |Ādolfs Ābele                                       |Ādolfs_Ābele                                       |Sein Klavierdozent hier war Arvīds Žilinskis (1905–1993), Unterricht in Orchestrierung erhielt er von Ādolfs Ābele.                                                                                                                                             
TP         |Advanced Gravis                                    |Advanced_Gravis_Computer_Technology                |Gravis Ultrasound oder GUS ist eine Soundkarte von Advanced Gravis für den IBM-kompatiblen PC.                                                                                                                                                                  
TP         |Advanced Nuclear Fuels                             |Advanced_Nuclear_Fuels                             |Advanced Nuclear Fuels, ein Kernbrennstoffe und Kernreaktorbauteile produzierendes Unternehmen.                                                                                                                                                                 
TP         |Aegler, Gottfried                                  |Gottfried_Aegler                                   |Aegler, Gottfried (* 1932), Schweizer Volksmusikant.                                                                                                                                                                                                            
...
``` 

#### Excellent
- Num new TP samples: 18

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


### Deteriorations over the unfinetuned Bert model
-> Note: only FN that were TP in the original Bert
-> Nearest neighbor sentences raussuchen hierfür (beispielhaft)

#### Mixed small
- Num new FN samples: 63

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |internationale Organisation                        |Internationale_Organisation_(Völkerrecht)          |Geprägt wurde der Begriff nach dem Ende des Ersten Weltkriegs als Bezeichnung für die letztlich misslungenen Versuche des amerikanischen Präsidenten Woodrow Wilson, den Völkerbund als internationale Organisation mit einem geschriebenen Völkerrecht zu etablieren.
FN         |Johannes Kauffmann                                 |Johannes_Kauffmann                                 |Johannes Kauffmann, Gründer des gleichnamigen Unternehmens.                                                                                                                                                                                                     
FN         |John McGahern                                      |John_McGahern                                      |An aktueller Literatur verlegt Steidl neben Günter Grass Autoren wie Erich Loest, John McGahern,                                                                                                                                                                
FN         |Klaus Bischoff                                     |Klaus_Bischoff_(Designer)                          |Entworfen wurde das 4,54 Meter lange und auf dem Golf basierende New Compact Coupé vom VW-Designchef Klaus Bischoff.                                                                                                                                            
FN         |L1-                                                |Lagrange-Punkte                                    |Sollte der Aufbau und die Nutzung der Raumstation Bigelow Alpha erfolgreich verlaufen, sieht Robert Bigelow die Zukunft in einer L1- oder auch Mondbasis.                                                                                                       
FN         |Mattel                                             |Mattel                                             |Beim Import aus solchen Ländern sind Qualitätskontrollen mehr und mehr unerlässlich, denn beispielsweise im Jahr 2007 kam es zu einer Vielzahl von Rückrufaktionen für Spielzeuge, die in der Volksrepublik China produziert wurden (Rückrufe von Mattel von Spielwaren mit zu hohem Bleigehalt in der Farbe).
FN         |Maugham-Verfilmung                                 |William_Somerset_Maugham                           |In den darauffolgenden Jahren arbeitete er für Orson Welles’ Film noir Die Lady von Shanghai (1947), drehte die Maugham-Verfilmung Fegefeuer (1953) in 3D und setzte eine Reihe von Western mit Randolph Scott in Szene, wie z.b. Um Kopf und Kragen (1957) oder Auf eigene Faust (1959).
FN         |Max und Moritz                                     |Max_und_Moritz_(Gewürzstreuer)                     |Ein besonderes Objekt ist „Max und Moritz“ des Bauhaus-Schülers und -Lehrers Wilhelm Wagenfeld, dieses wird von WMF ununterbrochen seit 1953 produziert.                                                                                                        
FN         |Max und Moritz                                     |Max_und_Moritz_(Gewürzstreuer)                     |Salz- und Pfefferstreuer Max und Moritz, Butterdose, Eierbecher und Servierplatten aus Cromargan für WMF.                                                                                                                                                       
FN         |OETZ                                               |OETZ_(Zeitschrift)                                 |Kursbericht: Schriftplakate – Artikel im OETZ, Ausgabe 9, Seite 44–47 von 1984.                                                                                                                                                                                 
FN         |Oliver K. Wnuk                                     |Oliver_Wnuk                                        |Oliver K. Wnuk (* 1976), deutscher Theater-, Fernseh- und Filmschauspieler.                                                                                                                                                                                     
...
``` 

#### Mixed large
- Num new FN samples: 249

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Tally Weijl                                        |Tally_Weijl                                        |Die Modehandelskette Tally Weijl hatte von 1996 bis 2006 ihren Hauptsitz in Zofingen.                                                                                                                                                                           
FN         |Tatneft                                            |Tatneft                                            |Das Mineralölunternehmen Tatneft hat seinen Firmensitz in der Stadt.                                                                                                                                                                                            
FN         |Tatneft                                            |Tatneft                                            |In der Umgebung wird durch Tatneft (Bereich Sainskneft) Erdöl gefördert.                                                                                                                                                                                        
FN         |Teatro Comunale di Bologna                         |Teatro_Comunale_di_Bologna                         |Teatro Comunale di Bologna, Bologna.                                                                                                                                                                                                                            
FN         |technischen Regelungen                             |Technische_Dienstvorschrift                        |Komplettiert wird die Vorschriftenlandschaft durch eine große Zahl von technischen Regelungen („TDv“) für nahezu jegliches technische Gerät.                                                                                                                    
FN         |The Big Picture                                    |The_Big_Picture_(Fernsehserie)                     |Außerdem trat er Anfang der 1960er Jahre als Moderator in der Fernsehserie The Big Picture auf, die von der United States Army zu Propagandazwecken produziert wurde.                                                                                           
FN         |The Big Picture                                    |The_Big_Picture_(Fernsehserie)                     |In der Episode Special Forces der von der US Army produzierten Fernsehserie The Big Picture von 1962 werden die Special Forces und ihre Geschichte von Henry Fonda als Moderator vorgestellt.                                                                   
FN         |Theo Sommer                                        |Theo_Sommer                                        |Bedeutende Journalisten, die ihre Ausbildung bei der Rems-Zeitung absolviert haben, sind Theo Sommer und Günter Ogger .                                                                                                                                         
FN         |The Stars and Stripes                              |The_Stars_and_Stripes                              |Nachdem er 1962 mit George Maciunas die Wiesbadener Festspiele Neuester Musik, später bekannt als das erste Fluxus-Festival, im städtischen Museum Wiesbaden organisiert hatte, wurde der erste Fluxus-bezogene Zeitungsartikel von Emmett Williams in der Zeitschrift The Stars and Stripes veröffentlicht.
FN         |Träger                                             |Trägersystem                                       |Blue Steel war eine britische Luft-Boden-Rakete, die zur Zeit des Kalten Krieges als Träger für einen thermonuklearen Sprengkopf diente.                                                                                                                        
FN         |Trane                                              |Trane                                              |Trane: Klimaanlagen und Wärmepumpen (die Fabrik wurde 1955 von General Electric errichtet).                                                                                                                                                                     
FN         |transnational                                      |Transnationalismus                                 |Die Cyberanthropologie ist ein neueres Fachgebiet der Ethnologie (Völkerkunde) oder Sozialanthropologie und untersucht transnational zusammengesetzte Online-Gemeinschaften unter Berücksichtigung kybernetischer Perspektiven.                                 
FN         |Traton                                             |Traton                                             |Die Volkswagen AG hält mittels der Traton SE mit 94,36 % die Mehrheit der Stammaktien an dem Konzern.                                                                                                                                                           
...
``` 

#### Geraete small
- Num new FN samples: 45

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Jochstück einer Wassertrage                        |Tragjoch                                           |Diese Gewässer hätten sämtlich eine Krümmung, die dem Jochstück einer Wassertrage ähnele.                                                                                                                                                                       
FN         |Keiler                                             |Keiler_(Panzer)                                    |Er gleicht im Funktionsprinzip dem deutschen Keiler, besitzt jedoch das britische Aardvark-Minenräumsystem sowie elektronisches und explosives Minenräumequipment.                                                                                              
FN         |Kombidämpfern                                      |Heißluftdämpfer                                    |Der Energieverbrauch von Kippbratpfannen ist höher als der von grundsätzlich geschlossenen Kochgeräten wie Kombidämpfern .                                                                                                                                      
FN         |Körting-Motoren                                    |Körting_Hannover                                   |Antrieb: zwei Körting-Motoren mit je 75 PS.                                                                                                                                                                                                                     
FN         |Kühler                                             |Kühler                                             |Zuletzt wird die nun Anstellwürze genannte Flüssigkeit in einem Kühler auf die optimale Gärtemperatur abgekühlt und je nach Biersorte die passende Hefekultur zugesetzt.                                                                                        
FN         |Kukrischwerter                                     |Khukuri                                            |In der Zwischenzeit stieg er jedoch zu Offiziersanwärter auf und lernte einen Kampfstil, für den er zwei Kukrischwerter nutzt.                                                                                                                                  
FN         |Lenkgestänge                                       |Spurstange                                         |Hierbei wird die Drehbewegung in engerer Analogie zur Lenkradbewegung auf das Lenkgestänge der Vorderräder übertragen.                                                                                                                                          
FN         |Lenkgestänge                                       |Spurstange                                         |Sie ist meist ein stangen- oder röhrenförmiger Träger, der am oberen Ende mit dem Lenkrad verbunden ist und dessen Bewegungen auf das Lenkgestänge der Fahrzeugräder überträgt.                                                                                 
FN         |Luftgitarre                                        |Luftgitarre                                        |Mertens Interessen umfassen auch die Luftgitarre: Er forscht nicht nur zum Thema, sondern richtet auch die deutsche Meisterschaft im Luftgitarrespielen aus und tritt selbst regelmäßig als Luftgitarrist auf.                                                  
FN         |MELF                                               |Metal_Electrode_Faces                              |SMD-Widerstände gibt es in runder (MELF) und in quaderförmiger Bauform.                                                                                                                                                                                         
...
``` 

#### Geraete large
- Num new FN samples: 626

``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Volumina                                           |Volumina_für_Orgel                                 |Sein Stück Doppelrohr II (1955) zählte zu den ersten skandinavischen Werken dieser Art, und seine Komposition Constellations I (1958) beeinflusste Ligetis Volumina (1962).                                                                                     
FN         |Volvo                                              |Volvo                                              |In einem aktuellen Projekt will das Imperial College in London zusammen mit Volvo und weiteren Organisationen ein neues Verbundmaterial aus Kohlenstofffasern (Carbonfasern) und Polymerharzen entwickeln, das auch für den Karosseriebau eingesetzt werden könnte.
FN         |Volvo                                              |Volvo_Trucks                                       |Deshalb mussten Fahrzeuge aus dem Westen beschafft werden, unter anderem von den Herstellern Mercedes-Benz, Magirus-Deutz und Volvo .                                                                                                                           
FN         |Volvo                                              |Volvo                                              |Viele von ihnen übernahmen anschließend die Produktionsprinzipien Henry Fords wie zum Beispiel Fiat, Renault oder Volvo.                                                                                                                                        
FN         |voneinander unabhängige Gefechtsköpfe              |Multiple_independently_targetable_reentry_vehicle  |Sie kann acht voneinander unabhängige Gefechtsköpfe des Typs W76 mit einer Sprengkraft von jeweils bis zu 100 Kilotonnen TNT-Äquivalent tragen.                                                                                                                 
FN         |Vossloh Kiepe                                      |Kiepe_Electric                                     |Die elektrische Ausrüstung stammt von Vossloh Kiepe, Düsseldorf.                                                                                                                                                                                                
FN         |Vox-Continental-Orgel                              |Vox_Continental                                    |Manzarek brachte der Vertrag den Besitz einer neuen Vox-Continental-Orgel .                                                                                                                                                                                     
FN         |Wagner Tiso                                        |Wagner_Tiso                                        |Außerdem arbeitete Stroeter in dieser Zeit mit Musikern wie Milton Nascimento, Edu Lobo, Chico Buarque, Wagner Tiso, Gilberto Gil, Carlinhos Brown und Marlui Miranda zusammen.                                                                                 
FN         |Walther-Werke                                      |Walther-Werke                                      |Anfang 1943 wurden die Walther-Werke bezugsfertig und die Fertigung von Pistolen und Gewehrteilen begann.                                                                                                                                                       
FN         |Walther-Werke                                      |Walther-Werke                                      |Auch entstanden in der Nähe von Konzentrationslagern Betriebsstätten entsprechend dem Konzept „Vernichtung durch Arbeit“, wie etwa die Ostindustrie GmbH, die Deutschen Ausrüstungswerke, die Walther-Werke und die Deutschen Erd- und Steinwerke.              
FN         |Wärmeerzeugers                                     |Wärmeerzeuger_(Gebäudeheizung)                     |Die Wärmeleistung entspricht der Feuerungswärmeleistung abzüglich der Verluste durch unvollständige Verbrennung, Restwärme im Abgas und der Wärmeverluste des Wärmeerzeugers .                                                                                  
FN         |Waymo                                              |Waymo                                              |Als am fortgeschrittensten werden Waymo und GM angesehen.                                                                                                                                                                                                       
...
``` 

#### Excellent
- Num new FN samples: 23

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





_________

## Comparison to the token-level classifier
#### Mixed small
- Number of samples, that the token-level classifier classified successfully, while the finetuned bert model failed: 148  
- Number of samples, that the finetuned bert model classified successfully, while the token-level classifier failed: 966

Samples, that the token-level classifier successfully classified, while the finetuned bert model failed.
```
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Phoenix Solar                                      |Phoenix_Solar                                      |Phoenix Solar, Unternehmen der Solarindustrie.                                                                                                                                                                                                                  
FN         |Postamt                                            |Österreichische_Post                               |Im November 1953 begann er als Mitarbeiter beim Postamt in Scharnstein und wurde zum Postamtsleiter ausgebildet.                                                                                                                                                
FN         |Präzession                                         |Präzession                                         |Auf Hipparchs Entdeckung der Präzession geht auch die Unterscheidung zwischen siderischem und tropischem Jahr zurück.                                                                                                                                           
FN         |Präzession                                         |Präzession                                         |Darüber hinaus sind die Geschwindigkeit der Präzession selbst und sogar der Öffnungswinkel des Präzessionskegels (die Schiefe der Ekliptik) über so lange Zeiträume deutlichen Änderungen unterworfen.                                                          
FN         |Purikura                                           |Purikura                                           |Automaten mit Photostickern kamen zuerst in Japan mit den so genannten Purikura auf, die sich durch zahlreiche weitere fortgeschrittene Funktionen von Fotoautomaten außerhalb Japans unterscheiden.                                                            
FN         |Quaker Oats                                        |PepsiCo                                            |Erst mit dem Sezessionskrieg 1861–65 begann die eigentliche Industrialisierung Akrons; hergestellt wurden vor allem Landmaschinen, Steinzeug, Zündhölzer (Barber, später Diamond Match), Petroleumlampen (Akron Lamp) sowie Haferflocken (Schumacher, später Quaker Oats).
FN         |Radio-Plattenspieler-Kombination SK 4              |Braun_SK_4                                         |Die Innovationen aus dem Bereich der Unterhaltungselektronik, wie etwa die Radio-Plattenspieler-Kombination SK 4, die tragbare Radio-Plattenspieler-Kombination „combi“ oder der Weltempfänger T 1000, brachten dem Unternehmen einen gewaltigen Imagegewinn ein, aber keinen wirtschaftlichen Erfolg.
FN         |Regie                                              |Regisseur                                          |Die Regie bei dieser Disney-Produktion führte Robert Butler, das Drehbuch schrieben Joseph L. McEveety und Robert L. King.                                                                                                                                      
FN         |Roten Juden                                        |Rote_Juden                                         |Das Volk war im Mittelalter als die Roten Juden (jiddisch „rojite jidlech“) bekannt.                                                                                                                                                                            
...
```

#### Mixed large
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 551 
- Number of samples, that the finetuned bert model classified successfully, while the token-level classifier failed: 3548

Samples, that the token-level classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |UTE                                                |UTE_(Unternehmen)                                  |Auch zeichnete er verantwortlich für den als Sitz der UTE (Arroyo Seco, Montevideo) dienenden Palacio de la Luz, der 1948 projektiert und 1951 eröffnet wurde.                                                                                                  
FN         |UTE                                                |UTE_(Unternehmen)                                  |Um seine staatliche Anstellung bei UTE nicht aufzugeben, verzichtete er sodann auch auf einen längerfristigen Vertrag bei den Boca Juniors.                                                                                                                     
FN         |Valovis Commercial Bank                            |Valovis_Commercial_Bank                            |Zum Vorsitzenden des Vorstandes wurde ab 1. August 2007 Robert Restani bestellt, der zuletzt Mitglied im Vorstand der KarstadtQuelle Bank (heute: Valovis Commercial Bank) war.                                                                                 
FN         |Vedette                                            |Vedette_(Militär)                                  |Sie steht auf dem höchsten Punkt Ingolstadts, möglicherweise an einer Stelle, an der sich einst eine römische Vedette befand.                                                                                                                                   
FN         |Verlagsgruppe Hüthig Heidelberg                    |Verlagsgruppe_Hüthig_Jehle_Rehm                    |Im Oktober 1991 wurde der Verlag an die Verlagsgruppe Hüthig Heidelberg verkauft, wobei einige Teile des gesellschaftswissenschaftlichen Programms an andere Verlage übergeben wurden.                                                                          
FN         |Vodev, Valentin                                    |Valentin_Vodev                                     |Vodev, Valentin (* 1978), österreichischer Industriedesigner.                                                                                                                                                                                                   
FN         |Volksbank Göppingen                                |Volksbank_Göppingen                                |Volksbank Göppingen eG, örtliche Genossenschaftsbank.                                                                                                                                                                                                           
FN         |Volvo-Fahrzeuge                                    |Volvo_Trucks                                       |Für den Fernverkehr wurden oftmals Volvo-Fahrzeuge eingesetzt.                                                                                                                                                                                                  
FN         |Volvo                                              |Volvo_Trucks                                       |Volvo baute als erster Lkw-Produzent nun auch Airbags in den Lkw ein.                                                                                                                                                                                           
...
```

#### Geraete small
- Number of samples, that the token-level classifier classified successfully, while the finetuned bert model failed: 61  
- Number of samples, that the finetuned bert model classified successfully, while the token-level classifier failed: 988

Samples, that the token-level classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Raut (Messer)                                      |Raut_(Messer)                                      |Raut (Messer), ein Messer aus Sumatra.                                                                                                                                                                                                                          
FN         |Schießereien                                       |Feuergefecht                                       |Hauptbestandteile von Actionfilmen sind daher meist aufwendig gedrehte Stunts, Nahkampf-Szenen, Schießereien, Explosionen und Verfolgungsjagden .                                                                                                               
FN         |Schneiderelle                                      |Schneiderelle                                      |Ein starres Metermaß (Schneiderelle) wird häufig im Textilhandel verwendet, wo Stoffe vom Ballen heruntergemessen werden.                                                                                                                                       
FN         |Schneiderelle                                      |Schneiderelle                                      |Noch heute werden die 50 cm oder 100 cm langen Maßstäbe im Schneiderhandwerk Schneiderelle genannt.                                                                                                                                                             
FN         |Schneiderelle                                      |Schneiderelle                                      |Schneiderelle, ein Längenmessgerät im Schneiderhandwerk.                                                                                                                                                                                                        
FN         |Schutzkragen                                       |Schutzkragen_(Medizin)                             |Schutzkragen, eine Vorrichtung zur Vermeidung des Wundenleckens in der Tiermedizin.                                                                                                                                                                             
FN         |Snack-Caddy-Service                                |Minibar_(Eisenbahnwesen)                           |Die IC-Züge der Linie 61 (Karlsruhe–Stuttgart–Nürnberg) verkehren seit dem Fahrplanwechsel im Juni 2011 gänzlich ohne gastronomischen Service, nachdem der nach Wegfall der Bordbistros im Dezember 2010 als „Ersatz“ eingeführte Snack-Caddy-Service ebenfalls eingestellt wurde.
FN         |Snack-Caddys                                       |Minibar_(Eisenbahnwesen)                           |Die Wagen sollen über „einfache Bordgastronomie“, also beispielsweise Snack-Caddys verfügen und weiterhin die Fahrradmitnahme ermöglichen.                                                                                                                      
FN         |Spachtel                                           |Malmesser                                          |Während dieser Zeit entstanden zahlreiche impressionistische Landschaftsbilder, gemalt mit Spachtel.                                                                                                                                                            
FN         |Spachteltechnik                                    |Malmesser                                          |Im Herbst 1866 führte Cézanne eine ganze Serie von Bildern in Spachteltechnik aus, vor allem Stillleben und Porträts.                                                                                                                                           
...
```

#### Geraete large
- Number of samples, that the token-level classifier classified successfully, while the finetuned bert model failed: 1410  
- Number of samples, that the finetuned bert model classified successfully, while the token-level classifier failed: 5437

Samples, that the token-level classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Raffaele Bossard                                   |Raffaele_Bossard                                   |Raffaele Bossard (* 1982).                                                                                                                                                                                                                                      
FN         |Raffaele Bossard                                   |Raffaele_Bossard                                   |Raffaele Bossard (1982), Bassist.                                                                                                                                                                                                                               
FN         |Raffaele Bossard                                   |Raffaele_Bossard                                   |Raffaele Bossard (* 1982), Schweizer Jazzmusiker.                                                                                                                                                                                                               
FN         |Raffaele Bossard                                   |Raffaele_Bossard                                   |Raffaele Bossard (* 1982), Schweizer Jazzmusiker.                                                                                                                                                                                                               
FN         |Rahsaan Roland Kirk                                |Rahsaan_Roland_Kirk                                |Rahsaan Roland Kirk (1936–1977), (Alle Saxofone).                                                                                                                                                                                                               
FN         |Raphael Zweifel                                    |Raphael_Zweifel                                    |Das Cello in Die Behauptung spielte Raphael Zweifel .                                                                                                                                                                                                           
FN         |Raphe Malik                                        |Raphe_Malik                                        |Daneben gehörte er dem Raphe Malik Quartet und dem One World Ensemble an und bildete mit Daniel Carter und David Nuss das Trio Tenor Rising, Drums Expanding.                                                                                                   
FN         |Ray Kaczynski                                      |Ray_Kaczynski                                      |Ray Kaczynski (* 1960), Jazz-Schlagzeuger.                                                                                                                                                                                                                      
FN         |Ray Kaczynski                                      |Ray_Kaczynski                                      |Ray Kaczynski (* 1960), US-amerikanischer Komponist und Schlagzeuger.                                                                                                                                                                                           
FN         |RBDe 567 315 (1983), 316 (1985), 317 (1991)        |TPF-TRN_RBDe_567                                   |RBDe 567 315 (1983), 316 (1985), 317 (1991) «Privatbahn-NPZ».                                                                                                                                                                                                   
FN         |Reflekta-Kamerawerk Tharandt                       |Reflekta-Kamerawerk_Tharandt                       |VEB Reflekta-Kamerawerk Tharandt; vormals Welta-Kamera-Werk Freital, u.a. Reflekta II, Weltaflex und Penti), Ausgliederung 1960;.                                                                                                                               
FN         |Regal Princess (Schiff, 2014)                      |Regal_Princess_(Schiff,_2014)                      |Regal Princess (Schiff, 2014), ein Kreuzfahrtschiff der Princess Cruises .                                                                                                                                                                                      
...
```

#### Excellent onesize
- Number of samples, that the token-level classifier classified successfully, while the finetuned bert model failed: 38 
- Number of samples, that the finetuned bert model classified successfully, while the token-level classifier failed: 406

Samples, that the token-level classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Ga                                                 |Gallium                                            |Zum Beispiel wandelt sich 71Ga durch Einfang eines Elektron-Neutrinos in 71Ge unter Emission eines Elektrons um.                                                                                                                                                
FN         |Geschichte des Tennis                              |Geschichte_des_Tennis                              |World Championship Tennis, ein Profi-Turnier 1967–1989, siehe hierzu Geschichte des Tennis (1945 bis 1967).                                                                                                                                                     
FN         |Hooke-Element                                      |Robert_Hooke                                       |In der Rheologie ist die lineare Elastizität neben der Plastizität und der Viskosität eine der drei Grundeigenschaften und wird in den rheologischen Modellen durch eine Feder, das Hooke-Element, dargestellt.                                                 
FN         |Johannisberg bei Jena-Lobeda                       |Johannisberg_(Jena-Lobeda)                         |Mehrere Rettungs- und Forschungsgraben wurden im weiteren Umfeld von Jena durchgeführt, wobei sich Schrickel besonders dem Neolithikum und Neumann der vorrömischen Eisenzeit und dem Mittelalter widmete, unter anderem der Wüstung Gumprechtsdorf im ehemaligen Staatsforst Klosterlausnitz (1952–1953), der Entstehung der mittelalterlichen Städte Jena und Lobeda (1953–1956), dem bronzezeitlichen und frühmittelalterlichen Burgwall auf dem Johannisberg bei Jena-Lobeda (1957, 1959) und der Burg bzw. dem Peterskloster in Saalfeld (1964).
FN         |Kelten                                             |Keltische_Religion                                 |Eine nachträgliche Beeinflussung könnte sich durch den kulturellen und wirtschaftlichen Kontakt mit den Kelten, Balten, Slawen und (spät) auch den Römern ergeben haben.                                                                                        
FN         |konstantinische                                    |Konstantin_der_Große                               |Der Gebrauch geht wahrscheinlich auf die vorkonstantinische Zeit zurück.                                                                                                                                                                                        
FN         |Machtkämpfen der 1990er Jahre                      |Afghanischer_Bürgerkrieg_(1989–2001)               |In den Machtkämpfen der 1990er Jahre verlor er sein Amt, konnte es aber 1996 noch einmal für wenige Wochen zurückgewinnen.                                                                                                                                      
FN         |Münster                                            |Konstanzer_Münster                                 |Das Gebiet erstreckt sich zwischen Münster, Konzilstraße, Seerhein und Unterer Laube, dem einstigen Stadtgraben.                                                                                                                                                
FN         |Münster                                            |Konstanzer_Münster                                 |Der eigentliche Sitzungssaal war der Bischofsdom, das heutige Münster.                                                                                                                                                                                          
FN         |Münster                                            |Konstanzer_Münster                                 |Die Städtische Wessenberg-Galerie befindet sich im Kulturzentrum am Münster und zeigt Kunst des 19. und 20. Jahrhunderts.                                                                                                                                       
...
```





_______________

## Comparison to the rule-based classifier
#### Mixed small
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 113 
- Number of samples, that the finetuned bert model classified successfully, while the rule-based classifier failed: 920

Samples, that the rule-based classifier successfully classified, while the finetuned bert model failed.
```
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Max und Moritz                                     |Max_und_Moritz_(Gewürzstreuer)                     |Ein besonderes Objekt ist „Max und Moritz“ des Bauhaus-Schülers und -Lehrers Wilhelm Wagenfeld, dieses wird von WMF ununterbrochen seit 1953 produziert.                                                                                                        
FN         |Max und Moritz                                     |Max_und_Moritz_(Gewürzstreuer)                     |Salz- und Pfefferstreuer Max und Moritz, Butterdose, Eierbecher und Servierplatten aus Cromargan für WMF.                                                                                                                                                       
FN         |Monument (Alarmierungssystem)                      |Monument_(Alarmierungssystem)                      |Monument (Alarmierungssystem), ehemaliges Alarmierungssystem des Warschauer Pakts.                                                                                                                                                                              
FN         |Nippon Yūsei                                       |Nippon_Yūsei                                       |Japan Post Holdings, der englische Name für das japanische Unternehmen Nippon Yūsei .                                                                                                                                                                           
FN         |Norris, Bruce                                      |Bruce_Norris                                       |Norris, Bruce (* 1960), US-amerikanischer Dramatiker und Schauspieler.                                                                                                                                                                                          
FN         |NOS (Unternehmen)                                  |NOS_(Unternehmen)                                  |NOS (Unternehmen), ein Medienunternehmen in Portugal.                                                                                                                                                                                                           
FN         |OETZ                                               |OETZ_(Zeitschrift)                                 |Kursbericht: Schriftplakate – Artikel im OETZ, Ausgabe 9, Seite 44–47 von 1984.                                                                                                                                                                                 
FN         |Oliver K. Wnuk                                     |Oliver_Wnuk                                        |Oliver K. Wnuk (* 1976), deutscher Theater-, Fernseh- und Filmschauspieler.                                                                                                                                                                                     
FN         |Paracelsus                                         |Paracelsus_(Schnitzler)                            |Paracelsus - Paracelsus (Arthur Schnitzler) .                                                                                                                                                                                                                   
...
```

#### Mixed large
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 513 
- Number of samples, that the finetuned bert model classified successfully, while the rule-based classifier failed: 2639

Samples, that the rule-based classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |Trane                                              |Trane                                              |Trane: Klimaanlagen und Wärmepumpen (die Fabrik wurde 1955 von General Electric errichtet).                                                                                                                                                                     
FN         |Traton                                             |Traton                                             |Die Volkswagen AG hält mittels der Traton SE mit 94,36 % die Mehrheit der Stammaktien an dem Konzern.                                                                                                                                                           
FN         |tresse                                             |Tresse                                             |Bereits 1889 hatte der „Etatsmäßige“ am Ärmelaufschlag des Waffenrocks zu der bereits vorhandenen Unteroffizierstresse eine zweite, etwas schmalere Tresse zur Unterscheidung vom Vizefeldwebel erhalten.                                                       
FN         |TTIPleaks                                          |TTIPleaks                                          |In einem Vortrag am Beginn der re:publica 2016 stellte Greenpeace geleakte Informationen zum Freihandelsabkommen TTIP vor, das sogenannte TTIPleaks .                                                                                                           
FN         |Tünche                                             |Tünche                                             |Die farbigen Fassungen von Triumphkreuz, deren Farbigkeit war auf Grundlage der Farbreste unter der bei der letzten Renovierung entfernten Tünche rekonstruiert worden, und Kanzel von 1902 wurden komplett entfernt.                                           
FN         |TV 4                                               |TV4_(Schweden)                                     |Außerdem ist eine von 16 Regionalstationen des privaten Fernsehsenders TV 4, TV 4 Öst, in Norrköping ansässig und produziert ein regionales Nachrichtenprogramm.                                                                                                
FN         |Tzu-Chi-Universität                                |Tzu-Chi-Universität                                |Tzu-Chi-Universität, eine private Universität in Hualien, Taiwan.                                                                                                                                                                                               
...
```

#### Geraete small
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 58 
- Number of samples, that the finetuned bert model classified successfully, while the rule-based classifier failed: 708

Samples, that the rule-based classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |L6/40                                              |L6/40                                              |Bersaglieri-Regiment, das 120. motorisierte Artillerieregiment und eine neue Panzerabteilung auf L6/40.                                                                                                                                                         
FN         |L6/40                                              |L6/40                                              |Nachdem man erkannt hatte, dass dies nicht annähernd genügend Feuerkraft darstellte, entschied man sich, den Turm des leichten Panzers L6/40 zu verwenden.                                                                                                      
FN         |Lern-Computern                                     |Lerncomputer                                       |Auch auf den Tastatur-Tasten von Lern-Computern für Kinder sind oftmals Anlaut-Bilder zu finden.                                                                                                                                                                
FN         |Luftgitarre                                        |Luftgitarre                                        |Mertens Interessen umfassen auch die Luftgitarre: Er forscht nicht nur zum Thema, sondern richtet auch die deutsche Meisterschaft im Luftgitarrespielen aus und tritt selbst regelmäßig als Luftgitarrist auf.                                                  
FN         |Messergriffs K 1103                                |Messergriff_K_1103                                 |Neben den hier beschriebenen Fragmenten waren dies die Fragmente des ebenfalls verzierten Messergriffs K 1103, Fragmente von zwei weiteren, unverzierten Messergriffen, Würfelstäbe, verschieden geformte Spielsteine aus Elfenbein, Spielkugeln aus Kalkstein, eine zur Hälfte erhaltene Birnenkeule aus Kalzit, ein Fischschwanzmesser, mehrere Mikrolithen, Scheibenperlen, Blattgoldfäden (eventuell von einem Gewand) sowie Bröckchen aus Malachit und Bleiglanz.
FN         |Microcomputern                                     |Mikrocomputer                                      |Einige der so mit BASIC vertrauten Schüler, Studenten und im Mittelstand tätigen Programmierer waren etwas später in der kurzlebigen Bastelcomputer-Szene Mitte der 1970er Jahre aktiv, die den kommerziellen Microcomputern vorausging, und machten BASIC dort bekannt; kaum eine andere damals verbreitete Hochsprache eignete sich so gut wie (ein abgespecktes) BASIC für den extrem beschränkten Speicherplatz dieser ersten Microcomputer.
FN         |Mobile Asteroid Surface Scout                      |Mobile_Asteroid_Surface_Scout                      |Mobile Asteroid Surface Scout, kurz MASCOT: Ein deutsch-französischer Lander der japanischen Asteroiden-Raumsonde Hayabusa 2 .                                                                                                                                  
FN         |Mobile Asteroid Surface Scout                      |Mobile_Asteroid_Surface_Scout                      |Mobile Asteroid Surface Scout (MASCOT), ein etwa 9,6 kg schwerer Lander und Rover mit den etwa schuhkartongroßen Abmessungen  Er trägt eine Nutzlast von ungefähr 3 kg und ist mit einem Infrarotspektrometer, einem Magnetometer, einem Radiometer und einer Weitwinkelkamera ausgestattet.
FN         |Normenausschuss Maschinenbau                       |Normenausschuss_Maschinenbau                       |Normenausschuss Maschinenbau im DIN Deutsches Institut für Normung e.                                                                                                                                                                                           
FN         |öse                                                |Öse                                                |Es ist mit einer 2,8 mm breiten Bordierung der Kreuzarme und einer querstehenden Standardöse am oberen Arm versehen, in welche der Tragering für das Ordensband eingezogen wird.                                                                                
...
```

#### Geraete large
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 1620 
- Number of samples, that the finetuned bert model classified successfully, while the rule-based classifier failed: 3251

Samples, that the rule-based classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
...
FN         |WTB                                                |Wire_Train_Bus                                     |Die in Österreich eingesetzten Steuerwagen der Baureihen 80-33 und 80-73, sowie die Railjet-Steuerwagen übertragen die Daten zwischen Lok und Steuerabteil über den Zugbus (WTB) entsprechend dem ÖBB Fernsteuerkonzept.                                        
FN         |WTB                                                |Wire_Train_Bus                                     |Die Steuerdaten werden nicht mehr über Einzelleitungen, sondern über serielle Bussysteme (Fahrzeugbus ist DVB, Zugbus ist WTB) übertragen.                                                                                                                      
FN         |WTB                                                |Wire_Train_Bus                                     |Eine weitere Möglichkeit ist die international normierte Wendezug- und Vielfachsteuerung über den WTB entsprechend den Telegrammen und Vorgaben der UIC Merkblätter 556 und 647.                                                                                
FN         |WTB                                                |Wire_Train_Bus                                     |Einige Lokomotiven der Baureihe 362 haben außerdem für den Einsatz mit Wendezügen WTB, Außenkameras und modernisierte Führerstände mit neuer Steuerung erhalten.                                                                                                
FN         |Ximo Tebar                                         |Ximo_Tebar                                         |Mitte der 1990er Jahre arbeitete er viel im Trio mit John McLaughlin, später im Trio mit Ximo Tebar .                                                                                                                                                           
FN         |Yannik Tiemann                                     |Yannik_Tiemann                                     |Yannik Tiemann (* 1990), deutscher Jazzmusiker.                                                                                                                                                                                                                 
FN         |Yannik Tiemann                                     |Yannik_Tiemann                                     |Yannik Tiemann (* 1990), deutscher Jazzmusiker.                                                                                                                                                                                                                 
FN         |Yannik Tiemann                                     |Yannik_Tiemann                                     |Yannik Tiemann (* 1990), Jazzmusiker.                                                                                                                                                                                                                           
FN         |Yuneec                                             |Yuneec                                             |Yuneec, z.b. Hexacopter Typhoon H Plus.                                                                                                                                                                                                                         
FN         |Yuri Honings´                                      |Yuri_Honing                                        |Er war Mitglied der Formationen „Erdmann 3000“ (formerly knows as Erdmann 2000) „Yuri Honings´“ „Wired Paradise“, Paul van Kemenade-international 5tett, Dejan Terzic „Underground“ und der Soulband „Spank You“.                                               
FN         |ZEMAG                                              |ZEMAG                                              |Auch die bei der ZEMAG in Zeitz vorgesehene Produktion von Achsen bereitete erhebliche Schwierigkeiten.                                                                                                                                                         
FN         |Zettelkästen                                       |Zettelkasten                                       |Outliner) ist ein Computerprogramm, das das Prinzip der strukturierten räumlichen Gliederung von Informationen (etwa in Form von Baumstrukturen oder Zettelkästen) auf eine digitale Plattform übersetzt.                                                       
FN         |Zigarettenmaschine                                 |Zigarettenmaschine                                 |Hinten führte ein Weg in denn Saal in dem die Zigarettenmaschine Calberla BB aufgestellt war.                                                                                                                                                                   
FN         |Zuckerhut-Glocken                                  |Zuckerhutglocke                                    |Drei „Zuckerhut-Glocken“ zeugen immer noch von dieser Zeit.                                                                                                                                                                                                     
FN         |Zum Heiligen Kreuz (Altmannstein)                  |Zum_Heiligen_Kreuz_(Altmannstein)                  |Altmannstein: Zum Heiligen Kreuz (Altmannstein) .                                                                                                                                                                                                               
...
```

#### Excellent onesize
- Number of samples, that the rule-based classifier classified successfully, while the finetuned bert model failed: 7
- Number of samples, that the finetuned bert model classified successfully, while the rule-based classifier failed: 547

Samples, that the rule-based classifier successfully classified, while the finetuned bert model failed.
``` 
Label      |Mention                                            |GT entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
FN         |Dali’s Mustache                                    |Dali’s_Mustache                                    |Halsman und Dalí veröffentlichten als Ergebnis ihrer Zusammenarbeit 1954 das Buch Dali’s Mustache, das 28 unterschiedliche Fotos seines Schnurrbarts zeigt.                                                                                                     
FN         |Die Betrogene                                      |Die_Betrogene                                      |Eine entscheidende Szene aus Thomas Manns Erzählung Die Betrogene spielt im Schloss Benrath, das hier den Namen Holterhof trägt.                                                                                                                                
FN         |Geschichte des Tennis                              |Geschichte_des_Tennis                              |World Championship Tennis, ein Profi-Turnier 1967–1989, siehe hierzu Geschichte des Tennis (1945 bis 1967).                                                                                                                                                     
FN         |löwe                                               |Löwe                                               |Junglöwe Ryan ist deprimiert, dass sein Gebrüll noch immer nicht so imposant klingt wie die Stimme seines Vaters.                                                                                                                                               
FN         |Melankoli                                          |Melancholie_(Munch)                                |Edvard Munch malt die erste Version seines Gemäldes Melankoli als Bestandteil seines Lebensfrieses .                                                                                                                                                            
FN         |Nimrod-Expedition                                  |Nimrod-Expedition                                  |Der Erhalt der am Cape Royds während der Nimrod-Expedition errichteten Hütte, die in Neuseeland als internationales Kulturerbe angesehen wird, liegt in den Händen des New Zealand Antarctic Heritage Trust.                                                    
FN         |Percy Ernst Schramm                                |Percy_Ernst_Schramm                                |Percy Ernst Schramm (1894–1970), Historiker.                                                                                                                                                                                                                    
```
