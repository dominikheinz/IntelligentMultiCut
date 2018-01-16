# Intelligent MultiCut

## Setup
Synchronisiere dein lokales Repository mit dem Remote Repsoitory auf Github.  
Für eine anschließende Installation bitte diese [Installationsanleitung](https://github.com/andredoering/multicut/wiki/Installation) 
befolgen

## Dokumentationen 
* [Klassen und Architektur](https://github.com/andredoering/multicut/blob/master/src/README.md)
* [Best Practise Error Ausgaben](https://github.com/andredoering/multicut/blob/master/doc/markdown/errors.md)
* [Algorithmen Erklärung](https://github.com/andredoering/multicut/blob/master/doc/markdown/algorithm.md)

## Hinzufügen von Config Attributen
1. Füge ein weiteres Key-Value Pair in die `src/config.json`. Es gehen auch  auch assoziative Arrays als Value. Tutorial zu [JSON](https://www.w3schools.com/js/js_json_syntax.asp)
2. Der Zugriff auf die Eigenschaften geschieht über die Base Klasse `self.config.get("key")`


## Base Class
Jede Klasse die von `Base` erbt, hat Zugriff auf Grundfunktionalitäten, die sinnvollerweise allen Klassen zur Verfügung stehen sollten (zum Beispiel Config Daten). 
So kannst du von Core erben:

    from src.classes.core.Base import Base
    class MyClass(Base):
        # dein Code

        def __init(self):
            print(self.config.get("debug"))

Die Base Klasse kann gerne erweitert werden um weitere Funktionalitäten, die allen zur Verfügung stehen sollten. Zum Beispiel eine Logging Klasse.


## Getestete Codecs (CutterController)
`MJPG` - extrem hohe Bitrate, große .AVI Dateien

`DIVX` - niedrige Bitrate, kleine .AVI Dateien



