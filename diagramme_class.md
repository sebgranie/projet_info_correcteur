# Diagramme de classe

```puml
@startuml

class EnsembleDictionnaire {
  + __init__(list: dictionnaires, int: strategie)
  + production_mots(str: mot_inconnu)
  + dictionnaires : list
  + strategie : int
}

EnsembleDictionnaire o-- "2" Dictionnaire
Dictionnaire ^-- EnsembleDictionnaire

class Dictionnaire {
  + __init__(list: mots, bool: muable)
  + chercher_mot(str: mot) : bool
  + compter_nombre_mots() : int
  + ajouter_mot(str: mot)
  + mots_possibles(str: mot_inconnu, int: seuil)
  + mots : list
  + muable : bool
}

interface gestionnaire_fichier_py {
  + TransformerFichierListe(str: fichier) : list
  + TransformerListeFichier(list: mots, str: fichier)
  + TransformerFichierTexte(str: fichier)
  + TransformerTexteFichier(list: texte, str: fichier)
  + TransformerListeCsv(str: liste, str: fichier)
}

interface distance_entre_mots_py {
  + CalculDistanceMots(str: mot1, str: mot2) : int
}

class CorrecteurAutomatique {
  + __init__(int: seuil, EnsembleDictionnaire: dictionnaire)
  + CorrigeTexte(list: texte) : str, str
  + CorrigeMot(str: mot, int: ligne) : str
  + seuil : int
  + dictionnaire : EnsembleDictionnaire
}

class CorrecteurInteractif {
  + __init__(int: seuil, EnsembleDictionnaire: dictionnaire)
  + CorrigeMot(str: mot, int: ligne) : str
}

CorrecteurInteractif --> gestionnaire_fichier_py
CorrecteurInteractif o-- EnsembleDictionnaire
CorrecteurAutomatique --> gestionnaire_fichier_py
Dictionnaire --> distance_entre_mots_py
CorrecteurAutomatique o-- EnsembleDictionnaire
CorrecteurAutomatique ^-- CorrecteurInteractif

@enduml
```
