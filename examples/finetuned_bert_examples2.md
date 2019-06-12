# Notes
- All examples here contain the top5 nearest neighbor sentences on the geraete_large dataset, as well as the context sentences that were not returned in the top5 list.
- The missed context sentences are split into two categories:
  1. Trivial: the mention of the query sentence is the same as the mention of the context sentence (not entity!)
  2. Non-Trivial: the mention of the query sentence is different from the metion of the context sentence (not entity!)
- Examples marked with *** are either interesting or tricky cases.
- The complete log including ALL evaluated samples can be found in `C:\Users\Nadja\Desktop\Masterthesis - Experiments\console_output.txt`
- From looking at the nn sentences, it can be seen that while the suggested nearest neighbor sentences are sometimes wrong (wrong entity), the main topic between the query sentence as well as the suggested nn sentences seems to always be quite similar (helicopter example, steam example, war examples in general, ...)

## FP Examples without any missed context sentences
### Ambiguous people
These cases are almost always tricky because the query will be for a specific person with a name that also refers to other people that lived during different times.

Note: 
``` 
FP | entity: Martin_Auer_(Musiker,_1976) | mention: Martin Auer (Musiker, 1976) | sentence: Martin Auer (Musiker, 1976) (* 1976), Jazztrompeter.
entity: Martin_Auer_(Musiker,_1963) | score: 0.17717 | mention: Martin Auer (Musiker, 1963) | sentence: Martin Auer (Musiker, 1963) (* 1963), deutscher Jazztrompeter.
entity: Martin_Auer_(Musiker,_1963) | score: 0.42480 | mention: Auer, Martin | sentence: Auer, Martin (* 1963), deutscher Jazztrompeter.
entity: Martin_Auer_(Musiker,_1976) | score: 0.43410 | mention: Auer, Martin | sentence: Auer, Martin (* 1976), deutscher Jazztrompeter und Flügelhornist.
entity: Martin_Nauer | score: 0.62380 | mention: Nauer, Martin | sentence: Nauer, Martin (* 1952), Schweizer Akkordeon- und Schwyzerörgelispieler.
entity: Martin_Fondse | score: 0.68068 | mention: Fondse, Martin | sentence: Fondse, Martin (* 1967), niederländischer Jazzmusiker (Piano, Arrangement, Komposition).
```
``` 
FP | entity: Martin_Auer_(Musiker,_1976) | mention: Martin Auer | sentence: Martin Auer (* 1976), Jazzmusiker.
entity: Martin_Auer_(Musiker,_1963) | score: 0.24072 | mention: Auer, Martin | sentence: Auer, Martin (* 1963), deutscher Jazztrompeter.
entity: Martin_Auer_(Musiker,_1976) | score: 0.26273 | mention: Auer, Martin | sentence: Auer, Martin (* 1976), deutscher Jazztrompeter und Flügelhornist.
entity: Martin_Auer_(Musiker,_1963) | score: 0.51859 | mention: Martin Auer (Musiker, 1963) | sentence: Martin Auer (Musiker, 1963) (* 1963), deutscher Jazztrompeter.
entity: Martin_Nauer | score: 0.55227 | mention: Nauer, Martin | sentence: Nauer, Martin (* 1952), Schweizer Akkordeon- und Schwyzerörgelispieler.
entity: Martin_Nauer | score: 0.55717 | mention: Martin Nauer | sentence: Martin Nauer (* 1952).
```
Note:
``` 
FP | entity: Johnny_De_Droit | mention: De Droit, Johnny | sentence: De Droit, Johnny (1892–1986), US-amerikanischer Jazz-Kornettist.
entity: Johnny_Müller | score: 0.52112 | mention: Müller, Johnny | sentence: Müller, Johnny (1915–1990), deutscher Mundharmonikasolist, Klarinetten- und Saxophonspieler.
entity: Johnny_De_Droit | score: 0.52424 | mention: Johnny De Droit | sentence: Der neueren Jazzforschung zufolge war das Stück in New Orleans unter dem Titel Number Two weithin bekannt, dessen Komponist Johnny De Droit war.
entity: Johnny_Parker_(Pianist) | score: 0.58655 | mention: Parker, Johnny | sentence: Parker, Johnny (1929–2010), britischer Jazz-Pianist.
entity: Johnny_Bernero | score: 0.62642 | mention: Bernero, Johnny | sentence: Bernero, Johnny (1931–2001), US-amerikanischer Rockabilly-Musiker und Schlagzeuger.
entity: Johnny_Müller | score: 0.65428 | mention: Johnny Müller | sentence: Die Originalmusik wurde jedoch vom Jazzmusiker Johnny Müller eingespielt.
```

### Very ambiguous entities
Note: for this example the suggested nn sentences all fit since they all refer to the same event except to different places. However, the places are not always mentioned within the context sentence, which makes this such a difficult example. Even as a human reader the suggested nn sentences seem plausible.
``` 
FP | entity: Maria_Himmelfahrt_(Kaltern) | mention: Maria Himmelfahrt (Kaltern) | sentence: Maria Himmelfahrt (Kaltern), Kaltern, Südtirol.
entity: Mariä_Himmelfahrt_(Erbendorf) | score: 0.49447 | mention: Mariä Himmelfahrt | sentence: St. Josef mit Jesus; Mariä Himmelfahrt, Erbendorf (1941).
entity: Mariä_Himmelfahrt_(Markt_Wald) | score: 0.52048 | mention: Mariä Himmelfahrt | sentence: Das Gebäude befindet sich nordwestlich der Kirche Mariä Himmelfahrt und steht unter Denkmalschutz.
entity: Mariä_Himmelfahrt_(Spabrücken) | score: 0.53847 | mention: Maria Himmelfahrt | sentence: Der Guardian Werner Rost gründete 1680 das Kloster Maria Himmelfahrt in Spabrücken, das allerdings bereits 1681 von Kölner Franziskanern übernommen wurde.
entity: Mariä_Himmelfahrt_(Spabrücken) | score: 0.54230 | mention: Pfarr- und Wallfahrtskirche Mariä Himmelfahrt | sentence: Pfarr- und Wallfahrtskirche Mariä Himmelfahrt, Spabrücken .
entity: Maria_Himmelfahrt_(Kaltern) | score: 0.55008 | mention: Maria Himmelfahrt | sentence: Die dem Heiligen Vigilius von Trient geweihte Kuratiekirche der Pfarrei Maria Himmelfahrt in Kaltern steht auf einer Porphyrkuppe, auf der einst auch eine heute verschwundene Burganlage bestand.
```

### Cases with numbers
Bert seems to have difficulties differentiating between entities that are similar but contain different numbers. However, for some of the examples the suggested nn sentences (even if they are FP sentences) are plausible for a human reader and might get mixed up even by human readers.

