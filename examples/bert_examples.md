## True positives
```
Label      |Mention                                            |TP entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------       
TP         |Buxheimer Chorgestühls                             |Buxheimer_Chorgestühl                              |Sladys Cathleen Bush († 6. Januar 1983), Reverend Mother St. Saviour’s Hospital, Verdienste um Rückführung des Buxheimer Chorgestühls aus England, verliehen 5. Mai 1981.                                                                                       
TP         |Panzer IV                                          |Panzerkampfwagen_IV                                |Da es der deutschen Rüstungsindustrie nicht gelang, der Wehrmacht die eigentlich vorgesehenen Standardpanzer der Typen Panzer III und Panzer IV in nennenswerter Stückzahl zur Verfügung zu stellen, bildete in den ersten beiden Jahren des Zweiten Weltkriegs der Panzer II mit knapp 1100 einsatzfähigen Fahrzeugen das Rückgrat der deutschen Panzerwaffe.
TP         |IV                                                 |Panzerkampfwagen_IV                                |Seine Feuerkraft war aber unzureichend, um Panzer der Typen Panzer  III oder IV zu vernichten.                                                                                                                                                                  
TP         |Panzers IV                                         |Panzerkampfwagen_IV                                |Die niedrige Silhouette erschwerte seine Entdeckung und Bekämpfung, die Form war beispielhaft und seine Feuerkraft entsprach der des Panzers IV und des Jagdpanzers IV/48.                                                                                      
TP         |Pz IV                                              |Panzerkampfwagen_IV                                |Etwa die Hälfte der Standard-Panzer (Pz IV) des Deutschen Reiches wurden hier hergestellt.                                                                                                                                                                      
TP         |Z 9001, KC 85/1 und KC 87                          |Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87  |Weitere vorgenommene Anpassungen gewährleisteten zusammen mit den ab diesem Zeitpunkt ebenfalls ausgelieferten Erweiterungsbaugruppen eine verbesserte Kompatibilität mit den ebenfalls von Robotron produzierten Kleincomputern Z 9001, KC 85/1 und KC 87 .    
TP         |Gewöhnliche Akelei                                 |Gemeine_Akelei                                     |Beispiele dafür sind die Gewöhnliche Akelei (Aquilegia vulgaris) und die Ästige Graslilie (Anthericum ramosum).                                                                                                                                                 
TP         |Akelei, Gemeine                                    |Gemeine_Akelei                                     |Akelei, Gemeine (Aquilegia vulgaris) – Familie: Ranunculaceae .                                                                                                                                                                                                 
TP         |Halophyten                                         |Salzpflanze                                        |Auf salzhaltigen Standorten, die in Wüsten recht häufig vorkommen, wachsen die Halophyten .                                                                                                                                                                     
TP         |salztoleranten Pflanzen                            |Salzpflanze                                        |Vor allem bei salztoleranten Pflanzen (Halophyten), die z.b. an den Meeresküsten wachsen.                                                                                                                                                                       
TP         |Fender-Rhodes-                                     |Fender_Rhodes                                      |Das Album wurde aufwendig produziert, Springsteen verwendete ein reichhaltiges Instrumentarium; zusätzlich zur üblichen Rockbesetzung wurden Klavier, Fender-Rhodes-E-Piano, Glockenspiel, Cembalo, Saxophon, Trompete (Randy Brecker), Flügelhorn und Hammond-Orgel eingesetzt.
TP         |Rhodes-Piano                                       |Fender_Rhodes                                      |Als Instrumente kommen E-Bass beziehungsweise Kontrabass, Tenorsaxophon, Klavier, Rhodes-Piano oder Vibraphon und mit Besen gespieltes Schlagzeug zum Einsatz.                                                                                                  
TP         |Fender Rhodes Electric Piano                       |Fender_Rhodes                                      |Das von ihm entwickelte „Fender Rhodes Electric Piano“ wurde zu einem wichtigen Bestandteil des Jazz, Rock, Pop und Soul.                                                                                                                                       
TP         |Rhodes                                             |Fender_Rhodes                                      |Tori Amos (Bösendorfer, Gesang, Rhodes, Wurlitzer, (ARP)), Adrian Belew, (Gitarre), Jon Evans (E-Bass), Matt Chamberlain (Schlagzeug),  John Philip Shenal (Streicherarrangement), Justin Meldal-Johnson (alternativer Bass), Mark Hawley und Marcel van Limbeek (Mix),Thomas Schenk (Photos) und viele andere.
```

