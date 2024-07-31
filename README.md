# Application de Tournoi d'Échecs

Cette application est une solution de gestion de tournois d'échecs. Elle est basée sur une architecture MVC (Modèle-Vue-Contrôleur) et permet de créer, gérer et suivre des tournois d'échecs via un menu principal intuitif.

## Fonctionnalités

### Menu Principal

Le menu principal de l'application offre plusieurs onglets permettant différentes actions :

1. **Créer un Nouveau Tournoi**
   - Permet de créer un nouveau tournoi en spécifiant les détails tels que le nom, le lieu, la date, le nombre de tours, les joueurs participants, etc.

2. **Gérer les Joueurs**
   - Ajout de nouveaux joueurs
   - Modification des informations des joueurs existants
   - Consultation de la liste des joueurs

3. **Démarrer un Tournoi**
   - Permet de lancer un tournoi déjà créé
   - Gestion automatique des rondes et appariements

4. **Suivi des Tournois en Cours**
   - Affiche les détails des tournois en cours
   - Permet de suivre les résultats et les classements des joueurs

5. **Rapports**
   - Génération de rapports sur les tournois passés
   - Statistiques et analyses des performances des joueurs

### Fichiers du Projet

#### Contrôleurs (`p4_controllers.py`)
- Contient la logique de gestion des interactions entre le modèle et la vue.
- Gère les actions de l'utilisateur et met à jour les vues en conséquence.
- Principales classes et méthodes : 
  - `TournamentController`
  - `PlayerController`
  - `MenuController`

#### Modèles (`p4_modeles.py`)
- Définit les structures de données et les opérations de manipulation des données.
- Modélise les entités principales comme les joueurs et les tournois.
- Principales classes et méthodes :
  - `Tournament`
  - `Player`
  - `Round`
  - `Match`

#### Vues (`p4_vues.py`)
- Gère l'affichage et la présentation des données à l'utilisateur.
- Fournit les interfaces utilisateur pour les différentes actions.
- Principales classes et méthodes :
  - `TournamentView`
  - `PlayerView`
  - `MenuView`

## Installation et Configuration

### Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.x
- `pip` (gestionnaire de paquets Python)

### Installation des Dépendances

Clonez le repository GitHub et installez les dépendances :

```bash
git clone https://github.com/Kudzu86/OpenclassroomsProjects/tree/p4-27/07
cd OpenclassroomsProjects/p4-27/07
pip install -r requirements.txt
