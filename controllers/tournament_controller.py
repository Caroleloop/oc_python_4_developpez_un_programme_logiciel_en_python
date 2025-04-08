import random
import datetime
from views.tournament_view import TournamentView
from models.tournament_model import Tournament
from models.player_model import Player
from controllers.match_controller import MatchController
from controllers.round_controller import RoundController
from controllers.player_controller import PlayerController
from views.utile import get_input, display_message


class TournamentController:
    def __init__(self, tournaments, players):
        self.view = TournamentView()
        self.model = Tournament
        self.player_model = Player
        self.match_controller = MatchController
        self.round_controller = RoundController
        self.player_controller = PlayerController
        Tournament.all_tournaments = tournaments
        Player.all_players = players
        self.past_matches = set()

    def tournament_management(self):
        while True:
            choice = self.view.display_tournament_menu()
            if choice == "1-1":
                self.create_tournament()
            elif choice == "1-2":
                self.add_players_to_the_tournament()
            elif choice == "1-3":
                self.delete_player_to_the_tournament()
            elif choice == "2-1":
                self.create_first_round()
            elif choice == "2-2":
                self.score_update()
            elif choice == "2-3":
                self.create_another_round()
            elif choice == "3":
                self.modify_tournament()
            elif choice == "4":
                self.delete_tournament()
            elif choice == "5":
                self.display_tournament()
            elif choice == "6":
                break
            else:
                print("choice invalide.")

    @staticmethod
    def tournament_id():
        """Request tournament id"""
        if not Tournament.all_tournaments:
            display_message("No tournaments found.")
            return None

        for tournament in Tournament.all_tournaments:
            display_message(
                f"ID: {tournament.id} | Name: {tournament.name_tournament} | Location: {tournament.location}"
                f"| Start date: {tournament.start_date} | End date: {tournament.end_date}"
            )

        while True:
            tournament_id = get_input("Enter the ID of the tournament you want to select: (or 'q' to quit): ").strip()
            if tournament_id.lower() == "q":
                return None

            try:
                tournament_id = int(tournament_id)
            except ValueError:
                display_message("Invalid input. Please enter a number.")
                continue

            tournament = next((t for t in Tournament.all_tournaments if t.id == tournament_id), None)

            if tournament:
                return tournament
            else:
                display_message("Tournament not found. Please try again.")

    def create_tournament(self):
        """Tournament creation"""
        name_tournament = get_input("\tTournament name: ").strip()
        location = get_input("\tTournament location: ").strip()
        start_date = get_input("\tStart date of the tournament:").strip()
        while True:
            number_rounds_input = get_input("\tNumber of tournament rounds (default: 4): ").strip()

            if not number_rounds_input:
                number_rounds = 4
                break

            try:
                number_rounds = int(number_rounds_input)
                if number_rounds < 4:
                    number_rounds = 4
                break
            except ValueError:
                print("Please enter a valid number.")

        description = get_input("\tTournament description: ").strip()

        tournament = Tournament(name_tournament, location, start_date, "", number_rounds, description)
        Tournament.save_data_tournament()

        add_player = get_input("\n\tDo you want to add players to the tournament? (y/n):")
        if add_player == "y":
            self.add_players_to_the_tournament(tournament)
        else:
            display_message("\n\tYou can add players later using the 'Add players' option.")

    def add_players_to_the_tournament(self, tournament=None):
        """Add players to a given tournament based on their IDs"""
        if tournament is None:
            tournament = self.tournament_id()
            if tournament is None:
                display_message("Action cancelled.")
                return

        display_message(f"Add players to tournament: {tournament.name_tournament} (ID: {tournament.id}).")
        display_message("Enter the IDs of the players to be added (type 'end' to finish).")

        while True:
            player_id = get_input("Player ID to be added: ").strip()

            if player_id.lower() == "end":
                break  # Exits the loop if the user types “end”.
            try:
                player_id = int(player_id)
            except ValueError:
                display_message("Invalid input. Please enter a number or 'end' to quit.")
            # Check if the player exists
            player = next((p for p in Player.all_players if p.id == player_id), None)

            if not player:
                display_message(f"Player with ID {player_id} not found.")
                continue

            # Check if the player is already registered
            if any(p_id == player_id for p_id in tournament.players):
                display_message(f"Player {player_id} is already registered in this tournament.")
                continue

                # Add player to tournament
            tournament.players.append(player_id)
            display_message(f"Player ID: {player_id} added successfully.")

        # Save changes in data_tournaments.json
        Tournament.save_data_tournament()
        display_message("All players have been added to the tournament.")

    def delete_player_to_the_tournament(self, tournament=None):
        """suprimer un joueur du tournois"""
        if tournament is None:
            tournament = self.tournament_id()
            if tournament is None:
                display_message("Action cancelled.")
                return

        display_message(f"Delete players to tournament: {tournament.name_tournament} (ID: {tournament.id}).")

        for player_id in tournament.players:
            player = next((p for p in Player.all_players if p.id == player_id), None)
            if player:
                display_message(f"ID: {player.id} | Last name: {player.last_name}  | First name: {player.first_name}")

        player_id = int(get_input("Quel est l'id du joueur à supprimer?:").strip())
        print(player_id)
        # Check if the player exists

        if player_id not in tournament.players:
            display_message("\nJoueur non trouvé dans ce tournoi.")
            return

        player = next((p for p in Player.all_players if p.id == player_id), None)
        if not player:
            display_message("\nJoueur non trouvé dans la base de données.")
            return

        # Request confirmation
        confirmation = (
            get_input(f"\nAre you sure you want to delete {player.last_name} {player.first_name}? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation == "y":
            tournament.players.remove(player_id)
            display_message("\nPlayer successfully deleted.")
        else:
            display_message("\nDeletion cancelled.")

        Tournament.save_data_tournament()

    def create_first_round(self):
        """Creates the first round of the tournament by randomly generating pairs of players."""
        tournament = self.tournament_id()
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

    def end_of_tournament(self):
        """tournament end date"""
        tournament = self.tournament_id()
        if tournament.start_date:
            display_message("The tournament has already begun.")
            return

        tournament.end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        Tournament.save_data_tournament()

        display_message(f"The tournament '{tournament.name_tournament}' ended on {tournament.start_date}.")

    def modify_tournament(self):
        """Allows the user to modify the information of an existing tournament by entering its ID.
        If the user leaves a field empty, the old value is retained."""
        tournament = self.tournament_id()

        # Display current information
        display_message(
            f"\nModifying tournament:\n\t "
            f"ID: {tournament.id}\n\t"
            f"Tournament name: {tournament.name_tournament}\n\t"
            f"Tournament location: {tournament.location}\n\t"
            f"Start date: {tournament.start_date}\n\t"
            f"Number of tournament rounds: {tournament.number_rounds}\n\t"
            f"Tournament description: {tournament.description}\n\t"
        )
        display_message("Leave blank to keep the current value.")

        # Request new information
        new_name_tournament = get_input(f"New name tournament ({tournament.name_tournament}): ").strip()
        new_location = get_input(f"New location ({tournament.location}): ").strip()
        new_start_date = get_input(f"New start_date ({tournament.start_date}): ").strip()
        new_number_rounds = get_input(f"New number rounds ({tournament.number_rounds}): ").strip()
        new_description = get_input(f"New description ({tournament.description}): ").strip()

        # Update information if a new value is provided
        if new_name_tournament:
            tournament.name_tournament = new_name_tournament
        if new_location:
            tournament.location = new_location
        if new_start_date:
            tournament.start_date = new_start_date
        if new_number_rounds:
            tournament.number_rounds = int(new_number_rounds)
        if new_description:
            tournament.description = new_description

        # Save modifications
        Tournament.save_data_tournament()
        display_message("Tournament successfully updated.")

    def delete_tournament(self):
        """Deleting a tournament with id"""
        tournament = self.tournament_id()

        # Request confirmation
        confirmation = (
            get_input(f"Are you sure you want to delete the tournament with the ID {tournament.id}? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation == "y":
            for i, t in enumerate(Tournament.all_tournaments):
                if t.id == tournament.id:
                    del Tournament.all_tournaments[i]
            Tournament.save_data_tournament()
            display_message("Tournament successfully deleted.")
        else:
            display_message("Deletion cancelled.")
        pass

    def shuffle_player(self, tournament_id):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
        """
        for tournament in Tournament.all_tournaments:
            if tournament.id == tournament_id:
                players_list = tournament.players

        # Player.all_players_list = tournament_data[tournament_id].get("players", [])
        if len(players_list) > 1:
            random.shuffle(players_list)
        return players_list

    def shuffle_player_by_score(self, tournament_id):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
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

    def create_pairs_round_1(self, players_list):
        """
        Generates player pairs for the first round according to random order.

        Returns:
            list[tuple]: A list of tuples containing the player pairs.
        """

        pairs = [(players_list[i], players_list[i + 1]) for i in range(0, len(players_list), 2)]
        return pairs

    def creation_pairs_other_rounds(self, players_list_by_score):
        """
        Generates player pairs for subsequent rounds based on scores.

        Returns:
            list[tuple]: A list of tuples representing player pairs.
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

            # Chercher un joueur avec qui il n'a pas encore joué
            for j in range(i + 1, len(players_list_by_score)):
                joueur_2 = players_list_by_score[j]

                if joueur_2 in joueurs_utilises:
                    continue

                paire = (joueur_1, joueur_2)
                paire_inverse = (joueur_2, joueur_1)

                if paire not in joueurs_deja_associes and paire_inverse not in joueurs_deja_associes:
                    pairs_by_score.append(paire)
                    self.past_matches.add(paire)  # Ajouter la paire entière aux matchs passés
                    joueurs_utilises.add(joueur_1)
                    joueurs_utilises.add(joueur_2)
                    break  # On a trouvé un match pour joueur_1, on passe au suivant

                joueurs_restants = [j for j in players_list_by_score if j not in joueurs_utilises]
                if len(joueurs_restants) == 2 and joueur_1 in joueurs_restants and joueur_2 in joueurs_restants:
                    pairs_by_score.append(paire)
                    self.past_matches.add(paire)
                    joueurs_utilises.add(joueur_1)
                    joueurs_utilises.add(joueur_2)
                    break

            i += 1  # Passer au joueur suivant
        return pairs_by_score

    def draw_white_black(self, pairs):
        """
        Randomly determines which player will play with the white or black pieces.

        Args:
            player1 (Player): First player of the pair.
            player2 (Player): Second player of the pair.

        Returns:
         tuple: (Player, Player) where the first element is the player who plays in white
         and the second element is the player who plays in black.
        """
        assigned_pairs = []
        for player1, player2 in pairs:
            if random.choice([True, False]):
                assigned_pairs.append({player1: "white", player2: "black"})  # player1 gets white, player2 gets black
            else:
                assigned_pairs.append({player2: "white", player1: "black"})  # player2 gets white, player1 gets black
        return assigned_pairs

    def score_update(self, tournament=None):
        """
        Updates player scores after a match and updates the current round.
        """
        tournament = self.tournament_id()
        if not tournament.rounds:
            display_message("No round found for this tournament.")
            return

        current_round = next((r for r in tournament.rounds if not r["end_date_round"]), None)

        if not current_round:
            display_message("All rounds have been completed.")
            return

        display_message(f" Update scores for  {current_round['name']} (ID: {current_round['id']})")

        for match in current_round["matches"]:
            player1, player2, colors = match
            display_message(f"Match between  {player1[0]} and {player2[0]}")

            valid_responses = ["1", "2", "draw"]
            result = None

            while result not in valid_responses:
                result = get_input(
                    f"Result  (1: Player  {player1[0]} wins, 2: Player  {player2[0]} wins, draw: equality) : "
                )
                if result not in valid_responses:
                    display_message("Invalid input. Please enter '1', '2', or 'draw'.")

            try:
                self.match_controller.match_result(player1, player2, result, match)
                self.match_controller.update_player_score(player1[0], player1[1])
                self.match_controller.update_player_score(player2[0], player2[1])
            except ValueError as e:
                display_message(str(e))
                return

        display_message("Scores updated and round over!\n")

        self.end_tournament(tournament)
        Tournament.save_data_tournament()

    @staticmethod
    def display_tournament():
        """display tournament"""
        Player.load_data_players()
        Tournament.load_data_tournaments()

        for tournament in Tournament.all_tournaments:
            display_message(
                f"\n\n\tID: {tournament.id}\n\t"
                f"Tournament name: {tournament.name_tournament}\n\t"
                f"Tournament location: {tournament.location}\n\t"
                f"Start date: {tournament.start_date}\n\t"
                f"Number of tournament rounds: {tournament.number_rounds}\n\t"
                f"Tournament description: {tournament.description}\n\t"
                f"End date: {tournament.end_date}"
            )
            display_message("\tPlayers: ")
            for player_id in tournament.players:
                player = next((p for p in Player.all_players if p.id == player_id), None)
                if player:
                    display_message(
                        f"\t\tID: {player.id}\n\t"
                        f"\tLast name: {player.last_name}\n\t"
                        f"\tFirst name: {player.first_name}\n\t"
                        f"\tBirthdate: {player.birthdate}\n\t"
                        f"\tNational chess identifier: {player.national_chess_identifier}\n\t"
                        f"\tScore: {player.score}\n"
                    )
                else:
                    display_message(f"\t\t- Player ID {player_id} not found.")

            display_message("\tRounds: ")
            for round_ in tournament.rounds:
                display_message(
                    f"\t\t{round_['name']}:\n "
                    f"\t\tStart round: {round_['start_date_round']}\n"
                    f"\t\tEnd round: {round_['end_date_round']}"
                )
                display_message("\t\tMatches: ")
                for match in round_["matches"]:
                    player1, player2, color = match
                    player1_info = next((p for p in Player.all_players if p.id == player1[0]), None)
                    player2_info = next((p for p in Player.all_players if p.id == player2[0]), None)

                    color_info = color[0]
                    color1 = "white" if color_info.get(str(player1_info.id)) == "white" else "black"
                    color2 = "white" if color_info.get(str(player2_info.id)) == "white" else "black"

                    if player1_info and player2_info:

                        display_message(
                            f"\t\t\t{player1_info.first_name} {player1_info.last_name} "
                            f"(ID: {player1_info.id}), color: {color1}, score: {player1[1]}  vs "
                            f"{player2_info.first_name} {player2_info.last_name} "
                            f"(ID: {player2_info.id}), color: {color2}, score: {player2[1]} "
                        )
                    else:
                        display_message("\t\t\t- Invalid player data.")

    def start_round(self, tournament):
        """Tournament starts with round 1"""

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

    def end_tournament(self, tournament):
        """Ends the tournament if it was the last round."""
        if not tournament.rounds:
            display_message("No round found for this tournament.")
            return

        # Find the last round in progress (the one that doesn't yet have an end date)
        current_round = next((r for r in tournament.rounds if not r["end_date_round"]), None)

        if not current_round:
            display_message("\nAll rounds have already been completed.")
            return

        # Mark the end of the round
        current_round["end_date_round"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if this is the last round of the tournament
        if current_round["id"] == tournament.number_rounds:
            tournament.end_date = current_round["end_date_round"]
            display_message(f"\nThe tournament '{tournament.name_tournament}' is finished!")
        else:
            display_message(f"{current_round['name']} finished. The tournament continues.")

    def create_another_round(self):
        """Create a new tournament round."""
        tournament = self.tournament_id()
        if len(tournament.players) < 2:
            display_message("Not enough players to start the tournament.")
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
