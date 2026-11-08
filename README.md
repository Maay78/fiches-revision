# fiches-revision

Petit outil de révision par fiches, en ligne de commande.

Premier projet personnel, écrit pour apprendre Python et Git. L'objectif n'est pas de remplacer Anki, mais de comprendre comment fonctionne un programme qui lit des fichiers, garde un état entre deux sessions et s'adapte à l'utilisateur.

## Fonctionnalités

- Plusieurs paquets de fiches, un par fichier
- Les fiches ratées reviennent plus souvent que celles qui sont maîtrisées
- Les scores sont conservés d'une session à l'autre
- Les réponses sont acceptées sans accents et avec une petite faute de frappe
- Mode auto-évaluation : la réponse s'affiche et vous indiquez vous-même si vous l'aviez
- Bilan des fiches à retravailler en fin de session

## Lancer le programme

Python 3 suffit, aucune dépendance à installer.



## Écrire ses fiches

Un paquet est un fichier `.txt` placé dans le dossier `fiches/`. Une ligne par fiche, avec une barre verticale entre la question et la réponse :

Question ? | réponse 


Pour créer un nouveau paquet, il suffit d'ajouter un fichier dans ce dossier. Au lancement, le programme demande lequel réviser.

## Réglages

En haut de `fiches.py` :

| Constante | Rôle |
|---|---|
| `QUESTIONS_PAR_SESSION` | Nombre de questions posées à chaque session |
| `MODE_AUTO_EVALUATION` | `True` pour s'auto-évaluer, `False` pour taper la réponse |

## Pistes d'amélioration

- Interface graphique
- Génération de fiches à partir d'un texte de cours
- Statistiques de progression dans le temps
