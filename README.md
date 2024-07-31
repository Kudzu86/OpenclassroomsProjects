# Application de Tournoi d'Échecs

Cette application est une solution de gestion de tournois d'échecs. Elle est basée sur une architecture MVC (Modèle-Vue-Contrôleur) et permet de créer, gérer et suivre des tournois d'échecs via un menu principal intuitif.


## Prérequis


Avant de pouvoir exécuter ce projet, assurez-vous d'avoir installé Python. Vous pouvez vérifier que le logiciel est bien installé en écrivant simplement "python" dans la console ou "python --version".

```
python --version
```


### Installation des Dépendances


Clonez le repository GitHub et installez les dépendances :

```
git clone https://github.com/Kudzu86/OpenclassroomsProjects/tree/p4-27/07
cd OpenclassroomsProjects/p4-27/07
pip install -r requirements.txt
```


### Exécution de l'Application


Pour lancer l'application, exécutez le script principal :

```
python controllers.py
```


## Fonctionnalités

### Menu Principal

Le menu principal de l'application offre plusieurs onglets permettant différentes actions :

- Ajouter/modifier des joueurs et des tournois à la base de données
- Voir le classement des joueurs et les tournois de la base de données
- Inscrire des joueurs aux tournois, générer les matchs et saisir les résultats
- Possibilité de réinitialiser la totalité des scores en fin de saison

### Fichiers du Projet

#### Contrôleurs (`controllers.py`)
- Contient la logique de gestion des interactions entre le modèle et la vue.
- Gère les actions de l'utilisateur et met à jour les vues en conséquence.
- Classe ApplicationController

#### Modèles (`modeles.py`)
- Définit les structures de données et les opérations de manipulation des données.
- Modélise les entités principales comme les joueurs et les tournois.
- Principales classes :
  - `Tournoi`
  - `Joueur`
  - `Tour`
  - `Match`

#### Vues (`vues.py`)
- Gère l'affichage et la présentation des données à l'utilisateur.
- Fournit les interfaces utilisateur pour les différentes actions.
- Classe View


### Utilisation


#### Gestion des Joueurs

1. Sélectionnez l'option "1. Ajouter/Modifier un joueur".
2. Ajoutez ou modifiez les joueurs via les options disponibles.
3. Sélectionnez l'option "3. Voir le classement général", pour afficher tous les joueurs de la base de données classés en fonction de leur classement général (tous les scores de tournois cumulés).

   
#### Gestion d'un Nouveau Tournoi

1. Sélectionnez l'option "2. Ajouter/Modifier un tournoi" dans le menu principal.
2. Entrez les informations requises : nom, lieu, date, nombre de tours, etc.
3. Vous pouvez voir la totalité des tournois de la base de données en sélectionant l'option "4. Voir les tournois".
4. Ajoutez les joueurs au tournoi en sélectionnant l'option "5. Inscrire un joueur à un tournoi".


#### Démarrage et Suivi des Tournois

1. Sélectionnez l'option "6. Générer les matchs et tours pour un tournoi" lorsque tous les participants sont inscrits.
2. Sélectionnez le tournoi correspondant, cette action vous génèrera un seul tour.
3. Sélectionnez l'option "7. Saisir/Modifier les résultats" pour rentrer les scores des matchs terminés.
4. Une fois tous les résultats du premier tour rentrés, vous pourrez à nouveau générer un tour via l'option "6. Générer les matcgs et tours pour un tournoi". etc.
5. La fin d'un tournoi est acté a la fin de 4ème tour, vous ne pourrez donc pas créer de 5ème tour.
6. Possibilité de réinitialiser la totalité des scores en fin de saison en sélectionnant l'option "8. Reinitialiser scores".


