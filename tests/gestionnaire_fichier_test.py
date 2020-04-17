from sources.gestionnaire_fichier import TransformerFichierListe_Dico, TransformerListeFichier_Dico, TransformerFichierListe_Texte, TransformerListeFichier_Texte
import pytest
import os
from pathlib import Path

# On dois trouver le chemin absolus du fichier avant de l'utiliser
# pour pouvoir invoquer les tests unitaires depuis plusieurs endroit
# dans le terminal
dic = Path(__file__).parent.resolve() / "words.txt"

def test_transformer_fichier_liste():
    assert isinstance(TransformerFichierListe_Dico(dic),list)
    l = TransformerFichierListe_Dico(dic)
    assert len(l) == 466551
    assert "ZZZ" in l
    assert "doubt" in l
    assert "garçon" not in l

def test_transformer_liste_fichier():
    liste = ["un", "deux", "trois"]
    TransformerListeFichier_Dico(liste, "fichier.txt")
    assert TransformerFichierListe_Dico("fichier.txt") == liste
    os.remove("fichier.txt")

def test_transformer_texte_fichier():
    texte = ["un", " ", "deux", "\n", "trois", " ", "quatre"]
    TransformerListeFichier_Texte(texte, "fichier.txt")
    assert TransformerFichierListe_Texte("fichier.txt") == texte
    os.remove("fichier.txt")
