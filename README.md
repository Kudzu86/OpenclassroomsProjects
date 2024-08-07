# Web Scraper pour Books to Scrape


Ce projet est un web scraper écrit en Python pour extraire des informations sur les livres depuis le site [Books to Scrape](http://books.toscrape.com/). Le scraper récupère les détails des livres, y compris l'image. Les informations sont ensuite enregistrées dans des fichiers CSV. Ces derniers, ainsi que les images des couvertures de livres, sont stockés dans des dossiers correspondants aux catégories.



## Prérequis


Avant de pouvoir exécuter ce projet, assurez-vous d'avoir installé Python. Vous pouvez vérifier que le logiciel est bien installé en écrivant simplement "python" dans la console ou "python --version".

```
python --version
```



### Installation


1. Clonez ce dépôt sur votre machine locale :

```
git clone https://github.com/Kudzu86/OpenclassroomsProjects.git
cd OpenclassroomsProjects
```

2. Créer l'environnement virtuel nommé .venv en exécutant la commande suivante :

```
python -m venv .venv
```

3. Activez votre environnement virtuel :

#### Pour macOS, Linux : ####
```
source .venv/bin/activate # Sur Windows, utilisez `.venv\Scripts\activate`
```

#### Pour Windows : ####

```
.venv\Scripts\activate
```

4. Installez les dépendances :

```
pip install -r requirements.txt
```


### Utilisation


Pour exécuter le scraper, lancez simplement le script scraper.py :

```
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



### Exclusion de l'environnement virtuel et des données extraites


Pour vous assurer que l'environnement virtuel et les données extraites ne sont pas stockés dans le repository, ajoutez les répertoires pertinents au fichier .gitignore :

```
# Environnement virtuel
.venv/

# Données extraites
*.csv
Books/
```



### Auteurs

AUER Eric



### Licence

Ce projet est sous licence TATOUTI. Voir le fichier LICENSE pour plus de détails.
