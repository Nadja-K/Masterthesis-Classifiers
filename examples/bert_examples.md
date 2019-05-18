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
*Note: all FN samples have in this case a notably higher distance (>0.8) than in comparison to the TP samples (~0.5-0.7)*

Entity: Buxheimer_Chorgestühl - TP
``` 
'Sladys Cathleen Bush († 6. Januar 1983), Reverend Mother St. Saviour’s Hospital, Verdienste um Rückführung des Buxheimer Chorgestühls aus England, verliehen 5. Mai 1981.'
<class 'list'>: [
('Buxheimer_Chorgestühl', 0.5976174473762512, 'Sein Sohn Graf Hugo Waldbott, ein berüchtigter Bankrotteur, ließ 1883 das kunsthistorisch berühmte Buxheimer Chorgestühl nach England versteigern.'), 
('Buxheimer_Chorgestühl', 0.6574574708938599, 'Bereits 1883 wurde das kunsthistorisch berühmte Buxheimer Chorgestühl im Auftrag des Grafen nach England versteigert.'), 
('Buxheimer_Chorgestühl', 0.6849910020828247, 'Im Auftrag des Priors Johannes Bilstein schuf er für die Kartause von Buxheim  von 1687 bis 1691 die Bildwerke des Chorgestühls und von 1699 bis 1700 die Schnitzwerke des Zelebrantensitzes und zweier Seitenaltäre.')
]

'Kloster Buxheim mit dem Buxheimer Chorgestühl .'
<class 'list'>: [
('Buxheimer_Chorgestühl', 0.6175221800804138, 'Bereits 1883 wurde das kunsthistorisch berühmte Buxheimer Chorgestühl im Auftrag des Grafen nach England versteigert.'), 
('Buxheimer_Chorgestühl', 0.6360011696815491, 'Sein Sohn Graf Hugo Waldbott, ein berüchtigter Bankrotteur, ließ 1883 das kunsthistorisch berühmte Buxheimer Chorgestühl nach England versteigern.'), 
('Buxheimer_Chorgestühl', 0.6362478137016296, 'Ignaz Waibel (1661–1733), Holzbildhauer, gestorben in Heimertingen; schuf unter anderem das Chorgestühl in der Kartause Buxheim .')
]

Die Kirche besitzt ein hochbarockes, überreich ausgeschmücktes Chorgestühl aus Nussbaumholz, das 1715–1717 von Georg Anton Machein (1685–1739) und seiner Werkstatt geschaffen wurde und wie das Buxheimer Chorgestühl zur figürlich ausgestatteten Gruppe der „schwäbischen Akanthus-Chorgestühle“ gehört.
<class 'list'>: [
('Buxheimer_Chorgestühl', 0.5818031430244446, 'Sein Sohn Graf Hugo Waldbott, ein berüchtigter Bankrotteur, ließ 1883 das kunsthistorisch berühmte Buxheimer Chorgestühl nach England versteigern.'), 
('Buxheimer_Chorgestühl', 0.6190299391746521, 'Bereits 1883 wurde das kunsthistorisch berühmte Buxheimer Chorgestühl im Auftrag des Grafen nach England versteigert.'), 
('Buxheimer_Chorgestühl', 0.6775097250938416, 'Der größte Kirchenschatz ist das barocke Chorgestühl, das Ignaz Waibl in den Jahren von 1687 bis 1691 schuf.')
]
```
------

