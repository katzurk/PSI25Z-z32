# Zadanie 2 - Komunikacja TCP

## Treść

Klient wysyła do serwera działanie, które serwer ma obliczyć i odesłać odpowiedź do klienta. Dla uproszczenia proszę
przyjąć, że klient wysyła 3 wiadomości w ramach działania: liczba1, znak „*”, liczba2. Po otrzymaniu tych 3
wiadomości serwer oblicza „liczba1 * liczba2” i odsyła wynik do klienta. Klient i serwer wypisują działanie oraz
wynik w konsoli. Program klienta ma być interaktywny, tzn. po uruchomieniu to użytkownik wpisuje działanie na
zasadzie: liczba1, enter, „*”, enter, liczba2, enter → powinien pokazać się wynik. Proszę założyć, że użytkownik
zawsze wpisze dobre liczby i znak działania (nie tracić czasu na walidacje).

## Uruchomienie

**Serwer**

`cd server`

`./run.sh`

**Klient**

`cd client`

`./run.sh`

**Usunięcie kontenerów**

`./clean.sh`
