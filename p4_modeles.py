import json
import os
from datetime import datetime, date
import random



class Joueur:
    def __init__(self, nom, prenom, date_naissance, id_joueur):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_joueur = id_joueur
        self.points = 0
        self.classement_joueur = 0

    def to_dict(self):
        return {
            'nom': self.nom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'id_joueur': self.id_joueur,
            'points': self.points,
            'classement_joueur': self.classement_joueur
        }

    @staticmethod
    def from_dict(data):
        joueur = Joueur(
            nom=data['nom'],
            prenom=data['prenom'],
            date_naissance=datetime.strptime(data['date_naissance'], '%d/%m/%Y').date(),
            id_joueur=data['id_joueur']
        )
        joueur.points = data.get('points', 0)
        joueur.classement_joueur = data.get('classement_joueur', 0)
        return joueur

    def __repr__(self):
        return f"Joueur(nom={self.nom}, prenom={self.prenom}, id_joueur={self.id_joueur})"




class Tour:
    def __init__(self, nom, matchs, joueur_exempt=None):
        self.nom = nom
        self.matchs = matchs
        self.joueur_exempt = joueur_exempt

    def creer_matchs(self, paires, db):
        for joueur1_id, joueur2_id in paires:
            joueur1 = db.joueurs_dict[joueur1_id]
            joueur2 = db.joueurs_dict[joueur2_id]
            match = Match(joueur1, joueur2, db)
            self.matchs.append(match)

    def ajouter_match(self, match):
        self.matchs.append(match)


    def to_dict(self):
        return {
            'nom': self.nom,
            'matchs': [match.to_dict() for match in self.matchs]
        }

    def generer_tours(self, paires, db):

        for paire in paires:
            joueur1 = next(j for j in db.joueurs if j.id_joueur == paire[0])
            joueur2 = next(j for j in db.joueurs if j.id_joueur == paire[1])
            if joueur1 and joueur2:
                match = Match(joueur1, joueur2, db)
                self.matchs.append(match)
            else:
                print(f"Erreur : Joueur(s) pour la paire {paire} non trouvé(s).")


    @staticmethod
    def from_dict(data, joueurs, db):
        tour = Tour(data['nom'], [])
        tour.matchs = [Match.from_dict(match_data, joueurs, db) for match_data in data['matchs']]
        return tour

    def __repr__(self):
        return f"Tour(nom={self.nom}, matchs={self.matchs})"
    
    def __str__(self):
        result = f"--- {self.nom} ---\n"
        if self.joueur_exempt:
            result += f"{self.joueur_exempt.prenom} {self.joueur_exempt.nom} est exempté ce tour.\n"
        result += "Matchs pour {self.nom} :\n"
        for match in self.matchs:
            joueur1 = match.joueur1
            joueur2 = match.joueur2
            result += f"- {joueur1.prenom} {joueur1.nom} (ID: {joueur1.id_joueur}) vs {joueur2.prenom} {joueur2.nom} (ID: {joueur2.id_joueur})\n"
        if self.joueur_exempt:
            result += f"Joueur exempté ce tour: {self.joueur_exempt.id_joueur}\n"
        return result


