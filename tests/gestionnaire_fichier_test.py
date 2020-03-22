from sources.gestionnaire_fichier import TransformerFichierListe, TransformerListeFichier
import pytest
import os
from pathlib import Path

# On dois trouver le chemin absolus du fichier avant de l'utiliser
# pour pouvoir invoquer les tests unitaires depuis plusieurs endroit
# dans le terminal
dic = Path(__file__).parent.resolve() / "words.txt"

def test_transformer_fichier_liste():
    assert isinstance(TransformerFichierListe(dic),list)
    l = TransformerFichierListe(dic)
    assert len(l) == 466551
    assert "ZZZ" in l
    assert "doubt" in l
    assert "garçon" not in l

def test_transformer_liste_fichier():
    liste = ["un", "deux", "trois"]
    TransformerListeFichier(liste, "fichier.txt")
    assert TransformerFichierListe("fichier.txt") == liste
    os.remove("fichier.txt")
