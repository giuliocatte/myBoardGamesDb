# myBoardGamesDb

Ero troppo pigro per fare un database dei miei giochi da tavolo, quindi ho fatto un
 software per generarlo a partire da [BoardGameGeek](https://boardgamegeek.com). 
 
È stato fatto con python 3.6, ma ci sono buone possibilità che funzioni anche con versioni precedenti e magari anche 2.7.

## setup
La parte python richiede di installare i moduli requests, fire, e bottle.
Tutti si possono installare via pip.
Poi nella cartella assets, occorre inserire [jquery](http://jquery.com/)
(il software e' stato fatto con la versione "-3.2.1.min",
se si vuole usarne un'altra è necessario modificare la versione nella
costante JQUERY_VERSION in gui.py').
Inoltre, sempre in assets, è necessario aggiungere la libreria [tablesorter](http://tablesorter.com/).
Se ci sono dubbi sui path, si possono vedere i nodi script nel file gui.py,
dove questi componenti sono utilizzati.

## usage
Per aggiornare il db locale da boardgamegeek, posizionarsi all'interno della directory ed eseguire
```
python bgg.py download
```
L'interfaccia al momento si può chiamare in due modi.
```
python bgg.py serve
```
tira su un server che risponde su http://localhost:8080/. Al momento l'unica chiamata sensata da fare in un browser è http://localhost:8080/owned.
```
python bgg.py generate
```
invece tira su il server, apre quella pagina su un browser, e poi
prova a spegnere il server
(tanto la pagina al momento non ha altre interazioni sul backend).

### note
* I giochi più vecchi del 75, sono stati messi in una sezione classici che sta in fondo a prescindere dall'ordinamento.
* Se si specifica nell'url ?theme={un tema} viene utilizzato uno dei temi di tablesorter, per default il tema è "green".


## known issues
* avevo provato ad usare gli sticky headers di tablesorter, ma per ora senza successo.
* in teoria, generate dovrebbe spegnere il server dopo aver generato la pagina.
Questo parrebbe succedere spesso, ma ogni tanto no (random).
Ci prova server.stop(), e inoltre se non erro è ciò a cui
dovrebbe servire il poll_interval passato a serve_forever.
