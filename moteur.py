"""Logique de revision, independante de l'affichage."""

import difflib
import json
import os
import random
import unicodedata

DOSSIER_FICHES = "fiches"
FICHIER_SCORES = "scores.json"


def charger_fiches(chemin):
    fiches = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or "|" not in ligne:
                continue
            question, reponse = ligne.split("|", 1)
            fiches.append((question.strip(), reponse.strip()))
    return fiches


def lister_paquets(dossier=DOSSIER_FICHES):
    if not os.path.isdir(dossier):
        return []
    return sorted(f for f in os.listdir(dossier) if f.endswith(".txt"))


def charger_paquet(paquet, dossier=DOSSIER_FICHES):
    return charger_fiches(os.path.join(dossier, paquet))


def charger_scores(paquet, chemin=FICHIER_SCORES):
    if not os.path.exists(chemin):
        return {}, {}
    with open(chemin, encoding="utf-8") as f:
        tous = json.load(f)
    return tous, tous.get(paquet, {})


def sauvegarder_scores(tous, paquet, scores, chemin=FICHIER_SCORES):
    tous[paquet] = scores
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(tous, f, ensure_ascii=False, indent=2)


def normaliser(texte):
    texte = texte.strip().lower()
    sans_accents = unicodedata.normalize("NFD", texte)
    return "".join(c for c in sans_accents if unicodedata.category(c) != "Mn")


def reponse_acceptee(proposition, attendue):
    proposition = normaliser(proposition)
    attendue = normaliser(attendue)

    if proposition == attendue:
        return True

    # Sur une reponse tres courte, une lettre de difference change le sens
    if len(attendue) < 5:
        return False

    return difflib.SequenceMatcher(None, proposition, attendue).ratio() >= 0.85


def poids(score):
    """Une fiche souvent ratee est tiree plus souvent qu'une fiche maitrisee."""
    return max(1, 1 + 3 * score["echecs"] - score["reussites"])


def choisir_fiches(fiches, scores, nombre):
    restantes = list(fiches)
    restants_poids = [
        poids(scores.get(question, {"reussites": 0, "echecs": 0}))
        for question, _ in fiches
    ]

    tirage = []
    while restantes and len(tirage) < nombre:
        choisie = random.choices(restantes, weights=restants_poids, k=1)[0]
        index = restantes.index(choisie)
        restantes.pop(index)
        restants_poids.pop(index)
        tirage.append(choisie)

    return tirage


def enregistrer_resultat(scores, question, correct):
    score = scores.setdefault(question, {"reussites": 0, "echecs": 0})
    if correct:
        score["reussites"] += 1
    else:
        score["echecs"] += 1


def fiches_a_retravailler(fiches, scores):
    resultat = []
    for question, _ in fiches:
        score = scores.get(question)
        if score and score["echecs"] > score["reussites"]:
            resultat.append((question, score))
    return resultat