# Digitális receptkönyv

##A program egy digitális receptkönyvet valósít meg.
 
##Telepítés
1. GitHub repository klónozása vagy ZIP fájlban való letöltése.
2. Belépés a projekt mappájába.
3. Program futtatása terminálban a következő paranccsal: python main.py.

##Külső függőségek: A program nem tartalmaz külső függőségeket.

##Használat:

###Egy választott recept megtekintése: A bal oldali receptlistából egy recept nevére kattintva megjelennek a hozzá tartozó részletek a jobb oldalon.

###Recept hozzáadása: A 'Recept hozzáadása' gombra kattintva megnyílik egy új ablak, amiben megadható a recept neve, kategóriája, hozzávalói és elkészítési módja. A recept nevének kitöltése kötelező. A hozzávalókat Enter-rel kell elválasztani egymástól. A 'Mentés' gombra kattintva a recept megjelenik a bal oldali recept listában. A 'Mégse' gombra kattintva a változtatások elvesznek.

###Recept törlése: A 'Recept törlése' gombra kattinva törlésre kerül a bal oldali receptlistából kiválasztott elem. Amennyiben nincs kiválasztott recept, erre egy felugró ablak figyelmeztet.

###Kerersés egy recept nevére: A bal fent található keresőmezőbe gépeléskor megjelennek azok a receptek a listában, amelyek nevében megtalálhatók a keresett karakterek.

###Szűrés kategória szerint: A keresőmező alatt található legördülő menüben egy kategória kiválasztásával lehet szűrni az ahhoz a kategóriához tartozón receptekre.

###Szűrés összetevők szerint: A kategória szűrő alatt található listában fel van sorolva minden összetevő, amely megtalálható a receptekben. Egyet vagy többet kiválasztva megjelennek azok a receptek, amelyek tartalmazzák az adott összetevőt/összetevőket.

###Szűrők törlése: A 'Szűrők törlése' gombra kattintva törlődik minden eddig beállított szűrő, a receptlisa minden eleme újra megjelenítésre kerül.