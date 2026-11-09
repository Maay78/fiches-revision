"""Version web."""

from flask import Flask, redirect, render_template, request, session, url_for

import moteur

QUESTIONS_PAR_SESSION = 5

app = Flask(__name__)
app.secret_key = "cle-de-developpement-a-changer"


@app.route("/")
def accueil():
    return render_template("accueil.html", paquets=moteur.lister_paquets())


@app.route("/reviser/<paquet>")
def demarrer(paquet):
    fiches = moteur.charger_paquet(paquet)
    _, scores = moteur.charger_scores(paquet)

    nombre = min(QUESTIONS_PAR_SESSION, len(fiches))
    tirage = moteur.choisir_fiches(fiches, scores, nombre)

    session["paquet"] = paquet
    session["tirage"] = tirage
    session["position"] = 0
    session["bonnes"] = 0

    return redirect(url_for("question"))


@app.route("/question")
def question():
    tirage = session.get("tirage")
    position = session.get("position", 0)

    if not tirage:
        return redirect(url_for("accueil"))

    if position >= len(tirage):
        return redirect(url_for("fin"))

    question, reponse = tirage[position]
    return render_template(
        "question.html",
        question=question,
        reponse=reponse,
        numero=position + 1,
        total=len(tirage),
    )


@app.route("/repondre", methods=["POST"])
def repondre():
    tirage = session.get("tirage")
    position = session.get("position", 0)

    if not tirage or position >= len(tirage):
        return redirect(url_for("accueil"))

    correct = request.form.get("resultat") == "juste"
    question = tirage[position][0]

    paquet = session["paquet"]
    tous, scores = moteur.charger_scores(paquet)
    moteur.enregistrer_resultat(scores, question, correct)
    moteur.sauvegarder_scores(tous, paquet, scores)

    session["position"] = position + 1
    if correct:
        session["bonnes"] = session.get("bonnes", 0) + 1

    return redirect(url_for("question"))


@app.route("/fin")
def fin():
    return render_template(
        "fin.html",
        bonnes=session.get("bonnes", 0),
        total=len(session.get("tirage", [])),
    )


if __name__ == "__main__":
    app.run(debug=True)