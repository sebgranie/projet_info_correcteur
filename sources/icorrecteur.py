import argparse
import logging
from dictionnaire import Dictionnaire, EnsembleDictionnaire
from gestionnaire_fichier import TransformerFichierListe_Dico, TransformerFichierListe_Texte, TransformerListeFichier_Dico, TransformerListeFichier_Texte

class CorrecteurInteractif(object):
    def __init__(self, dictionnaire):
        self.dictionnaire = dictionnaire

    def CorrigeTexte(self, texte):
        '''
        Corrige un texte passe en argument et
        retourne le corrige et un résume des corrections.
        '''
        corrige = []
        correction = []
        sous_liste = []
        mot_trouves = 0
        mot_inconnu = 0
        ligne = 1
        logging.debug(texte)
        for mot in texte:
            if not mot.isalpha() or \
               self.dictionnaire.chercher_mot(mot.lower()) or \
               len(mot) < 2:
                if mot.isalpha():
                    mot_trouves +=1
                corrige.append(mot)
            else:
                seuil = int(len(mot)/2)
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
        inférieure à la moitié de la taille du mot inconnu. Elle renvoit le mot
        une fois corrigé.
        '''
        seuil = int(len(mot)/2)
        mots_possibles = self.dictionnaire.mots_possibles(mot.lower(),seuil)

        if not mots_possibles:
            print(f"Aucun mots n'ont été trouvé dans les dictionnaires pour le mot érroné {mot}")
        else:

            mots_possibles = sorted(mots_possibles)

            print(f"\nLe mot {mot} (ligne {ligne}) n'est pas dans les dictionnaires.\n")
            print(f"Seuil : {seuil}")
            for i in range(len(mots_possibles)):
                print(f"{i+1}. {mots_possibles[i][1]} ({mots_possibles[i][0]})")

            print("\nSi vous souhaitez choisir une des propositions de corrections suivantes, veuillez saisir son numéro : ")
            print("Sinon, veuillez saisir + pour ajouter ce mot inconnu à votre dictionnaire personnel :")
            print("Si vous souhaitez garder ce mot sans l'ajouter à votre dictionnaire personnel, pressez entrer :")
            print("Notre dernière proposition est que vous corrigiez vous-même directement le mot, dans ce cas veuillez l'écrire à nouveau :")

            while True:
                choix_utilisateur = input()

                if choix_utilisateur == "+":
                    self.dictionnaire.ajouter_mot(mot.lower())
                    return mot
                if choix_utilisateur == "":
                    return mot
                if choix_utilisateur.isalpha():
                    return choix_utilisateur
                else:
                    try:
                        reponse_utilisateur_integer = int(choix_utilisateur)
                        if reponse_utilisateur_integer < 1 or reponse_utilisateur_integer > len(mots_possibles):
                            print("Veuillez recommencer votre demande avec un chiffre approprié.")
                        else:
                            return mots_possibles[reponse_utilisateur_integer - 1][1]
                    except ValueError:
                        print("Votre saisie n'est pas adaptée, veuillez recommencer")

        return mot


if __name__ == "__main__":

# ArgumentParser permet d'améliorer la compréhension du programme
# vis à vis de l'utilisateur, en particulier quelle(s) variable(s) sont
# demandés en paramètres de la fonction.
    parser = argparse.ArgumentParser(description="Correction interactif d'un texte ")
    parser.add_argument('text_original', action="store", type=str)
    parser.add_argument('text_corrige', action="store", type=str)
    parser.add_argument('text_correction', action="store", type=str)
    parser.add_argument('dic_text', action="store", type=str)
    parser.add_argument('dic_perso', action="store", type=str)
    parser.add_argument('strategie', action="store", type=int, help="1 = comparer chacun des mots avec ceux dans les dictionnaires.    \
                                                                       2 = produit les mots qui, suite à une opérations élémentaire sont dans les dictionnaires.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    arguments = parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Construction de l'objet dictionnaire fourni immuable
    dictionnaire_fixe = Dictionnaire(TransformerFichierListe_Dico(arguments.dic_text), False)

    # Construction de l'objet dictionnaire perso muable
    liste_mots_dic_perso = []
    try:
        liste_mots_dic_perso = TransformerFichierListe_Dico(arguments.dic_perso)
    except FileNotFoundError as f:
        print("Vous avez choisi un fichier inexistant.")
    dictionnaire_personnel = Dictionnaire(liste_mots_dic_perso, True)

    # L'ensemble de dictionnaire permet d'encapsuler le contenu des 2 dictionnaires à travers une interface unique
    ensemble_dictionnaire = EnsembleDictionnaire([dictionnaire_fixe, dictionnaire_personnel], arguments.strategie)

    # ( Instanciation de la classe CorrecteurInteratif )
    correcteur_interactif = CorrecteurInteractif(ensemble_dictionnaire)

    # On assigne à corrige et correction le résultat de la méthode CorrigeTexte sur l'objet correcteur_interactif
    corrige, correction = correcteur_interactif.CorrigeTexte(TransformerFichierListe_Texte(arguments.text_original))

    # On transforme les listes utilisées dans le programme sous forme de fichier
    TransformerListeFichier_Texte(corrige,arguments.text_corrige)
    TransformerListeFichier_Texte(correction, arguments.text_correction)

    # On transforme le dictionnaire personnel (liste) sous forme de fichier
    TransformerListeFichier_Dico(dictionnaire_personnel.mots_dico, arguments.dic_perso)
