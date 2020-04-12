import string
from distance_entre_mots import CalculDistanceMots


class Dictionnaire(object):
    def __init__(self, mots, muable = True):
        if isinstance(mots, list):
            self.mots = mots
        else:
            raise TypeError("L'argument mots n'est pas une liste de mots.")
        self.muable = muable

    # L'intérêt d'utiliser les méthodes suivantes est de réduire la
    # taille du code quand nous manipulons les objets.

    # Cette méthode permet de compter le nombre de mot
    # d'un dictionnaire par exemple pour connaître le
    # nombre d'élement qu'il contient.
    def compter_nombre_mots(self):
        return len(self.mots)                  # Retourne le nombre de mot du dictionnaire

    # Cette méthode permet d'ajouter un mot à un dictionnaire.
    # Cette fonctionnnalité est intéressante lorsque
    # l'utilisateur souhaite ajouter un mot initialement
    # introuvable dans le dictionnaire. Cette méthode fonctionne
    # seulement si le caractère muable du dictionnaire est validé.
    def ajouter_mot(self, mot):
        if self.muable:                         # ajout du mot seulement dans le dictionnaire muable (dictionnaire perso)
            if isinstance(mot, str):            # fonctionne seulement si le paramètre est une chaîne de caractère (type: str)
                if not self.chercher_mot(mot):  # Mot introuvable dans le dictionnaire
                    self.mots.append(mot)       # Traduit l'unicité d'un mot dans le dictionnaire
            else:
                raise TypeError("TypeError exception thrown")

    # Cette méthode est très utile pour vérifier la présence d'un
    # mot du texte à corriger dans le dictionnaire. Elle renvoit
    # un booléen: True le mot est dans le dictionnaire,
    # (respectivement False le mot ne s'y trouve pas).
    def chercher_mot(self, mot):
        return mot in self.mots                 # Retourne un booléen

    def mots_possibles(self, mot_inconnu, seuil):
        mots_possibles = []
        for mot in self.mots:
            distance = CalculDistanceMots(mot_inconnu, mot)
            if distance < seuil:
                mots_possibles.append([distance,mot])
        return mots_possibles




# L'objectif de cette classe est d'encapsuler les deux dictionnaires:
# le dictionnaire de Mr Crégut et le dictionnairre personnel.
# L'objectif est de pouvoir centraliser les actions demandés dans le
# programme principal. Nous y retrouvons les mêmes noms de méthodes
# que dans la classe dictionnaire ci-dessus.
class EnsembleDictionnaire(Dictionnaire):
    def __init__(self, dictionnaires, strategie):
        self.strategie = strategie
        if isinstance(dictionnaires, list):
            self.dictionnaires = dictionnaires
        else:
            raise TypeError("Ce n'est pas une liste")

    def compter_nombre_mots(self):
        mots = 0
        for d in self.dictionnaires:
            mots = mots + d.compter_nombre_mots()
        return mots

    def chercher_mot(self, mot):
        for d in self.dictionnaires:
            if d.chercher_mot(mot):
                return True
        return False

    def ajouter_mot(self, mot):
        for d in self.dictionnaires:
            d.ajouter_mot(mot)


    def mots_possibles(self, mot_inconnu, seuil):
        mots_possibles = []
        if self.strategie == 1:
            for d in self.dictionnaires:
                mots_possibles.extend(d.mots_possibles(mot_inconnu, seuil))
            return mots_possibles
        else:
            liste_ajout = self.production_mots(mot_inconnu)

            for i in range(seuil):
                for mot in liste_ajout:
                    liste_ajout.extend(self.production_mots(mot))

            for d in self.dictionnaires:
                for i in range(len(liste_ajout)):
                    if d.chercher_mot(liste_ajout[i]):
                        mots_possibles.append([1,liste_ajout[i]])

    def production_mots(self,mot_inconnu):
        liste_ajout = []
        alphabet = list(string.ascii_lowercase)
        '''
        Ajout
        '''
        for indice in range(len(mot_inconnu)):
            for lettre in alphabet:
                liste_ajout.append(mot_inconnu[:indice] + lettre + mot_inconnu[indice:])
        '''
        Suppression
        '''
        for indice in range(len(mot_inconnu)):
            mot_suppression = mot_inconnu[:indice] + mot_inconnu[(indice+1):]
            liste_ajout.append(mot_suppression)
        '''
        Transposition

        Nous itérons jusqu'à len(mot_inconnu)-1 pour ne pas
        interchanger la dernière lettre du mot avec un caractère
        vide ce qui donne en sortie le mot à l'identique.
        '''
        for indice in range(len(mot_inconnu)-1):
            liste_ajout.append(mot_inconnu[:indice] + mot_inconnu[indice+1:indice+2] + \
                                mot_inconnu[indice:indice+1] + mot_inconnu[indice+2:])
        '''
        Substitution
        '''
        for indice in range(len(mot_inconnu)):
            for lettre in alphabet:
                liste_ajout.append(mot_inconnu[:indice] + lettre + mot_inconnu[indice+1:])

        return liste_ajout





