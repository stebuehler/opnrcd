from dash import dcc 

def offcanvas_content():
    content = dcc.Markdown('''
        #### OPNRCD-ANLTK
        Eine Netz-Applikation zur quantitativen und komparativen Analyse von OPNRCD-Strophen oder OPNRCD-Strophen-Gruppen. Funktional auf mobilen Endgeräten aber idealerweise auf einem Rechner mit Mauszeiger benutzt.

        #### Filter
        Ermöglichen, eine Teilmenge aller OPNRCD-Strophen zu selektieren. Wirken auf alle Reiter gleichzeitig. Für Reiter "Zeitreihe" ist nur der Jahres-Filter aktiv.

        #### Anzeigeoptionen
        Erlauben, die Graphik auf dem jeweiligen Reiter anzupassen. Separat pro Reiter.

        #### Strophenattribute
        - **Baujahr:** Jahr, in dem die OPNRCD-Strophe als "Lied" erschaffen wurde.  
        - **Baujahr Jahrzehnt:** Aggregierte Version von "Baujahr".
        - **Dauer:** Dauer der Strophe.  
        - **Jahr:** Beschreibt das OPNRCD-Jahr.  
        - **Kontinent:** Aggregierte Version von "Nationalität".  
        - **Künstler:** Interpret der Strophe.  
        - **Nationalität:** Die Nationalität des (Haupt-)Interpreten.  
        - **Sprache:** (Haupt-)Sprache, in der der Strophentext verfasst ist. Kann "Mehrere" sein, falls mehrere ähnlich stark vertretene Sprachen vorhanden sind.          
        - **Timestamp:** Startzeit der Strophe auf der jeweiligen OPNRCD.  
        - **Titel:** Name der Strophe.  

        #### Strophenbewertung
        Die Bewertung der Strophen in den sechs Kategorien wurde stets in alkoholisiertem Zustand im Reinraum von geschultem Personal (OPNRCDKMT) durchgeführt; und ist ISO-zertifiziert. Alle Kategorien weisen ganzzahlige Wert zwischen eins und zehn auf. Ausser die Kategorie Weirdness, welche sich von eins bis acht erstreckt.
        - **Künstlerische Relevanz:** Beschreibt den künstlerischen Wert der Strophe im musikhistorischen und generell kunsthistorischen Zusammenhang.  
        - **Musikalische Härte:** Sic. Für eine genaue Definition verweisen wir auf https://homepage.univie.ac.at/christoph.reuter/unterwegs/DAGA2017_Paper_Czedik-Eysenberg_Knauf_Reuter.pdf.  
        - **Tanzbarkeit:** Beschreibt die Eignung der Strophe zum Einzel- oder Gruppentanz. Strophen mit etablierten OPNR-Tänzen wurden besonders hoch bewertet.  
        - **Verblödungsfaktor:** Kann durch textliche oder musikalische Verblödung getrieben sein, sowie durch verblödete Äusserungen des Künstlers.  
        - **Nervofantigkeit:** Variable welche die Genervtheit einer durchschnittlichen OPNRCD-Hörperson durch wiederholte akustische Exponiertheit zu besagter Strophe quantifiziert.  
        - **Weirdness:** Beschreibt wie komisch, resp. einzigartig die besagte Strophe ist.

        #### Skits
        Skits (belustigende Zwischenspiele, die aber keine echten OPNRCD-Strophen sind) sind von der Bewertung und allen momentan verfügbaren Analytik-Exponaten **ausgeschlossen**. Die Dauer der Skits ist in der Gesamtdauer pro OPNRCD enthalten, welche auf dem "Strophensteckbrief"-Reiter, sowie auf dem "Zeitreihe"-Reiter ausgewiesen wird. In allen anderen Reitern summiert sich die Gesamtdauer aller echten OPNRCD-Strophen zu einer kürzeren Dauer.

        #### Impressum
        OPNRBZNZ GmbH  
        Ankerstrasse 12  
        0000 T0tzball0nienburg  
        Ankerland  
        ''')
    return content