import re
def TransformerFichierListe(fichier):
    '''
    Cette fonction transforme un fichier qui contient un mot
    par ligne en une liste contenant tout ces mots. Cette fonction
    est utilisée pour l'utilisation des dictionnaires.
    '''
    liste = []
    with open(fichier, "r") as f:
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
    with open(fichier, "r") as f:
        for ligne in f:
            # n contient iterativement chaque ligne du fichier.
            # on utilise split pour enlever le caractère
            # (unique) '\n' à la fin de la ligne
            mots_ligne = []
            for word in re.split(r'(\W+)',ligne):  # re.split permet de découper les mots du texte
                                                   # tout en conservant la ponctuation
                mots_ligne.append(word)

            texte.append(mots_ligne)
    return texte

def TransformerTexteFichier(texte ,fichier):
    '''
    L'objectif de cette fonction est de transformer
    notre liste de liste une fois corrigée, en fichier texte.
    On rappelle que chaque sous-liste contient les mots d'une
    seule ligne.
    '''
    with open(fichier, "w") as f:
        for ligne in texte:
            for mot in range(len(ligne)):
                if mot == len(ligne)-1:
                    f.write(ligne[mot]+"\n") # écrire le mot suivi du caractère unique \n
                                             # pour revenir à la ligne au prochain mot
                else:
                    f.write(ligne[mot]+" ")  # écrire le mot dans le fichier texte
                mot = mot + 1


def TransformerListeFichier(mots, fichier):
    '''
    Cette fonction transforme un liste de mots en un fichier
    sur lequel est écrit tous les mots de la liste avec un mot
    par ligne. Cette fonction est utilisée pour l'utilisation
    des dictionnaires.
    '''
    with open(fichier, "w") as f:
        for n in mots:
            f.write(n+"\n")
