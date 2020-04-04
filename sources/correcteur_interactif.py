import argparse
from gestionnaire_fichier import TransformerFichierListe, TransformerListeFichier, TransformerTexteFichier, TransformerFichierTexte
from distance_entre_mots import CalculDistanceMots
from dictionnaire import Dictionnaire, EnsembleDictionnaire


class CorrecteurInteractif(object):
    def __init__(self, seuil, dictionnaire): # définition du constructeur
        self.seuil = seuil
        self.dictionnaire = dictionnaire

    def CorrigeTexte(self, texte):
        '''
        Corrige un texte passe en argument et
        retourne le corrige et un resume des corrections.
        '''
        # corrige est une grande liste dans laquelle seront
        # encapsulées toutes les sous-listes de mots du texte
        # contenant uniquement des mots justes. Comme expliqué
        # precedemment, chaque sous-liste correspond à une
        # ligne du texte.

        # correction est une liste qui résume l'inventaire des
        # mots corrigés.
        corrige = []
        correction = []
        print(texte)
        for liste_mot in texte:
            sous_liste = []
            for mot in liste_mot:
                if self.dictionnaire.chercher_mot(mot.lower()) or len(mot) < 2: #le mot du texte se trouve dans le dictionnaire
                    sous_liste.append(mot)
                else:
                    pass
            corrige.append(sous_liste)

                # for mot_dico in self.dictionnaire:
                #     if len(liste_mot[mot]) < 2:
                #         pass
                #     if texte[liste_mot][mot] in self.dictionnaire:
                #         pass

                #     liste_mot_corriges = []
                #     if d[len(texte[liste_mot][mot])][self.dictionnaire[mot_dico]] != 0:
                #         print("Le mot" + texte[liste_mot][mot] + " est introuvable")
                #         print("Veuillez choisir l'une des corrections proposées ou \
                #                voulez-vous ajouter" + texte[liste_mot][mot] + \
                #               "au dictionnaire ?")
                #         liste_mots_possibles =[]
                #         if d[len(texte[liste_mot][mot])][self.dictionnaire[mot_dico]] <= self.seuil:
                #             liste_mots_possibles.append(self.dictionnaire[mot_dico])
                #         print("")




        return [corrige, correction]  #Liste contenant deux sous-listes décrites précedemment.


if __name__ == "__main__":

# ArgumentParser permet d'améliorer la compréhension du programme
# vis à vis de l'utilisateur , en particulier quelle(s) variable(s) sont
# demandés en paramètres de la fonction.
    parser = argparse.ArgumentParser(description="Correction interactif d'un texte ")
    parser.add_argument('text_original', action="store", type=str)
    parser.add_argument('text_corrige', action="store", type=str)
    parser.add_argument('text_correction', action="store", type=str)
    parser.add_argument('seuil', action="store", type=int)
    parser.add_argument('dic_text', action="store", type=str)
    parser.add_argument('dic_perso', action="store", type=str)
    arguments = parser.parse_args()

    # L'objet argument permet d'obtenir les arguments du programme
    print(arguments.text_original)
    print(arguments.text_corrige)
    print(arguments.text_correction)
    print(arguments.seuil)
    print(arguments.dic_text)
    print(arguments.dic_perso)

    # dictionnaire fourni immuable
    dictionnaire_fixe = Dictionnaire(TransformerFichierListe(arguments.dic_text), \
                                     False)
    # dictionnaire perso muable
    dictionnaire_personnel = Dictionnaire(TransformerFichierListe(arguments.dic_perso), \
                                           True)
    # L'ensemble de dictionnaire permet d'encapsuler le contenu des 2 dictionnaires à
    # travers une interface unique
    ensemble_dictionnaire = EnsembleDictionnaire([dictionnaire_fixe, dictionnaire_personnel])

    # Instanciation de la classe CorrecteurInteratif
    correcteur_interactif = CorrecteurInteractif(arguments.seuil, ensemble_dictionnaire)

    #
    corrige, correction = correcteur_interactif.CorrigeTexte(TransformerFichierTexte(arguments.text_original))

    # L'objectif est de reformer le texte initialement à corriger par
    # le texte composé uniquement de mots justes. Cette fonction utilise
    # pour cela la liste corrigée composée de tous les mots du texte.
    TransformerTexteFichier(corrige ,arguments.text_corrige)