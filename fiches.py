import json
import os
import random

FICHIER_FICHES = "fiches.txt"
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


def charger_scores(chemin):
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_scores(chemin, scores):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def normaliser(texte):
    return texte.strip().lower()


def poids(score):
    """Une fiche souvent ratee est tiree plus souvent qu'une fiche maitrisee."""
    return 1 + 3 * score["echecs"] - score["reussites"]


def choisir_fiches(fiches, scores, nombre):
    poids_fiches = []
    for question, reponse in fiches:
        score = scores.get(question, {"reussites": 0, "echecs": 0})
        poids_fiches.append(max(1, poids(score)))

    tirage = []
    restantes = list(fiches)
    restants_poids = list(poids_fiches)

    while restantes and len(tirage) < nombre:
        choisie = random.choices(restantes, weights=restants_poids, k=1)[0]
        index = restantes.index(choisie)
        restantes.pop(index)
        restants_poids.pop(index)
        tirage.append(choisie)

    return tirage


def poser_questions(tirage, scores):
    bonnes = 0

    for numero, (question, reponse) in enumerate(tirage, start=1):
        print(f"\n[{numero}/{len(tirage)}] {question}")
        proposition = input("> ")

        score = scores.setdefault(question, {"reussites": 0, "echecs": 0})

        if normaliser(proposition) == normaliser(reponse):
            print("Correct")
            score["reussites"] += 1
            bonnes += 1
        else:
            print(f"Faux. Reponse attendue : {reponse}")
            score["echecs"] += 1

    return bonnes


def afficher_bilan(fiches, scores):
    print("\nFiches a retravailler :")
    a_revoir = []
    for question, _ in fiches:
        score = scores.get(question)
        if score and score["echecs"] > score["reussites"]:
            a_revoir.append((question, score))

    if not a_revoir:
        print("  aucune, tout est maitrise")
        return

    for question, score in a_revoir:
        print(f"  {question}  ({score['reussites']} ok / {score['echecs']} ko)")


fiches = charger_fiches(FICHIER_FICHES)
scores = charger_scores(FICHIER_SCORES)

print(f"{len(fiches)} fiches chargees")

tirage = choisir_fiches(fiches, scores, nombre=len(fiches))
bonnes = poser_questions(tirage, scores)

sauvegarder_scores(FICHIER_SCORES, scores)

print(f"\nScore : {bonnes}/{len(tirage)}")
afficher_bilan(fiches, scores)