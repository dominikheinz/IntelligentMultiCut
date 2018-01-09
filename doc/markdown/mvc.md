# Architektur (MVC)   
<b>designed by André Döring & Ruben Klepp</b>

### Model  

Jede Klasse, die als Model agiert, wie z.B. <b>User, MetaData</b> etc, wird unter <code>src/classes/models/</code> abgespeichert und kann
von einer Controller Klasse verwendet werden.

### Controller

Controller werden unter <code>src/classes/controllers/</code> abgelegt. Controller <b>veerben</b> von der (Basis-)Klasse <code>Base</code> und haben somit
die Möglichkeit auf Core Attribute (wie z.B. <code>Config</code>) der Elternklasse zuzugreifen.

### View

Hier wird die GUI entstehen und abgelegt. Daten werden von der View an den Controller gegeben und durch den Controller verarbeitet und zurück an die GUI (View gegeben).




