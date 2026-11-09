"""Version terminal."""

import moteur

QUESTIONS_PAR_SESSION = 5
MODE_AUTO_EVALUATION = True


def choisir_paquet(paquets):
    print("Paquets disponibles :")
    for numero, nom in enumerate(paquets, start=1):
        print(f"  {numero}. {nom[:-4]}")

    while True:
        saisie = input("Lequel ? ").strip()
        if saisie.isdigit() and 1 <= int(saisie) <= len(paquets):
            return paquets[int(saisie) - 1]
        print("Numero invalide.")


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
            correct = moteur.reponse_acceptee(proposition, reponse)
            if not correct:
                print(f"Faux. Reponse attendue : {reponse}")

        if correct:
            print("Correct")
            bonnes += 1

        moteur.enregistrer_resultat(scores, question, correct)

    return bonnes


paquets = moteur.lister_paquets()

if not paquets:
    print("Aucun paquet trouve.")
    raise SystemExit

paquet = paquets[0] if len(paquets) == 1 else choisir_paquet(paquets)

fiches = moteur.charger_paquet(paquet)
tous_les_scores, scores = moteur.charger_scores(paquet)

print(f"\n{paquet[:-4]} : {len(fiches)} fiches disponibles")

nombre = min(QUESTIONS_PAR_SESSION, len(fiches))
tirage = moteur.choisir_fiches(fiches, scores, nombre)

print(f"Session de {nombre} questions\n")

bonnes = poser_questions(tirage, scores)
moteur.sauvegarder_scores(tous_les_scores, paquet, scores)

print(f"\nScore : {bonnes}/{len(tirage)}")

a_revoir = moteur.fiches_a_retravailler(fiches, scores)
print("\nFiches a retravailler :")
if not a_revoir:
    print("  aucune, tout est maitrise")
for question, score in a_revoir:
    print(f"  {question}  ({score['reussites']} ok / {score['echecs']} ko)")