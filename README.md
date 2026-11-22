# Scheda allenamento

Pagina statica per il telefono: mostra la seduta del giorno del ciclo novembre 2026 – febbraio 2027, con i kg calcolati dai massimali di calcolo.

- `index.html`: la pagina (HTML, CSS e JavaScript in un unico file, nessuna dipendenza).
- `programma.json`: i dati del programma. **Non va modificato a mano.**
- `genera_programma.py`: genera `programma.json`. Per cambiare il programma si modifica questo file e si lancia `python genera_programma.py`.

Il pulsante "Segna come fatta" in fondo a ogni seduta salva la spunta (con la data) nel browser del telefono: non passa da un server e non si sincronizza tra dispositivi.

I carichi degli esercizi a doppia progressione (pulley, lat machine, shoulder press, pressa del venerdì) si aggiornano dalla sezione "Carichi delle progressioni" o con − e + sulla scheda; i valori di partenza sono in `CARICHI` dentro `genera_programma.py`.

I massimali si cambiano dalla pagina (sezione "Massimali di calcolo") e restano salvati nel browser del telefono. Per aprire direttamente una seduta si usa un link come `…/#6-ven` (settimana 6, venerdì).

Prova in locale: `python -m http.server`, poi apri `http://localhost:8000`. Aperta come file, la pagina non riesce a leggere il JSON.
