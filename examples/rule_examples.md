## True positives
```
Mention                                 TP entities                             FP entities                             FN entities                             
---------------                         ---------------                         ---------------                         ---------------         
Dana Incorporated                       {'Dana_Incorporated'}                   set()                                   set()                                   
Ullrich, Walter                         {'Walter_Ullrich_(Schauspieler)'}       set()                                   set()                                   
Walter Ullrich                          {'Walter_Ullrich_(Schauspieler)'}       set()                                   set()                                   
Walter Ullrich (Schauspieler)           {'Walter_Ullrich_(Schauspieler)'}       set()                                   set()                                   
Johannes Vollrath                       {'Johannes_Vollrath'}                   set()                                   set()                                   
Vollrath, Johannes                      {'Johannes_Vollrath'}                   set()                                   set()                                   
Polski Holding Nieruchomości            {'Polski_Holding_Nieruchomości'}        set()                                   set()  
Globalen Pakt für Flüchtlinge           {'Globaler_Pakt_für_Flüchtlinge'}       set()                                   set()                                   
Flughafen Buenos Aires-El Palomar       {'Flughafen_Buenos_Aires-El_Palomar'}   set()                                   set()                                   
```

## True positives + False positives
``` 
Mention                                 TP entities                             FP entities                             FN entities                             
---------------                         ---------------                         ---------------                         ---------------         
Georg Hartmann (Intendant)              {'Georg_Hartmann_(Intendant)'}          {'Georg_Hartmann_(Sänger)'}             set()                                   
LMB                                     {'Langenthal-Melchnau-Bahn'}            {'Lena_Meyer-Bergner'}                  set()                                   
AT-Verlag                               {'AT_Verlag'}                           {'AQ-Verlag'}                           set()                                   
SAS                                     {'Saporisky_Awtomobilebudiwny_Sawod'}   {'Salomon_An-Ski', 'Susanne_Schulz'}    set()                                   
TBS                                     {'Turner_Broadcasting_System'}          {'TIM_Brasil'}                          set()                                   
Denzel                                  {'Denzel_(Automobilhersteller)'}        {'Denel'}                               set()                                   
```

## False positives + False negatives
```
Mention                                 TP entities                             FP entities                             FN entities                             
---------------                         ---------------                         ---------------                         ---------------         
OSM                                     set()                                   {'OMS_(Unternehmen)'}                   {'OSM_Maritime_Group'}                  
AMC-                                    set()                                   {'AMK_(Unternehmen)'}                   {'AMC_Networks'}                        
Voll                                    set()                                   {'Volg'}                                {'Karosseriefabrik_Voll'}               
KABEG                                   set()                                   {'Kabel_eins'}                          {'Kärntner_Landeskrankenanstalten-Betriebsgesellschaft'}
NP                                      set()                                   {'Nico_Pyrotechnik', 'Namibia_Post'}    {'Edeka_Minden-Hannover'}               
Lot                                     set()                                   {'LATS', 'Lotter_(Unternehmen)'}        {'Lot_von_Orkney'}                      
Rotter-Bühnen                           set()                                   {'Rote_Bühne'}                          {'Fritz_Rotter_(Theaterunternehmer)'}   
Rotter                                  set()                                   {'Rotte_(Luftfahrt)'}                   {'Fritz_Rotter_(Theaterunternehmer)'}   
Wilhelm Sauer                           set()                                   {'WS-*'}                                {'W._Sauer_Orgelbau_Frankfurt_(Oder)'}  
BAM                                     set()                                   {'TamS', 'Bader_(Unternehmen)'}         {'Royal_BAM_Group'}                     
Olms                                    set()                                   {'OMS_(Unternehmen)'}                   {'Georg_Olms_Verlag'}                   
AGC                                     set()                                   {'Ashanti_Goldfields_Corporation'}      {'Asahi_Glass'}                         
```

## False negatives
```
Mention                                 TP entities                             FP entities                             FN entities                             
---------------                         ---------------                         ---------------                         ---------------         
Dana Inc.                               set()                                   set()                                   {'Dana_Incorporated'}                   
Dana Corp.                              set()                                   set()                                   {'Dana_Incorporated'}                   
Dana-Verteilergetriebe                  set()                                   set()                                   {'Dana_Incorporated'}                   
Dana                                    set()                                   set()                                   {'Dana_Incorporated'}  
El Palomar                              set()                                   set()                                   {'Flughafen_Buenos_Aires-El_Palomar'}   
UNO-Flüchtlingspakts                    set()                                   set()                                   {'Globaler_Pakt_für_Flüchtlinge'}       
Flüchtlingspakt                         set()                                   set()                                   {'Globaler_Pakt_für_Flüchtlinge'}       
UNO-Flüchtlingspakt                     set()                                   set()                                   {'Globaler_Pakt_für_Flüchtlinge'}       
Jernhusen AB                            set()                                   set()                                   {'Jernhusen'}                           
Kulturverein Rote Bühne                 set()                                   set()                                   {'Rote_Bühne'}                          
Sportwagenmanufaktur                    set()                                   set()                                   {'Denzel_(Automobilhersteller)'}        
```
