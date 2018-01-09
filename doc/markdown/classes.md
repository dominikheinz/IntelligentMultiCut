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

(To-Do : Klasse noch unvollstaendig, ausfuehrliche Doku folgt zu einem spaeteren Zeitpunkt.) 

## View

### GUI
Diese Klasse dient der <b>Benutzerfreundlichkeit</b>, sowie der <b>Visualisierung</b> von Prozessen anderer Klassen.
Sie vereint alle im Programm vorhandenen Funktionalitäten und führt diese, infolge an einen entsprechenden Input, auch aus.
Aufgerufen und instanziiert wird sie in der Klasse: <b>App</b>

### VideoCutter
Diese Klasse übernimmt das <b>Zusammenschneiden</b> aller Videos basierend auf den Ergebnissen des Algorithmus. Der VideoCutter bekommt im Konstruktur eine Liste an <b>Quellpfaden</b>, den gewünschten <b>Ausgabepfad</b>, die Algoergebnisse in Form einer <b>Tupelliste</b> und die <b>Framerate</b>. In der aktuellsten Version wird die <b>Framerate</b> automatisch anhand des ersten Videos berechnet. Es wird davon ausgegangen, dass der Benutzer in der Länge synchronisierte Videos mit gleicher Framerate auswählt. Die <b>Cut-Methode</b> führt den eigentlichen Schnitt mit der <code>movie-py</code> lib aus.

### ProgressCalculator
Diese Klasse errechnet eine <b>Prozentzahl</b>, die an die Progressbar übergeben wird. Der Konstruktor bekommt eine Liste an <b>Videoquellpfaden</b> und errechnet alle weiteren Attribute selbst. Die <b>Calculate-Methode</b> betrachtet die <b>JSON-Ordner</b>, prüft die aktuelle Anzahl an Dateien und stellt sie ins Verhältnis zum erwarteten Endwert an Dateien. Die Kommunikation zwischen Progressbar und Calculator ist noch in Bearbeitung.

### FileManager
Diese Klasse dient dazu, <b>Dateioperationen</b> auszuführen. Im momentanen Stand beherbergt sie eine <b>Copy-Methode</b>, die eine Datei von einem Ort zu einem anderen Ort zu kopiert.

### ThumbnailCreator
Diese Klasse ist für das Erstellen von Videothumbnails verantwortlich. Die Thumbnails werden für die <b>Dateivorschau</b> in der GUI verwendet.

### Calculator
Diese Klasse wurde zum Zweck geschaffen, <b>zufällige Tupel</b> zu Testzwecken zu generieren. Momentan ist die Klasse noch nicht ganz bugfrei, da auch leere Tupel generiert werden, die den VideoCutter crashen lassen. Es ist nicht empfohlen diese Klasse zu verwenden.
