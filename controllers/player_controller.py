import re
from datetime import datetime

from models.player_model import Player
from views.player_view import PlayerView
from views.menu_view import MenuView
from utile.utile import get_input, display_message


class PlayerController:
    def __init__(self, players):
        """Initializes the player controller with a list of players.

        Args:
            players (list): List of existing Player instances.

        Attributes:
            player_model (Player): Reference to the Player model.
            view (PlayerView): View instance to handle player-related interactions.
            menu_view (MenuView): View instance for displaying menu options.
        """
        Player.all_players = players
        self.player_model = Player
        self.view = PlayerView()
        self.menu_view = MenuView()

    def player_management(self):
        """Main loop for player management menu.

        Handles the user's menu selections for:
            1. Adding a new player.
            2. Modifying existing player.
            3. Deleting a player.
            4. Displaying all players.
            5. Exiting to previous menu.
        """
        while True:
            choice = self.view.display_player_menu()
            if choice == "1":
                self.add_new_player()
            elif choice == "2":
                self.modify_player()
            elif choice == "3":
                self.delete_player()
            elif choice == "4":
                self.display_players(Player.all_players)
            elif choice == "5":
                break
            else:
                self.view.display_message("Invalid choice.")

    @staticmethod
    def player_id():
        """Prompts user for a player ID.

        Returns:
            int: ID of the selected player.
        """
        for player in Player.all_players:
            display_message(f"ID: {player.id} | Last name: {player.last_name} | First name: {player.first_name}")
        player_id = get_input("\nEnter the ID of the player: ")
        player_id = int(player_id)
        return player_id

    def add_new_player(self):
        """Creates a new player and saves it to the player list and database.

        Returns:
            Player: The newly created player instance.
        """
        last_name = get_input("Player's last name: ")
        first_name = get_input("Player's first name: ")
        while True:
            birthdate = get_input("Birthdate (YYYY-MM-DD): ")
            if re.match(r"\d{4}-\d{2}-\d{2}", birthdate):
                try:
                    datetime.strptime(birthdate, "%Y-%m-%d")
                    break
                except ValueError:
                    display_message("Invalid date. This date does not exist.")

            display_message("Invalid date format. Use YYYY-MM-DD.")
        # national_chess_identifier = get_input("National chess identifier: ")
        while True:
            national_chess_identifier = get_input("National chess identifier: ").strip()
            if re.match(r"^[A-Z]{2}\d{5}$", national_chess_identifier):
                break  # Identifiant valide, on sort de la boucle
            else:
                display_message(
                    "Invalid identifier. Expected format: two letters followed by five digits (e.g. AB12345)."
                )

        new_player = Player(last_name, first_name, birthdate, national_chess_identifier, score=0)
        Player.save_data_players()
        return new_player

    def modify_player(self):
        """Modifies an existing player's information.

        Prompts for player ID and allows editing of:
            - Last name
            - First name
            - Birthdate (validated)
            - National chess identifier (validated)
        Keeps old values if input is left blank.
        """
        player_id = self.player_id()

        # Find the player to modify
        player_to_modify = next((p for p in Player.all_players if p.id == player_id), None)
        if not player_to_modify:
            display_message("Player not found.")
            return

        # Display current information
        display_message(
            f"Modifying player:\n\tLast name: {player_to_modify.last_name}\n\t"
            f"First name: {player_to_modify.first_name}\n\t"
            f"Birthdate: {player_to_modify.birthdate}\n\t"
            f"National chess identifier: {player_to_modify.national_chess_identifier}\n"
        )
        display_message("Leave blank to keep the current value.\n")

        # Request new information
        new_last_name = get_input(f"New last name ({player_to_modify.last_name}): ").strip()
        new_first_name = get_input(f"New first name ({player_to_modify.first_name}): ").strip()
        new_birthdate = get_input(f"New birthdate ({player_to_modify.birthdate}): ").strip()
        if new_birthdate:
            if re.match(r"\d{4}-\d{2}-\d{2}", new_birthdate):
                try:
                    datetime.strptime(new_birthdate, "%Y-%m-%d")
                    player_to_modify.birthdate = new_birthdate
                except ValueError:
                    display_message("Invalid date. This date does not exist.")
            else:
                display_message("Invalid date format. Use YYYY-MM-DD.")

        new_identifier = get_input(
            f"New national chess identifier ({player_to_modify.national_chess_identifier}): "
        ).strip()
        if new_identifier:
            if re.match(r"^[A-Z]{2}\d{5}$", new_identifier):
                player_to_modify.national_chess_identifier = new_identifier
            else:
                display_message(
                    "Invalid identifier. Expected format: two letters followed by five digits (e.g. AB12345)."
                )

        # Update information if a new value is provided
        if new_last_name:
            player_to_modify.last_name = new_last_name
        if new_first_name:
            player_to_modify.first_name = new_first_name
        if new_birthdate:
            player_to_modify.birthdate = new_birthdate
        if new_identifier:
            player_to_modify.national_chess_identifier = new_identifier

        # Save modifications
        Player.save_data_players()
        display_message("\nPlayer successfully updated.")

    def delete_player(self):
        """Deletes a player from the database after confirmation.

        Asks for the player's ID and a confirmation from the user before deletion.
        """
        player_id = self.player_id()

        # Check if the player exists
        player_to_delete = next((p for p in Player.all_players if p.id == player_id), None)

        if not player_to_delete:
            display_message("\nPlayer not found.")
            return

        # Request confirmation
        confirmation = (
            get_input(
                f"\nAre you sure you want to delete {player_to_delete.last_name} {player_to_delete.first_name}?"
                f"(y/n): "
            )
            .strip()
            .lower()
        )

        if confirmation == "y":
            for i, p in enumerate(Player.all_players):
                if p.id == player_id:
                    del Player.all_players[i]
            Player.save_data_players()
            display_message("\nPlayer successfully deleted.")
        else:
            display_message("\nDeletion cancelled.")

    @staticmethod
    def sort_players_by_score(players):
        """Sorts the players by their score in descending order.

        Args:
            players (list): List of Player instances.

        Returns:
            list: Sorted list of players by score (highest to lowest).
        """
        sorted_players_by_score = sorted(players, key=lambda x: x.score, reverse=True)
        return sorted_players_by_score

    @staticmethod
    def sort_players_in_alphabetical_order(players):
        """Sorts players alphabetically by last name, then by first name.

        Args:
            players (list): List of Player instances.

        Returns:
            list: Alphabetically sorted list of players.
        """
        sorted_players_by_last_name = sorted(players, key=lambda x: (x.last_name.lower(), x.first_name.lower()))
        return sorted_players_by_last_name

    @staticmethod
    def display_players(players):
        """Displays a list of players with full information.

        Args:
            players (list): List of Player instances.
        """
        for player in players:
            display_message(
                f"\tID: {player.id}\n\t"
                f"Last name: {player.last_name}\n\t"
                f"First name: {player.first_name}\n\t"
                f"Birthdate: {player.birthdate}\n\t"
                f"National chess identifier: {player.national_chess_identifier}\n\t"
                f"Score: {player.score}\n\n"
            )
