import random
import datetime
from utile.utile import display_message
from models.tournament_model import Tournament


class RoundController:
    def __init__(self):
        """Initializes the round controller.

        Attributes:
            past_matches (set): Set containing all previously played player pairs.
            tounament_model (Tournament): Reference to the Tournament model.
        """
        self.past_matches = set()
        self.tounament_model = Tournament

    def create_round(self, name_round, start_time, end_time):
        """Creates a new round and initializes its structure.

        Args:
            name_round (str): Name of the round (e.g., "Round 1").
            start_time (str): Round start datetime ('YYYY-MM-DD HH:MM').
            end_time (str): Round end datetime ('YYYY-MM-DD HH:MM').

        Returns:
            dict: Dictionary representing the round with metadata and empty match list.
        """
        round_data = {"name": name_round, "start_time": start_time, "end_time": end_time, "matches": []}
        return round_data

    def initialize_current_round(self, tournament):
        """Initializes the current round number if not already defined.

        Args:
            tournament (Tournament): The tournament to initialize.
        """
        if not hasattr(tournament, "current_round"):
            tournament.current_round = 1

    def shuffle_player(self, tournament_id):
        """Randomly shuffles the players of the tournament.

        Args:
            tournament_id (str): The ID of the tournament.

        Returns:
            list: Shuffled list of player IDs.
        """
        for tournament in Tournament.all_tournaments:
            if tournament.id == tournament_id:
                players_list = tournament.players

        # Player.all_players_list = tournament_data[tournament_id].get("players", [])
        if len(players_list) > 1:
            random.shuffle(players_list)
        return players_list

    def shuffle_player_by_score(self, tournament_id):
        """Sorts players by score in descending order.

        Args:
            tournament_id (str): The ID of the tournament.

        Returns:
            list: List of player IDs sorted by score.
        """
        for tournament in Tournament.all_tournaments:
            if tournament.id == tournament_id:
                players_list = tournament.players

        scores = {player_id: 0 for player_id in players_list}

        for round_data in tournament.rounds:
            for match in round_data["matches"]:
                for player_score in match[:2]:
                    player_id, score = player_score
                    scores[player_id] += score

        players_list_by_score = sorted(players_list, key=lambda player: scores[player], reverse=True)

        return players_list_by_score

    def create_first_round(self):
        """Creates the first round for a tournament, generates pairs, and assigns colors."""
        tournament = Tournament.tournament_id()
        # check that the tournament has players
        if len(tournament.players) < 2:
            display_message("Not enough players to start the tournament.")
            return

        if len(tournament.players) % 2 != 0:
            display_message(
                "\nThe number of players is odd. An even number even to create tournament matches."
                "Please add or remove a player."
            )
            return

        # Check if Round 1 already exists
        if any(round_["name"] == "Round 1" for round_ in tournament.rounds):
            display_message("Round 1 has already been created.")
            return

        players_list = self.shuffle_player(tournament.id)
        pairs = self.create_pairs_round_1(players_list)
        matches = []

        # For each pair, we determine the colors (White or Black)
        for p1, p2 in pairs:
            # Assuming draw_white_black returns a list of pairs
            colors = self.draw_white_black([(p1, p2)])
            matches.append([[p1, 0], [p2, 0], colors])
            for match in matches:
                self.past_matches.add((match[0][0], match[1][0]))

        round_id = 1
        round_1 = {
            "id": round_id,
            "name": f"Round {round_id}",
            "start_date_round": "",
            "end_date_round": "",
            "matches": matches,
        }

        tournament.rounds.append(round_1)
        # tournament.current_round = 0

        # Remplace l'ancien tournoi dans la liste des tournois
        for i, t in enumerate(Tournament.all_tournaments):
            if t.id == tournament.id:
                Tournament.all_tournaments[i] = tournament
                break

        self.start_round(tournament)
        Tournament.save_data_tournament()
        display_message("First round successfully created!")

    @staticmethod
    def create_pairs_round_1(players_list):
        """Creates pairs of players randomly for the first round.

        Args:
            players_list (list): List of player IDs.

        Returns:
            list[tuple]: List of player ID pairs.
        """
        pairs = [(players_list[i], players_list[i + 1]) for i in range(0, len(players_list), 2)]
        return pairs

    def creation_pairs_other_rounds(self, players_list_by_score):
        """Creates unique player pairs for other rounds based on score.

        Args:
            players_list_by_score (list): List of player IDs sorted by score.

        Returns:
            list[tuple]: List of player ID pairs ensuring no repetition if possible.
        """

        # shuffle_player_by_score = self.shuffle_player_by_score(tournament_id)
        pairs_by_score = []
        joueurs_deja_associes = set(self.past_matches)  # Copier les paires déjà jouées
        joueurs_utilises = set()  # Liste des joueurs déjà affectés à un match

        i = 0
        while i < len(players_list_by_score):
            joueur_1 = players_list_by_score[i]

            if joueur_1 in joueurs_utilises:
                i += 1
                continue

            paire_trouvee = False

            # Chercher un joueur avec qui il n'a pas encore joué
            for j in range(i + 1, len(players_list_by_score)):
                joueur_2 = players_list_by_score[j]

                if joueur_2 in joueurs_utilises:
                    continue

                paire = (joueur_1, joueur_2)
                paire_inverse = (joueur_2, joueur_1)

                if paire not in joueurs_deja_associes and paire_inverse not in joueurs_deja_associes:
                    pairs_by_score.append(paire)
                    self.past_matches.add(paire)
                    joueurs_utilises.update([joueur_1, joueur_2])
                    paire_trouvee = True
                    break

            if not paire_trouvee:
                # Aucun joueur dispo avec qui il n'a pas joué, on forcera à la fin
                i += 1
            else:
                i += 1  # Avance quand une paire est trouvée

        # Forcer les paires restantes même si elles ont déjà été jouées
        joueurs_restants = [j for j in players_list_by_score if j not in joueurs_utilises]
        while len(joueurs_restants) >= 2:
            joueur_1 = joueurs_restants.pop(0)
            joueur_2 = joueurs_restants.pop(0)
            paire = (joueur_1, joueur_2)
            pairs_by_score.append(paire)
            self.past_matches.add(paire)
            joueurs_utilises.update([joueur_1, joueur_2])

        return pairs_by_score

    def draw_white_black(self, pairs):
        """Randomly assigns white and black pieces to each player in the pairs.

        Args:
            pairs (list[tuple]): List of player pairs.

        Returns:
            list[dict]: List of dictionaries with color assignments.
        """
        assigned_pairs = []
        for player1, player2 in pairs:
            if random.choice([True, False]):
                assigned_pairs.append({player1: "white", player2: "black"})  # player1 gets white, player2 gets black
            else:
                assigned_pairs.append({player2: "white", player1: "black"})  # player2 gets white, player1 gets black
        return assigned_pairs

    def create_another_round(self):
        """Create a new tournament round."""
        tournament = Tournament.tournament_id()
        if len(tournament.players) < 2:
            display_message("Not enough players to start the tournament.")
            return

        # Check if the tournament is already finished
        if len(tournament.rounds) >= tournament.number_rounds:
            display_message("The tournament is already finished. No more rounds can be created.")
            return

        # checks whether the last round has been completed
        if tournament.rounds:
            last_round = tournament.rounds[-1]
            if not last_round["end_date_round"]:
                display_message("\nYou must end the previous round before starting a new one.")
                return

        players_list_score = self.shuffle_player_by_score(tournament.id)
        pairs = self.creation_pairs_other_rounds(players_list_score)

        matches = []
        for p1, p2 in pairs:
            colors = self.draw_white_black([(p1, p2)])
            matches.append([[p1, 0], [p2, 0], colors])
            for match in matches:
                self.past_matches.add((match[0][0], match[1][0]))

        round_id = len(tournament.rounds) + 1

        # Creating the new round
        new_round = {
            "id": round_id,
            "name": f"Round {round_id}",
            "start_date_round": "",
            "end_date_round": "",
            "matches": matches,
        }

        tournament.rounds.append(new_round)
        for i, t in enumerate(Tournament.all_tournaments):
            if t.id == tournament.id:
                Tournament.all_tournaments[i] = tournament
                break

        self.start_round(tournament)
        Tournament.save_data_tournament()
        display_message(f"Round {round_id} has been successfully created!")

    @staticmethod
    def start_round(tournament):
        """Starts the latest round of the tournament by assigning its start date.

        Args:
            tournament (Tournament): The tournament whose round is to be started.
        """
        if not tournament.rounds:
            display_message("No round has yet been created.")
            return

        latest_round = tournament.rounds[-1]

        if "start_date_round" in latest_round and latest_round["start_date_round"]:
            display_message(f"{latest_round['name']} has already begun.")
            return

        latest_round["start_date_round"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        tournament.current_round += 1
        Tournament.save_data_tournament()
