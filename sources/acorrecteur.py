import argparse
import random
import logging
from dictionnaire import Dictionnaire, EnsembleDictionnaire
from gestionnaire_fichier import TransformerFichierListe_Dico, TransformerFichierListe_Texte, TransformerListeFichier_Dico, TransformerListeFichier_Texte

class CorrecteurAutomatique(object):
    def __init__(self, seuil, dictionnaire):
        self.seuil = seuil
        self.dictionnaire = dictionnaire

    def CorrigeTexte(self, texte):
        '''
        Corrige un texte passé en argument et
        retourne le corrige et un résume des corrections.
        '''
        corrige = []
        correction = []
        sous_liste = []
        mot_trouves = 0
        mot_inconnu = 0
        ligne = 1
        logging.debug(texte)
        print(f"Seuil : {self.seuil}")
        for mot in texte:
            if not mot.isalpha() or \
               self.dictionnaire.chercher_mot(mot.lower()) or \
               len(mot) < 2:
                if mot.isalpha():
                    mot_trouves +=1
                corrige.append(mot)
            else:
                mot_inconnu +=1
                mot_corrige = self.CorrigeMot(mot, ligne)

                corrige.append(mot_corrige)
                sous_liste.append([ligne, mot, mot_corrige])

            if "\n" in mot:
                ligne += 1

        correction.append(f"{mot_trouves} mots trouvés dans le dictionnaire.\n")
        correction.append(f"{mot_inconnu} mots inconnus.\n")
        for i in sous_liste:
            if i[2] == i[1]:
                correction.append(f"{i[0]}. {i[1]} \n")
            else:
                correction.append(f"{i[0]}. {i[1]} --> {i[2]}\n")

        return [corrige, correction]



    def CorrigeMot(self, mot, ligne):
        '''
        L'objectif de cette fonction est de corriger un mot en proposant
        à l'utilisateur une série de mot qui se situe à une distance
        inférieure au seuil rentré par l'utilisateur. Elle renvoit le mot
        une fois corrigé.
        '''
        mots_possibles = self.dictionnaire.mots_possibles(mot.lower(),self.seuil)

        mots_possibles_ordonnes = sorted(mots_possibles)
        mots_meme_distance = []
        if mots_possibles_ordonnes:
            for mot in mots_possibles_ordonnes:
                if mots_possibles_ordonnes[0][0] == mot[0]:
                    mots_meme_distance.append(mot[1])
            return random.choice(mots_meme_distance)
        else:
            return mot


if __name__ == '__main__':

# ArgumentParser permet d'améliorer la compréhension du programme
# vis à vis de l'utilisateur, en particulier quelle(s) variable(s) sont
# demandés en paramètres de la fonction.
    parser = argparse.ArgumentParser(description="Correction interactif d'un texte ")
    parser.add_argument('text_original', action="store", type=str)
    parser.add_argument('text_corrige', action="store", type=str)
    parser.add_argument('text_correction', action="store", type=str)
    parser.add_argument('dic_text', action="store", type=str)
    parser.add_argument('dic_perso', action="store", type=str)
    parser.add_argument('seuil', action="store", type=int)
    parser.add_argument('strategie', action="store", type=int, help="1 = comparer chacun des mots avec ceux dans les dictionnaires.    \
                                                                       2 = produit les mots qui, suite à une opérations élémentaire sont dans les dictionnaires.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    arguments = parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)



    # Construction de l'objet dictionnaire fourni immuable
    dictionnaire_fixe = Dictionnaire(TransformerFichierListe_Dico(arguments.dic_text), False)

    # Construction de l'objet dictionnaire perso muable
    dictionnaire_personnel = Dictionnaire(TransformerFichierListe_Dico(arguments.dic_perso), True)

    # L'ensemble de dictionnaire permet d'encapsuler le contenu des 2 dictionnaires à travers une interface unique
    ensemble_dictionnaire = EnsembleDictionnaire([dictionnaire_fixe, dictionnaire_personnel], arguments.strategie)

    # Construction de l'objet correcteur automatique
    correcteur_automatique = CorrecteurAutomatique(arguments.seuil, ensemble_dictionnaire)

    # On assigne à corrige et correction le résultat de la méthode CorrigeTexte sur l'objet correcteur_interactif
    corrige, correction = correcteur_automatique.CorrigeTexte(TransformerFichierListe_Texte(arguments.text_original))

    # On transfomr les liste corrige et correction sous forme de fichier
    TransformerListeFichier_Texte(corrige,arguments.text_corrige)
    TransformerListeFichier_Texte(correction, arguments.text_correction)

    # On transforme la liste de mots du dictionnaire personnel sous forme de fichier
    TransformerListeFichier_Dico(dictionnaire_personnel.mots_dico, arguments.dic_perso)