Note: The top1 nn suggestion for this example is a FP. However, it DOES contain a mention of a 500-Series GPU which is why this is a very difficult case.
``` 
FP | entity: Nvidia-GeForce-500-Serie | mention: Geforce GT 520 | sentence: Die erste Grafikkarte mit PureVideo HD der fünften Generation (manchmal als VP5 abgekürzt) war die Geforce GT 520 .
entity: Nvidia-GeForce-200-Serie | score: 0.38418 | mention: GeForce GTX 285 | sentence: Die GeForce GTX 580 ist die erste Grafikkarte von Nvidia im High-End-Sektor seit der GeForce GTX 285, bei der die GPU in der Vollausbaustufe eingesetzt wird.
entity: Nvidia-GeForce-500-Serie | score: 0.45640 | mention: GeForce GTX 590 | sentence: Die Karte wies eine um ca. 40 Prozent höhere Performance gegenüber ihrem Vorgänger, der GeForce GTX 590, auf.
entity: Nvidia-GeForce-500-Serie | score: 0.58816 | mention: GeForce GT 545 (DDR3) und GTX 555 | sentence: Am 24. April wurde das Verfahren mit der GeForce GT 545 (DDR3) und GTX 555 als GeForce GT 640 und GT 645 wiederholt.
entity: Nvidia-GeForce-500-Serie | score: 0.61358 | mention: GeForce-500-Serie | sentence: Die GeForce-600-Serie ist eine Serie von Desktop-Grafikchips der Firma Nvidia und Nachfolger der GeForce-500-Serie.
entity: Nvidia-GeForce-400-Serie | score: 0.62409 | mention: GeForce-400-Serie | sentence: Die GeForce-500-Serie ist eine Serie von Desktop-Grafikchips des Unternehmens Nvidia und Nachfolger der GeForce-400-Serie.
```
Note: 
``` 
FP | entity: Akai_MPC_1000 | mention: Akai MPC 1000 | sentence: Akai MPC 1000 (2003), neues Produkt der MPC Familie klein und günstig und mit USB-Anschluss und Compactflash Karte.
entity: Akai_MPC_60 | score: 0.46140 | mention: Akai MPC 60 | sentence: Leiber hatte sich gerade ein Akai MPC 60 zugelegt und begonnen, damit zu experimentieren.
entity: Akai_MPC_60 | score: 0.50915 | mention: Akai MPC 60 | sentence: Endtroducing wurde ausschließlich mit dem Sampler und Sequenzer Akai MPC 60 produziert.
entity: Akai_MPC_1000 | score: 0.54121 | mention: MPC 1000 | sentence: Diese waren vor der Entwicklung der MPC 1000 unter dem Namen MIDI Production Center bekannt.
entity: IBM_Personal_Computer | score: 0.65329 | mention: IBM-PC | sentence: Die IBM-PC mit dem 16-Bit-Prozessor 8088 von Intel konnten unter dem Betriebssystem MS-DOS nicht mehr als 640 Kilobyte an RAM nutzen.
entity: IBM_Personal_Computer | score: 0.69576 | mention: IBM PC | sentence: Nachdem 1981 der erste IBM PC auf dem Markt veröffentlicht wurde, änderten die Byte-Macher ihre Veröffentlichungspolitik.
```
Note: 
``` 
FP | entity: RS-28_(Rakete) | mention: RS-28 | sentence: Aufgrund der noch nicht vollendeten Entwicklung der neuen ballistischen Interkontinentalrakete RS-28, wurde diese Übergangslösung für die Bestückung mit dem benannten Hyperschallkörper, der selbst über einen oder mehrere atomare Sprengköpfe zwischen 1 und 2 Megatonnen verfügen kann, entschieden.
entity: Radio_Sputnik_(Satellit) | score: 0.52017 | mention: RS-16 | sentence: Neben der Erforschung von Navigations- und Steuerungstechnik diente er auch als Amateurfunksatellit RS-16.
entity: Radio_Sputnik_(Satellit) | score: 0.57107 | mention: RS-14 | sentence: Für Amateurfunkzwecke war der Satellit als AMSAT-OSCAR 21 (Westen) bzw. RS-14 (Osten) bekannt.
entity: RS-28_(Rakete) | score: 0.59174 | mention: RS-28 (Rakete) | sentence: RS-28 (Rakete), eine russische Interkontinentalrakete.
entity: Radio_Sputnik_(Satellit) | score: 0.67776 | mention: RS-47 | sentence: Ab dem 30. November 2014 sendete Kosmos 2499 als Amateurfunksatellit Telemetrie-Signale im 70-Zentimeter-Band auf 435,465 MHz in CW mit dem Rufzeichen RS-47 .
entity: R-7 | score: 0.70637 | mention: R-7 | sentence: Die Entwicklung und Erprobung der ersten funktionsfähigen Interkontinentalrakete R-7 durch die Sowjetunion 1957 verursachte im Westen den sogenannten Sputnik-Schock .
```


### Other cases
Note: this one is very tricky because the FP nn sentences all refer to something that would fit (helicopter). This proves that the main topic of a sentence CAN be captured (and compared to other sentences) with bert embeddings.
``` 
FP | entity: Polizeihubschrauberstaffel_Sachsen-Anhalt | mention: Polizeihubschrauberstaffel Sachsen-Anhalt | sentence: Polizeihubschrauberstaffel Sachsen-Anhalt (ICAO-Code), siehe Polizeihubschrauber #Liste der Hubschrauberstaffeln der Bundespolizei und Landespolizeien .
entity: Polizeihubschrauber | score: 0.56054 | mention: Polizeihubschrauber | sentence: Wasserschutzpolizei nebst Polizeihubschrauber&shy;staffel .
entity: Polizeihubschrauberstaffel_Sachsen-Anhalt | score: 0.56541 | mention: Polizeihubschrauberstaffel | sentence: Als Zentrale Sonderdienste waren der Landesbereitschaftspolizei weiterhin die Polizeihubschrauberstaffel, das Landespolizeiorchester sowie das Polizeiärztliche Zentrum/Ärztlicher Gutachterdienst, die Heilfürsorge und die Landesstelle für polizeiliche Medienarbeit zugeordnet.
entity: Polizeihubschrauber | score: 0.59238 | mention: Polizeihubschrauber | sentence: An der Stelle, an der heute die Polizeihubschrauber der Hessischen Polizei stehen, wurde eine Halle für Segelflugzeuge errichtet.
entity: Polizeihubschrauber | score: 0.59540 | mention: Polizeihubschrauber | sentence: Zusätzlich werden Polizeihubschrauber eingesetzt, die am Standort Fuhlendorf stationiert sind und dem Bundespolizei-Flugdienst der Bundespolizeidirektion 11 zugeordnet sind.
entity: Polizeihubschrauber | score: 0.64327 | mention: Polizeihubschrauber | sentence: Bekannte Beispiele im zivilen Bereich sind die Rettungs- und Polizeihubschrauber.
```
Note: 
``` 
FP | entity: Waterman_Aerobile | mention: Aerobile | sentence: Am 21. März 1937 führte er den Jungfernflug des Arrowbile oder Aerobile durch.
entity: Volvo_Aero | score: 0.75610 | mention: Volvo Aero | sentence: Es gab Kontakte nach Schweden, und so konnte eine Lizenzfertigung bei Volvo Aero eingerichtet werden.
entity: Aero_A.200 | score: 0.77393 | mention: Aero A.200 | sentence: Die technische Bewertung dauerte bis zum 4. September und die meisten Punkte errangen die Bf 108 (450–452 Punkte), danach die Pallavicino PS-1 (438), Fi 97 (428–431), Aero A.200 (429) und RWD-9 (427).
entity: Aérospatiale | score: 0.80509 | mention: Aérospatiale | sentence: Die Aérospatiale AS 332 ist ein Hubschrauber des französischen Herstellers Aérospatiale, später Eurocopter und heute Airbus Helicopters.
entity: Aérospatiale | score: 0.83177 | mention: Aérospatiale | sentence: Die Aérospatiale SA 321 Super Frelon („Super-Hornisse“) ist ein mittelschwerer Transporthubschrauber des französischen Herstellers Aérospatiale.
entity: Waterman_Aerobile | score: 0.83507 | mention: Waterman Arrowbile | sentence: Das erste erfolgreich geflogene Autoflugzeug mit Tragflächen war das Waterman Arrowbile von Waldo Waterman aus dem Jahr 1937.
```

## FP Examples with missed context sentences
### Ambiguous people