## False negatives
```
Label      |Mention                                            |FN entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
FN         |regulieren                                         |Salzpflanze                                        |Sie dienen dazu, den Salzgehalt der Pflanze zu regulieren.                                                                                                                                                                                                      
FN         |Salzsteppe                                         |Salzpflanze                                        |Der Ort liegt in einer Salzsteppe – nur an den Ufern des perennierenden Flusses befindet sich Galeriewald.                                                                                                                                                      
FN         |über dem 30-Jahres-Mittel                          |Globale_Erwärmung                                  |In den ersten zehn Monaten des Jahres 2005 lagen die Werte um 1,04 °C über dem 30-Jahres-Mittel .                                                                                                                                                               
FN         |Z 9001                                             |Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87  |Trotz des Kalten Krieges und des damit verbundenen Hochtechnologie-Embargos CoCom gelang es 1984, mit Z 9001 und HC 900 in der DDR entwickelte Heimcomputer herzustellen.                                                                                       
FN         |Aquilegia vulgaris                                 |Gemeine_Akelei                                     |Bestimmte Arten besiedeln als Generalisten eine Vielzahl von Habitaten; so findet sich Aquilegia vulgaris sowohl in Fels-, Wald und Grasvegetation.                                                                                                             
FN         |1795                                               |Teilungen_Polens                                   |Polen nutzte die Schwäche des in den Russischen Bürgerkrieg verwickelten Sowjetrussland und griff es an, um im Osten Gebiete zurückzuerobern, die bis 1795 zu Zeiten von Polen-Litauen unter polnischer Herrschaft gestanden hatten.                            
FN         |Krustenflechten                                    |Flechte                                            |Die Sandsteinfelsen selbst weisen einen leichten Bewuchs mit Krustenflechten auf.                                                                                                                                                                               
FN         |Verteidigungsrede                                  |Apologie_(Platon)                                  |Sokrates wurde wegen Asebie zum Tode verurteilt (siehe Platons „Verteidigungsrede“ des Sokrates und seinen Dialog Kriton) .                                                                                                                                     
FN         |Berninatriebwagen                                  |Berninabahn                                        |In der Schweiz wurden die Einholmstromabnehmer bei der Rhätischen Bahn 1962 versuchsweise auf zwei Berninatriebwagen (37 und 38) und ab 1964 auf allen Neubaufahrzeugen, bei den SBB Re 4/4" versuchsweise ab 1967 (11107–09) und systematisch ab 1969 (ab 11156) aufgebaut, in Norwegen wurden sie erst ab 1985 eingeführt.
```

## Nearest neighbors (excellent dataset)
Entity: Buxheimer_Chorgestühl - TP
``` 
'Sladys Cathleen Bush († 6. Januar 1983), Reverend Mother St. Saviour’s Hospital, Verdienste um Rückführung des Buxheimer Chorgestühls aus England, verliehen 5. Mai 1981.'
<class 'list'>: [('Buxheimer_Chorgestühl', 0.5976174473762512), ('Buxheimer_Chorgestühl', 0.6574574708938599), ('Buxheimer_Chorgestühl', 0.6849910020828247), ('Burg_Rötteln', 0.8529830574989319), ('Adam_von_Trott_zu_Solz', 0.8545027375221252)]

'Kloster Buxheim mit dem Buxheimer Chorgestühl .'
<class 'list'>: [('Buxheimer_Chorgestühl', 0.6175221800804138), ('Buxheimer_Chorgestühl', 0.6360011696815491), ('Buxheimer_Chorgestühl', 0.6362478137016296), ('Buxheimer_Chorgestühl', 0.7346323132514954), ('Burg_Groitzsch', 0.751562774181366)]

Die Kirche besitzt ein hochbarockes, überreich ausgeschmücktes Chorgestühl aus Nussbaumholz, das 1715–1717 von Georg Anton Machein (1685–1739) und seiner Werkstatt geschaffen wurde und wie das Buxheimer Chorgestühl zur figürlich ausgestatteten Gruppe der „schwäbischen Akanthus-Chorgestühle“ gehört.
<class 'list'>: [('Buxheimer_Chorgestühl', 0.5818031430244446), ('Buxheimer_Chorgestühl', 0.6190299391746521), ('Buxheimer_Chorgestühl', 0.6775097250938416), ('Buxheimer_Chorgestühl', 0.7003189921379089), ('Buxheimer_Chorgestühl', 0.731023907661438)]
```
------

