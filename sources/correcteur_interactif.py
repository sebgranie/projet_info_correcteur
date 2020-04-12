import argparse
from dictionnaire import Dictionnaire, EnsembleDictionnaire
from gestionnaire_fichier import TransformerFichierListe, TransformerFichierTexte, TransformerListeFichier, TransformerTexteFichier
from acorrecteur import CorrecteurAutomatique

class CorrecteurInteractif(CorrecteurAutomatique):
    def __init__(self, seuil, dictionnaire): # définition du constructeur , les attributs de la classe sont toujours précédes de self.
        self.seuil = seuil                   # initialisation des attributs
        self.dictionnaire = dictionnaire

    def CorrigeMot(self, mot, ligne):
        '''
        L'objectif de cette fonction est de corriger un mot en proposant
        à l'utilisateur une série de mot qui se situe à une distance
        inférieure au seuil rentré par l'utilisateur. Elle renvoit le mot
        une fois corrigé.
        '''
        mots_possibles = self.dictionnaire.mots_possibles(mot.lower(),self.seuil)  # Variable locale qui est la liste des mots dont la distance entre
                                                                           # chacun de ses mots et le mot inconnu est inférieure au seuil.
        if not mots_possibles:  # Condition si aucun mot n'a été trouvé pour un certain mot inconnu du texte
            print(f"Aucun mots n'ont été trouvé dans les dictionnaires pour le mot érroné {mot}")
        else:

            print(f"\nLe mot {mot} (ligne {ligne}) n'est pas dans les dictionnaires.\n")

            for i in range(len(mots_possibles)):  # i varie entre 0 jusqu'au nombre de mots trouvés dans le dictionnaire possible - 1
                # Il est important d'ajuster l'indice i car range débute à 0 et un texte commence à la
                # première ligne et l'indice 0 d'une liste et le premier élément de la liste.
                print(f"{i+1}. {mots_possibles[i][1]} ({mots_possibles[i][0]})")

            print("\nSi vous souhaitez choisir une des propositions de corrections suivantes, veuillez saisir son numéro : ")
            print("Sinon, veuillez saisir + pour ajouter ce mot inconnu à votre dictionnaire personnel :")
            print("Si vous souhaitez garder ce mot sans l'ajouter à votre dictionnaire personnel, pressez entrer :")
            print("Notre dernière proposition est que vous corrigiez vous-même directement le mot, dans ce cas veuillez l'écrire à nouveau :")

            while True:  # Condition toujours vérifiée pour être sûr que l'utilisateur puisse effectuer un choix
                         # Il est important de vérifier que toutes les branches du while se termine par un return pour ne pas être bloqué.
                choix_utilisateur = input()  # Variable locale possèdant le choix de l'utilisateur

                if choix_utilisateur == "+":
                    self.dictionnaire.ajouter_mot(mot.lower()) # Ajout du mot inconnu au dictionnaire personnel
                    return mot  # Le mot inconnu est recopié à l'identique dans la liste corrige
                if choix_utilisateur == "": # Conservation du mot sans ajout au dictionnaire perso
                    return mot
                if choix_utilisateur.isalpha():  # L'utilisateur décide de réecrire le mot lui-même
                    return choix_utilisateur     # Le mot corrige par l'utilisateur remplace alors le mot inconnu
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
    parser.add_argument('seuil', action="store", type=int)
    parser.add_argument('dic_text', action="store", type=str)
    parser.add_argument('dic_perso', action="store", type=str)
    parser.add_argument('--strategie', action="store", default=2, type=int, help="1 = comparer chacun des mots avec ceux dans les dictionnaires.    \
                                                                       2 = produit les mots qui, suite à une opérations élémentaire sont dans les dictionnaires.")
    arguments = parser.parse_args()

    # Construction de l'objet dictionnaire fourni immuable
    dictionnaire_fixe = Dictionnaire(TransformerFichierListe(arguments.dic_text), \
                                     False)
    # Construction de l'objet dictionnaire perso muable
    dictionnaire_personnel = Dictionnaire(TransformerFichierListe(arguments.dic_perso), \
                                           True)
    # L'ensemble de dictionnaire permet d'encapsuler le contenu des 2 dictionnaires à
    # travers une interface unique
    ensemble_dictionnaire = EnsembleDictionnaire([dictionnaire_fixe, dictionnaire_personnel], arguments.strategie)

    # ( Instanciation de la classe CorrecteurInteratif )
    correcteur_interactif = CorrecteurInteractif(arguments.seuil, ensemble_dictionnaire)

    corrige, correction = correcteur_interactif.CorrigeTexte(TransformerFichierTexte(arguments.text_original))


    TransformerTexteFichier(corrige,arguments.text_corrige)

    TransformerTexteFichier(correction, arguments.text_correction)

    TransformerListeFichier(dictionnaire_personnel.mots, arguments.dic_perso)