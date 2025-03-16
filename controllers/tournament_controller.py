import random
import datetime
from views.tournament_view import TournamentView
from models.tournament_model import Tournament
from models.player_model import Player
from views.utile import get_input, display_message


class TournamentController:
    def __init__(self):
        self.view = TournamentView()
        self.model = Tournament
        self.player_model = Player

    def tournament_management(self):
        while True:
            choice = self.view.display_tournament_menu()
            if choice == "1-1":
                self.create_tournament()
            elif choice == "1-2":
                self.add_players_to_the_tournament()
            elif choice == "1-3":
                self.create_first_round()
            elif choice == "2-1":
                self.start_round_1()
            elif choice == "2-2":
                self.score_update()
            elif choice == "2-3":
                self.start_another_round()
            elif choice == "2-4":
                self.end_of_tournament()
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

    def create_tournament(self):
        """Tournament creation"""
        name_tournament = get_input("\tTournament name: ").strip()
        location = get_input("\tTournament location: ").strip()
        # number_rounds = get_input("\tNumber of tournament rounds: ")
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

        new_tournament = Tournament(name_tournament, location, "", "", number_rounds, description)
        new_tournament.save_data_tournament()

    def add_players_to_the_tournament(self):
        """Add players to a given tournament based on their IDs"""
        # Load player and tournament data
        players_data = Player.load_from_file()
        tournament_data = Tournament.load_from_file()

        # Request tournament ID
        tournament_id = get_input("Enter tournament ID to add players: ").strip()
        tournament_id = int(tournament_id)
        tournament = next((t for t in tournament_data if t.id == tournament_id), None)

        if not tournament:
            display_message("Tournament not found.")
            return

        display_message(f"Add players to tournament {tournament.name_tournament} (ID: {tournament_id}).")
        display_message("Enter the IDs of the players to be added (type 'fin' to finish).")

        while True:
            player_id = get_input("Player ID to be added: ").strip()

            if player_id.lower() == "fin":
                break  # Exits the loop if the user types “end”.
            try:
                player_id = int(player_id)
            except ValueError:
                display_message("Invalid input. Please enter a number or 'fin' to quit.")
            # Check if the player exists
            player = next((p for p in players_data if p.id == player_id), None)

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

        # Sauvegarder les modifications dans data_tournaments.json
        Tournament.save_data_tournament()
        display_message("All players have been added to the tournament.")

    def create_first_round(self):
        """Creates the first round of the tournament by randomly generating pairs of players."""
        tournaments = Tournament.load_from_file()

        tournament_id = get_input("Enter tournament ID : ").strip()
        try:
            tournament_id = int(tournament_id)
        except ValueError:
            display_message("Invalid ID. Please enter a number.")
            return

        tournament = next((t for t in tournaments if t.id == tournament_id), None)

        if not tournament:
            display_message("Tournament not found.")
            return

        # check that the tournament has players
        if len(tournament.players) < 2:
            display_message("Not enough players to start the tournament.")
            return

        # Check if Round 1 already exists
        if any(round_["nom"] == "Round 1" for round_ in tournament.rounds):
            display_message("Round 1 has already been created.")
            return

        players_list = self.shuffle_player(tournament_id)
        pairs = self.create_pairs_round_1(players_list)
        # matches = [[[p1, 0], [p2, 0]] for p1, p2 in pairs]
        matches = []

        # For each pair, we determine the colors (White or Black)
        for p1, p2 in pairs:
            colors = self.draw_white_black([(p1, p2)])[0]  # Assuming draw_white_black returns a list of pairs
            matches.append([[p1, 0], [p2, 0], colors])  # Store players with initial score (0) and their colors

        round_1 = {
            "nom": "Round 1",
            "date_debut": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "date_fin": "",
            "matches": matches,
        }

        tournament.rounds.append(round_1)
        tournament.current_round = 1

        # Remplace l'ancien tournoi dans la liste des tournois
        for i, t in enumerate(tournaments):
            if t.id == tournament_id:
                tournaments[i] = tournament
                break

        print(tournament.rounds)

        Tournament.save_data_tournament()
        display_message("First round successfully created!")

    def end_of_tournament(self):
        """tournament end date"""
        tournament_data = Tournament.load_from_file()
        tournament_id = get_input("Enter the tournament ID to start Round 1: ").strip()
        try:
            tournament_id = int(tournament_id)
        except ValueError:
            display_message("Invalid ID. Please enter a valid number.")
            return

        tournament = next((t for t in tournament_data if t.id == tournament_id), None)

        if not tournament:
            display_message("Tournament not found.")
            return

        if tournament.start_date:
            display_message("The tournament has already begun.")
            return

        tournament.end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        Tournament.save_data_tournament()

        display_message(f"The tournament '{tournament.name_tournament}' ended on {tournament.start_date}.")

    def modify_tournament(self):
        """Allows the user to modify the information of an existing tournament by entering its ID.
        If the user leaves a field empty, the old value is retained."""
        tournament_id = get_input("Enter the ID of the tournament to modify: ")
        tournament_id = int(tournament_id)
        tournament = Tournament.load_from_file()  # Load existing players

        # Find the tournament to modify
        tournament_to_modify = next((t for t in tournament if t.id == tournament_id), None)

        if not tournament_to_modify:
            display_message("Tournament not found.")
            return

        # Display current information
        display_message(
            f"\nModifying tournament:\n\t "
            f"{tournament_to_modify.name_tournament}\n\t"
            f"{tournament_to_modify.location}\n\t"
            f"{tournament_to_modify.start_date} {tournament_to_modify.number_rounds}\n\t"
            f"{tournament_to_modify.description}\n\t"
        )
        display_message("Leave blank to keep the current value.")

        # Request new information
        new_name_tournament = get_input(f"New name tournament ({tournament_to_modify.name_tournament}): ").strip()
        new_location = get_input(f"New location ({tournament_to_modify.location}): ").strip()
        new_start_date = get_input(f"New start_date ({tournament_to_modify.start_date}): ").strip()
        new_number_rounds = get_input(f"New number rounds ({tournament_to_modify.number_rounds}): ").strip()
        new_number_rounds = int(new_number_rounds)
        new_description = get_input(f"New description ({tournament_to_modify.description}): ").strip()

        # Update information if a new value is provided
        if new_name_tournament:
            tournament_to_modify.name_tournament = new_name_tournament
        if new_location:
            tournament_to_modify.location = new_location
        if new_start_date:
            tournament_to_modify.start_date = new_start_date
        if new_number_rounds:
            tournament_to_modify.number_rounds = new_number_rounds
        if new_description:
            tournament_to_modify.description = new_description

        # Save modifications
        Tournament.save_data_tournament()
        display_message("Tournament successfully updated.")

    def delete_tournament(self):
        """Deleting a tournament with id"""
        tournament_id_input = get_input("Enter the ID of the tournament to be deleted: ")
        tournament_id = int(tournament_id_input)
        tournaments = Tournament.load_from_file()  # Load tournament before modification

        # Check if the tournament exists
        tournament_to_delete = next((t for t in tournaments if t.id == tournament_id), None)

        if not tournament_to_delete:
            display_message("Tournament not found.")
            return

        # Request confirmation
        confirmation = (
            get_input(f"Are you sure you want to delete the tournament with the ID {tournament_id}? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation == "y":
            for i, t in enumerate(tournaments):
                if t.id == tournament_id:
                    del tournaments[i]
            Tournament.save_data_tournament()
            display_message("Tournament successfully deleted.")
        else:
            display_message("Deletion cancelled.")
        pass

    def shuffle_player(self, tournament_id):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
        """
        tournament_data = Tournament.load_from_file()

        for tournament in tournament_data:
            if tournament.id == tournament_id:
                players_list = tournament.players

        # self.players_list = tournament_data[tournament_id].get("players", [])
        if len(players_list) > 1:
            random.shuffle(players_list)
        return players_list

    def create_pairs_round_1(self, players_list):
        """
        Generates player pairs for the first round according to random order.

        Returns:
            list[tuple]: A list of tuples containing the player pairs.
        """

        pairs = [(players_list[i], players_list[i + 1]) for i in range(0, len(players_list), 2)]
        return pairs

    def creation_pairs_other_rounds(self):
        """
        Generates player pairs for subsequent rounds based on scores.

        Returns:
            list[tuple]: A list of tuples representing player pairs.
        """
        sorted_players_by_score = sorted(self.players_list, key=lambda x: x.score, reverse=True)
        pairs = [
            (sorted_players_by_score[i], sorted_players_by_score[i + 1])
            for i in range(0, len(sorted_players_by_score), 2)
        ]
        return pairs

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
                assigned_pairs.append((player1, player2, ["White", "Black"]))  # player1 gets white, player2 gets black
            else:
                assigned_pairs.append((player2, player1, ["White", "Black"]))  # player2 gets white, player1 gets black
        return assigned_pairs

    def score_update(self, player, points):
        """
        Updates the player's score after a match.
        Gives the results of the match: the winner receives 1 point, the loser receives 0 points,
        in the event of a draw each receives 0.5 points.

        Args:
            player (Player): The player whose score is to be updated.
            points (float): Number of points obtained (1 for a win, 0.5 for a draw, 0 for a loss).

        Results: “1” if player1 wins,
                 “2” if player2 wins,
                 “draw” for a tie
        """
        pass

    def display_tournament(self):
        """display tournament"""
        tournaments = Tournament.load_from_file()
        players_data = Player.load_from_file()

        for tournament in tournaments:
            display_message(
                f"\tID: {tournament.id}\n\t"
                f"Tournament name: {tournament.name_tournament}\n\t"
                f"Tournament location: {tournament.location}\n\t"
                f"Start date: {tournament.start_date}\n\t"
                f"Number of tournament rounds: {tournament.number_rounds}\n\t"
                f"Tournament description: {tournament.description}\n\t"
                f"End date: {tournament.end_date}\n\t"
                # f"Players: {tournament.players}\n\t"
                # f"Rounds: {tournament.rounds}\n\t"
            )
            display_message("\tPlayers: ")
            for player_id in tournament.players:
                player = next((p for p in players_data if p.id == player_id), None)
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
                display_message("essai")
                display_message(
                    f"\t\t- {round_['nom']}\n "
                    f"\t\t start round: {round_['date_debut']}\n"
                    f"\t\t end round: {round_['date_fin']}\n"
                )
                display_message("\t\t Matches: ")
                for match in round_["matches"]:
                    player1, player2, colors = match  # each match is a list of player data and colors
                    player1_info = next((p for p in players_data if p.id == player1[0]), None)
                    player2_info = next((p for p in players_data if p.id == player2[0]), None)

                    if player1_info and player2_info:
                        display_message(
                            f"\t\t\t{player1_info.first_name} {player1_info.last_name} "
                            f"(ID: {player1_info.id}) score: {player1_info.score} - {colors[0]} vs "
                            f"{player2_info.first_name} {player2_info.last_name} "
                            f"(ID: {player2_info.id}) score: {player2_info.score} - {colors[1]}"
                        )
                    else:
                        display_message("\t\t\t- Invalid player data.")

    def start_round_1(self):
        """début du tournois avec le round 1"""
        tournament_data = Tournament.load_from_file()
        tournament_id = get_input("Enter the tournament ID to start Round 1: ").strip()
        try:
            tournament_id = int(tournament_id)
        except ValueError:
            display_message("Invalid ID. Please enter a valid number.")
            return

        tournament = next((t for t in tournament_data if t.id == tournament_id), None)
        if not tournament:
            display_message("Tournament not found.")
            return

        round_1 = next((r for r in tournament.rounds if r["nom"] == "Round 1"), None)
        if not round_1:
            display_message("Le Round 1 n'a pas encore été créé.")
            return

        round_1["date_debut"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        Tournament.save_data_tournament()
        display_message("Round 1 off to a successful start!")

    def end_round(self):
        """début du tournois avec le round 1"""
        tournament_data = Tournament.load_from_file()
        tournament_id = get_input("Enter the tournament ID to start Round 1: ").strip()
        try:
            tournament_id = int(tournament_id)
        except ValueError:
            display_message("Invalid ID. Please enter a valid number.")
            return

        tournament = next((t for t in tournament_data if t.id == tournament_id), None)
        if not tournament:
            display_message("Tournament not found.")
            return

        round_1 = next((r for r in tournament.rounds if r["nom"] == "Round 1"), None)
        if not round_1:
            display_message("Le Round 1 n'a pas encore été créé.")
            return

        round_1["end_debut"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        Tournament.save_data_tournament()
        display_message("Round 1 off to a successful start!")

    def start_another_round(self):
        pass
