Questo è il repository lato backend del progetto.

Per avviarlo è necessario aver installato python versione 3.9 o superiore.
E' inoltre consigliato l'uso dei virtual environments.
Maggiori informazioni sono disponibili sul sito di [Flask](https://flask.palletsprojects.com/en/stable/installation/), con cui è stato realizzato il backend.

## Avvio del progetto

Dopo aver effettuato il clone del progetto è necessario entrare nella sua cartella e dare i seguenti comandi:

```bash
# MacOS/Linux
python3 -m venv .venv
. .venv/bin/activate
pip install Flask
python3 data-import.py
flask --app app.py run --debug

# Windows
py -3 -m venv .venv
.venv\Scripts\activate
pip install Flask
py -3 -m data-import.py
flask --app app.py run --debug
```

Una volta avviato il server basta andare alla pagina [http://localhost:5000](http://localhost:5000) per accedere alla versione legacy del frontend (cioè la versione realizzata prima di creare un progetto specifico in React del frontend).

## Struttura del progetto

Nella cartella Server/ sono presenti i file del backend, nello specifico:
* app.py, il "main" del server
* La cartella data/ contenente i file csv utilizzati dallo script data-import.py per inizializzare il database. Modificando i vari file e rieseguendo lo script è possibile modificare i dati del database.
* La cartella entities/ contenente le api responsabili delle varie entità del progetto e le query per la manipolazione dei dati
* La cartella static/ contentente le risorse web che costituiscono la vecchia versione del frontend del progetto.
