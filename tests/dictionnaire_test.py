from sources.dictionnaire import Dictionnaire
import pytest

def test_dictionnaire_chercher_mot():
    d = Dictionnaire(["oui", "non","manger"])
    assert d.chercher_mot("oui")
    assert d.chercher_mot("non")
    assert d.chercher_mot("manger")
    assert not d.chercher_mot("ous")
    d.ajouter_mot("ous")
    assert d.chercher_mot("ous")

def test_compter_nombre_mot():
    d = Dictionnaire(["oui", "non","manger"])
    assert d.compter_nombre_mots() == 3

    d.mots.pop(2)
    assert d.compter_nombre_mots() == 2

    d = Dictionnaire([])
    assert d.compter_nombre_mots() == 0


def test_ajouter_mot():
    d = Dictionnaire(["oui", "non","manger"])
    d.ajouter_mot("chat")
    assert d.compter_nombre_mots() == 4

    # on teste qu'aucun mot n'est dupliqué
    d.ajouter_mot("chat")
    assert d.compter_nombre_mots() == 4

    with pytest.raises(TypeError):
        d.ajouter_mot(8)
    assert d.compter_nombre_mots() == 4


def test_constructeur():
    a = ["oui", "non","manger"]
    d = Dictionnaire(a)
    assert d.mots ==  a



