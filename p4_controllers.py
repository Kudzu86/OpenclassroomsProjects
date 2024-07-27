from p4_modeles import Database, Tournoi, Tour, Match
from p4_vues import View
from datetime import datetime, date

class ApplicationController:
    def __init__(self, view, db):
        self.view = view
        self.db = db

    def run(self):
        while True:
            self.view.afficher_menu()
            choix = input("Choisissez une option: ")
            if choix == '1':
                self.gerer_joueur()
            elif choix == '2':
                self.gerer_tournoi()
            elif choix == '3':
                self.voir_joueurs()
            elif choix == '4':
                self.voir_tournois()
            elif choix == '5':
                self.inscrire_joueur_tournoi()
            elif choix == '6':
                self.generer_matchs_et_tours()
            elif choix == '7':
                self.saisir_modifier_resultats()
            elif choix == '8' :
                self.reinitialiser_scores()
            elif choix == '9' :
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez choisir une option valide.")

    def gerer_joueur(self):
        choix = self.view.choisir_action_joueur()
        if choix == '1':
            self.ajouter_joueur()
        elif choix == '2':
            self.modifier_joueur()
        else:
            print("Choix invalide.")

    def gerer_tournoi(self):
        choix = self.view.choisir_action_tournoi()
        if choix == '1':
            self.ajouter_tournoi()
        elif choix == '2':
            self.modifier_tournoi()
        else:
            print("Choix invalide.")

    def ajouter_joueur(self):
        joueur = self.view.prompt_joueur()
        self.db.ajouter_joueur(joueur)
        print("Joueur ajouté avec succès!")
        self.db.save()

    def modifier_joueur(self):
        id_joueur = input("Entrez l'ID du joueur à modifier: ")
        joueur = self.db.joueurs_dict.get(id_joueur)
        if joueur:
            print(f"Joueur actuel: {joueur}")
            nom = input(f"Nom (actuel: {joueur.nom}): ") or joueur.nom
            prenom = input(f"Prénom (actuel: {joueur.prenom}): ") or joueur.prenom
            date_naissance = input(f"Date de naissance (actuel: {joueur.date_naissance.strftime('%d/%m/%Y')}): ") or joueur.date_naissance.strftime('%d/%m/%Y')
            joueur.nom = nom
            joueur.prenom = prenom
            joueur.date_naissance = datetime.strptime(date_naissance, '%d/%m/%Y').date()
            print("Joueur modifié avec succès!")
            self.db.save()
        else:
            print("Joueur non trouvé.")

    def ajouter_tournoi(self):
        tournoi = self.view.prompt_tournoi()
        self.db.ajouter_tournoi(tournoi)
        print("Tournoi ajouté avec succès!")
        self.db.save()


    def modifier_tournoi(self):
        id_tournoi = input("Entrez l'ID du tournoi à modifier: ")
        tournoi = next((t for t in self.db.tournois if t.id_tournoi == id_tournoi), None)
        if tournoi:
            print(f"Tournoi actuel: {tournoi}")
            nom_tournoi = input(f"Nom du tournoi (actuel: {tournoi.nom_tournoi}): ") or tournoi.nom_tournoi
            lieu = input(f"Lieu (actuel: {tournoi.lieu}): ") or tournoi.lieu
            date_debut = input(f"Date de début (actuel: {tournoi.date_debut.strftime('%d/%m/%Y')}): ") or tournoi.date_debut.strftime('%d/%m/%Y')
            date_fin = input(f"Date de fin (actuel: {tournoi.date_fin.strftime('%d/%m/%Y')}): ") or tournoi.date_fin.strftime('%d/%m/%Y')
            tournoi.nom_tournoi = nom_tournoi
            tournoi.lieu = lieu
            tournoi.date_debut = datetime.strptime(date_debut, '%d/%m/%Y').date()
            tournoi.date_fin = datetime.strptime(date_fin, '%d/%m/%Y').date()
            print("Tournoi modifié avec succès!")
            self.db.save()
        else:
            print("Tournoi non trouvé.")

    def voir_joueurs(self):
        self.view.afficher_joueurs(self.db.joueurs)

    def voir_tournois(self):
        tournois = self.db.tournois
        tournoi = self.view.afficher_tournois(self.db, tournois)
        if tournoi:
            print(f"Détails du tournoi sélectionné: {tournoi.nom_tournoi}\n\n")


            

    def inscrire_joueur_tournoi(self):
        tournoi = self.view.prompt_inscription_tournoi(self.db.tournois)
        if tournoi is not None:
            participant = self.view.prompt_choix_joueur(self.db.joueurs)
            
            message = tournoi.ajouter_participant(participant)
            print(message)
            
            if "ajouté" in message:
                self.db.save()
            
            print(f"Nombre de participants : {len(tournoi.participants)}")


    def generer_matchs_et_tours(self):
        tournoi = self.view.prompt_selection_tournoi(self.db.tournois)
        if tournoi:
            tournoi.generer_un_tour(self.db)
            print(f"\nMatchs et tours générés pour le tournoi {tournoi.nom_tournoi}.\n")
            self.db.save()
        else:
            print("Aucun tournoi sélectionné.")
        

    def afficher_tours(self, tournoi):
        print(f"Tournoi: {tournoi.nom_tournoi} à {tournoi.lieu}")
        for i, tour in enumerate(tournoi.tours):
            if isinstance(tour, Tour):
                print(f"Tour {i + 1}: {tour.nom}, avec {len(tour.matchs)} matchs.")
            else:
                print(f"Erreur: L'élément à l'index {i} n'est pas un objet Tour.")

    def afficher_tours_et_matchs(self, tournoi):
        self.view.afficher_tours_et_matchs(tournoi)


    def afficher_tournois_disponibles(self):
        tournois = self.db.tournois  
        self.view.afficher_tournois_disponibles(tournois)

    def saisir_modifier_resultats(self):
        self.afficher_tournois_disponibles()

        choix_tournoi = int(input("Entrez le numéro du tournoi pour saisir/modifier les résultats: ")) - 1
        if choix_tournoi < 0 or choix_tournoi >= len(self.db.tournois):
            print("Numéro de tournoi invalide.")
            return

        tournoi = self.db.tournois[choix_tournoi]
        print(f"Tournoi sélectionné: {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut} au {tournoi.date_fin}")

        self.afficher_tours_et_matchs(tournoi)

        tour_num = int(input("Entrez le numéro du tour pour saisir/modifier les résultats (ou 0 pour quitter): "))
        if tour_num == 0:
            return

        tour = next((t for t in tournoi.tours if t.nom == f"Tour {tour_num}"), None)
        if not tour:
            print("Tour non trouvé.")
            return

        self.afficher_tours_et_matchs(tournoi)

        match_num = int(input("Entrez le numéro du match pour saisir/modifier le résultat (ou 0 pour quitter): "))
        if match_num == 0:
            return

        match = next((m for m in tour.matchs if tour.matchs.index(m) + 1 == match_num), None)
        if not match:
            print("Match non trouvé.")
            return

        print(f"Match sélectionné : {match.joueur1.prenom} {match.joueur1.nom} vs {match.joueur2.prenom} {match.joueur2.nom}")

        while True:
            try:
                joueur1_score = float(input(f"Entrez le score pour {match.joueur1.prenom} {match.joueur1.nom} (0, 0.5, 1): "))
                if joueur1_score not in [0, 0.5, 1]:
                    raise ValueError("Le score doit être 0, 0.5 ou 1.")
                joueur2_score = 1 - joueur1_score
                break
            except ValueError as e:
                print(f"Entrée invalide : {e}. Veuillez entrer un score valide.")

        match.set_scores(joueur1_score, joueur2_score)
        print(f"Résultats mis à jour pour le match {match_num}.")


        tournoi.classement_tournoi()
        self.db.save()

    

    def reinitialiser_scores(self):
        confirmation = input("Êtes-vous sûr de vouloir réinitialiser la totalité des scores et résultats de la base de données ? (oui/non): ")
        
        if confirmation.lower() == 'oui':
            for joueur in self.db.joueurs:
                joueur.points = 0

            for tournoi in self.db.tournois:
                # Parcourir chaque tour dans le tournoi
                for tour in tournoi.tours:
                    # Parcourir chaque match dans le tour
                    for match in tour.matchs:
                        # Réinitialiser les scores des joueurs dans le match
                        match.joueur1_score = 0
                        match.joueur2_score = 0
                        match.resultat = "0 - 0"
            

            self.db.save()
            
            print("Les scores de tous les joueurs et de tous les matchs ont été réinitialisés à 0.")
        else:
            print("Réinitialisation des scores annulée.")


if __name__ == "__main__":
    view = View()
    print('view')
    db = Database()
    print('data')
    app = ApplicationController(view, db)
    print('cont')
    app.run()