Entity: Panzerkampfwagen_IV - TP
```
Da es der deutschen Rüstungsindustrie nicht gelang, der Wehrmacht die eigentlich vorgesehenen Standardpanzer der Typen Panzer III und Panzer IV in nennenswerter Stückzahl zur Verfügung zu stellen, bildete in den ersten beiden Jahren des Zweiten Weltkriegs der Panzer II mit knapp 1100 einsatzfähigen Fahrzeugen das Rückgrat der deutschen Panzerwaffe.
<class 'list'>: [
('Panzerkampfwagen_IV', 0.594403088092804, 'In den 1930er Jahren fertigte das Grusonwerk erste Prototypen des Panzer I, später dann die Panzer IV (bis Ende 1941 als einziger Hersteller) und auf der Basis des Panzer IV das Sturmgeschütz IV sowie den Geschützwagen IV (Selbstfahrlafette Dicker Max), außerdem verschiedene Sonderkraftfahrzeuge (Sd.Kfz.).'), 
('Panzerkampfwagen_IV', 0.6223129630088806, 'Kampfgruppe Stephan stand nur eine Einheit entgegen: Die 8th Hussars, Teil der 4th Armoured Brigade, mit schätzungsweise 50 M3 Stuart, die gegen etwa 120 deutsche Panzer kämpften (die meisten davon Panzer III und Panzer IV).'), 
('Panzerkampfwagen_IV', 0.6255852580070496, 'Da wurden Panzerkampfwagen und Panzerhaubitzen repariert, wo auch die Reparatur von Panzer IV eingesetzt.')
]

'Die Bewaffnung, eine 3,72-cm-Kanone L/47,8, war derjenigen der deutschen leichten Panzer überlegen, und auch die Panzerung der Front war mit 25 mm nur unwesentlich schwächer als die der Panzerkampfwagen III und IV (frühe Versionen ~30 mm).'
<class 'list'>: [
('Panzerkampfwagen_IV', 0.5290290713310242, 'Etwa 1942 begannen die Entwicklungen der E-Reihe, um die zu dieser Zeit vorhandenen Panzertypen III und IV und die größeren Panther und Tiger zu ersetzen.'), 
('Panzerkampfwagen_IV', 0.7833786606788635, 'Kampfgruppe Stephan stand nur eine Einheit entgegen: Die 8th Hussars, Teil der 4th Armoured Brigade, mit schätzungsweise 50 M3 Stuart, die gegen etwa 120 deutsche Panzer kämpften (die meisten davon Panzer III und Panzer IV).'), 
('Panzerkampfwagen_IV', 0.8628944754600525, 'Vom Heereszeugamt wurde die Panzer-Division Schlesien mit 21 Panzern des Typ IV ausgestattet, im März 1945 kamen weitere 20 Panzer hinzu.')
]

'Seine Kanone konnte zwar den deutschen Panzer III und Panzer IV, die ein Drittel des Panzerbestandes der Wehrmacht im Juni 1941 ausmachten, gefährlich werden, jedoch war seine Panzerung schwächer und seine Mobilität zu gering.'
<class 'list'>: [
('Panzerkampfwagen_IV', 0.5443574786186218, 'Kampfgruppe Stephan stand nur eine Einheit entgegen: Die 8th Hussars, Teil der 4th Armoured Brigade, mit schätzungsweise 50 M3 Stuart, die gegen etwa 120 deutsche Panzer kämpften (die meisten davon Panzer III und Panzer IV).'), 
('Panzerkampfwagen_IV', 0.6129261255264282, 'Da wurden Panzerkampfwagen und Panzerhaubitzen repariert, wo auch die Reparatur von Panzer IV eingesetzt.'), 
('Panzerkampfwagen_IV', 0.6449486017227173, 'Vom Heereszeugamt wurde die Panzer-Division Schlesien mit 21 Panzern des Typ IV ausgestattet, im März 1945 kamen weitere 20 Panzer hinzu.')
]

'Die niedrige Silhouette erschwerte seine Entdeckung und Bekämpfung, die Form war beispielhaft und seine Feuerkraft entsprach der des Panzers IV und des Jagdpanzers IV/48.'
<class 'list'>: [
('Panzerkampfwagen_IV', 0.5672314167022705, 'Da wurden Panzerkampfwagen und Panzerhaubitzen repariert, wo auch die Reparatur von Panzer IV eingesetzt.'), 
('Panzerkampfwagen_IV', 0.6187441945075989, 'Das Panzer-Regiment 39 wurde kurz danach mit 50 neuen Panzerkampfwagen IV aufgefüllt.'), 
('Panzerkampfwagen_IV', 0.6368076801300049, 'Sein Panzerkampfwagen IV sowie ein Panzerkampfwagen 35(t) und ein Panzerkampfwagen 38(t) wurden während eines Panzergefechtes von einem polnischen TKS abgeschossen.')
]

```
Entity: Panzerkampfwagen_IV - FN
```
'Etwa die Hälfte der Standard-Panzer (Pz IV) des Deutschen Reiches wurden hier hergestellt.'
<class 'list'>: [
('Honda_NSX', 0.8897862434387207, 'Die restlichen vier Werkswagen kamen aus Japan; zwei Honda NSX GTi und zwei Nissan Skyline GT-R LM .'), 
('M1_Abrams', 0.9130476117134094, 'Anfangs steuert der Spieler den schweren Kampfpanzer M1A1 Abrams, später übernimmt man eine UAV-Drohne.'), 
('Messerschmitt_Bf_108', 0.9194908142089844, 'Die Fliegertruppen der Legion Condor nutzen diesen Flugplatz mit Maschinen vom Typ Ju 52, Junkers W 34, Bf 108, Klemm L25 und Jagdflugzeugstaffel mit He 51 als Stützpunkt.')
]
```
------

