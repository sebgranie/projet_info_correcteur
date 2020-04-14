# Correcteur orthographique

[TOC]

## 1. Code

### 1.1. Dependences

* **Python3**

Nous avons utilisé Python3 pour réaliser ce projet. Veuillez vérifier que vous ayez cette version installée avant d'executer le code. Pour verifier que Python3 est bien installé sur votre systèm, executez:

```
python3 --version
```

Vous devriez avoir un resultat qui commence par 3. Example:

```
Python3 3.7.7
```

* **numpy**

Nous avons choisi d'utiliser la librairie `numpy` afin de faciliter la manipulation de matrices.

Installation:

```
pip3 install numpy
```


### 1.2. Diagramme de classe

Voici le diagramme de classe representant l'architecture de notre code. Les '_I_' en violet representent des fichiers comportants seuleument des fonctions.

![diagramme-classe](diagramme-classe.png)

### 1.3. Execution

Executer les commandes suivantes dans le terminal au niveau du dossier `projet_info_correcteur`:
Nous utiliserons le texte `resources/exemple1.txt` comme example de texte à corriger.

#### 1.4.1 Correcteur Interactif:

La commande suivante permets de lister les arguments obligatoires et optionels de ce correcteur:

```sh
python3 sources/icorrecteur.py --help
```

Voici un example sur system **Unix** (Linux et macOS):

```sh
python3 sources/icorrecteur.py ressources/example1.txt \
                               ressources/example1_corrige.txt \
                               ressources/example1_correction.txt \
                               4 \
                               ressources/frgut.dic \
                               ressources/dictionnaire_perso.dic
```

Voici le même exemple sur **Windows**:

```sh
python3 sources/icorrecteur.py ressources\example1.txt \
                               ressources\example1_corrige.txt \
                               ressources\example1_correction.txt \
                               4 \
                               ressources\frgut.dic \
                               ressources\dictionnaire_perso.dic
```

#### 1.4.2 Correcteur Automatique:

La commande suivante permets de lister les arguments obligatoires et optionels de ce correcteur:

```sh
python3 sources/acorrecteur.py --help
```

* **Unix** (Linux et macOS):

```sh
python3 sources/acorrecteur.py ressources/example1.txt \
                               ressources/example1_corrige.txt \
                               ressources/example1_correction.txt \
                               4 \
                               ressources/frgut.dic \
                               ressources/dictionnaire_perso.dic
```

* **Windows**:

```sh
python3 sources/acorrecteur.py ressources\example1.txt \
                               ressources\example1_corrige.txt \
                               ressources\example1_correction.txt \
                               4 \
                               ressources\frgut.dic \
                               ressources\dictionnaire_perso.dic
```



### 1.3. Tests

Le module `pytest` dois être installé pour executer les tests. Veuillez l'installer de cette manière:
```
pip3 install pytest
```

Pour executer tous les tests du projet, écrire:

```bash
$ pytest tests/
```

Voici les result attendu:

```
================================== test session starts ===================================
platform darwin -- Python 3.7.7, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: <chemin>/projet_info_correcteur
collected 8 items
tests/dictionnaire_test.py ....                                                    [ 50%]
tests/distance_entre_mots_test.py .                                                [ 62%]
tests/gestionnaire_fichier_test.py ...                                             [100%]

=================================== 8 passed in 0.43s ====================================
```

## 2. Analyse

Dependences

```
jupyterlab
matplotlib
```

Pour les installer:

```
pip3 install jupyterlab
pip3 install matplotlib
```


Pour utiliser matplotlib en interactif dans le Jupyter Lab:
Installer `conda`
```
conda install node.js
```