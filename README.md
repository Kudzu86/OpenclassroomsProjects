# Web Scraper pour Books to Scrape


Ce projet est un web scraper écrit en Python pour extraire des informations sur les livres depuis le site [Books to Scrape](http://books.toscrape.com/). Le scraper récupère les détails des livres, y compris l'image. Les informations sont ensuite enregistrées dans des fichiers CSV. Ces derniers, ainsi que les images des couvertures de livres, sont stockés dans des dossiers correspondants aux catégories.



## Prérequis


Avant de pouvoir exécuter ce projet, assurez-vous d'avoir installé Python et les dépendances nécessaires. Vous pouvez installer les dépendances en utilisant le fichier `requirements.txt`.

```
pip install -r requirements.txt
```



### Installation


Clonez ce dépôt sur votre machine locale :

```
Copier le code

git clone https://github.com/Kudzu86/OpenclassroomsProjects.git
cd OpenclassroomsProjects/Projet2
```

Activez votre environnement virtuel et installez les dépendances :

```
Copier le code

python -m venv .venv
source .venv/bin/activate # Sur Windows, utilisez `.venv\Scripts\activate`
pip install -r requirements.txt
```



### Utilisation


Pour exécuter le scraper, lancez simplement le script scraper.py :

```
Copier le code

python scraper.py
```

Le script téléchargera les informations de chaque livre et les enregistrera dans des fichiers CSV dans un dossier Books, avec chaque catégorie de livre ayant son propre sous-dossier.




### Structure du Projet


scraper.py : Le script principal contenant le scraper.

requirements.txt : Liste des dépendances nécessaires pour exécuter le projet.

Books/ : Dossier où les fichiers CSV et les images de couverture des livres seront enregistrés.



### Fonctionnalités


Extraction des livres par catégorie : Récupère tous les liens des livres pour chaque catégorie du site.
Extraction des détails des livres : Récupère les informations détaillées pour chaque livre et télécharge l'image de la couverture.
Enregistrement dans des fichiers CSV : Crée des fichiers CSV pour chaque catégorie avec les informations des livres.



### Auteurs

AUER Eric



### Licence

Ce projet est sous licence TATOUTI. Voir le fichier LICENSE pour plus de détails.
