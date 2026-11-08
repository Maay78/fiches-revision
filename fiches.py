import json
import os
import random
import difflib
import unicodedata

DOSSIER_FICHES = "fiches"
FICHIER_SCORES = "scores.json"
QUESTIONS_PAR_SESSION = 5
MODE_AUTO_EVALUATION = True


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

def lister_paquets(dossier):
    if not os.path.isdir(dossier):
        return []
    noms = [f for f in os.listdir(dossier) if f.endswith(".txt")]
    return sorted(noms)


def choisir_paquet(paquets):
    print("Paquets disponibles :")
    for numero, nom in enumerate(paquets, start=1):
        print(f"  {numero}. {nom[:-4]}")

    while True:
        saisie = input("Lequel ? ").strip()
        if saisie.isdigit() and 1 <= int(saisie) <= len(paquets):
            return paquets[int(saisie) - 1]
        print("Numero invalide.")

def charger_scores(chemin, paquet):
    if not os.path.exists(chemin):
        return {}, {}
    with open(chemin, encoding="utf-8") as f:
        tous = json.load(f)
    return tous, tous.get(paquet, {})


def sauvegarder_scores(chemin, tous, paquet, scores):
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

    similarite = difflib.SequenceMatcher(None, proposition, attendue).ratio()
    return similarite >= 0.85


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

def demander_auto_evaluation():
    while True:
        reponse = input("Tu avais juste ? [o/n] ").strip().lower()
        if reponse in ("o", "oui", "y"):
            return True
        if reponse in ("n", "non"):
            return False
        print("Reponds par o ou n.")

def poser_questions(tirage, scores):
    bonnes = 0
    for numero, (question, reponse) in enumerate(tirage, start=1):
        print(f"\n[{numero}/{len(tirage)}] {question}")

        if MODE_AUTO_EVALUATION:
            input("(Entree pour voir la reponse) ")
            print(f"Reponse : {reponse}")
            correct = demander_auto_evaluation()
        else:
            proposition = input("> ")
            correct = reponse_acceptee(proposition, reponse)
            if not correct:
                print(f"Faux. Reponse attendue : {reponse}")

        score = scores.setdefault(question, {"reussites": 0, "echecs": 0})

        if correct:
            print("Correct")
            score["reussites"] += 1
            bonnes += 1
        else:
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


paquets = lister_paquets(DOSSIER_FICHES)

if not paquets:
    print(f"Aucun paquet trouve dans le dossier {DOSSIER_FICHES}.")
    raise SystemExit

if len(paquets) == 1:
    paquet = paquets[0]
else:
    paquet = choisir_paquet(paquets)

fiches = charger_fiches(os.path.join(DOSSIER_FICHES, paquet))
tous_les_scores, scores = charger_scores(FICHIER_SCORES, paquet)

print(f"\n{paquet[:-4]} : {len(fiches)} fiches disponibles")

nombre = min(QUESTIONS_PAR_SESSION, len(fiches))
tirage = choisir_fiches(fiches, scores, nombre)

print(f"Session de {nombre} questions\n")

bonnes = poser_questions(tirage, scores)

sauvegarder_scores(FICHIER_SCORES, tous_les_scores, paquet, scores)

print(f"\nScore : {bonnes}/{len(tirage)}")
afficher_bilan(fiches, scores)