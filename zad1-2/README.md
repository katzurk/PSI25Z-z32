# Zadanie 1.2 - Komunikacja UDP

## Treść

Klient ma za zadanie odczytać plik z dysku (proszę wygenerować plik z losowymi 10000B) i wysłać do serwera jego
zawartość w paczkach po 100B. Serwer ma zrekonstruować cały plik i obliczyć jego hash. Jako dowód działania proszę
m.in. porównać hash obliczony przez serwer z hashem obliczonym przez klienta (może to być wydrukowane w konsoli
klienta/serwera, hashe muszą być identyczne). Należy zaimplementować prosty protokół niezawodnej transmisji,
uwzględniający możliwość gubienia datagramów. Gubione pakiety muszą być wykrywane i retransmitowane aby
serwer mógł odtworzyć cały plik. Należy uruchomić program w środowisku symulującym błędy gubienia pakietów.
(Informacja o tym, jak to zrobić znajduje się w skrypcie opisującym środowisko Dockera)

## Uruchomienie

**Serwer**

`cd server`

`./run.sh`

**Klient**

`cd client`

`./run.sh`

**Usunięcie kontenerów**

`./clean.sh`