Entity: Panzerkampfwagen_IV - TP
```
Da es der deutschen Rüstungsindustrie nicht gelang, der Wehrmacht die eigentlich vorgesehenen Standardpanzer der Typen Panzer III und Panzer IV in nennenswerter Stückzahl zur Verfügung zu stellen, bildete in den ersten beiden Jahren des Zweiten Weltkriegs der Panzer II mit knapp 1100 einsatzfähigen Fahrzeugen das Rückgrat der deutschen Panzerwaffe.
<class 'list'>: [('Panzerkampfwagen_IV', 0.594403088092804), ('Panzerkampfwagen_IV', 0.6223129630088806), ('Panzerkampfwagen_IV', 0.6255852580070496), ('Panzerkampfwagen_IV', 0.6782673001289368), ('Panzerkampfwagen_IV', 0.6971943974494934)]

'Die Bewaffnung, eine 3,72-cm-Kanone L/47,8, war derjenigen der deutschen leichten Panzer überlegen, und auch die Panzerung der Front war mit 25 mm nur unwesentlich schwächer als die der Panzerkampfwagen III und IV (frühe Versionen ~30 mm).'
<class 'list'>: [('Panzerkampfwagen_IV', 0.5290290713310242), ('Panzerkampfwagen_IV', 0.7833786606788635), ('Panzerkampfwagen_IV', 0.8628944754600525), ('Panzerkampfwagen_IV', 0.8685219883918762), ('Panzerkampfwagen_IV', 0.8925269842147827)]

'Seine Kanone konnte zwar den deutschen Panzer III und Panzer IV, die ein Drittel des Panzerbestandes der Wehrmacht im Juni 1941 ausmachten, gefährlich werden, jedoch war seine Panzerung schwächer und seine Mobilität zu gering.'
<class 'list'>: [('Panzerkampfwagen_IV', 0.5443574786186218), ('Panzerkampfwagen_IV', 0.6129261255264282), ('Panzerkampfwagen_IV', 0.6449486017227173), ('Panzerkampfwagen_IV', 0.655887246131897), ('Panzerkampfwagen_IV', 0.6667240262031555)]

'Die niedrige Silhouette erschwerte seine Entdeckung und Bekämpfung, die Form war beispielhaft und seine Feuerkraft entsprach der des Panzers IV und des Jagdpanzers IV/48.'
<class 'list'>: [('Panzerkampfwagen_IV', 0.5672314167022705), ('Panzerkampfwagen_IV', 0.6187441945075989), ('Panzerkampfwagen_IV', 0.6368076801300049), ('Panzerkampfwagen_IV', 0.6418173909187317), ('Panzerkampfwagen_IV', 0.644843578338623)]

```
Entity: Panzerkampfwagen_IV - FN
```
'Etwa die Hälfte der Standard-Panzer (Pz IV) des Deutschen Reiches wurden hier hergestellt.'
<class 'list'>: [('Honda_NSX', 0.8897862434387207), ('M1_Abrams', 0.9130476117134094), ('Messerschmitt_Bf_108', 0.9194908142089844), ('STS-121', 0.9260827898979187), ('Messerschmitt_Bf_108', 0.9349502921104431)]
```
------

Entity: Robotron_Z_9001 - TP
```
'Weitere vorgenommene Anpassungen gewährleisteten zusammen mit den ab diesem Zeitpunkt ebenfalls ausgelieferten Erweiterungsbaugruppen eine verbesserte Kompatibilität mit den ebenfalls von Robotron produzierten Kleincomputern Z 9001, KC 85/1 und KC 87 .'
<class 'list'>: [('Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87', 0.7105315923690796), ('Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87', 0.7961461544036865), ('STS-1', 0.8715468645095825), ('STS-1', 0.8896685242652893), ('Microsoft_Windows_NT_3.1', 0.8936411738395691)]
```
Entity: Robotron_Z_9001 - FN
```
'Trotz des Kalten Krieges und des damit verbundenen Hochtechnologie-Embargos CoCom gelang es 1984, mit Z 9001 und HC 900 in der DDR entwickelte Heimcomputer herzustellen.'
<class 'list'>: [('M1_Abrams', 0.9495426416397095), ('USS_Thresher_(SSN-593)', 0.9607008099555969), ('Microsoft_Windows_NT_3.1', 0.9901816844940186), ('USS_Thresher_(SSN-593)', 0.994082510471344), ('USS_Thresher_(SSN-593)', 0.999332070350647)]
```
------

