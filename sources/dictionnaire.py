class Dictionnaire(object):
    def __init__(self, mots):
        self.mots = mots

    def compter_nombre_mots(self):
        return len(self.mots)

    def ajouter_mot(self, mot):
        if isinstance(mot, str):
            if not self.chercher_mot(mot):
                self.mots.append(mot)
        else:
            raise TypeError("TypeError exception thrown")

    def chercher_mot(self, mot):
        return mot in self.mots


