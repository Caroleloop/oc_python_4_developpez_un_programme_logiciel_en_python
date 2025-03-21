import re


from models.player_model import Player
from views.player_view import PlayerView
from views.menu_view import MenuView
from views.utile import get_input, display_message


class PlayerController:
    def __init__(self, players):
        """Controller to manage players."""
        self.players = players
        self.player_model = Player
        self.view = PlayerView()
        self.menu_view = MenuView()

    def player_management(self):
        while True:
            choice = self.view.display_player_menu()
            if choice == "1":
                self.add_new_player()
            elif choice == "2":
                self.modify_player(self.players)
            elif choice == "3":
                self.delete_player()
            elif choice == "4":
                self.display_players()
            elif choice == "5":
                break
            else:
                self.view.display_message("Invalid choice.")

    def add_new_player(self):
        """Create a player, save it in the database"""
        # Player.load_from_file()
        last_name = get_input("Player's last name: ")
        first_name = get_input("Player's first name: ")
        while True:
            birthdate = get_input("Birthdate (YYYY-MM-DD): ")
            if re.match(r"\d{4}-\d{2}-\d{2}", birthdate):
                break
            display_message("Invalid date format. Use YYYY-MM-DD.")
        national_chess_identifier = get_input("National chess identifier: ")

        new_player = Player(last_name, first_name, birthdate, national_chess_identifier, score=0)
        Player.save_data_players()
        return new_player

    def modify_player(self, players):
        """Allows the user to modify the information of an existing player by entering his ID.
        If the user leaves a field empty, the old value is retained."""
        player_id = get_input("Enter the ID of the player to modify: ")
        player_id = int(player_id)
        # players = Player.load_from_file()  # Load existing players

        # Find the player to modify
        player_to_modify = next((p for p in self.players if p.id == player_id), None)
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
        new_identifier = get_input(
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
        Player.save_data_players()
        display_message("\nPlayer successfully updated.")

    def delete_player(self):
        """Deletes a player."""
        player_id = get_input("\nEnter the ID of the player to be deleted: ")
        player_id = int(player_id)
        # players = Player.load_from_file()  # Load players before modification

        # Check if the player exists
        player_to_delete = next((p for p in self.players if p.id == player_id), None)

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
            # players = [p for p in players if p.id != player_id]  # Delete player
            for i, p in enumerate(self.players):
                if p.id == player_id:
                    del self.players[i]
            Player.save_data_players()
            display_message("\nPlayer successfully deleted.")
        else:
            display_message("\nDeletion cancelled.")

    def sort_players_by_score(self, players):
        """Loads players from file and sorts them by score"""
        # players_data = Player.load_from_file()
        sorted_players_by_score = sorted(players, key=lambda x: x.score, reverse=True)
        return sorted_players_by_score

    def sort_players_in_alphabetical_order(self):
        """Loads players from file and sorts them alphabetically (last name, first name)."""
        # players = Player.load_from_file()
        sorted_players_by_last_name = sorted(self.players, key=lambda x: (x.last_name.lower(), x.first_name.lower()))
        return sorted_players_by_last_name

    def display_players(self):
        """display players"""
        # players = Player.load_from_file()
        for player in self.players:
            display_message(
                f"\tID: {player.id}\n\t"
                f"Last name: {player.last_name}\n\t"
                f"First name: {player.first_name}\n\t"
                f"Birthdate: {player.birthdate}\n\t"
                f"National chess identifier: {player.national_chess_identifier}\n\n"
            )


if __name__ == "__main__":
    pass