Entity: Globale_Erwärmung - TP
```
Damit kommt der Reduktion menschgemachter Schwefeloxidemissionen eine gewisse Relevanz in der Debatte um die globale Erwärmung zu, denn zumindest regional trägt Schwefelsäureverwitterung heute in erheblichem Maße zur natürlichen Karbonatverwitterung bei.
<class 'list'>: [('Globale_Erwärmung', 0.5372828245162964), ('Globale_Erwärmung', 0.54360431432724), ('Globale_Erwärmung', 0.5467216968536377), ('Globale_Erwärmung', 0.5734097361564636), ('Globale_Erwärmung', 0.5740107297897339)]

'Die Obstbäume sollen dazu beitragen, den Klimawandel zu stoppen und das Umweltbewusstsein sowie die Umweltbildung voranzutreiben.'
<class 'list'>: [('Globale_Erwärmung', 0.5852254033088684), ('Globale_Erwärmung', 0.5886877179145813), ('Globale_Erwärmung', 0.601567804813385), ('Globale_Erwärmung', 0.602410078048706), ('Globale_Erwärmung', 0.6395124793052673)]

'Allerdings taut das Eis auf Grund der globalen Erwärmung immer früher auf, was für die dort lebenden Eisbären zunehmend zur Bedrohung wird.'
<class 'list'>: [('Globale_Erwärmung', 0.5908368825912476), ('Globale_Erwärmung', 0.6156753301620483), ('Globale_Erwärmung', 0.6396892070770264), ('Globale_Erwärmung', 0.6556941866874695), ('Globale_Erwärmung', 0.6648976802825928)]
```
Entity: Globale_Erwärmung - FN
```
'In den ersten zehn Monaten des Jahres 2005 lagen die Werte um 1,04 °C über dem 30-Jahres-Mittel .'
<class 'list'>: [('Erythropoetin', 0.8738728165626526), ('U-Bahn_Berlin', 0.9046849608421326), ('Herz-Lungen-Wiederbelebung', 0.9286186695098877), ('Fürstenenteignung', 0.9293089509010315), ('InterCityExperimental', 0.9379472732543945)]
```

## Toy dataset: 'Baum'
* 2 Entities: 'Baum' und 'Baum_(Datenstruktur)'
* 6 Sätze pro Entity

### Evaluation results
```
Label      |Mention                                            |FN entity                                          |Sentence                             
------     |--------------------------------                   |------------------------------                     |---------------------------------------------------------------------------------
TP         |Bäume                                              |Baum_(Datenstruktur)                               |Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.                                                                                                                                                                              
TP         |Baum                                               |Baum_(Datenstruktur)                               |Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.                                                                                                                                                                                                    
TP         |Baum                                               |Baum_(Datenstruktur)                               |Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.                                                                                                                   
FN         |Baum                                               |Baum                                               |Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.             
TP         |Baum                                               |Baum                                               |Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.                                                                             
TP         |Baum                                               |Baum                                               |Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.                                                                                  
```

### Nearest neighbors
Entity: Baum_(Datenstruktur) - TP
```
'Binärbäume sind in der Informatik die am häufigsten verwendete Unterart der Bäume.'
<class 'list'>: [('Baum_(Datenstruktur)', 0.7276687026023865), ('Baum', 0.788140058517456), ('Baum', 0.8124741911888123), ('Baum', 0.813956618309021), ('Baum_(Datenstruktur)', 0.9829342365264893)]

'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.'
<class 'list'>: [('Baum_(Datenstruktur)', 0.6402598023414612), ('Baum', 0.6694390177726746), ('Baum', 0.8944177627563477), ('Baum', 0.9251293540000916), ('Baum_(Datenstruktur)', 0.9450399279594421)]

'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.'
<class 'list'>: [('Baum_(Datenstruktur)', 0.5761043429374695), ('Baum', 0.7123711705207825), ('Baum_(Datenstruktur)', 0.8777676224708557), ('Baum', 0.9040076732635498), ('Baum', 0.9416137337684631)]
```
-----

