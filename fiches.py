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


fiches = charger_fiches("fiches.txt")
import random


def normaliser(texte):
    return texte.strip().lower()


def poser_questions(fiches):
    tirage = fiches[:]
    random.shuffle(tirage)
    bonnes = 0

    for numero, (question, reponse) in enumerate(tirage, start=1):
        print(f"\n[{numero}/{len(tirage)}] {question}")
        proposition = input("> ")

        if normaliser(proposition) == normaliser(reponse):
            print("Correct")
            bonnes += 1
        else:
            print(f"Faux. Reponse attendue : {reponse}")

    return bonnes


fiches = charger_fiches("fiches.txt")
print(f"{len(fiches)} fiches chargees\n")

bonnes = poser_questions(fiches)
print(f"\nScore : {bonnes}/{len(fiches)}")