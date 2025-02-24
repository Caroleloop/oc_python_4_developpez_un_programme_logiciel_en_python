import json
import os


class Player:
    counter = 0
    all_players = []

    def __init__(self, last_name, first_name, birthdate, national_chess_identifier, score: int = 0):
        """Initializes player data"""
        Player.counter += 1
        self.id = Player.counter

        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_chess_identifier = national_chess_identifier
        self.score = score

        # add player to the list of players
        Player.all_players.append(self)

    def __str__(self):
        """Returns the player's full name as 'Last Name First Name'.

        Returns:
            str: Player's full name.
        """
        return self.first_name + " " + self.last_name

    @staticmethod
    def save_data_players(filename="data_players.json"):
        """Save all player data to a JSON file.

        Args:
            filename (str, optional): Name of the JSON file. Defaults to "data_players.json".

        Returns:
            bool:
                - `True` if the data was saved successfully.
                - `False` if the save operation failed.

        Raises:
            IOError: If an error occurs while writing to the file.ta.
        """
        # file path to data_player.json
        file_path = os.path.join(os.getcwd(), filename)

        try:
            # Write updated data to file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([player.__dict__ for player in Player.all_players], file, indent=4, sort_keys=True)
                return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    @staticmethod
    def load_from_file(filename="data_players.json"):
        """
        Loads players from a JSON file and repopulates the player list.

        Args:
            filename (str, optional): The file name to load players from. Defaults to "data_players.json".
        """
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            Player.all_players = []
            for player_data in data:
                player = Player(
                    player_data["last_name"],
                    player_data["first_name"],
                    player_data["birthdate"],
                    player_data["national_chess_identifier"],
                    player_data["score"],
                )
                player.id = player_data["id"]

            return Player.all_players
        else:
            print(f"Le fichier {filename} n'existe pas.")
            return []

    @staticmethod
    def get_player_data(player_id):
        """Searches for and returns player information based on registration ID
        Args:
           registration_ID (str): registration ID of searched player.

        Returns:
            dict or None:
                - A dictionary containing the player's information if found:
                    -"id" (int) :
                    - “name” (str) : Name of the player.
                    - “prenom” (str) : Player's first name.
                    - “date_naissance” (str): Player's date of birth.
                    - “national_chess_identifier” (int): Player's unique identifier.
                    - “score” (int): Player's current score.
                - `None` if no player matches the name provided.

        Raises:
            ValueError: If the name is empty or invalid."""
        for player in Player.all_players:
            if player.id == player_id:
                return {
                    "id": player.id,
                    "last_name": player.last_name,
                    "first_name": player.first_name,
                    "birthdate": player.birthdate,
                    "national_chess_identifier": player.national_chess_identifier,
                    "score": player.score,
                }

        raise ValueError("No players found with this id")


if __name__ == "__main__":
    Player("Carlsen", "Magnus", "1990-11-30", "NOR12345")
    Player("Nakamura", "Hikaru", "1987-12-09", "USA67890")
    Player("Firouzja", "Alireza", "2003-06-18", "FRA54321")
    Player("Ding", "Liren", "1992-10-24", "CHN98765")
    Player("Gukesh", "Dommaraju", "2006-05-29", "IND24680")
    Player.save_data_players()
    Player.load_from_file("data_players.json")
    show_player = Player.get_player_data(2)
    print(str(show_player))