Entity: Baum - TP
``` 
'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.'
<class 'list'>: [('Baum', 0.636604905128479), ('Baum_(Datenstruktur)', 0.6838067173957825), ('Baum', 0.7196763157844543), ('Baum', 0.7200324535369873), ('Baum_(Datenstruktur)', 0.9561135172843933)]

'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.'
<class 'list'>: [('Baum', 0.6356381773948669), ('Baum', 0.6585741639137268), ('Baum', 0.6621947288513184), ('Baum_(Datenstruktur)', 0.8742358088493347), ('Baum_(Datenstruktur)', 0.9532246589660645)]
```
Entity: Baum - FN
``` 
'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.'
<class 'list'>: [('Baum_(Datenstruktur)', 0.6486752033233643), ('Baum', 0.7490174174308777), ('Baum_(Datenstruktur)', 0.9003958106040955), ('Baum', 0.9382489919662476), ('Baum', 0.9400196075439453)]
```


## Sentence Tokenizer 
### Main steps
1. **Text normalization**: Convert all whitespace characters to spaces, and (for the Uncased model) lowercase the input and strip out accent markers. E.g., ```John Johanson's, → john johanson's,```.

2. **Punctuation splitting**: Split all punctuation characters on both sides (i.e., add whitespace around all punctuation characters). Punctuation characters are defined as (a) Anything with a P* Unicode class, (b) any non-letter/number/space ASCII character (e.g., characters like $ which are technically not punctuation). E.g., ```john johanson's, → john johanson ' s ,```

3. **WordPiece tokenization**: Apply whitespace tokenization to the output of the above procedure, and apply WordPiece tokenization to each token separately. (Our implementation is directly based on the one from tensor2tensor, which is linked). E.g., ```john johanson ' s , → john johan ##son ' s ,```

### German examples
```
Amina Claudine Myers (* 21. März 1943[1] in Blackwell, Arkansas) ist eine US-amerikanische Jazzmusikerin (Pianistin, Organistin und Sängerin).
['amin', '##a', 'c', '##lau', '##dine', 'mye', '##rs', '(', '*', '21', '.', 'mar', '##z', '1943', '[', '1', ']', 'in', 'black', '##well', ',', 'ark', '##ansa', '##s', ')', 'ist', 'eine', 'us', '-', 'amerikanische', 'jazz', '##musiker', '##in', '(', 'pianist', '##in', ',', 'organist', '##in', 'und', 'sanger', '##in', ')', '.']
```
```
Eva Gaëlle Green [ˌɛ.va.ˈgʁeːn] (* 6. Juli 1980 in Paris) ist eine französische Schauspielerin. Sie wurde 2003 durch ihre Rolle in Bernardo Bertoluccis Film Die Träumer bekannt und war 2016 für den Golden Globe nominiert.
['eva', 'gael', '##le', 'green', '[', '[UNK]', '.', 'va', '.', 'ˈ', '##g', '##ʁ', '##e', '##ː', '##n', ']', '(', '*', '6', '.', 'juli', '1980', 'in', 'pari', '##s', ')', 'ist', 'eine', 'fra', '##nzo', '##sische', 's', '##chau', '##spieler', '##in', '.', 'sie', 'wurde', '2003', 'durch', 'ihre', 'rolle', 'in', 'bern', '##ardo', 'be', '##rto', '##lu', '##cci', '##s', 'film', 'die', 'tra', '##ume', '##r', 'bekannt', 'und', 'war', '2016', 'fur', 'den', 'golden', 'globe', 'nominiert', '.']
```
```
Euphorie (gr. ευφορία, lat. euphoria, euforia) bezeichnet eine vorübergehende, subjektiv wahrgenommene überschwängliche Gemütsverfassung.
['eu', '##ph', '##orie', '(', 'gr', '.', 'ε', '##υ', '##φο', '##ρια', ',', 'lat', '.', 'eu', '##ph', '##oria', ',', 'eu', '##for', '##ia', ')', 'bezeichnet', 'eine', 'voru', '##berg', '##ehen', '##de', ',', 'sub', '##jekt', '##iv', 'wa', '##hr', '##genommen', '##e', 'u', '##bers', '##ch', '##wang', '##liche', 'ge', '##mut', '##s', '##ver', '##fassung', '.']
```
```
Die Tanganjika-Lachepidemie war eine 1962 in Tanganjika (heute Teil von Tansania) aufgetretene Epidemie von Lachanfällen, die mehrere Monate andauerte und etwa 1000 meist junge Personen betraf.
['die', 'tangan', '##jik', '##a', '-', 'lac', '##he', '##pide', '##mie', 'war', 'eine', '1962', 'in', 'tangan', '##jik', '##a', '(', 'heute', 'teil', 'von', 'tan', '##san', '##ia', ')', 'auf', '##getreten', '##e', 'epi', '##demie', 'von', 'lac', '##han', '##fallen', ',', 'die', 'mehrere', 'mon', '##ate', 'anda', '##uert', '##e', 'und', 'etwa', '1000', 'meist', 'junge', 'personen', 'bet', '##raf', '.']
```
```
Die Erkrankung hat den Charakter einer Psychose und äußert sich unter anderem in religiösen Wahnvorstellungen: Der oder die Betroffene identifiziert sich z. B. in einigen Fällen mit einer heiligen Person aus dem Alten oder Neuen Testament und gibt sich als diese aus.
['die', 'er', '##kra', '##nku', '##ng', 'hat', 'den', 'charakter', 'einer', 'ps', '##ych', '##ose', 'und', 'außer', '##t', 'sich', 'unter', 'anderem', 'in', 're', '##ligi', '##osen', 'wa', '##hn', '##vor', '##stellungen', ':', 'der', 'oder', 'die', 'bet', '##roffen', '##e', 'ide', '##nti', '##fiziert', 'sich', 'z', '.', 'b', '.', 'in', 'einigen', 'fallen', 'mit', 'einer', 'heiligen', 'person', 'aus', 'dem', 'alten', 'oder', 'neuen', 'testament', 'und', 'gibt', 'sich', 'als', 'diese', 'aus', '.']
```

