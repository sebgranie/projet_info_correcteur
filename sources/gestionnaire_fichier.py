def TransformerFichierListe(fichier):
    liste = []
    with open(fichier, "r") as f:
        for n in f:
            # on utilise split pour enlever le caractère
            # (unique) '\n' à la fin de la ligne
            for word in n.split():
                liste.append(word)

    return liste

def TransformerListeFichier(mots, fichier):
    with open(fichier, "w") as f:
        for n in mots:
            f.write(n+"\n")
