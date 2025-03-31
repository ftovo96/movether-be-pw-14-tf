Questo è il repository lato backend del progetto "Movether".

Per avviarlo è necessario aver installato python versione 3.9 o superiore.
E' inoltre consigliato l'uso dei virtual environments.
Maggiori informazioni sono disponibili sul sito di [Flask](https://flask.palletsprojects.com/en/stable/installation/), con cui è stato realizzato il backend.

## Avvio del progetto

Dopo aver effettuato il clone del progetto è necessario entrare nella cartella Server/ e dare i seguenti comandi:

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

Una volta avviato il server andare all'indirizzo [http://localhost:3000](http://localhost:3000) (dopo aver avviato il progetto del frontend) per accedere alla versione in React/Next.js oppure all'indirizzo [http://localhost:5000](http://localhost:5000) per accedere alla versione "legacy" del frontend (cioè la versione realizzata prima di creare un progetto specifico in React del frontend).

Per fare test è possibile usare gli utenti:
    * Rossi (email: mario.rossi@gmail.com - password: password123)
    * Bianchi (email: rosa.bianchi@gmail.com - password: password456)

## Struttura del progetto

Nella cartella [Server/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Server) sono presenti i file del backend, nello specifico:
* [app.py](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Server/app.py), il "main" del server
* La cartella [data/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Server/data) contenente i file csv utilizzati dallo script [data-import.py](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Server/data-import.py) per inizializzare il database. Modificando i vari file e rieseguendo lo script è possibile modificare i dati del database.
* La cartella [entities/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Server/entities) contenente le api responsabili delle varie entità del progetto e le query per la manipolazione dei dati
* La cartella [static/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Server/static) contentente le risorse web che costituiscono la vecchia versione del frontend del progetto.

Nella cartella [Documentazione/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Documentazione) sono presenti i vari documenti contenenti le specifiche del progetto:
* [Casi d'uso](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Documentazione/Casi%20d'uso.pdf)
* [Diagramma casi d'uso](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Documentazione/Diagramma%20casi%20d'uso.pdf)
* [Diagramma ER](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Documentazione/Diagramma%20ER.pdf)
* [Documentazione API](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Documentazione/Documentazione%20API.pdf)
* [Mockup dell'interfaccia](https://github.com/ftovo96/movether-be-pw-14-tf/blob/main/Documentazione/Mockup%20Interfaccia.pdf)
Sono inoltre presenti al suo interno le cartelle [Videos/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Documentazione/Videos) e [Screenshots/](https://github.com/ftovo96/movether-be-pw-14-tf/tree/main/Documentazione/Screenshots) con dimostrazioni d'uso del progetto.
