import re
import csv


def TransformerFichierListe(fichier):
    '''
    Cette fonction transforme un fichier qui contient un mot
    par ligne en une liste contenant tout ces mots. Cette fonction
    est utilisée pour l'utilisation des dictionnaires.
    '''
    liste = []
    with open(fichier, "r", encoding = 'utf-8') as f:
        for n in f:
            # n contient iterativement chaque ligne du fichier.
            # on utilise split pour enlever le caractère
            # (unique) '\n' à la fin de la ligne
            for word in n.split():
                liste.append(word)
    return liste

def TransformerFichierTexte(fichier):
    '''
    Cette fonction transforme le fichier texte à corriger
    du prof en une liste de liste de mots. Chaque sous-liste
    correspond aux mots d'une ligne du texte initial.
    Le but est de faciliter la remise en forme du texte corrigé
    où chaque fin de liste correspond à un saut de ligne.
    '''
    texte = []
    with open(fichier, "r", encoding = 'utf-8') as f:
        for ligne in f:
            for word in re.split(r'(\W+)',ligne):  # re.split permet de découper les mots du texte
                                                    # tout en conservant la ponctuation
                texte.append(word)

    return list(filter(None, texte))  # filter permet d'enlever les caractères de taille 0 exemple ""

def TransformerTexteFichier(texte ,fichier):
    '''
    L'objectif de cette fonction est de transformer
    notre liste de liste une fois corrigée, en fichier texte.
    On rappelle que chaque sous-liste contient les mots d'une
    seule ligne.
    '''
    with open(fichier, "w", encoding = 'utf-8') as f:
        for mot in texte:
            f.write(mot)  # écrire le mot dans le fichier texte

def TransformerListeFichier(mots, fichier):
    '''
    Cette fonction transforme un liste de mots en un fichier
    sur lequel est écrit tous les mots de la liste avec un mot
    par ligne. Cette fonction est utilisée pour l'utilisation
    des dictionnaires.
    '''
    with open(fichier, "w", encoding = 'utf-8') as f:
        for n in mots:
            f.write(n+"\n")

def TransformerListeCsv(liste, fichier):
    '''
    Toutes les listes en entrée de la fonction sont de taille 4.
    L'objectif est de transformer toutes les sous-listes qui composent la liste
    en entrée sous forme de tableau.
    '''
    with open(fichier, 'a+', encoding = 'utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for n in liste:
            csvwriter.writerow(n)