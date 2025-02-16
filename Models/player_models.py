import json
import os


class Player:
    def __init__(self, last_name, first_name, birthdate, national_chess_identifier, score: int = 0):
        """Initializes player data"""
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_chess_identifier = national_chess_identifier
        self.score = score

    def full_name_player(self):
        """Returns the player's full name as 'Last Name First Name'.

        Returns:
            str: Player's full name.
        """
        return self.first_name + " " + self.last_name

    def data_player(self):
        """Returns player information in dictionary form.

        Returns:
            dict: Contains the following information:
            - "last_name" (str): Player's name.
            - “first name” (str): Player's first name.
            - "birthdate" (str): Player's birthdate.
            - “national_chess_identifier” (int): Player's national_chess_identifier.
        """
        data_player = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "national_chess_identifier": self.national_chess_identifier,
        }
        return data_player

    def add_a_new_player(self, last_name, first_name, birthdate, national_chess_identifier):
        """Adds a new player to the list of participants.

        Agrs :
            last_name (str): Player's last name.
            first name (str): Player's first name.
            birthdate (str): Player's birthdate (format 'YYYY-MM-DD').
            national_chess_identifier (int): Player's national_chess_identifier

        Retunrs :
            Player: An instance of the player added.
        """
        pass

    def save_data_player(self):
        """Saves player data in a json file.

        Returns:
            bool:
                - `True` if the data has been saved successfully.
                - False` if backup failed.

        Raises:
            IOError: If an error occurs while writing data.
        """
        # file path to data_player.json
        file_path = os.path.join(os.getcwd(), "data_player.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    players_data = json.load(file)  # Load existing data
                except json.JSONDecodeError:
                    players_data = {}  # If the file is empty or corrupted
        else:
            players_data = {}

        # Find the next unique identifier (player_1, player_2, ...)
        next_id = "player_{}".format(len(players_data) + 1)

        # Add the player under his unique identifier
        players_data[next_id] = self.data_player()

        # Write updated data to file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(players_data, file, indent=4, ensure_ascii=False)

    def get_player_data(self, last_name):
        """Searches for and returns player information based on registration ID
        Args:
           registration_ID (str): registration ID of searched player.

        Returns:
            dict or None:
                - A dictionary containing the player's information if found:
                    - “name” (str) : Name of the player.
                    - “prenom” (str) : Player's first name.
                    - “date_naissance” (str): Player's date of birth.
                    - “id_echecs” (int): Player's unique identifier.
                    - “score” (int): Player's current score.
                - `None` if no player matches the name provided.

        Raises:
            ValueError: If the name is empty or invalid."""
        """file path to data_player.json"""
        file_path = os.path.join(os.getcwd(), "data_player.json")

        # Load JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Checking and displaying information
        for key, player_info in data.items():
            if player_info.get("last_name") == last_name:
                return player_info

        return "No players found with this last name (Please capitalize the last name)"


if __name__ == "__main__":
    player1 = Player("Dupond", "Georges", "1974-08-14", "AA12345")
    name = player1.full_name_player()
    data = player1.save_data_player()
    show_player = player1.get_player_data("Dupond")
    print(name)
    print(show_player)
