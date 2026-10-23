
from source.chargeur_profil import charger_profil


def test_charger_les_trois_profils():
    for nom in [
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION",
    ]:
        profil = charger_profil(nom)

        assert profil is not None
        assert profil["nom_profil"] == nom


def test_profil_inexistant():
    assert charger_profil("POSTE-INEXISTANT") is None


def test_parametres_existants():
    profil = charger_profil("POSTE-COMPTABLE")

    assert "ram_min" in profil
    assert "espace_disque_min" in profil
    assert "nom_pc" in profil


def test_date_validation_presente():
    for nom in [
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION",
    ]:
        profil = charger_profil(nom)
        assert "date_validation" in profil
        assert profil["date_validation"] != ""



def test_profils_contiennent_25_controles():
    for nom in [
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION",
    ]:
        profil = charger_profil(nom)
        assert "controles" in profil
        assert len(profil["controles"]) == 25



def test_structure_des_controles():
    profil = charger_profil("POSTE-COMPTABLE")

    for controle in profil["controles"]:
        assert "id" in controle
        assert "nom" in controle
        assert "actif" in controle
        assert isinstance(controle["actif"], bool)


def test_tous_les_profils_ont_les_25_controles_du_catalogue():
    from source.controles.catalogue_controles import CATALOGUE_CONTROLES

    for nom in [
        "POSTE-COMPTABLE",
        "POSTE-ACCUEIL",
        "POSTE-DIRECTION",
    ]:
        profil = charger_profil(nom)
        noms_controles = [
            controle["nom"] for controle in profil["controles"]
        ]

        assert len(noms_controles) == 25
        assert set(noms_controles) == set(CATALOGUE_CONTROLES)
