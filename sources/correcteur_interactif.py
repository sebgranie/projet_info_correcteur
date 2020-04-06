import argparse
from dictionnaire import Dictionnaire, EnsembleDictionnaire
from distance_entre_mots import CalculDistanceMots
from gestionnaire_fichier import TransformerFichierListe, TransformerFichierTexte, TransformerListeFichier, TransformerTexteFichier

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
        mot_trouves = 0
        mot_inconnu = 0
        ligne = 1
        print(texte)
        print(f"Seuil : {self.seuil}")
        for mot in texte:
            if not mot.isalpha() or \
               self.dictionnaire.chercher_mot(mot.lower()) or \
               len(mot) < 2:   #  soit de taille inférieure à 2, soit qui
                               #  se trouve dans le dictionnaire, soit qui
                               #  ne comporte pas que des lettres de l'alphabet
                mot_trouves +=1
                corrige.append(mot)
            else:
                mot_inconnu +=1
                corrige.append(self.CorrigeMot(mot, ligne))

            if "\n" in mot:
                ligne += 1

        return [corrige, correction]  #Liste contenant deux sous-listes décrites précedemment.

    def CorrigeMot(self, mot, ligne):
        '''
        L'objectif de cette fonction est de corriger un mot en proposant
        à l'utilisateur une série de mot qui se situe à une distance
        inférieure au seuil rentré par l'utilisateur. Elle renvoit le mot
        une fois corrigé.
        '''
        mots_possibles = self.dictionnaire.mots_possibles(mot,self.seuil)
        if len(mots_possibles) == 0:
            print(f"Aucun mots n'ont été trouvé dans les dictionnaires pour le mot érroné {mot}")
        else:
            # print(mots_possibles)
            # print(mot)
            # print()
            print(f"Le mot {mot} (ligne {ligne}) n'est dans les dictionnaires.")
            for i in range(len(mots_possibles)):
                print(f"{i+1}. {mots_possibles[i]} ({int(CalculDistanceMots(mot, mots_possibles[i]))})")
            print()
            print("Si vous souhaitez choisir une des propositions de corrections suivantes, veuillez saisir son numéro : ")
            print("Sinon, veuillez saisir + pour ajouter ce mot inconnu à votre dictionnaire personnel :")
            print("Si vous souhaitez garder ce mot sans l'ajouter à votre dictionnaire personnel, pressez entrer :")
            print("Notre dernière proposition est que vous corrigiez vous-même directement le mot, dans ce cas veuillez l'écrire à nouveau :")

            while True:
                choix_utilisateur = input()

                if choix_utilisateur == "+":
                    self.dictionnaire.ajouter_mot(mot)
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
                            return mots_possibles[reponse_utilisateur_integer - 1]
                    except ValueError:
                        print("Votre saisie n'est pas adaptée, veuillez recommencer")

        return mot

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

    corrige, correction = correcteur_interactif.CorrigeTexte(TransformerFichierTexte(arguments.text_original))

    # L'objectif est de reformer le texte initialement à corriger par
    # le texte composé uniquement de mots justes. Cette fonction utilise
    # pour cela la liste corrigée composée de tous les mots du texte.
    TransformerTexteFichier(corrige ,arguments.text_corrige)

    TransformerListeFichier(dictionnaire_personnel.mots, arguments.dic_perso)