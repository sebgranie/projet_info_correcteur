from gestionnaire_fichier import TransformerFichierListe, TransformerListeFichier
import pytest
import os

def test_transformer_fichier_liste():
    assert isinstance(TransformerFichierListe("words.txt"),list)
    l = TransformerFichierListe("words.txt")
    assert len(l) == 466551
    assert "ZZZ" in l
    assert "doubt" in l
    assert "garçon" not in l

def test_transformer_liste_fichier():
    liste = ["un", "deux", "trois"]
    TransformerListeFichier(liste, "fichier.txt")
    assert TransformerFichierListe("fichier.txt") == liste
    os.remove("fichier.txt")