Entity: Robotron_Z_9001 - TP
```
'Weitere vorgenommene Anpassungen gewährleisteten zusammen mit den ab diesem Zeitpunkt ebenfalls ausgelieferten Erweiterungsbaugruppen eine verbesserte Kompatibilität mit den ebenfalls von Robotron produzierten Kleincomputern Z 9001, KC 85/1 und KC 87 .'
<class 'list'>: [
('Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87', 0.7105315923690796, 'Für die Aus- und Weiterbildung wurden auch Kleincomputer wie der KC 85 und KC 87 verwendet.'), 
('Robotron_Z_9001,_Robotron_KC_85/1,_Robotron_KC_87', 0.7961461544036865, 'Ab Mitte der 1980er Jahre wurden neben professionellen Computern zwar auch Konsumgüter wie der Home-Computer Robotron KC 87 produziert, aber bis zum Ende der DDR blieben die Produktionszahlen solcher Geräte eher gering.'), 
('STS-1', 0.8715468645095825, 'Anschließend war er Mitglied der Unterstützungsmannschaften für die ersten drei Shuttle-Missionen STS-1, STS-2 und STS-3 am Kennedy Space Center.')
]
```
Entity: Robotron_Z_9001 - FN
```
'Trotz des Kalten Krieges und des damit verbundenen Hochtechnologie-Embargos CoCom gelang es 1984, mit Z 9001 und HC 900 in der DDR entwickelte Heimcomputer herzustellen.'
<class 'list'>: [
('M1_Abrams', 0.9495426416397095, 'Der erste Lizenznehmer der L/44-Kanone, General Dynamics, führte sie 1986 als M256 bei der A1-Version des M1 Abrams ein.'), 
('USS_Thresher_(SSN-593)', 0.9607008099555969, 'Im April 1963 ging die Skylark mit dem U-Boot USS Thresher (SSN-593) auf dessen Erprobungsfahrten, bei denen die Thresher verloren ging.'), 
('Microsoft_Windows_NT_3.1', 0.9901816844940186, 'Ab Windows NT 3.1 wird stattdessen die grafische Datenträgerverwaltung () verwendet und ab Windows 2000 steht zusätzlich das Konsolenprogramm diskpart zur Verfügung.')
]
```
------

