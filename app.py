"""Version web."""

from flask import Flask, render_template

import moteur

app = Flask(__name__)


@app.route("/")
def accueil():
    paquets = moteur.lister_paquets()
    return render_template("accueil.html", paquets=paquets)


if __name__ == "__main__":
    app.run(debug=True)