class Tournoi:
    def __init__(self, nom_tournoi, lieu, date_debut, date_fin, id_tournoi):
        self.nom_tournoi = nom_tournoi
        self.lieu = lieu
        if isinstance(date_debut, str):
            self.date_debut = datetime.strptime(date_debut, '%d/%m/%Y').date()
        else:
            self.date_debut = date_debut
        if isinstance(date_fin, str):
            self.date_fin = datetime.strptime(date_fin, '%d/%m/%Y').date()
        else:
            self.date_fin = date_fin
        self.id_tournoi = id_tournoi
        self.tours = []
        self.tour_actuel = 0
        self.description = ""
        self.participants = []
        self.db = None
        self.joueur_exempt = None
        self.resultats = {}


    def ajouter_tour(self, tour):
        if isinstance(tour, Tour):
            self.tours.append(tour)
            print(f"Tour ajouté : {tour}")
        else:
            print(f"Erreur : L'objet ajouté n'est pas un Tour.")


    def generer_matchs_et_tours(self, db):
        if len(self.participants) < 2:
            print("Pas assez de participants pour générer des matchs.")
            return

        joueurs = [db.joueurs_dict[id_joueur] for id_joueur in self.participants]
        tours = []
        total_tours = 4
        paires_deja_jouees = set()
        exemptions = set()

        while len(joueurs) > 1:
            matchs = []
            if len(joueurs) % 2 != 0:
                joueur_exempt = joueurs.pop()
            else:
                joueur_exempt = None

            while len(joueurs) > 1:
                joueur1 = joueurs.pop(0)
                for joueur2 in joueurs:
                    paire = (joueur1.id_joueur, joueur2.id_joueur)
                    if paire in paires_deja_jouees or (paire[1], paire[0]) in paires_deja_jouees:
                        continue
                    paires_deja_jouees.add(paire)
                    matchs.append(Match(joueur1, joueur2, db))
                    joueurs.remove(joueur2)
                    break

            # Création et ajout du tour
            tour = Tour(nom=f"Tour {len(tours) + 1}", matchs=matchs, joueur_exempt=joueur_exempt)
            tours.append(tour)

            # Affichage du tour
            print(f"\n--- {tour.nom} ---")
            if tour.joueur_exempt:
                print(f"{tour.joueur_exempt.prenom} {tour.joueur_exempt.nom} est exempté ce tour car le nombre de joueurs est impair.")
            print(f"\nMatchs pour {tour.nom} :")
            for match in tour.matchs:
                joueur1 = match.joueur1
                joueur2 = match.joueur2
                print(f"- {joueur1.prenom} {joueur1.nom} vs {joueur2.prenom} {joueur2.nom}")

            if tour.joueur_exempt:
                print(f"Joueur exempté ce tour: {tour.joueur_exempt.id_joueur} ({tour.joueur_exempt.nom} {tour.joueur_exempt.prenom})")

        # Mise à jour du tournoi avec les nouveaux tours
        self.tours = tours

    def saisir_resultats(self, paires):
        for joueur1, joueur2 in paires:
            gagnant = None
            while gagnant not in [joueur1, joueur2]:
                print(f"Match: {joueur1} vs {joueur2}")
                gagnant_id = input(f"Entrez l'ID du gagnant (entre {joueur1} et {joueur2}): ")
                if gagnant_id == joueur1:
                    gagnant = joueur1
                elif gagnant_id == joueur2:
                    gagnant = joueur2
                else:
                    print("ID invalide, veuillez réessayer.")
            self.resultats[gagnant] += 1  

    def mettre_a_jour_classement_apres_tour(self, db):
        print("Classement après ce tour :")
        classement = sorted(self.participants, key=lambda id_joueur: self.resultats[id_joueur], reverse=True)
        for rang, id_joueur in enumerate(classement, start=1):
            joueur = next(j for j in self.db.joueurs if j.id_joueur == id_joueur)
            print(f"{rang}. {joueur.prenom} {joueur.nom} - {self.resultats[id_joueur]} points")


    def ajouter_participant(self, joueur):
        if joueur.id_joueur not in self.participants:
            self.participants.append(joueur.id_joueur)
            self.resultats[joueur.id_joueur] = 0
            return f"Joueur {joueur.prenom} {joueur.nom} ajouté au tournoi avec succès !"
        else:
            return f"Le joueur {joueur.prenom} {joueur.nom} est déjà inscrit à ce tournoi."
        

    def generer_paires(self):
        if len(self.participants) % 2 != 0:
            exempt_id = random.choice(self.participants)
            exempt = next(j for j in self.db.joueurs if j.id_joueur == exempt_id)
            self.joueur_exempt = exempt_id
            print(f"{exempt.prenom} {exempt.nom} est exempté car le nombre de joueurs est impair.")
        else:
            self.joueur_exempt = None

        if len(self.participants) > 0:
            classement = sorted(self.participants, key=lambda id_joueur: self.resultats.get(id_joueur, 0), reverse=True)
        else:
            classement = []

        paires = []
        i = 0
        while i < len(classement) - 1:
            joueur1 = classement[i]
            joueur2 = classement[i + 1]
            paires.append((joueur1, joueur2))
            i += 2
        
        return paires
    


    def ajouter_joueur(self, joueur):
        if joueur.id_joueur not in [joueur.id_joueur for joueur in self.db.joueurs]:
            self.participants.append(joueur.id_joueur)
            print(f"Joueur {joueur.prenom} {joueur.nom} ajouté à la base de données avec succès !")
        else:
            print(f"Le joueur {joueur.prenom} {joueur.nom} est déjà inscrit dans la base de données.")

        

    def to_dict(self):
        return {
            'nom_tournoi': self.nom_tournoi,
            'lieu': self.lieu,
            'date_debut': self.date_debut.strftime('%d/%m/%Y'),
            'date_fin': self.date_fin.strftime('%d/%m/%Y'),
            'id_tournoi': self.id_tournoi,
            'tours': [tour.to_dict() for tour in self.tours],
            'joueurs_tournoi': self.participants,
            'joueur_exempt': self.joueur_exempt
        }


    @staticmethod
    def from_dict(data, db):
        nom_tournoi = data['nom_tournoi']
        lieu = data['lieu']
        date_debut = datetime.strptime(data['date_debut'], '%d/%m/%Y').date()
        date_fin = datetime.strptime(data['date_fin'], '%d/%m/%Y').date()
        id_tournoi = data['id_tournoi']

        tournoi = Tournoi(nom_tournoi, lieu, date_debut, date_fin, id_tournoi)
        participants = data.get('joueurs_tournoi', [])
        tournoi.participants = participants
        tournoi.joueur_exempt = data.get('joueur_exempt', None)

        tournoi.db = db
        tournoi.tours = [Tour.from_dict(tour_data, tournoi.db.joueurs, db) for tour_data in data.get('tours', [])]

        return tournoi


    def __repr__(self):
        return f"Tournoi(nom_tournoi={self.nom_tournoi}, lieu={self.lieu}, date_debut={self.date_debut}, date_fin={self.date_fin})"




