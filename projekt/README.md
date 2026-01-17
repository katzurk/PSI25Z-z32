# Projekt

## Treść

Celem projektu jest zaprojektowanie oraz implementacja szyfrowanego protokołu opartego na protokole TCP, tzw. mini TLS.

**Założenia**

- Architektura klient-serwer
- Serwer jest w stanie obsłużyć kilku klientów równocześnie - maksymalna ich ilość zostaje podana jako parametr uruchomienia
- Klient inicjuje połączenie z serwerem poprzez wysłanie wiadomości ClientHello, na którą serwer odpowiada wiadomością ServerHello
- Wiadomości ClientHello oraz ServerHello służą do wymiany kluczy szyfrujących, nie są one szyfrowane
- Sesja może zostać zakończona zarówno przez klienta jak i serwer, poprzez wysłanie wiadomości EndSession
- Wszystkie wiadomości między klientem a serwerem, w tym EndSession, są szyfrowane

## Uruchomienie

**Serwer**

`cd server`

`./run.sh [liczba klientów]`

**Klient**

`cd client`

`./run.sh`

**Usunięcie kontenerów**

`./clean.sh`
