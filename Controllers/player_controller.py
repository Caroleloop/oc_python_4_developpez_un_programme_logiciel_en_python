import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.player_model import Player
from views.player_view import PlayerView
from views.menu_view import MenuView


class PlayerController:
    def __init__(self):
        """Controller to manage players."""
        self.player_model = Player()
        self.view = PlayerView()
        self.menu_view = MenuView()

    def player_management(self):
        while True:
            choice = self.view.display_player_menu()
            if choice == "1":
                self.add_new_player()
            elif choice == "2":
                self.modify_player()
            elif choice == "3":
                self.delete_player()
            elif choice == "4":
                break
            else:
                self.view.display_message("Invalid choice.")

    def add_new_player(self):
        """Create a player, save it in the database"""
        last_name = self.menu_view.get_input("Player's last name: ")
        first_name = self.menu_view.get_input("Player's first name: ")
        while True:
            birthdate = self.menu_view.get_input("Birthdate (YYYY-MM-DD): ")
            if re.match(r"\d{4}-\d{2}-\d{2}", birthdate):
                break
            self.menu_view.display_message("Invalid date format. Use YYYY-MM-DD.")
        national_chess_identifier = self.view.get_input("National chess identifier: ")

        new_player = Player(last_name, first_name, birthdate, national_chess_identifier, score=0)
        new_player.save_data_players()
        return new_player

    def modify_player(self):
        """Allows the user to modify the information of an existing player by entering his ID.
        If the user leaves a field empty, the old value is retained."""
        player_id = self.menu_view.get_input("Enter the ID of the player to modify: ")
        players = self.load_player_data()  # Load existing players

        # Find the player to modify
        player_to_modify = next((p for p in players if p["id"] == player_id), None)

        if not player_to_modify:
            self.menu_view.display_message("Player not found.")
            return

        # Display current information
        self.menu_view.display_message(
            f"Modifying player: {player_to_modify['last_name']} {player_to_modify['first_name']} "
            f"{player_to_modify['birthdate']} {player_to_modify['national_chess_identifier']}"
        )
        self.menu_view.display_message("Leave blank to keep the current value.")

        # Request new information
        new_last_name = self.menu_view.get_input(f"New last name ({player_to_modify.last_name}): ").strip()
        new_first_name = self.menu_view.get_input(f"New first name ({player_to_modify.first_name}): ").strip()
        new_birthdate = self.menu_view.get_input(f"New birthdate ({player_to_modify.birthdate}): ").strip()
        new_identifier = self.menu_view.get_input(
            f"New national chess identifier ({player_to_modify.national_chess_identifier}): "
        ).strip()

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
        self.player_model.save_players(players)
        self.menu_view.display_message("Player successfully updated.")

    def delete_player(self):
        """Deletes a player."""
        player_id = self.menu_view.get_input("Enter the ID of the player to be deleted: ")
        players = Player.load_player_data()  # Load players before modification

        # Check if the player exists
        player_to_delete = next((p for p in players if p["id"] == player_id), None)

        if not player_to_delete:
            self.menu_view.display_message("Player not found.")
            return

        # Request confirmation
        confirmation = (
            self.menu_view.get_input(
                f"Are you sure you want to delete {player_to_delete.last_name} {player_to_delete.first_name}? (y/n): "
            )
            .strip()
            .lower()
        )

        if confirmation == "y":
            players = [p for p in players if p["id"] != player_id]  # Delete player
            Player.save_players(players)  # Save new list
            self.menu_view.display_message("Player successfully deleted.")
        else:
            self.menu_view.display_message("Deletion cancelled.")

    def sort_players_by_score(self):
        """Loads players from file and sorts them by score"""
        players_data = Player.load_player_data()
        sorted_players_by_score = sorted(players_data, key=lambda x: x.score, reverse=True)
        return sorted_players_by_score

    def sort_players_in_alphabetical_order(self):
        """Loads players from file and sorts them alphabetically (last name, first name)."""
        players = Player.load_player_data()
        sorted_players_by_last_name = sorted(players, key=lambda x: (x.last_name.lower(), x.first_name.lower()))
        return sorted_players_by_last_name


if __name__ == "__main__":
    pass
