# Zadanie 1.1 - Komunikacja UDP

## Treść

Klient wysyła, a serwer odbiera datagramy oraz odsyła ustaloną odpowiedź. Klient powinien wysyłać kolejne datagramy o przyrastającej wielkości, tj. 2, 4, 8, 16, 32, itd. bajtów. Ustalić eskperymentalnie z dokładnością do jednego bajta jak duży datagram jest obsługiwany. Wyjaśnić. Zmierzyć czas pomiędzy wysłaniem wiadomości a odebraniem odpowiedzi po stronie klienta i zestawić wyniki na wykresie.

## Uruchomienie

**Serwer**

`./server/run.sh [port]`

**Klient**

`./client/run.sh [port]`

**Usunięcie kontenerów**

`./clean.sh`