### English examples
```
Students of Ascended Master Teachings organizations (also known as Ascended Master Activities) believe that their doctrine has been given to humanity by the Ascended Masters, individuals believed to have lived in physical bodies, acquired the wisdom and mastery needed to become immortal and free of the cycles of "re-embodiment" and karma, and have attained their "ascension", a state of "one-ness" with God.
['students', 'of', 'as', '##cended', 'master', 'teaching', '##s', 'organizations', '(', 'also', 'known', 'as', 'as', '##cended', 'master', 'activities', ')', 'believe', 'that', 'their', 'doctrine', 'has', 'been', 'given', 'to', 'humanity', 'by', 'the', 'as', '##cended', 'masters', ',', 'individuals', 'believed', 'to', 'have', 'lived', 'in', 'physical', 'bodies', ',', 'acquired', 'the', 'wis', '##dom', 'and', 'master', '##y', 'needed', 'to', 'become', 'im', '##mortal', 'and', 'free', 'of', 'the', 'cycles', 'of', '"', 're', '-', 'em', '##bod', '##iment', '"', 'and', 'kar', '##ma', ',', 'and', 'have', 'att', '##ained', 'their', '"', 'as', '##cension', '"', ',', 'a', 'state', 'of', '"', 'one', '-', 'nes', '##s', '"', 'with', 'god', '.']
```
```
Lucifer (/ˈluːsɪfər/ LEW-si-fər; "light-bringer") is a Latin name for the planet Venus as the morning star in the ancient Roman era, and is often used for mythological and religious figures associated with the planet.
['lu', '##ci', '##fer', '(', '/', 'ˈ', '##lu', '##ː', '##s', '##ɪ', '##fə', '##r', '/', 'le', '##w', '-', 'si', '-', 'f', '##ər', ';', '"', 'light', '-', 'bring', '##er', '"', ')', 'is', 'a', 'latin', 'name', 'for', 'the', 'planet', 'ven', '##us', 'as', 'the', 'morning', 'star', 'in', 'the', 'ancient', 'roman', 'era', ',', 'and', 'is', 'often', 'used', 'for', 'my', '##th', '##ological', 'and', 'religious', 'figures', 'associated', 'with', 'the', 'planet', '.']
```
```
Sabrina the Teenage Witch is a comic book series published by Archie Comics about the adventures of a fictional American teenager named Sabrina Spellman.
['sa', '##bri', '##na', 'the', 'teen', '##age', 'wit', '##ch', 'is', 'a', 'comic', 'book', 'series', 'published', 'by', 'archi', '##e', 'comics', 'about', 'the', 'adventure', '##s', 'of', 'a', 'fictional', 'american', 'teen', '##ager', 'named', 'sa', '##bri', '##na', 'spell', '##man', '.']
```
```
Game of Thrones is an American fantasy drama television series created by David Benioff and D. B. Weiss for HBO. 
['game', 'of', 'throne', '##s', 'is', 'an', 'american', 'fantasy', 'drama', 'television', 'series', 'created', 'by', 'da', '##vid', 'beni', '##off', 'and', 'd', '.', 'b', '.', 'wei', '##ss', 'for', 'h', '##bo', '.']
```

