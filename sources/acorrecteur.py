import argparse
import random
from dictionnaire import Dictionnaire, EnsembleDictionnaire
from distance_entre_mots import CalculDistanceMots
from gestionnaire_fichier import TransformerFichierListe, TransformerFichierTexte, TransformerListeFichier, TransformerTexteFichier


class CorrecteurAutomatique(object):
    def __init__(self, seuil, dictionnaire): # définition du constructeur , les attributs de la classe sont toujours précédes de self.
        self.seuil = seuil                   # initialisation des attributs
        self.dictionnaire = dictionnaire

    def CorrigeTexte(self, texte):
        '''
        Corrige un texte passe en argument et
        retourne le corrige et un resume des corrections.
        '''
        # corrige est la liste qui contient le texte une fois corrigé.
        # correction est une liste qui résume l'historique des mots corrigés.
        corrige = []
        correction = []
        sous_liste = []
        # On initialise des compteurs permettant d'être réutiliser dans les
        # messages renvoyés à l'utilisateur.

        mot_trouves = 0
        mot_inconnu = 0
        ligne = 1
        print(texte)
        print(f"Seuil : {self.seuil}")
        for mot in texte:    # On itère successivement chacun des caractères de la liste texte à corriger
            if not mot.isalpha() or \
               self.dictionnaire.chercher_mot(mot.lower()) or \
               len(mot) < 2:   #  soit qui ne comporte pas que des lettres de l'alphabet,
                               #  soit qui se trouve dans le dictionnaire,
                               #  soit de taille inférieure à 2.
                if mot.isalpha():  #  .isalpha() est utile pour vérifier qu'un str
                                   #  comporte ou non uniquement des lettres de l'alphabet.
                    mot_trouves +=1  # incrémentation du compteur du nombre de mots connus trouvé dans le texte
                corrige.append(mot)  # Ajout par conséquent de ce mot à la liste corrige
            else:
                mot_inconnu +=1  # Ici sont comptés tous les mots qui vont subir une correction
                mot_corrige = self.CorrigeMot(mot, ligne)  # Déclaration de la variable locale pour permettre
                                                           # de la réutilliser plusieurs fois par la suite
                corrige.append(mot_corrige)  # On ajoute mot à la liste corrige une fois être
                                             # passé dans la méthode CorrigeMot
                sous_liste.append([ligne, mot, mot_corrige])  # Création d'une sous-liste d'information concernant un mot
                                                              # initialement inconnu qui est ensuite ajoutée à la liste correction

            # Condition de détection du caractère unique \n caractéristique d'un retour à la ligne.
            # Ceci permet de garder la forme du texte initial lors de la remise en forme du texte, constitué des mots corrigés.
            if "\n" in mot:
                ligne += 1  # Incrémentation du nombre de ligne

        # Message communiqué à l'utilisateur sur le nombre de mots sans correction et ayant potentiellement subi une correction.
        correction.append(f"{mot_trouves} mots trouvés dans le dictionnaire.\n")
        correction.append(f"{mot_inconnu} mots inconnus.\n")
        for i in sous_liste:   # Itération parmi les sous-liste de la liste correction
            correction.append(f"{i[0]}. {i[1]} --> {i[2]}\n")  # Message communiqué à l'utilisateur renseignant sur la ligne,
                                                 # le mot inconnu et sa transformation finale dans la liste de mots corrigés.

        return [corrige, correction]  #Liste contenant deux sous-listes décrites précedemment.



    def CorrigeMot(self, mot, ligne):
        '''
        L'objectif de cette fonction est de corriger un mot en proposant
        à l'utilisateur une série de mot qui se situe à une distance
        inférieure au seuil rentré par l'utilisateur. Elle renvoit le mot
        une fois corrigé.
        '''
        mots_possibles = self.dictionnaire.mots_possibles(mot,self.seuil)  # Variable locale qui est la liste des mots dont la distance entre
                                                                           # chacun de ses mots et le mot inconnu est inférieure au seuil.
        u = self.seuil
        mots_possibles_egale_distance = []
        for i in range(len(mots_possibles)):  # i varie entre 0 jusqu'au nombre de mots trouvés dans le dictionnaire possible - 1
            while CalculDistanceMots(mot, mots_possibles[i]) < u:
                u = CalculDistanceMots(mot, mots_possibles[i])
            if u == CalculDistanceMots(mot, mots_possibles[i]):
                mots_possibles_egale_distance.append(mots_possibles[i])
                return random.choice(mots_possibles_egale_distance)




if __name__ == '__main__':

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
    arguments = parser.parse_args()

    # Construction de l'objet dictionnaire fourni immuable
    dictionnaire_fixe = Dictionnaire(TransformerFichierListe(arguments.dic_text), \
                                     False)
    # Construction de l'objet dictionnaire perso muable
    dictionnaire_personnel = Dictionnaire(TransformerFichierListe(arguments.dic_perso), \
                                           True)
    # L'ensemble de dictionnaire permet d'encapsuler le contenu des 2 dictionnaires à
    # travers une interface unique
    ensemble_dictionnaire = EnsembleDictionnaire([dictionnaire_fixe, dictionnaire_personnel])

    # ( Instanciation de la classe CorrecteurAutomatique )

    correcteur_automatique = CorrecteurAutomatique(arguments.seuil, ensemble_dictionnaire)

    corrige, correction = correcteur_automatique.CorrigeTexte(TransformerFichierTexte(arguments.text_original))


    TransformerTexteFichier(corrige,arguments.text_corrige)

    TransformerTexteFichier(correction, arguments.text_correction)

    TransformerListeFichier(dictionnaire_personnel.mots, arguments.dic_perso)
