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
            choix = self.view.display_tournament_menu()
            if choix == "1":
                self.create_tournament()
            elif choix == "2":
                self.manage_tournament()
            elif choix == "3":
                self.modify_tournament()
            elif choix == "4":
                self.delete_tournament()
            elif choix == "5":
                break
            else:
                print("Choix invalide.")

    def create_tournament(self):
        """Création d’un tournoi"""
        name_tournament = get_input(" Tournament name: ")
        location = get_input("Tournament location: ")
        start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        end_date = self.tournament_end_date()
        number_rounds = get_input("Number of tournament rounds: ")
        rounds = []
        description = get_input("Tournament description: ")
        players = []

        new_tournamùent = Tournament(
            name_tournament, location, start_date, end_date, number_rounds, description, rounds, players
        )
        new_tournamùent.save_data_tournament()

    def add_players_to_the_tournament(self):
        """Add players to a given tournament based on their IDs"""
        # Load player and tournament data
        players_data = Player.load_from_file()
        tournament_data = Tournament.load_from_file()

        # Request tournament ID
        tournament_id = get_input("Enter tournament ID to add players: ").strip()
        tournament = next((t for t in tournament_data if t["id"] == tournament_id), None)

        if not tournament:
            display_message("Tournament not found.")
            return

        display_message(f"Add players to tournament {tournament['name_tournament']} (ID: {tournament_id}).")
        display_message("Enter the IDs of the players to be added (type 'fin' to finish).")

        while True:
            player_id = get_input("Player ID to be added: ").strip()

            if player_id.lower() == "fin":
                break  # Exits the loop if the user types “end”.

            # Check if the player exists
            player = next((p for p in players_data if p["id"] == player_id), None)

            if not player:
                display_message(f"Player with ID {player_id} not found.")
                continue

            # Check if the player is already registered
            if any(p["id"] == player_id for p in tournament["players"]):
                display_message(f"Player {player_id} is already registered in this tournament.")
                continue

            # Add player to tournament
            tournament["players"].append(player)
            display_message(f"Player ID: {player_id} added successfully.")

        # Sauvegarder les modifications dans data_tournaments.json
        Tournament.save_data()
        display_message("All players have been added to the tournament.")

    def tournament_end_date(self):
        """tournament end date"""
        end_tournament = get_input("Is the tournament finished? (y/n): ").strip().lower()
        if end_tournament == "y":
            end_date = self.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            return end_date

    def modify_tournament(self):
        """Allows the user to modify the information of an existing tournament by entering its ID.
        If the user leaves a field empty, the old value is retained."""
        tournament_id = get_input("Enter the ID of the tournament to modify: ")
        tournament = Tournament.load_from_file()  # Load existing players

        # Find the tournament to modify
        tournament_to_modify = next((t for t in tournament if t["id"] == tournament_id), None)

        if not tournament_to_modify:
            display_message("Tournament not found.")
            return

        # Display current information
        display_message(
            f"Modifying tournament: {tournament_to_modify.name_tournament} {tournament_to_modify.location}"
            f"{tournament_to_modify.start_date} {tournament_to_modify.number_rounds}"
            f"{tournament_to_modify.description}"
        )
        display_message("Leave blank to keep the current value.")

        # Request new information
        new_name_tournament = get_input(f"New name tournament ({tournament_to_modify.last_name}): ").strip()
        new_location = get_input(f"New location ({tournament_to_modify.location}): ").strip()
        new_start_date = get_input(f"New bistart_daterthdate ({tournament_to_modify.start_date}): ").strip()
        new_number_rounds = get_input(f"New number rounds ({tournament_to_modify.number_rounds}): ").strip()
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
        Tournament.save_data_tournament(tournament)
        display_message("Tournament successfully updated.")

    def delete_tournament(self):
        """Deleting a tournament with id"""
        tournament_id = get_input("Enter the ID of the tournament to be deleted: ")
        tournament = Tournament.load_from_file()  # Load tournament before modification

        # Check if the tournament exists
        tournament_to_delete = next((t for t in tournament if t["id"] == tournament_id), None)

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
            tournament = [t for t in tournament if t["id"] != tournament_id]  # Delete tournament
            Tournament.save_data_tournament(tournament)  # Save new list
            display_message("Tournament successfully deleted.")
        else:
            display_message("Deletion cancelled.")
        pass

    def shuffle_player(self):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
        """
        tournament_data = Tournament.load_from_file()
        self.players_list = tournament_data.get("players", [])
        if len(self.players_list) > 1:
            random.shuffle(self.players_list)
        return self.players_list

    def create_pairs_round_1(self):
        """
        Generates player pairs for the first round according to random order.

        Returns:
            list[tuple]: A list of tuples containing the player pairs.
        """
        self.shuffle_player()
        pairs = [(self.players_list[i], self.players_list[i + 1]) for i in range(0, len(self.players_list), 2)]
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
                assigned_pairs.append((player1, player2))  # player1 gets white, player2 gets black
            else:
                assigned_pairs.append((player2, player1))  # player2 gets white, player1 gets black
        return assigned_pairs

    def update_score(self, player, points):
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
