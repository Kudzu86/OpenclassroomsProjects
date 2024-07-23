from p4_modeles import Database, Tournoi, Tour, Match
from p4_vues import View

class ApplicationController:
    def __init__(self, view, db):
        self.view = view
        self.db = db

    def run(self):
        while True:
            self.view.afficher_menu()
            choix = input("Choisissez une option: ")
            if choix == '1':
                self.ajouter_joueur()
            elif choix == '2':
                self.ajouter_tournoi()
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
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez choisir une option valide.")

    def ajouter_joueur(self):
        joueur = self.view.prompt_joueur()
        self.db.ajouter_joueur(joueur)
        print("Joueur ajouté avec succès!")

    def ajouter_tournoi(self):
        tournoi = self.view.prompt_tournoi()
        self.db.ajouter_tournoi(tournoi)
        print("Tournoi ajouté avec succès!")

    def voir_joueurs(self):
        self.view.afficher_joueurs(self.db.joueurs)

    def voir_tournois(self):
        self.view.afficher_tournois(self.db.tournois)

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
        tournoi.generer_matchs_et_tours(db)


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
    # Affiche les tournois disponibles pour la sélection
        self.afficher_tournois_disponibles()

        # Sélection du tournoi
        choix_tournoi = int(input("Entrez le numéro du tournoi pour saisir/modifier les résultats: ")) - 1
        if choix_tournoi < 0 or choix_tournoi >= len(self.db.tournois):
            print("Numéro de tournoi invalide.")
            return

        tournoi = self.db.tournois[choix_tournoi]
        print(f"Tournoi sélectionné: {tournoi.nom_tournoi} à {tournoi.lieu}, du {tournoi.date_debut} au {tournoi.date_fin}")

        # Affiche les tours et les matchs disponibles
        self.afficher_tours_et_matchs(tournoi)

        # Sélection du tour
        tour_num = int(input("Entrez le numéro du tour pour saisir/modifier les résultats (ou 0 pour quitter): "))
        if tour_num == 0:
            return

        tour = next((t for t in tournoi.tours if t.nom == f"Tour {tour_num}"), None)
        if not tour:
            print("Tour non trouvé.")
            return

        # Affiche les matchs pour le tour sélectionné
        self.afficher_tours_et_matchs(tournoi)

        # Sélection du match
        match_num = int(input("Entrez le numéro du match pour saisir/modifier le résultat (ou 0 pour quitter): "))
        if match_num == 0:
            return

        match = next((m for m in tour.matchs if tour.matchs.index(m) + 1 == match_num), None)
        if not match:
            print("Match non trouvé.")
            return

        print(f"Match sélectionné : {match.joueur1.prenom} {match.joueur1.nom} vs {match.joueur2.prenom} {match.joueur2.nom}")

        # Saisie des scores
        try:
            joueur1_score = int(input(f"Entrez le score pour {match.joueur1.prenom} {match.joueur1.nom}: "))
            joueur2_score = int(input(f"Entrez le score pour {match.joueur2.prenom} {match.joueur2.nom}: "))
        except ValueError:
            print("Score invalide. Les scores doivent être des nombres entiers.")
            return

        # Mise à jour des scores du match
        match.set_scores(joueur1_score, joueur2_score)
        print(f"Résultats mis à jour pour le match {match_num}.")

        # Mise à jour des points des joueurs en fonction des résultats
        if joueur1_score > joueur2_score:
            match.joueur1.points += 1
        elif joueur2_score > joueur1_score:
            match.joueur2.points += 1
        # Si égalité, aucun point n'est attribué (ajustez si nécessaire)

        # Sauvegarde des modifications dans la base de données
        self.db.save()




if __name__ == "__main__":
    view = View()
    db = Database()
    app = ApplicationController(view, db)
    app.run()
