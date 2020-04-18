import string
from distance_entre_mots import CalculDistanceMots


class Dictionnaire(object):
    '''
    L'objectif de la classe Dictionnaire est de pouvoir
    manipuler les dictionnaires à l'aide de méthodes dans
    le cadre de ce projet informatique comme on le ferait
    dans le monde réel. L'attribut mots_dico représente
    les mots d'un dictionnaire.
    '''
    def __init__(self, mots_dico, muable = True):
        if isinstance(mots_dico, list):
            self.mots_dico = mots_dico
        else:
            raise TypeError("L'argument mots_dico n'est pas une liste de mots.")
        self.muable = muable

    def compter_nombre_mots(self):
        return len(self.mots_dico)

    def ajouter_mot(self, mot):
        if self.muable:
            if isinstance(mot, str):
                if not self.chercher_mot(mot):
                    self.mots_dico.append(mot)
            else:
                raise TypeError("TypeError exception thrown")

    def chercher_mot(self, mot):
        return mot in self.mots_dico

    def mots_possibles(self, mot_inconnu, seuil):
        mots_possibles = []
        for mot in self.mots_dico:
            distance = CalculDistanceMots(mot_inconnu, mot)
            if distance < seuil:
                mots_possibles.append([distance,mot])
        return mots_possibles


class EnsembleDictionnaire(Dictionnaire):
    '''
    L'objectif de cette classe est d'encapsuler les deux dictionnaires:
    le dictionnaire principal et le dictionnairre personnel.
    L'objectif est de pouvoir centraliser les actions demandés dans le
    programme principal. Nous y retrouvons par conséquent les mêmes noms
    de méthodes que dans la classe dictionnaire ci-dessus.
    '''
    def __init__(self, dictionnaires, strategie):
        self.strategie = strategie
        print(f"Nous allons corriger le texte grâce à la stratégie {self.strategie}.")
        if isinstance(dictionnaires, list):
            self.dictionnaires = dictionnaires
        else:
            raise TypeError("Ce n'est pas une liste.")

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
        '''
        L'objectif de cette méthode est de produire une liste
        nommée mots_possibles composée de sous-listes constituées
        de deux éléments (la distance entre le mot_inconnu initial
        et un mot possible de correction, et ce mot possible)
        '''
        mots_possibles = []
        if self.strategie == 1:
            for d in self.dictionnaires:
                mots_possibles.extend(d.mots_possibles(mot_inconnu, seuil))
            return mots_possibles
        else:
            liste_ajout = [[0, mot_inconnu]]
            debut = 0
            fin = 1
            for i in range(seuil):
                for j in range(debut, fin, 1):
                    liste_ajout.extend(self.production_mots(liste_ajout[j][1], i+1))
                debut = fin
                fin = len(liste_ajout)

            for mot in liste_ajout:
                if self.chercher_mot(mot[1]):
                    mots_possibles.append(mot)

            return mots_possibles

    def production_mots(self, mot_inconnu, distance):
        mots_generes = []
        alphabet = list(string.ascii_lowercase)
        '''
        Ajout
        '''
        for indice in range(len(mot_inconnu)):
            for lettre in alphabet:
                mots_generes.append([distance, mot_inconnu[:indice] + lettre + mot_inconnu[indice:]])
        '''
        Suppression
        '''
        for indice in range(len(mot_inconnu)):
            mot_suppression = mot_inconnu[:indice] + mot_inconnu[(indice+1):]
            mots_generes.append([distance, mot_suppression])
        '''
        Transposition

        Nous itérons jusqu'à len(mot_inconnu)-1 pour ne pas
        interchanger la dernière lettre du mot avec un caractère
        vide ce qui donne en sortie le mot à l'identique.
        '''
        for indice in range(len(mot_inconnu)-1):
            mots_generes.append([distance, mot_inconnu[:indice] + mot_inconnu[indice+1:indice+2] + \
                                mot_inconnu[indice:indice+1] + mot_inconnu[indice+2:]])
        '''
        Substitution
        '''
        for indice in range(len(mot_inconnu)):
            for lettre in alphabet:
                mots_generes.append([distance, mot_inconnu[:indice] + lettre + mot_inconnu[indice+1:]])

        return mots_generes





