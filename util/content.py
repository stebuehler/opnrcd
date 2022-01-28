from dash import dcc 

def offcanvas_content():
    content = dcc.Markdown('''
        #### Bewertung
        Die Bewertung der Strophen in den sechs Kategorien wurde stets in alkoholisiertem Zustand im Reinraum von geschultem Personal (OPNRCDKMT) durchgeführt; und ist ISO-zertifiziert. Alle Kategorien weisen ganzzahlige Wert zwischen eins und zehn auf. Ausser die Kategorie Weirdness, welche sich von eins bis acht erstreckt.
        
        #### Impressum
        OPNRBZNZ GmbH  
        Ankerstrasse 12  
        0000 T0tzball0nienburg  
        Ankerland  
        ''')
    return content