Entity: Globale_Erwärmung - TP
```
Damit kommt der Reduktion menschgemachter Schwefeloxidemissionen eine gewisse Relevanz in der Debatte um die globale Erwärmung zu, denn zumindest regional trägt Schwefelsäureverwitterung heute in erheblichem Maße zur natürlichen Karbonatverwitterung bei.
<class 'list'>: [
('Globale_Erwärmung', 0.5372828245162964, 'Der Bericht beschreibt für die 15 größten Industrienationen die notwendigen technologischen Maßnahmen, um die globale Erwärmung bis zum Jahr 2050 auf 2 °C zu begrenzen (vgl. Zwei-Grad-Ziel) .'), 
('Globale_Erwärmung', 0.54360431432724, 'Diese Aussagen sind seit Jahren die dominierende Basis der politischen und wissenschaftlichen Diskussionen über die globale Erwärmung .'), 
('Globale_Erwärmung', 0.5467216968536377, 'Weitere Kritikpunkte waren die hohe Umweltbelastung in Form von Emissionen von Schadstoffen wie Ruß und Stickoxiden; später dann auch von Kohlenstoffdioxid, das zu den wichtigsten Treibhausgasen zählt und maßgeblich die aktuelle globale Erwärmung mitverursacht.')
]

'Die Obstbäume sollen dazu beitragen, den Klimawandel zu stoppen und das Umweltbewusstsein sowie die Umweltbildung voranzutreiben.'
<class 'list'>: [
('Globale_Erwärmung', 0.5852254033088684, 'Miranda Schreurs arbeitet in den Bereichen umweltpolitische Governance, Policy und Politik des Klimawandels, Energiepolitik, soziale Bewegungen sowie Umweltpolitik Deutschlands, der EU, der USA und Ostasiens.'), 
('Globale_Erwärmung', 0.5886877179145813, 'Die Kernidee: Neuwälder, die mit ihrem Wachstum den Klimawandel auf natürliche Weise abbremsen werden (durch die CO2-Bindung im Holz) – mit einem Konzept, welches auf die nachhaltige Nutzung für die Begünstigung klimarelevanter Aspekte ausgerichtet ist.'), 
('Globale_Erwärmung', 0.601567804813385, 'Viele Artikel richten sich gegen sozialstaatliche wie auch umweltpolitische Maßnahmen, es wird zum Beispiel der Klimawandel bestritten.')
]

'Allerdings taut das Eis auf Grund der globalen Erwärmung immer früher auf, was für die dort lebenden Eisbären zunehmend zur Bedrohung wird.'
<class 'list'>: [
('Globale_Erwärmung', 0.5908368825912476, 'Relativ bekannt wurde das große Experiment ATOC (Acoustic Thermography of the Ocean Climate) im Pazifik, mit dem die nötigen großräumigen Mittelungen zur Bestimmung der globalen Erwärmung erreicht werden sollten.'), 
('Globale_Erwärmung', 0.6156753301620483, 'Der mit der globalen Erwärmung begründete Eingriff in die traditionell bewährte und gesundheitlich vorteilhafte Bauphysik historischer Gebäude gibt nicht nur Vermietern und Mietern energetisch sanierter Häuser und Wohnungen Anlass zu juristischen Auseinandersetzungen.'), 
('Globale_Erwärmung', 0.6396892070770264, 'Der Mensch erhöht indirekt den Wasserdampfgehalt in der Atmosphäre, weil durch die globale Erwärmung die Lufttemperatur und damit die Verdunstungsrate steigen.')
]
```
Entity: Globale_Erwärmung - FN
```
'In den ersten zehn Monaten des Jahres 2005 lagen die Werte um 1,04 °C über dem 30-Jahres-Mittel .'
<class 'list'>: [
('Erythropoetin', 0.8738728165626526, 'Er wurde daraufhin wegen EPO-Missbrauchs für zwei Jahre gesperrt.'), 
('U-Bahn_Berlin', 0.9046849608421326, 'Im Jahr 1929 war geplant, das wachsende Weißensee an das U-Bahn-Netz anzuschließen.'), 
('Herz-Lungen-Wiederbelebung', 0.9286186695098877, 'Neben der üblichen Beratung veranstaltet der BDS Kurse über Herz-Lungen-Wiederbelebung, Erste Hilfe, Wasserrettung, Notfallmaßnahmen, Aqua-Fitness, Tauchen und Wasserspringen.')
]
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
<class 'list'>: [
('Baum_(Datenstruktur)', 0.7276687026023865, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum', 0.788140058517456, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. '), 
('Baum', 0.8124741911888123, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.'), 
('Baum', 0.813956618309021, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum_(Datenstruktur)', 0.9829342365264893, 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird. ')
]

'Im Ergebnis erhält man einen Baum, wie den rechts gezeigten.'
<class 'list'>: [
('Baum_(Datenstruktur)', 0.6402598023414612, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum', 0.6694390177726746, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum', 0.8944177627563477, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.'), 
('Baum', 0.9251293540000916, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. '), 
('Baum_(Datenstruktur)', 0.9450399279594421, 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird. ')
]

'Ein solcher Baum lässt sich durch Klassen für die verschiedenen Elemente und Verwendung von Aggregationen gut als Objektstruktur beschreiben.'
<class 'list'>: [
('Baum_(Datenstruktur)', 0.5761043429374695, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum', 0.7123711705207825, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum_(Datenstruktur)', 0.8777676224708557, 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird. '), 
('Baum', 0.9040076732635498, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. '), 
('Baum', 0.9416137337684631, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.')
]
```
-----