### Very ambiguous entities
Note: 
``` 
FP | entity: Christuskirche_(Flensburg) | mention: Christuskirche | sentence: In den 1950er Jahren beteiligte sich die Bundeswehr am Bau der Christuskirche, die seitdem mit als Garnisonkirche des Stützpunktes dient.
entity: Christuskirche_(Detmold) | score: 0.21816 | mention: Christuskirche | sentence: Ebenfalls im Jahr 1908 wurde in Detmold die neuerbaute Christuskirche eingeweiht, in deren Gruft fortan die Gebeine der Linie Lippe-Biesterfeld bestattet wurden.
entity: Christuskirche_(Landshut) | score: 0.21910 | mention: Christuskirche | sentence: Es besteht eine gewisse Verwechslungsgefahr mit der Christuskirche im Westen Landshuts, da diese ursprünglich auch als Erlöserkirche bezeichnet wurde.
entity: Christuskirche_(Flensburg) | score: 0.24498 | mention: Christuskirche | sentence: In der am Rand des Stadtbezirks liegenden Fördestraße befindet sich weiterhin die Christuskirche die als Garnisonkirche dient.
entity: Christuskirche_(Flensburg) | score: 0.24847 | mention: Christuskirche | sentence: Im Stadtteil Mürwik befindet sich heute die nächste Garnisonkirche, die Christuskirche am Rande der Marineschule Mürwik .
entity: Christuskirche_(Flensburg) | score: 0.25567 | mention: Christuskirche | sentence: Im Gegensatz zur größeren nahezu zeitgleich gebauten evangelischen Christuskirche an der Fördestraße, befindet sich die St.-Ansgar-Kirche somit versteckt jenseits der Hauptstraßen Mürwiks.

Trivial missed context sentences (query sentence mention == context sentence mention): 
mention: Christuskirche | sentence: Anfang des 20. Jahrhunderts lag ungefähr an der Stelle zwischen der Christuskirche und dem KBA der Osbek-Hof.
mention: Christuskirche | sentence: Christus als Weltenrichter, Muschelkalkrelief an der Christuskirche Flensburg-Mürwik, 1958.
mention: Christuskirche | sentence: Die Mürwiker Christuskirche liegt unterhalb des Placks und ist zu Fuß in zehn Minuten erreichbar.
mention: Christuskirche | sentence: Die Kapelle ist nicht mit der Christuskirche im Stadtteil Mürwik zu verwechseln.
mention: Christuskirche | sentence: Zudem ist er in der Gemeindearbeit der Christuskirche involviert.

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Kirchengemeinde Mürwik | sentence: Als Gymnasiast betätigte er sich als Kindergottesdienst&shy;helfer in der Kirchengemeinde Mürwik bei dem Pastor und späteren Propst und Bischof Karl Ludwig Kohlwage.
```
Note: 
``` 
FP | entity: St._Martin_(Zürich-Fluntern) | mention: katholische Kirche St. Martin | sentence: Die 1938 erbaute katholische Kirche St. Martin an der Krähbühlstrasse führt die Tradition des Martinspatroziniums weiter.
entity: St._Martin_(Kirchberg_an_der_Iller) | score: 0.37736 | mention: Katholische Pfarrkirche St. Martin | sentence: Mai: Katholische Pfarrkirche St. Martin, Kirchberg an der Iller 	.
entity: Stiftskirche_St._Martin_und_St._Severus | score: 0.41115 | mention: Katholische Pfarrkirche St. Martin und St. Severus | sentence: Katholische Pfarrkirche St. Martin und St. Severus, ehemalige Stiftskirche, Münstermaifeld .
entity: St._Martin_(Linden) | score: 0.42649 | mention: Kirche St. Martin | sentence: Der Friedhof wurde 1862 angelegt als Begräbnisstätte der evangelisch-lutherischen Gemeinde der Kirche St. Martin, nachdem der Industrielle Georg Egestorff der Gemeinde das Grundstück hierfür geschenkt hatte.
entity: St._Martin_(Zürich-Fluntern) | score: 0.43721 | mention: Kirche St. Martin | sentence: Aber die städtische Liegenschaftenverwaltung war nicht bereit, die alte Kirche den Katholiken abzutreten, weshalb nordöstlich von ihr an der Krähbühlstrasse in den Jahren 1938–1939 die katholische Kirche St. Martin errichtet wurde.
entity: St.-Martinus-Kirche_(Olpe) | score: 0.44853 | mention: St.-Martinus-Kirche | sentence: An der nach einem Brand neu errichteten St.-Martinus-Kirche in Olpe schuf er als erstes größeres Werk die Kreuzigungsgruppe mit Madonna über dem Hauptportal.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: St. Martin (Zürich-Fluntern) | sentence: Genau das gleiche Element findet sich auch an der Südseite der ebenfalls von Anton Higi erbauten Kirche St. Martin (Zürich-Fluntern) .
```
Note: *** The mention of the query sentence is extremely ambiguous and it makes sense that the wrong nn sentences were returned. The missed context sentence does not even mention trumpets or drums at all (instead flutes). This makes this an even more difficult sample.
```  
FP | entity: Spielzeuginstrument | mention: Spielzeugtrompete und -Trommeln | sentence: Im ersten Bild tritt im „Tanz des Großvaters“ eine Bühnenmusik aus spielenden Kindern auf, die mit obligater Spielzeugtrompete und -Trommeln sowie mit Spielzeugbecken sowie Kuckucks- und Wachtelflöten (in C-Dur) ad libitum besetzt ist.
entity: Trompete | score: 0.67000 | mention: Trompete | sentence: Es gibt eine Reihe von Notensätzen für Instrumente: Keyboard, Gitarre, Flöte, Oboe, Oboenduo, Klarinette, Klarinettenduo und  Trompete .
entity: Trompete | score: 0.68621 | mention: Trompete | sentence: Der Internationale Aeolus Bläserwettbewerb wird für die Musikinstrumente Flöte, Oboe, Klarinette, Fagott, Saxophon, Trompete, Horn, Posaune und Tuba ausgerichtet.
entity: Trompete | score: 0.69009 | mention: Trompete | sentence: Mit sieben Jahren lernte er Klavier zu spielen, später kamen Gitarre, Sitar und Trompete dazu.
entity: Batá-Trommel | score: 0.73558 | mention: batá-Trommel | sentence: So erlauben etwa die Yoruba bis heute nicht den Gebrauch der zeremoniell zu Ehren des Gottes Shango eingesetzten batá-Trommel.
entity: Spielzeuginstrument | score: 0.73849 | mention: Spielzeuginstrument | sentence: Sie ist auch für Kinder leicht erlernbar und eignet sich daher auch als Spielzeuginstrument .

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Spielzeuginstrument | sentence: Pfeifen dienen auch als Spielzeuginstrument für Kinder.
```
Note: *** the suggested entities actually fit because they refer to something that is very related although slightly different.
``` 
FP | entity: Random-Access_Memory | mention: RAM-Bausteinen | sentence: Eine bei vorhandenem EPROM-Programmiergerät sehr kostengünstige Lösung bieten auch schon einfache Simulatoren aus batteriegepufferten RAM-Bausteinen mit Schreibschutzschalter, die am EPROM-Programmiergerät programmiert und danach mit aktiviertem Schreibschutz auf die Testschaltung gesteckt werden.
entity: Dynamic_Random_Access_Memory | score: 0.57107 | mention: DRAM-Baustein | sentence: Die Column Address Strobe Latency (CL) misst die Verzögerung zwischen der Adressierung (Adressierung einer Spalte) in einem DRAM-Baustein und der Bereitstellung der an dieser Adresse gespeicherten Daten.
entity: RAM-Disk | score: 0.68596 | mention: RAM-Disk | sentence: Das funktioniert, weil sich das gesamte Betriebssystem samt Abspielsoftware bereits vollständig im Arbeitsspeicher in einer RAM-Disk befindet.
entity: Random-Access_Memory | score: 0.71633 | mention: RAM | sentence: Durch dieses Feature ist es möglich, ohne Änderung des ROMs bzw. der darin enthaltenen Firmware die Erweiterung in den RAM zu laden und jederzeit durch Austausch der Speicherkarte zu deaktivieren.
entity: Random-Access_Memory | score: 0.72869 | mention: Ram-Speichers | sentence: Guilty Gear trumpfte zu seinem Erscheinen mit bildschirmfüllenden Special Moves auf Sonys Konsole auf, die bis dato aufgrund des limitierten Ram-Speichers damals auf der Playstation als nicht realisierbar galten.
entity: RAM-Disk | score: 0.73684 | mention: RAM-Disk | sentence: Es ist ähnlich wie ein Dateisystem was in einer RAM-Disk verwendet wird, aber einfacher als dieses, weil es keine physikalischen Strukturen simulieren muss.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: RAM | sentence: RAM: 64 MB (19 MB nach Start verfügbar).
mention: RAM | sentence: Das Legend wird von einem 600 MHz Qualcomm MSM 7227 Prozessor betrieben und hat 384 MB RAM.
mention: RAM- | sentence: Innerhalb eines Mikrobefehlzyklus kann sowohl die CPU als auch ein Ein-Ausgabe-Kontroller auf einen externen 16 kB umfassenden RAM-Datenspeicher (RAM, engl. )
mention: RAM | sentence: Es hat einen Quad-Core-Prozessor vom Typ Snapdragon 800 und 2 GB RAM.
mention: RAM | sentence: DNF arbeitet schneller und benötigt weniger RAM .
```

