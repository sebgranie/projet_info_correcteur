import re

def TransformerFichierListe(fichier):
    '''
    Cette fonction transforme un fichier qui contient un mot
    par ligne en une liste contenant tout ces mots. Cette fonction
    est utilisée pour l'utilisation des dictionnaires.
    '''
    liste = []
    with open(fichier, "r", encoding='utf-8') as f:
        for n in f:
            for word in n.split():
                liste.append(word)
    return liste

def TransformerFichierTexte(fichier):
    '''
    Cette fonction transforme le fichier texte à
    corriger en une liste de liste de mots qui pourra
    être affichée lors de l'éxécution du programme
    en rajoutant la commande "-v" à la fin des
    arguments requis par le programme.
    '''
    texte = []
    with open(fichier, "r", encoding='utf-8') as f:
        for ligne in f:
            for word in re.split(r'(\W+)',ligne):  # re.split permet de découper les mots du texte
                                                    # tout en conservant la ponctuation
                texte.append(word)

    return list(filter(None, texte))  # filter permet d'enlever les caractères de taille 0 exemple ""

def TransformerTexteFichier(texte ,fichier):
    '''
    L'objectif de cette fonction est de
    transformer nos liste corrige et correction
    une fois corrigée, en fichier texte.
    '''
    with open(fichier, "w", encoding='utf-8') as f:
        for mot in texte:
            f.write(mot)

def TransformerListeFichier(mots, fichier):
    '''
    Cette fonction transforme un liste de mots en
    un fichier. Cette fonction est utilisée dans notre
    programme pour transformer le format des dictionnaires.
    '''
    with open(fichier, "w", encoding='utf-8') as f:
        for n in mots:
            f.write(n + "\n")