class Match:
    def __init__(self, joueur1, joueur2, db):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.joueur1_score = 0
        self.joueur2_score = 0
        self.db = db
            
            
    def set_scores(self, joueur1_score, joueur2_score):
        self.joueur1_score = joueur1_score
        self.joueur2_score = joueur2_score
        self.db.save()

    def to_dict(self):
        return {
            'joueur1': self.joueur1.id_joueur,
            'joueur2': self.joueur2.id_joueur,
            'joueur1_score': self.joueur1_score,
            'joueur2_score': self.joueur2_score
        }

    @staticmethod
    def from_dict(data, joueurs, db):
        joueur1 = next((joueur for joueur in joueurs if joueur.id_joueur == data['joueur1']), None)
        joueur2 = next((joueur for joueur in joueurs if joueur.id_joueur == data['joueur2']), None)
        if joueur1 and joueur2:
            match = Match(joueur1, joueur2, db)
            match.set_scores(data['joueur1_score'], data['joueur2_score'])
            return match
        return None

    def __repr__(self):
        return f"Match(joueur1={self.joueur1}, joueur2={self.joueur2}, joueur1_score={self.joueur1_score}, joueur2_score={self.joueur2_score})"





class Database:
    def __init__(self):
        self.joueurs_file = 'joueurs.json'
        self.tournois_file = 'tournois.json'
        self.joueurs_dict = {}
        self.joueurs = []  
        self.tournois = []
        self.participants = []
        self.load_data()

    def load_data(self):
        self.joueurs = self.load_joueurs()  
        self.joueurs_dict = {j.id_joueur: j for j in self.joueurs}  
        self.tournois = self.load_tournois()

    def load_joueurs(self):
        joueurs = []
        if os.path.exists(self.joueurs_file):
            with open(self.joueurs_file, 'r', encoding='utf-8') as file:
                joueurs_data = json.load(file)
                joueurs = [Joueur.from_dict(joueur) for joueur in joueurs_data]
        return joueurs

    def load_tournois(self):
        tournois = []
        if os.path.exists(self.tournois_file):
            with open(self.tournois_file, 'r', encoding='utf-8') as file:
                tournois_data = json.load(file)
            for tournoi_data in tournois_data:
                tournoi = Tournoi.from_dict(tournoi_data, self)
                tournois.append(tournoi)
        return tournois

    def ajouter_joueur(self, joueur):
        if joueur.id_joueur not in [j.id_joueur for j in self.joueurs]:
            self.joueurs.append(joueur)
            self.joueurs_dict[joueur.id_joueur] = joueur
            self.save()

    def ajouter_tournoi(self, tournoi):
        if tournoi.id_tournoi not in [t.id_tournoi for t in self.tournois]:
            self.tournois.append(tournoi)
            self.save()

    def save(self):
        with open(self.joueurs_file, 'w', encoding='utf-8') as file:
            json.dump([joueur.to_dict() for joueur in self.joueurs], file, indent=4, default=self.default)

        with open(self.tournois_file, 'w', encoding='utf-8') as file:
            json.dump([tournoi.to_dict() for tournoi in self.tournois], file, indent=4, default=self.default)

    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%d/%m/%Y')
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')






