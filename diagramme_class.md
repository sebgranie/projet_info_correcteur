# Diagramme de classe

```puml
@startuml

class Dictionnaires {

}

Dictionnaires *-- "2" Dictionnaire
Dictionnaire ^-- Dictionnaires

class Dictionnaire {
  + Dictionnaire(list: mots)
  + RechercherMot(string: mot) : bool
  + CompterNombreMots() : int
  + AjouterMot(string: mot)
  + mots : list
}

interface gestionnaire_fichiers_py {
  + TransformerFichierListe(string: fichier) : list
  + TransformerListeFichier(list: mots, string: fichier)
}

interface distance_entre_mots_py {
  + CalculDistanceMots(string: mot1, string: mot2) : int
}

class CorrecteurInteractif {
  + CorrecteurInteractif(string: fichier_text_origi nal, string: fichier_text_corrige, string: fichier_correction, int: seuil, Dictionnaires: dictionnaires)
  + CorrigeTexte()
  + list : texte
}

CorrecteurInteractif --> gestionnaire_fichiers_py
CorrecteurInteractif --> distance_entre_mots_py
CorrecteurInteractif o-- Dictionnaires

class CorrecteurAutomatique {
  + CorrecteurAutomatique(string: fichier_text_original, string: fichier_text_corrige, int: seuil, Dictionnaires: dictionnaires)

}

CorrecteurAutomatique --> gestionnaire_fichiers_py
CorrecteurAutomatique --> distance_entre_mots_py
CorrecteurAutomatique o-- Dictionnaires

CorrecteurInteractif ^-- CorrecteurAutomatique

@enduml
```


Liste de mots en python

```py



dic1 = Dictionnaire(["arbre", "Animal", "vélo"])
dic2 = Dictionnaire(["voiture"])

dic2.AjouterMot("stylo")

```

Liste de mots dans un fichier dictionnaire

`perso.dic`:
```txt
arbre
Animal
vélo
```

@startuml{title.png}

class Animal {
}

class Elephant {
}

Animal ^-- Elephant

class Voiture {
}

class Roue {
}

Voiture *-- "4" Roue

@enduml
```