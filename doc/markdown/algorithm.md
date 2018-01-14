# Algorithmen   
<b>Designed by Dominik Heinz & Gero Knoblauch</b>

### Allgemeines
Intelligent Multicut stellt <b>4 verschiedene Algorithmen</b> zur Verfügung, die je nach Anwendungsszenario anders arbeiten. Die Steuerung aller Algorithmen erfolgt über die <code>AlgorithmController.py</code> Klasse. Jeder Algorithmus kann per ID aufgerufen werden.

1. AlgorithmController
2. Algorithmen
   * Singleperson
   * Multiperson Closeup
   * Multiperson Peoplecount
   * DistanceDetection  
3. Korrekturmaßnahmen

### 1. AlgorithmController 

Der AlgorithmController ist für die <b>Steuerung der einzelnen Algorithmen</b> zuständig.
Er wird im Konstruktor mit einem <code>MetaDataController</code> Objekt initialisiert.
Die Klasse bietet zwei Funktionen <code>run_algorithm(self, algo_id)</code> und <code>filter_cut_frames(self, switch_frames)</code>.
Die <code>filter_cut_frames(self, switch_frames)</code> Methode extrahiert die Frames an denen die Videos gecuttet werden sollen.
Die <code>run_algorithm(self, algo_id)</code> Methode wendet einen Algorithmus auf die im Konstruktor übergebenen Metadaten an. Der Parameter <code>algo_id</code> kann <code>0</code>, <code>1</code>, <code>2</code> oder <code>3</code> sein und verwendet dementsprechend die versch. Algorithmen.

### 2. Algorithmen

#### 2.1. Singleperson

Der Singleperson-Algorithmus errechnet errechnet in jedem Frame von der erkannten Person die Genauigkeit aller Gelenke.
Anschliessend wird davon der Durchschnitt errechnet. Das hat zur Folge die Kamera in der die Person bei der mehr Gelenke erkannt werden einen höheren Score zugeteilt bekommen. Dementsprechend wird immer auf die Kamera geschaltet in der von der Person möglichst viele Körperteile mit einer hohen Genauigkeit erkannt werden.
Die Methode <code>def run_pose_algorithm(self, show_graph):</code> wendet den Algorithmus auf die im Konstruktor übergebenen Frames an und gibt das ein Array zurück das angibt wie die Clips geschnitten werden müssen.
Der boolsche Parameter <code>show_graph</code> bietet die Möglichkeit einen Graphen nach erfolgreicher Prozessierung anzuzeigen um nachvollziehen zu können wie der Algorithmus gearbeitet hat.
Hier ist das Beispiel einer Person die in einem Gang zwischen zwei Kameras auf und ab laeuft.

![alt-text-2](https://i.imgur.com/alesAzE.jpg)

Ist die Person mit dem Ruecken zu der einen Kamera gedreht ist sie von der Vorderseite von der anderen Seite zu sehen.
Dementsprechend ist die Genauigkeit der Posenerkennung geringer wenn man die Person von der Rueckseite sieht.
Der Graph zeigt wie die Genaugkeit wischen den zwei Kameras zyklisch wechselt, - mit jeder Drehung weg von der einen zu der anderen Kamera.

#### 2.2. Multiperson Closeup

Der Multiperson-Closeup Algorithmus vereint den Distance Detection Algorithmus und den Mutiperson Algorithmus.
Der Algorithmus prueft von allen erkannten Personen in einem Frame welche am naehsten zur Kamera steht.
Die Kamera in der eine Person am naehsten zur Kamera steht bekommt einen hoeheren Score und wird dementsprechend den anderen bevorzugt.

#### 2.3. Multiperson Peoplecount

Der Multiperson-Peoplecount Algorithmus prueft alle erkannten Personen in einem Frame. Die Kameraperspektive in der die meisten Personen erkannt werden, wird bevorzugt.

#### 2.4. DistanceDetection

Der Distance Detection Algorithmus wählt die Kamera in der die erkannte Person am nähsten an der Kamera ist.

<img src="Distance1.gif?raw=true"> ![alt-text-2](https://i.imgur.com/aDejcoV.jpg)

Der Algorithmus errechnet anhand von <b>Augenabstand</b> und <b>Augen-Nasen-Abstand</b>.
Je näher die Person an die Kamera kommt desto groesser werden die Abstände und dementsprechend der finale Score.
Der Algorithmus wird im Konstruktor mit den Frames initialisiert.
Die Methode <code>def run_distance_algorithm(self, show_graph):</code> wendet den Algorithmus auf die Frames an.
Der boolsche Parameter <code>show_graph</code> bietet die Möglichkeit einen Graphen nach erfolgreicher Prozessierung anzuzeigen um nachvollziehen zu können wie der Algorithmus gearbeitet hat.
Nach erfolgreicher Bearbeitung gibt die <code>def run_distance_algorithm(self, show_graph):</code> ein Array mit den Informationen zurück an welcher Kamera zu welchem Zeitpunkt geschnitten werden soll.

### 3. Korrekturmaßnahmen

Nicht selten kommt es vor dass das OpenPose Framework bei der Videoanalyse Personen falsch erkennt. Diese Messfehler beinflussen die Ergebnisse der Algorithmen. 
Aus diesem Grund werden Messdaten mithilfe eines Smoothing Algorithmus korrigiert.
Die Messdaten werden mithilfe von <b>median filtering</b> geglättet.
Dabei gibt der smoothing factor <code>s</code> an wieviele Werte links und rechts in die Glattung mit einberechnet werden.
Die Werte werden nach groesse sortiert und der mittlere Wert wird verwendet.
Nehmen wir an wir haben ein smoothing factor von <code>3</code>
Das heisst wir pruefen von unserem aktuellen Wert, bspw. <code>7</code> je 3 Werte davor und danach.
Das koennte Bspw so aussehen: <code>[4,8,6,7,9,6,4]</code>. Diese Werte werden sortiert. Das ergibt folgende Zahlenfolge:
<code>[4,4,6,6,7,8,9]</code>. Davon wird der mittlere Wert, also <code>6</code> wird verwerwendet.

Hier ein Beispiel von einem un-gesmoothtem Graph (am Bsp Distance Detection Algorithmus):
![alt-text-2](https://i.imgur.com/mniifra.jpg)

Man erkennt die Ausschlaege in dem Graphen, was ohne einen Threshold zu flickering beim Output-Video kommt.
Die Messfehler kommen grossteils wegen der <b>Messfehler von Openpose</b>.
Hier der selbe Graph nach der Fehlerkorrektur:

![alt-text-2](https://i.imgur.com/NC5ECoW.jpg)

Die Ubergange haben keine grossen Ausreisser mehr und die Ubergange sind glatter.
