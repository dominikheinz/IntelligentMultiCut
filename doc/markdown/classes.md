# Klassen

## Core

### App

Die Klasse App dient als Hauptapplikation. Diese Klasse wird in <code>main.py</code> instanziiert und beinhaltet alle Controller, Views und Models. 

### Config

Diese Klasse dient zum einlesen der <code>/src/config.json</code>, welche feste Applikationsparameter beinhaltet (<i>wie z.B. debug mode, verbose etc.</i>). 
Alle Parameter werden als Attribute in einem <b>dictionary</b> gespeichert und können mit <code>get()</code> von außen erfragt werden. Sie wird in der <b>Base</b> Klasse includiert und wird jedem Controller durch Polymorphie zur Verfügung gestellt.

## Controller

### Base

Diese Klasse ist eine Basisklasse, welche als Oberklasse für die Controller dient. Sie beinhaltet Core Attribute (<i>z.B. Config</i>) und stellt durch Polymorphie jeder veerbten Kindklasse die Attribute zur Verfügung.

### OpenPoseController   
 
Dieser Controller dient zur Verwaltung und Benutzung des <b>OpenPose</b> Frameworks.
Es führt die <code>OpenPoseDemo.exe</code> mit gewünschten (von der View gesetzten) Parametern aus.
Die Methode <code>process(video_name)</code> verarbeitet ein Video welches sich unter <code>/import/videos</code> befinden muss und speichert z.B. die <b>Keypoints</b>
im JSON Format unter <code>/export/json/video_name</code> ab. 

### PoseAnalysis

Dieser Controller dient dazu die erkannten Personen anhand diverser Kriterien zu gewichten.
Der bereitgestellte Wert kann genutzt werden um die beste Kameraperspektive mit den errechneten Posen zu bestimmen.

### CleanController

Dieser Controller kümmert sich um Aufräumarbeiten. Er löscht generierte JSON Dateien.

### CutterController

Diese Klasse übernimmt das <b>Zusammenschneiden</b> aller Videos basierend auf den Ergebnissen des Algorithmus. Der CutterController bekommt im Konstruktur eine Liste an <b>Quellpfaden</b>, die Algoergebnisse in Form einer <b>Tupelliste</b> und die <b>Framerate</b> für das Ausgabevideo. Es wird davon ausgegangen, dass der Benutzer Videos mit gleicher Framerate auswählt. Die <b>Cut-Methode</b> führt den eigentlichen Schnitt mit der <code>OpenCV</code> lib aus.

Der Cutter wurde in seiner Funktionalität dahingehend erweitert, dass er nun auch das Synchronisieren von Eingabevideos übernimmt. Hierzu wird der <code>SyncController</code> eingesetzt, der den abzuschneidenen Teil anhand der Audiospur ermittelt.

### SnycController

Diese Klasse übernimmt das Synchronisieren von Videos über die Detektion eines lauten Geräusches. Aus allen Videos werden die Tonspuren extrahiert und analysiert. Findet der Controller einen Ausschlag in der Lautstärkekurve, der einen gewissen Grenzbereich überschreitet, so wird dieser Zeitpunkt als neuer Startzeitpunkt für das Video genommen. Der Bereich bis zum neuen Startpunkt wird durch den CutterController abgeschnitten.

### ProgressCalculator

Diese Klasse errechnet eine <b>Prozentzahl</b>, die an die Progressbar übergeben wird. Der Konstruktor bekommt eine Liste an <b>Videoquellpfaden</b> und errechnet alle weiteren Attribute selbst. Die <b>Calculate-Methode</b> betrachtet die <b>JSON-Ordner</b>, prüft die aktuelle Anzahl an Dateien und stellt sie ins Verhältnis zum erwarteten Endwert an Dateien.

## View

### GUI

Diese Klasse dient der <b>Benutzerfreundlichkeit</b>, sowie der <b>Visualisierung</b> von Prozessen anderer Klassen.
Sie vereint alle im Programm vorhandenen Funktionalitäten und führt diese, infolge an einen entsprechenden Input, auch aus.
Aufgerufen und instanziiert wird sie in der Klasse: <b>App</b>

### FileManager

Diese Klasse dient dazu, <b>Dateioperationen</b> auszuführen. Im momentanen Stand beherbergt sie eine <b>Copy-Methode</b>, die eine Datei von einem Ort zu einem anderen Ort zu kopiert.

### ThumbnailCreator

Diese Klasse ist für das Erstellen von Videothumbnails verantwortlich. Die Thumbnails werden für die <b>Dateivorschau</b> in der GUI verwendet.

### Calculator

Diese Klasse wurde zum Zweck geschaffen, <b>zufällige Tupel</b> zu Testzwecken zu generieren. Momentan ist die Klasse noch nicht ganz bugfrei, da auch leere Tupel generiert werden, die den VideoCutter crashen lassen. Es ist nicht empfohlen diese Klasse zu verwenden.
