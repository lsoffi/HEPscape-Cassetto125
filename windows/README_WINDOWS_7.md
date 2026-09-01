# HEPscape! — installazione su Windows 7 a 64 bit

Queste istruzioni sono dedicate a **Windows 7 Home Premium a 64 bit** e al trigger **KX-007 / Prolific PL2303**.

## 1. Verificare il trigger

1. Collega il trigger KX-007 a una porta USB del PC.
2. Apri **Start → Pannello di controllo → Sistema → Gestione dispositivi**.
3. Cerca la sezione **Porte (COM e LPT)**.
4. Il dispositivo dovrebbe apparire come **Prolific USB-to-Serial**, **PL2303** o con un nome simile, seguito da una porta come `COM3`.

Se compare un triangolo giallo oppure il dispositivo appare tra i dispositivi sconosciuti, manca il driver corretto. Non scaricare driver da siti casuali: identifica prima il nome e l'eventuale codice di errore mostrato da Windows.

## 2. Installare Python

Windows 7 richiede **Python 3.8.10 a 64 bit**. Versioni più recenti non sono compatibili.

Scarica l'installer ufficiale:

<https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe>

Durante l'installazione:

1. seleziona **Add Python 3.8 to PATH**;
2. scegli **Install Now**;
3. attendi il completamento.

## 3. Preparare HEPscape!

1. Copia tutta la cartella `HEPscape-Cassetto125` sul PC Windows.
2. Apri la sottocartella `windows`.
3. Fai doppio clic su `Installa_Windows_7.bat`.
4. Attendi il messaggio **Installazione completata**.

## 4. Avviare e provare

1. Collega trigger e cassetto.
2. Fai doppio clic su `Avvia_HEPscape_Windows.bat`.
3. Lascia aperta la finestra nera.
4. Apri nel browser <http://localhost:5000/open>.
5. Se il cassetto si apre, apri `hepscape_run_validation_v3.html` e prova il codice **125**.

## Arresto

Chiudi la finestra nera del server, poi scollega il trigger USB. Il collegamento RJ12 può restare inserito.
