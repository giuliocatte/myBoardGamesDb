# myBoardGamesDb

Ero troppo pigro per fare un database dei miei giochi da tavolo, quindi ho fatto un
 software per generarlo a partire da [BoardGameGeek](https://boardgamegeek.com).

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
Al momento si può chiamare in due modi.
```
python bgg serve
```
tira su un server che risponde su http://localhost:8080/. Al momento l'unica chiamata sensata da fare in un browser è http://localhost:8080/owned.
```
python bgg generate
```
invece tira su il server, apre quella pagina su un browser, e poi
prova a spegnere il server
(tanto la pagina al momento non ha altre interazioni sul backend).

## known issues
* in teoria, chiamando l'url /owned?theme={un tema} si dovrebbe utilizzare un tema per la
tabella diverso dal default. In pratica, l'url sembra venir generato correttamente,
 ma il css per qualche motivo non funziona
* in teoria, generate dovrebbe spegnere il server dopo aver generato la pagina.
Questo parrebbe succedere ogni tanto (random), ma spesso no.
Ci prova server.stop(), e inoltre se non erro è ciò a cui
dovrebbe servire il poll_interval passato a serve_forever.
