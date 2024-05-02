# rendszertervezes
 
Ez a kód a rendszertervezés beadandó feladatomhoz készült egy a számítógépemen futatott virtuális környezetben. Ezt a saját gépen is szükséges futtatni, hogy leforduljon megfelelően a kód.
Hogy milyen függőségeket használtam a virtuális környezetemben megtalálod a requirements.txt fájlban. Ezeket telepíteni a "pip install -r requirements.txt" kóddal lehetséges.

Egyedül dolgoztam a projecten, így úgy gondoltam, hogy python programozási nyelvet választom és VC Edtior Django Frameworköt használok ugyanis nagyon sok előre beépített feature van ebben ami igazán megkönyítette a munkámat. Emellett egy nagyon alap HTML kód is szerepel ami megjeleníti a user felületi adatokat. 
A szervert a "python manage.py runserver" paranccsal lehet elindítani miután "cd <path>" paranccsal belépsz a felső könyvtár struktúrába ahol ez a fájl megtalálható (manage.py). Ez abban az esetben működik,hogy ha csak python3 van csak telepítve, ha python2 is telepítve van akkor "python3 manage.py runserver" parancsot kell futtatni. Bármilyen műveletet is hajtasz végre itt a CMD ablakon minden megjelenik.

Admin felület 
http://127.0.0.1:8000/admin --> user/pw (admin/Autorent1!)

User felület:
http://127.0.0.1:8000/autorent/ ---> főoldal, innen még nem lehet kattintással továbblépni
http://127.0.0.1:8000/autorent/user --> adatlekérés sqlite adatbázisból, nagyon egyszerű felület