### Cases with numbers
Note: *** this one is a very difficult case in my opinion and yet the correct entity is the top2 result.
``` 
FP | entity: Mercedes-Benz_O_405_GTD | mention: Mercedes-Benz O 405 GTD | sentence: So wiegt beim Typ Mercedes-Benz O 405 GTD allein die elektrische Ausrüstung sechs Tonnen.
entity: Mercedes-Benz_O_405_GN | score: 0.31186 | mention: Mercedes-Benz O 405 GN | sentence: Dargestellt werden Fahrzeuge des Typs Mercedes-Benz O 405 GN und Citaro 2 G .
entity: Mercedes-Benz_O_405_GTD | score: 0.38316 | mention: Mercedes-Benz O 405 GTD | sentence: Von 1990 bis 2005 wurden sie durch den SVE mit Duo-Bussen des Typs Mercedes-Benz O 405 GTD bedient.
entity: Mercedes-Benz_M_159 | score: 0.49284 | mention: Mercedes-Benz M 159 | sentence: Der Motor ist der R6-Ottomotor Mercedes-Benz M 159 mit Vergaser, der 60 PS (44 kW) aus 2,6 l Hubraum leistet.
entity: Mercedes-Benz_OM_300_(groß) | score: 0.53422 | mention: Mercedes-Benz OM 325 | sentence: Der L 325 wird von dem 1954 eingeführten Dieselmotor Mercedes-Benz OM 325 angetrieben.
entity: Mercedes-Benz_OM_654 | score: 0.56726 | mention: Mercedes-Benz OM 654 | sentence: Die E-Klasse der Baureihe 213 ist als erste Baureihe mit dem neu entwickelten Dieselmotor Mercedes-Benz OM 654 erhältlich.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: O 405 GTD | sentence: Nachfolger der O 305 GTD-Kleinserie ist der in 47 Exemplaren gebaute Typ O 405 GTD .
mention: O 405 GTD | sentence: Ihm folgten acht weitere Prototypen verschiedener Bauarten, bevor ab 1988 die 19 Serienwagen der Baureihe O 405 GTD ausgeliefert wurden.
```
Note: *** another difficult example where the top2 result is the correct entity. It should be noted that the query sentence itself isn't exactly informative. This makes this an even more difficult sample.
``` 
FP | entity: Mercedes-Benz_O_405_GTD | mention: Mercedes-Benz O 405 GTD | sentence: Mercedes-Benz O 405 GTD, Obusfahrzeug.
entity: Mercedes-Benz_O_405_GN | score: 0.42871 | mention: Mercedes-Benz O 405 GN | sentence: Dargestellt werden Fahrzeuge des Typs Mercedes-Benz O 405 GN und Citaro 2 G .
entity: Mercedes-Benz_O_405_GTD | score: 0.47445 | mention: Mercedes-Benz O 405 GTD | sentence: Von 1990 bis 2005 wurden sie durch den SVE mit Duo-Bussen des Typs Mercedes-Benz O 405 GTD bedient.
entity: Mercedes-Benz_M_159 | score: 0.55774 | mention: Mercedes-Benz M 159 | sentence: Der Motor ist der R6-Ottomotor Mercedes-Benz M 159 mit Vergaser, der 60 PS (44 kW) aus 2,6 l Hubraum leistet.
entity: Mercedes-Benz_OM_300_(groß) | score: 0.61259 | mention: Mercedes-Benz OM 325 | sentence: Der L 325 wird von dem 1954 eingeführten Dieselmotor Mercedes-Benz OM 325 angetrieben.
entity: Mercedes-Benz-Werk_Wörth | score: 0.64644 | mention: Mercedes-Benz-Werk Wörth | sentence: Die Fahrzeuge dieser Reihe werden im Mercedes-Benz-Werk Wörth gebaut.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: O 405 GTD | sentence: Nachfolger der O 305 GTD-Kleinserie ist der in 47 Exemplaren gebaute Typ O 405 GTD .
mention: O 405 GTD | sentence: Ihm folgten acht weitere Prototypen verschiedener Bauarten, bevor ab 1988 die 19 Serienwagen der Baureihe O 405 GTD ausgeliefert wurden.
```
Note: *** very difficult example in my opinion. The query sentence as well as the wrong nn sentences are very similar and even the mentions. They only differentiate slightly in terms of their numbers.
``` 
FP | entity: Jaguar_XJ_13 | mention: Jaguar XJ 13 | sentence: Der LM SCF XJ 13, der dem Jaguar XJ 13 nachempfunden ist, wird von Sports Car Factory aus den USA importiert.
entity: Jaguar_XJ_(Mark_I) | score: 0.32965 | mention: Jaguar XJ 12 | sentence: Außerdem war der Miami Spyder mit dem Zwölfzylindermotor vom Jaguar XJ 12 im Angebot.
entity: Jaguar_XJ_13 | score: 0.35181 | mention: Jaguar XJ 13 | sentence: Der Tredicim ähnelte dem Jaguar XJ 13, war aber keine direkte Nachbildung, da er länger und breiter war.
entity: Jaguar_XJ_(Mark_I) | score: 0.41069 | mention: Jaguar XJ 12 | sentence: Allerdings hatte dieses Modell nicht mehr die Alleinstellung wie der Quattroporte I, denn mittlerweile gab es auch den Mercedes 450 SEL 6,9 und den Jaguar XJ 12, die vergleichbare Fahrleistungen und die Perfektion der größeren Serie boten.
entity: Jaguar_XJ_(Mark_I) | score: 0.43236 | mention: Jaguar XJ 12 | sentence: Ein V12-Motor vom Jaguar XJ 12 trieb das Fahrzeug an.
entity: Jaguar_XJ_13 | score: 0.43449 | mention: Jaguar XJ 13 | sentence: Dies war ein Nachbau des Jaguar XJ 13.

Trivial missed context sentences (query sentence mention == context sentence mention): 
mention: Jaguar XJ 13 | sentence: Bei der Vorstellung des Jaguar E-Type mit V12-Motor und obenliegender Nockenwelle sollte es auch Filmaufnahmen des einzigen Fahrgestells des Jaguar XJ 13 geben.

Difficult missed context sentences (query sentence mention != context sentence mention): 
-
```
Note: *** very difficult because these are very ambiguous entities that refer to something almost identical
``` 
FP | entity: Focke-Achgelis_Fa_223 | mention: Focke-Achgelis Fa 223 | sentence: Auch der erste Transporthubschrauber der Welt, die Focke-Achgelis Fa 223, war im Krieg in Serienbau gegangen.
entity: Focke-Achgelis_Fa_330 | score: 0.32535 | mention: Focke-Achgelis Fa 330 | sentence: Als Ersatz für die Kriegsmarine diente der Focke-Achgelis Fa 330 Erkundungstragschrauber.
entity: Focke-Achgelis_Fa_330 | score: 0.36926 | mention: Focke-Achgelis Fa 330 | sentence: Einen Einmann-Tragschrauber aus der Zeit des Zweiten Weltkriegs stellte die Focke-Achgelis Fa 330 dar, der in größerer Stückzahl gebaut wurde.
entity: Focke-Achgelis_Fa_330 | score: 0.41562 | mention: Focke-Achgelis Fa 330 | sentence: Vom Wintergarten aus wurden für Beobachtungsaufgaben auch motorlose, vom U-Boot geschleppte Kleintragschrauber wie die Focke-Achgelis Fa 330 gestartet.
entity: Focke-Achgelis_Fa_223 | score: 0.80309 | mention: Fa 223 | sentence: Im August 1939 verließ ein neuer Hubschrauber das Werk, der Prototyp der Fa 223.
entity: Focke-Achgelis_Fa_330 | score: 0.83874 | mention: Fa 330 „Bachstelze“ | sentence: Ein weiterer technisch anspruchsvoller Entwurf war der Hubschrauber Fa 330 „Bachstelze“, für den Klages am 3. März 1944 den „Dr.-Fritz-Todt-Preis in Stahl“ erhielt.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Fa 223 | sentence: Auf diesen wurde ein Rotor einer Fa 223 gesetzt.
```
Note: *** difficult because the query sentence contain a different entity that is actually refered to by the top1 sentence.
``` 
FP | entity: Moskwitsch-410 | mention: Moskwitsch-410 | sentence: Ebenfalls auf Basis des Moskwitsch-402 gab es ein höhergelegtes Fahrzeug mit Allradantrieb, den Moskwitsch-410, dessen Technik später auf den Stand des Moskwitsch-407 gebracht wurde.
entity: Moskwitsch-407 | score: 0.36526 | mention: Moskwitsch-407 | sentence: Er ist der Nachfolger des Moskwitsch-407 und erhielt bereits größtenteils die neu entwickelten Fahrwerksteile seines Nachfolgers Moskwitsch-408.
entity: Moskwitsch-410 | score: 0.37769 | mention: Moskwitsch-410 | sentence: Unter der Bezeichnung Moskwitsch-423 (russisch ???????-423) wurde von 1957 bis 1958 eine Version als Kombi gebaut, mit dem Moskwitsch-410 gab es auch eine Ausführung als Geländewagen.
entity: Moskwitsch-407 | score: 0.43168 | mention: Moskwitsch-407 | sentence: Motor und Getriebe sowie große Teile des Chassis stammten vom Moskwitsch-407.
entity: Moskwitsch-407 | score: 0.44514 | mention: Moskwitsch-407 | sentence: Motortyp: „MZMA-407“, aus dem Personenwagen Moskwitsch-407 .
entity: Moskwitsch-410 | score: 0.49151 | mention: Moskwitsch-410N | sentence: Unter der Bezeichnung Moskwitsch-423N (russisch ???????-423?) wurde bis 1963 eine Version als Kombi gebaut, der Moskwitsch-430 ist ein Kastenwagen und mit dem Moskwitsch-410N gab es auch eine Ausführung als Geländewagen.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Moskwitsch-410N | sentence: Moskwitsch-410N – Version des Fahrzeugs mit Limousinenkarosse, aber mit einem geländetauglichen Fahrwerk und Allradantrieb .
```
Note: numbers
``` 
FP | entity: Porsche_944 | mention: Porsche 944 | sentence: Der 924 ist die Grundlage für weitere Fahrzeugneuentwicklungen wie die des Porsche 944 und dessen Nachfolger Porsche 968 .
entity: Porsche_906 | score: 0.40380 | mention: Porsche 906 | sentence: Porsche hatte durch den Bau von 50 Fahrzeugen die Homologation des Porsche 906 für die Rennklasse der Sportwagen-Prototypen geschafft.
entity: Porsche_944 | score: 0.40759 | mention: Porsche 944 | sentence: Der Porsche 944 Turbo Cup Frankreich war eine französische Rennserie, die als Markenpokal für Porsche 944 Turbos ausgetragen wurde.
entity: Porsche_906 | score: 0.40990 | mention: Porsche 906 | sentence: Sein letzter Sieg war der Triumph beim Großen Preis der Avus 1967 auf einem Porsche 906 .
entity: Porsche_356 | score: 0.48060 | mention: Porsche 356 | sentence: Ungewöhnlich am 2002 präsentierten New Speedster, einer modernen Interpretation des Porsche 356 als Speedster, war die Verwendung eines Frontmotors vom Mini Metro bzw. Rover 100.
entity: Porsche_968 | score: 0.49760 | mention: Porsche 968 | sentence: Dieser Auffassung, welcher das Berufungsgericht noch zuneigte, ist der Bundesgerichtshof im Porsche-Urteil (es ging um einen Porsche 968 Cabrio) nicht gefolgt.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Porsche 944 S | sentence: Ein Jahr später fuhr er mit einem Porsche 944 S in der Escort Endurance Series auf den dritten Rang in der Saisonwertung.
mention: 944 Turbo | sentence: Ihm folgten u.a. der Strosek 944 Turbo und nicht zuletzt das 911er Modell als „Flatnose“ mit Projektionsscheinwerfern.
mention: Porsche 944 Turbo | sentence: Im darauffolgenden Jahr startete er nochmals mit einem Porsche 944 Turbo in einigen Rennen der Trans-Am-Meisterschaft.
```
Note: for this one the mention is quite different (SS-24), however while the top2 suggested nn sentences are wrong, they still refer to rockets for war purposes (which is the same as the SS-24 or RT-23). It would also be difficult for a human reader to know that SS-24 and RT-23 are synonyms.
``` 
FP | entity: RT-23 | mention: SS-24 | sentence: SS-24 "Scalpel" oder RT-23 .
entity: R-12_(Rakete) | score: 0.74646 | mention: R-12 | sentence: Dort waren Raketen des Typs R-12 stationiert.
entity: R-12_(Rakete) | score: 0.75293 | mention: R-12 | sentence: Auch als Zugmittel für die nukleare Mittelstreckenrakete R-12 kam die Sattelzugmaschine zum Einsatz.
entity: RT-23 | score: 0.75437 | mention: RT-23 | sentence: Geplant war, das eisenbahngestützte Raketensystem RT-23 unabhängiger betreiben zu können.
entity: Typ_11_Leichtes_Maschinengewehr | score: 0.76194 | mention: Typ-11-6,5-mm-MGs | sentence: Rechts vom Fahrer saß ein Schütze, der eines der vier Typ-11-6,5-mm-MGs bediente.
entity: RS-28_(Rakete) | score: 0.77018 | mention: RS-28 (Rakete) | sentence: RS-28 (Rakete), eine russische Interkontinentalrakete.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: RT-23 | sentence: Eingesetzt wurden sie unter anderem für die Bespannung der Eisenbahn-Raketen-Komplexe RT-23 »Molodjec«.
mention: RT-23 | sentence: Der MAZ-7904 war einer von mehreren Versuchen Mitte der 1980er-Jahre, das eisenbahngestützte Interkontinentalraketensystem RT-23 auf ein Radfahrzeug zu verlasten.
mention: RT-23 | sentence: Bereits zu Beginn der 1980er-Jahre wurden bei MAZ unter dem Projektnamen Zelina-2 verschiedene Versuche unternommen, das bis dahin eisenbahngestützte Interkontinentalraketensystem RT-23 auf Radfahrzeuge zu verlasten.
mention: RT-23 | sentence: Der militärische Eisenbahnraketenkomplex () war ein von der Sowjetunion in den frühen 1980er Jahren in Dienst gestellter Zug, welcher mit Interkontinentalraketen vom Typ RT-23 bewaffnet war.
```
Note: *** This is probably a rather bad example where bert seems to fail. The query sentence refers to a helicopter (although it is very difficult even for a human reader to see this), while the top1 suggested nn sentence refers to a car. However, the top2 suggested nn sentence is for the correct GT entitiy.
``` 
FP | entity: Robinson_R66 | mention: R66 | sentence: Das neueste Modell ist zurzeit die R66 – ein Fünfsitzer, der erstmals mit einem Turbinenantrieb ausgestattet ist.
entity: Volkswagen_R | score: 0.73317 | mention: R | sentence: Auf der IAA 2009 wurde der Golf R als Nachfolger des Golf R32 vorgestellt.
entity: Robinson_R66 | score: 0.80637 | mention: Robinson R66 | sentence: Als Nachfolger des Erfolgsmodells Bell 206, steht die 505 in direkter Konkurrenz zur Robinson R66 .
entity: RMS_Rhone | score: 0.85307 | mention: RMS Rhone | sentence: RMS Rhone, ein gesunkenes Schiff.
entity: M548 | score: 0.86956 | mention: M548 | sentence: Es wurde vom Transportfahrzeug M548 abgeleitet.
entity: BMW_N52 | score: 0.88238 | mention: N52 | sentence: Dort ersetzte er den Sechszylinder N52 und wird seitdem sukzessive auch in anderen Baureihen verwendet.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Robinson R66 | sentence: Robinson R66, Hubschrauber der US-amerikanischen Firma Robinson Helicopters.
mention: Robinson R66 | sentence: Arch hatte gut 1019 Stunden Flugerfahrung, davon knapp 184 auf dem Helikopter Robinson R66.
mention: Robinson R66 | sentence: Höller war ab 2010 mit dem österreichischen Kunstflugpiloten und Red-Bull-Air-Race-Weltmeister Hannes Arch liiert, der am 8. September 2016 mit seinem Helikopter (Robinson R66) kurz nach dem Start von der Elberfelder Hütte in Kärnten abstürzte und dabei ums Leben kam.
```
Note: *** here the GT entity is already in itself very ambiguous. It makes sense that bert + annoy would have trouble mapping sentences to this entity to begin with (especially since there are other entities that refer to something similar, albeit more specified and not as ambiguous)
``` 
FP | entity: Mercedes-Benz_OM_470/OM_471/OM_472/OM_473 | mention: Typ OM 473 | sentence: Der integrierte Primärretarder dieser Kupplung leistet maximal 350 kW (476 PS) – im Vergleich dazu: Die Bremsleistung des Dieselmotors Typ OM 473 beträgt maximal 475 kW (646 PS).
entity: Mercedes-Benz_OM_457 | score: 0.70190 | mention: OM 457 | sentence: Das Fahrzeug ist unter anderem mit dem Mercedes-Benz Reihensechszylindermotor OM 457 erhältlich, der nach der Einführung der Abgasnorm Euro 6 in Europa nicht mehr vermarktet werden kann und nun von BFDA in Lizenz vor Ort gefertigt wird.
entity: Mercedes-Benz_OM_457 | score: 0.72876 | mention: OM 457 LA | sentence: Bis Euro-5-Norm wurde in den genannten Omnibussen die Baureihe OM 457 LA (11,97-Liter-Reihensechszylinder mit Pumpe-Leitung-Düse-Einspritzung) eingesetzt.
entity: Mercedes-Benz_OM_470/OM_471/OM_472/OM_473 | score: 0.77504 | mention: OM 470 | sentence: OM 470, mehrere Varianten:.
entity: Tatra_603 | score: 0.78236 | mention: Typs 603 | sentence: Er hatte den luftgekühlten 2,5-Liter-V8-Motor des Typs 603 eingebaut und verfügte über 12 Sitzplätze.
entity: Laurin_&_Klement_E | score: 0.82642 | mention: Typ E | sentence: Der Laurin & Klement C2 mit der Bezeichnung 12/14 HP vom Typ E abgeleitet, war jedoch deutlich kleiner.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Motoren | sentence: Mercedes hat seit 2015 alle Motoren für die Euro VI-Norm neu entwickelt.
```

