import re
from p4_modeles import Joueur, Tournoi, Tour
from datetime import datetime


class View:
    @staticmethod
    def afficher_menu():
        print("Menu Principal")
        print("1. Ajouter un joueur")
        print("2. Ajouter un tournoi")
        print("3. Voir les joueurs")
        print("4. Voir les tournois")
        print("5. Inscrire un joueur à un tournoi")
        print("6. Générer les matchs et tours pour un tournoi")
        print("7. Saisir/Modifier les résultats")
        print("8. Quitter")

    @staticmethod
    def afficher_joueurs(joueurs):
        print("Liste des joueurs:")
        for joueur in joueurs:
            print(f"{joueur.nom} {joueur.prenom}, Né(e) le {joueur.date_naissance}, ID: {joueur.id_joueur}, Points: {joueur.points}")

    @staticmethod
    def afficher_tournois(tournois):
        print("Liste des tournois:")
        for tournoi in tournois:
            print(f"{tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut.strftime('%d/%m/%Y')} au {tournoi.date_fin.strftime('%d/%m/%Y')}, ID: {tournoi.id_tournoi}, nombre de participants : {len(tournoi.participants)}")

    @staticmethod
    def validate_joueur_id(id_joueur):
        return re.match(r'^[A-ZA-Z]{2}\d{5}$', id_joueur) is not None
    
    @staticmethod
    def valider_format_date(date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False    

    @staticmethod
    def prompt_joueur():
        nom = input("Nom du joueur: ")
        prenom = input("Prénom du joueur: ")
        while True:
            date_naissance = input("Date de naissance (JJ/MM/AAAA): ")
            if View.valider_format_date(date_naissance):
                break
            else:
                print("Format de date incorrect. Utilisez JJ/MM/AAAA")

            while True:
                id_joueur = input("ID du joueur (2 lettres suivies de 5 chiffres, ex. TR45871): ")
                if View.validate_joueur_id(id_joueur):
                    break
                else:
                    print("L'ID du joueur doit contenir 2 lettres suivies de 5 chiffres. Veuillez réessayer.")
            return Joueur(nom, prenom, date_naissance, id_joueur)

    @staticmethod
    def prompt_tournoi():
        nom_tournoi = input("Nom du tournoi: ")
        lieu = input("Lieu du tournoi: ")
        while True:
            date_debut = input("Date de début (JJ/MM/AAAA): ")
            if View.valider_format_date(date_debut):
                break
            else:
                print("Format de date incorrect. Utilisez JJ/MM/AAAA") 
        while True:
            date_fin = input("Date de fin (JJ/MM/AAAA): ")
            if View.valider_format_date(date_fin):
                break
            else:
                print("Format de date incorrect. Utilisez JJ/MM/AAAA") 
        id_tournoi = input("ID du tournoi: ")
        return Tournoi(nom_tournoi, lieu, date_debut, date_fin, id_tournoi)

    @staticmethod
    def prompt_inscription_tournoi(tournois):
        print("Sélectionner un tournoi pour inscrire un joueur:")
        for i, tournoi in enumerate(tournois):
            print(f"{i + 1}. {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut} au {tournoi.date_fin}")
        choix = int(input("Choix: ")) - 1
        return tournois[choix]

    @staticmethod
    def prompt_selection_tournoi(tournois):
        print("Sélectionner un tournoi pour générer les matchs et tours:")
        for i, tournoi in enumerate(tournois):
            print(f"{i + 1}. {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut.strftime('%d/%m/%Y')} au {tournoi.date_fin.strftime('%d/%m/%Y')}")
        choix = int(input("Choix: ")) - 1
        if 0 <= choix < len(tournois):
            return tournois[choix]
        else:
            print("Choix invalide.")
            return None

    @staticmethod
    def prompt_choix_joueur(joueurs):
        print("1. Choisir un joueur existant")
        print("2. Ajouter un nouveau joueur")
        choix = int(input("Choix: "))
        if choix == 1:
            print("Sélectionner un joueur:")
            for i, joueur in enumerate(joueurs):
                print(f"{i + 1}. {joueur.nom} {joueur.prenom}")
            choix_joueur = int(input("Choix: ")) - 1
            return joueurs[choix_joueur]
        elif choix == 2:
            return View.prompt_joueur()
        

    @staticmethod
    def create_matchs_and_tours(db):
        tournois = db.tournois
        if not tournois:
            print("Aucun tournoi disponible. Ajoutez d'abord un tournoi.")
            return

        print("Sélectionner un tournoi pour générer les matchs et tours:")
        for i, tournoi in enumerate(tournois):
            print(f"{i + 1}. {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut.strftime('%d/%m/%Y')} au {tournoi.date_fin.strftime('%d/%m/%Y')}")

        choix = int(input("Choix: ")) - 1
        if 0 <= choix < len(tournois):
            tournoi = tournois[choix]
            tournoi.generer_matchs_et_tours(db)
            print(f"Matchs et tours créés pour le tournoi {tournoi.nom_tournoi} !")
        else:
            print("Choix invalide. Veuillez réessayer.")


    @staticmethod
    def afficher_tours_et_matchs(tournoi):
        print(f"--- Tournoi: {tournoi.nom_tournoi} ---")
        if not tournoi.tours:
            print("Aucun tour disponible.")
            return

        for index, tour in enumerate(tournoi.tours, start=1):
            print(f"{index}. {tour.nom}")
            for match in tour.matchs:
                print(f"  Match {tour.matchs.index(match) + 1}: {match.joueur1.prenom} {match.joueur1.nom} vs {match.joueur2.prenom} {match.joueur2.nom}")


    @staticmethod
    def prompt_score_match(match):
        print(f"Match: {match.joueur1} vs {match.joueur2}")
        joueur1_score = int(input(f"Score de {match.joueur1} : "))
        joueur2_score = int(input(f"Score de {match.joueur2} : "))
        return joueur1_score, joueur2_score
    

    def afficher_tournois_disponibles(self, tournois):
        print("Sélectionnez un tournoi pour modifier les résultats :")
        for i, tournoi in enumerate(tournois):
            print(f"{i + 1}. {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut} au {tournoi.date_fin}")



    