Entity: Baum - TP
``` 
'Die Edel-Tanne ist ein immergrüner Baum, der die größten Wuchshöhen unter den Tannen erreicht, es werden Wuchshöhen über 80 Meter und Stammdurchmesser (BHD) über 2 Meter erreicht.'
<class 'list'>: [
('Baum', 0.636604905128479, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum_(Datenstruktur)', 0.6838067173957825, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum', 0.7196763157844543, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.'), 
('Baum', 0.7200324535369873, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. '), 
('Baum_(Datenstruktur)', 0.9561135172843933, 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird. ')
]

'Die Korb-Weide wächst als sommergrüner Strauch (nur selten als Baum) mit besonders langen Ruten (Ästen, Zweigen) und erreicht Wuchshöhen von 3 bis 8, im Extremfall 10 Metern.'
<class 'list'>: [
('Baum', 0.6356381773948669, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.'), 
('Baum', 0.6585741639137268, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. '), 
('Baum', 0.6621947288513184, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum_(Datenstruktur)', 0.8742358088493347, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum_(Datenstruktur)', 0.9532246589660645, 'Die Darstellung des DNS-Namensraumes erfolgt als Wurzelbaum.')
]
```
Entity: Baum - FN
``` 
'Nach altem chinesischen Verständnis ist Penjing die Kunst, eine Harmonie zwischen den Naturelementen, der belebten Natur und dem Menschen in miniaturisierter Form darzustellen: Die belebte Natur wird hierbei meist durch einen Baum dargestellt.'
<class 'list'>: [
('Baum_(Datenstruktur)', 0.6486752033233643, 'In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp, mit dem sich hierarchische Strukturen abbilden lassen. Die durch die Hierarchie vorgegebenen Objekte nennt man Knoten.'), 
('Baum', 0.7490174174308777, 'Als Baum wird im allgemeinen Sprachgebrauch eine verholzte Pflanze verstanden, die aus einer Wurzel, einem daraus emporsteigenden, hochgewachsenen Stamm und einer belaubten Krone besteht.'), 
('Baum_(Datenstruktur)', 0.9003958106040955, 'Diesen Anforderungen werden dagegen die auf einer höheren Komplexitätsstufe stehenden kontextsensitiven Grammatiken (Typ 1) und kontextfreien Grammatiken (Typ 2) gerecht, z. B. Chomskys „Phrasenstrukturgrammatik“, in der die Ableitung eines Satzes als Baumstruktur dargestellt wird. '), 
('Baum', 0.9382489919662476, 'Die Pflanzenarten dieser Familie sind meist immergrüne (einige Eucalyptus-Arten sind laubabwerfend) Gehölze: Bäume und Sträucher.'), 
('Baum', 0.9400196075439453, 'Die Vertreter der Rosengewächse sind Bäume, Sträucher oder krautige Pflanzen, wobei die strauchige Wuchsform als die ursprüngliche innerhalb der Familie angesehen wird. ')
]
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