### Other cases
Note: 
``` 
FP | entity: Altenberger_Dom | mention: Zisterzienserabtei Altenberg | sentence: Aber auch figürliche Motive wurden eingefügt, wie in der Zisterzienserabtei Altenberg.
entity: Stift_Engelszell | score: 0.61351 | mention: Zisterzienserklosters Engelszell | sentence: Klaus Jansen OCSO (* 31. März 1922 in Neuss; † 9. Februar 2008) war Abt des Zisterzienserklosters Engelszell in Oberösterreich .
entity: Altenberger_Dom | score: 0.64742 | mention: Dom Unserer Lieben Frau zu Altenberg | sentence: Sie wird von der katholischen Pfarrgemeinde St. Mariä Himmelfahrt am Dom Unserer Lieben Frau zu Altenberg und der evangelischen Domgemeinde Altenberg genutzt.
entity: Kloster_Rebdorf | score: 0.65490 | mention: Augustiner-Chorherrenstift Rebdorf | sentence: Außer dem Bischof hatte auch das Augustiner-Chorherrenstift Rebdorf Besitz im Dorf, so 1452 zwei Zinspflichtige.
entity: Stadtkirche_St._Jakob_(Rothenburg_ob_der_Tauber) | score: 0.65933 | mention: Stadtkirche St. Jakob (Rothenburg ob der Tauber) | sentence: Restaurierung der Chorfenster in der Stadtkirche St. Jakob (Rothenburg ob der Tauber) .
entity: Allerheiligen_(Zürich-Neuaffoltern) | score: 0.67007 | mention: Allerheiligen (Zürich-Neuaffoltern) | sentence: Nach dem Vorbild der Kirche Allerheiligen (Zürich-Neuaffoltern), mit deren Neubau erstmals im Bistum Chur die Konstitution über die heilige Liturgie des Zweiten Vatikanischen Konzils konsequent umgesetzt wurde, befindet sich auch in der St.-Anna-Kirche der Taufstein im vorderen Teil der Kirche, nahe dem Altarraum.

Trivial missed context sentences (query sentence mention == context sentence mention): 
-

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Altenberger Dom | sentence: Grablege der Grafen und Herzöge von Berg sowie der Herzöge von Jülich-Berg im Altenberger Dom .
mention: Altenberger Dom | sentence: Der an ein 27 m breites Querhaus angrenzende vollständig erhaltene Chor weist einen kreuzrippengewölbten Umgang um das rechteckige Chorjoch und die Apsis mit sieben Radialkapellen vom Typ Clairvaux II (vgl. etwa Kloster Pontigny, Kloster Royaumont, Altenberger Dom, Kloster Heisterbach, Kloster Marienstatt) auf.
mention: Altenberger Dom | sentence: Das sehr große Gotteshaus, errichtet ab der Mitte des 13. Jahrhunderts, wird heute Altenberger Dom genannt.
mention: Altenberger Dom | sentence: Für sein Orgelwerk Wegkreuze erhielt er 1980 den Kompositionspreis Altenberger Dom, ebenfalls ausgezeichnet wurde 1981 in Stuttgart seine Komposition Psalm 13 für Soli, Chor und Orchester sowie 1985 sein Wenn ich dein je vergesse für sechzehn Solostimmen und gemischten Chor anlässlich der Internationalen Bachakademie, auch in Stuttgart.
mention: Altenberger Dom | sentence: Der Ortsname Odenthal, bis in die Gegenwart jahrzehntelange Heimat des Erzählers, wird vermieden, der sichtbare und hörbare Kontakt zum Altenberger Dom jedoch mehrfach erwähnt.
mention: Altenberger Dom | sentence: Unter großer Anteilnahme fand am 29. Dezember 2012 eine ökumenische Trauerfeier im Altenberger Dom statt, an der rund 2500 Menschen teilnahmen.
mention: Altenberger Dom | sentence: Die Markuskapelle liegt zwischen dem Altenberger Dom und dem Küchenhof innerhalb der Immunität des ehemaligen Klosters.
mention: Altenberger Dom | sentence: In vielen Kirchen sind Plastiken von Lenz-Gerharz zu finden, darunter seien neben vielen weiteren hier nur zwei Skulpturen mit dem Namen Schutzmantel-Madonna (Altenberger Dom 1953, Berlin-Charlottenburg, St. Canisius 1977, beim Brand der Kirche 1995 zerstört) erwähnt, weiterhin Hl.
mention: Altenberger Dom | sentence: Die Kopfreliquien der beiden Märtyrer gehörten zum bedeutenden Reliquienschatz im Altenberger Dom, der im Zuge der Säkularisation Anfang des 19. Jahrhunderts zum Großteil verloren ging.
mention: Altenberger Dom | sentence: Er wurde 1931 von Generalpräses Carl Mosterts hauptamtlich als Domführer vom Altenberger Dom eingesetzt.
mention: Altenberger Dom | sentence: Die 1133 gegründete Zisterzienserabtei Altenberg war 1803 säkularisiert worden, die Gebäude, die unmittelbar südlich an den Altenberger Dom anschlossen, wurden verkauft und dienten als Chemiefabrik.
mention: Altenberger Dom | sentence: Dabei steht für ihn das zisterziensische Erbe Altenbergs mit dem Altenberger Dom im Vordergrund.
mention: Altenberger Dom | sentence: Zahlreiche Großbauvorhaben standen unter seiner Leitung, darunter die umfänglichen Restaurierungsprojekte am Altenberger Dom, den Brühler Schlössern Augustusburg und Falkenlust sowie am Schloss Bensberg .
mention: Altenberger Dom | sentence: Am 27. Mai 2018 wurde Christian Jasper im Altenberger Dom durch Weihbischof Ansgar Puff zum Diakon für das Erzbistum Köln geweiht.
mention: Altenberger Dom | sentence: Später gab es die Abpfarrung St. Mariä Himmelfahrt in Altenberg  mit der Pfarrkirche Altenberger Dom in Oberodenthal und der Bau der Filialkirche St. Engelbert in Voiswinkel, die seit 1950 besteht und zu Unterodenthal gehört.
```
Note: 
``` 
FP | entity: Orgelbau_Fasen | mention: Orgelbau Hubert Fasen (Oberbettingen) | sentence: Derzeit wird eine durch Orgelbau Hubert Fasen (Oberbettingen) mit 23 Registern aufgebaut, die am 2.
entity: Orgelbauwerkstatt_Gebrüder_Müller | score: 0.63821 | mention: Orgelbauwerkstatt Gebrüder Müller | sentence: Eine Orgel aus der Orgelbauwerkstatt Gebrüder Müller aus Reifferscheid (1898) wurde 1961 durch eine aus der „Manufacture d’orgues Georg Haupt“, aus Lintgen ersetzt.
entity: Orgelbauwerkstatt_Gebrüder_Müller | score: 0.65219 | mention: Orgelbauwerkstatt Gebrüder Müller | sentence: Diese einmanualige Orgel wurde 1837 in der Orgelbauwerkstatt Gebrüder Müller in Reifferscheid mit einem weiteren Manual ausgestattet und von 10 auf 21 Register erweitert.
entity: Orgelbauwerkstatt_Gebrüder_Müller | score: 0.65514 | mention: Orgelbauwerkstatt Gebrüder Müller | sentence: Die 1850 erworbene Orgel wurde 1883 in der Orgelbauwerkstatt Gebrüder Müller auf acht Register ausgebaut und verstärkt, 1947 instandgesetzt und 1961 durch den Orgelbauer Kühn generalüberholt.
entity: Orgelbauwerkstatt_Gebrüder_Müller | score: 0.65954 | mention: Orgelbauwerkstatt Gebrüder Müller | sentence: Die Orgel ist ein Werk der Orgelbauwerkstatt Gebrüder Müller aus Reifferscheid.
entity: Orgelbau_Fasen | score: 0.69956 | mention: Orgelbau Fasen | sentence: In den Jahren 1997/1998 erfolgte eine umfangreiche Restaurierung und teilweise Rekonstruktion zur Wiederherstellung des ursprünglichen Zustands durch die Firma Orgelbau Fasen.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Hubert Fasen | sentence: Die Orgelbaufirma Hubert Fasen aus Oberbettingen nahm eine Umdisponierung vor, stellte auf elektrische Traktur um und intonierte das Instrument neu auf die Erfordernisse der romanischen Stiftskirche.
mention: Orgelbau Fasen | sentence: Bis zum Abbau 2012 befand sich das Instrument in der St. Simon's Church in Southsea, Hampshire und wurde zwischen 2012 und 2014 durch die Firma Orgelbau Fasen aus Oberbettingen umgebaut und 2014 in Irrel aufgestellt.
mention: Orgelbau Fasen | sentence: Orgelbau Fasen setzt das Instrument um, schuf ein neues Gehäuse, restaurierte das Werk und ersetzte zwei Register.
```
Note: *** here the query sentence is very difficult to map anything specific at all in my opinion.
``` 
FP | entity: Abbrand_(Metallurgie) | mention: Verzundern | sentence: Kein bzw. geringes Verzundern an der Oberfläche.
entity: Chemisch-mechanischer_Langzeitzünder | score: 0.70583 | mention: Langzeitzündern | sentence: Viele Bomben mit Langzeitzündern gingen noch unberechenbar hoch.
entity: Abbrand_(Metallurgie) | score: 0.70901 | mention: Zunder | sentence: Mechanische Vorbehandlungsmethoden dienen dazu, grobe Verunreinigungen wie Rost, Zunder oder ähnliche feste Verunreinigungen zu entfernen.
entity: Abbrand_(Metallurgie) | score: 0.71511 | mention: Zunder | sentence: Es wird angewendet, um Korrosion, Zunder, Verunreinigungen oder Oberflächenbeschichtungen zu entfernen und eine definierte Oberflächenreinheit und -rauheit zu erreichen.
entity: Zündverzug | score: 0.72264 | mention: Zündverzug | sentence: Dadurch kann der Zündverzug reduziert werden, was sich in einem auch ohne Hilfsmittel guten Abgasverhalten bemerkbar macht.
entity: Abbrand_(Metallurgie) | score: 0.73363 | mention: Zunder | sentence: Der Zunderwäscher (englisch: descaler oder scale breaker) dient dazu, den Zunder (d. h. Verunreinigungen aus Eisenoxid an der Oberfläche) durch hohen Wasserdruck zu entfernen, um ein Einwalzen des Eisenoxids in das Material zu verhindern.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Abbrand (Metallurgie) | sentence: Den Abbrand auf Metalloberflächen durch das Einwirken von Sauerstoff, siehe Abbrand (Metallurgie) .
mention: Abbrand | sentence: Sauerstoffzutritt bedingt Oxidbildung - gelegentlich auch Abbrand genannt -  in unterschiedlichem, durch die Sauerstoffaffinität der Schmelzebestandteile bedingtem Ausmaß.
mention: Zunderbeständigkeit | sentence: Aufgrund seiner besonderen Korrosions- und Zunderbeständigkeit, einem relativ niedrigen spezifischen elektrischen Widerstand sowie einem niedrigen Temperaturkoeffizienten desselben wird Nickelin überwiegend im Bereich der Elektrotechnik verwendet, wo es in Form von Drähten, Bändern und Blechen zu Widerständen aller Art und als Heizleiterlegierung zu Wärmekabeln bzw. Heizdrähten verarbeitet wird.
mention: zunderbeständig | sentence: Die erreichte Schutzschicht ist verformbarer, weniger spröde und ebenfalls zunderbeständig .
mention: zunderfrei | sentence: Auch Kupfer, das durch Kaltverformung hart und spröde geworden ist, kann man durch Erholungsglühen (Rekristallisationsglühen) mit anschließendem Abschrecken wieder zäh und zugleich zunderfrei bekommen.
mention: Abbrand | sentence: Da dies nicht immer erreichbar ist, sind Volumenzuschläge (V_Z) beispielsweise für den Randbeschnitt bei Tiefziehteilen, für den Schmiedegrat oder für Abbrand beim Warmumformen zu berücksichtigen.
mention: Zunder | sentence: Needlegun-Scaler) sind handgehaltene, zumeist pneumatisch betriebene Geräte zum Entfernen von Rost oder Zunder.
mention: Zunder | sentence: Unter biologischer Entrostung versteht man die Entfernung von Rost oder Zunder von metallischen Oberflächen mithilfe biologisch gebildeter Rostumwandler.
mention: Abbrand | sentence: Die Nachteile der aktiven Gase, wie die toxische Wirkung und Entflammbarkeit von CO als auch Abbrand von Legierungselementen im Werkstoff werden im Patent nicht angesprochen.
mention: Hammerschlag | sentence: Der Deuchel wurde mit „Synter“ (vermutlich aber Hammerschlag) und später mit altem Eisen nochmals eingeschmolzen und zu Schwarzblechen verarbeitet.
```
Note: another very difficult example where the suggested nn sentences seem like a somewhat logical fit for the query sentence even tho they refer to different entities.  Again, the main topic between all sentences is quite similar (related to steam).
``` 
FP | entity: Dampfgarer | mention: Dampfgarkesseln | sentence: Moderne Feldküchen besitzen neben Dampfgarkesseln auch Bräter, Backröhren und Warmhaltebehälter.
entity: Dampfkesselanlage | score: 0.49783 | mention: Dampfkesselanlage | sentence: Die Bischofsmühle besaß eine Dampfkesselanlage, die zur Unterstützung der geringen nutzbaren Wasserfallhöhe von nur 0,6 m die Wasserkraft ergänzen sollte.
entity: Dampfkesselanlage | score: 0.56733 | mention: Dampfkesselanlage | sentence: Das heutige Kennzeichen der Bischofsmühle ist nicht ein ober- oder unterschlächtiges Wasserrad, sondern ein efeubewachsener Schornstein, der zu einer Dampfkesselanlage gehörte, die seit 1882 die geringe Wasserkraft ergänzen sollte.
entity: Dampfkesselanlage | score: 0.57295 | mention: Dampfkesselanlage | sentence: Das Power Building wurde 1890 zur Aufnahme einer Dampfkesselanlage zur Strom- und Wärmeerzeugung errichtet, die erst 1960 durch den Anschluss an das öffentliche Netz abgeschaltet wurde.
entity: Heizkessel | score: 0.60990 | mention: Dampfkessel | sentence: Die Dachhaube war über dem Fahrmotor, dem Dampfkessel und dem Haupttransformator abnehmbar.
entity: Dampfgarer | score: 0.62954 | mention: Dampfgaren | sentence: Mit dem „Varoma“-Aufsatz wird Dampfgaren ermöglicht.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Dampfgarer | sentence: Das Produktportfolio umfasst nebst Kaffeemaschinen auch elektrische Küchengeräte wie Handmixer, Standmixer, Standküchenmaschinen, Dampfgarer und Luftbefeuchter .
mention: Dampfgaren | sentence: In Deutschland gab es in der zweiten Hälfte des 20. Jahrhunderts zahlreiche Dämpfanlagen, in denen durch Dampfgaren von Kartoffeln in größeren Behältern stärkereiches Futter für die Schweinemast gewonnen wurde.
```
Note: the top nn sentences are all sort of fitting in regard to the main topic: electricity
``` 
FP | entity: Leiter_(Physik) | mention: elektrisch leitfähig | sentence: Stephen Gray teilte 1729 Materialien in elektrisch leitfähig und elektrisch isolierend ein und demonstrierte, dass auch der menschliche Körper Strom leiten konnte.
entity: Elektrowerkzeug | score: 0.66925 | mention: Elektrowerkzeug | sentence: Eine Lackfräse ist ein handgeführtes Elektrowerkzeug, mit dem Farben und Lacke von Holzflächen und Kunststoffen entfernt werden können.
entity: Elektrowerkzeug | score: 0.66976 | mention: Elektrowerkzeug | sentence: Die Putzfräse ist ein handgeführtes Elektrowerkzeug, welches zum Abtragen von Putzen im Wandbereich, aber auch zum Entfernen von Farbbeschichtungen oder Kleberresten eingesetzt wird.
entity: Elektrowerkzeug | score: 0.67528 | mention: Elektrowerkzeug | sentence: Der Betonschleifer ist ein handgeführtes Elektrowerkzeug, welches zum Schleifen mineralischer Untergründe eingesetzt wird.
entity: Elektrolytische_Bleiraffination | score: 0.70317 | mention: elektrolytischen Reinigung | sentence: Er ist für die Betts-Methode zur elektrolytischen Reinigung von Blei bekannt und wird zur Herstellung von besonders reinem Blei benutzt (etwa von Bismut-Beimengungen).
entity: Leiter_(Physik) | score: 0.71915 | mention: elektrischen Leitung | sentence: Er beschreibt den ohmschen Widerstand R einer elektrischen Leitung bezogen auf ihre Länge a.

Trivial missed context sentences (query sentence mention == context sentence mention): 

Difficult missed context sentences (query sentence mention != context sentence mention): 
mention: Leiter | sentence: Elektrodynamische Schallwandler, beispielsweise Mikrofone und Lautsprecher, bestehen im Prinzip aus einem feststehenden, permanenten Magnetfeld und einem darin beweglich angeordneten elektrischen Leiter, der in der Praxis entweder zu einer Schwingspule aufgewickelt ist oder aus einer leichten Metallfolie besteht.
mention: Adern | sentence: Eine Klemme dient in der Elektrotechnik zum lösbaren Anschluss oder der Verbindung von Drähten, Adern und Leitungen.
mention: Leitern | sentence: Die Annäherung des Magnetfeldes von einem Permanentmagneten erzeugt in einem Supraleiter genauso wie in anderen Leitern Wirbelströme, die wiederum ein Magnetfeld erzeugen, das dem auslösenden Magnetfeld entgegengerichtet ist.
mention: Adern | sentence: Ein Kabel besteht aus acht einzelnen Adern.
mention: Leiter | sentence: Allgemein müssen für eine TEM-Leitung zwei getrennte, ideale Leiter existieren, deren Anordnung in Ausbreitungsrichtung gleichförmig ist und sich in einem homogenen Raum befindet.
mention: leitenden Körper | sentence: Die Spiegelladung oder Bildladung ist eine gedankliche Hilfsstütze, um das Verhalten einer Ladung Q vor einem leitenden Körper oder einer dielektrischen Grenzfläche im Abstand R zu veranschaulichen.
mention: Leitung | sentence: Mit X-by-Wire wird der Ersatz von mechanischen Verbindungen, Signalen und Systemen zur manuellen Steuerung durch die Leitung elektrischer, elektronischer, optoelektronischer oder optischer Steuersignale zwischen den verwendeten Bedienelementen und den ausführenden Aktoren bezeichnet.
mention: Leiter | sentence: Der Kabeljungwerker stellt elektrische Kabel und Leiter aller Art her.
mention: elektrische Leiter | sentence: Da es sich beim Federkontaktstift um ein Kontaktelement handelt, sind im Normalfall nur gute elektrische Leiter als Werkstoffe zu verwenden.
mention: Leiter | sentence: Sie besteht aus einem festen Leiter, an dem ein U-förmiger Drahtbügel hängt, der sich frei wie ein Pendel bewegen kann.
mention: Leitern | sentence: Darüber hinaus kann mit einem Kabeltester im Fehlerfall (z.b. Kurzschluss zwischen zwei oder mehreren Leitern, Erdschluss eines Leiters) die Fehlerstelle durch eine Messung des Widerstands (Gleichstrommessung oder Wechselstrommessung) eingegrenzt werden, damit die Leitung nicht komplett freigelegt werden muss.
mention: Aluminiumleiter | sentence: Die Federkraftklemme vermeidet Fehlerquellen, die sich bei klassischen Schraubverbindungen durch Wärmeentwicklung, Vibrationen oder Materialfließen (z.b. bei einem Aluminiumleiter) ergeben können.
mention: Leiter | sentence: Erkenntnisse über Materialien als Leiter, Halbleiter und Nichtleiter, über Akustik, über Elektromagnetismus, elektrische Leitfähigkeit, Ladung und Entladung sowie das Verhalten magnetischer Felder sowie Wissen über die Funktionsweise von Apparaten, Bauteilen bzw. -elementen, insbesondere von Antennen, Spulen, Kondensatoren, Widerständen, Isolatoren und Batterien und Messgeräten sowie die Berechnung einzelner Vorgänge und Parameter zur Bestimmung der zu verwendenden Teile.
mention: Leiter | sentence: Bei Thermomagnetischen Effekten erzeugt ein Wärmestrom in einem Leiter oder Halbleiter, der sich in einem Magnetfeld befindet, eine Potential- oder Temperaturdifferenz.
mention: Leiter-Übergänge | sentence: Nach einer Zeit in der Industrie, während der er als technischer Leiter der neu eingerichteten RFID-Abteilung von Finser Packaging SA tätig war, begann er 2007 ein Promotionsstudium an der ETH Lausanne, das er 2010 mit einer Doktorarbeit über Isolator-Leiter-Übergänge in polymeren Nanomaterialien aus Graphit abschloss.
mention: Leiter | sentence: Siti stellt Kabel und Leiter her und gehört in dieser Branche zu den größten Unternehmen Indiens.
```

## (Good) TP Examples
``` 

```
``` 

```

## Examples where the mention is not equal the GT entity or the mention of the suggested nn sentence
``` 

```
``` 

```

## 