import json
import os


class Tournament:
    counter = 0
    all_tournaments = []

    def __init__(self, name_tournament, location, start_date, end_date, number_rounds, description):
        """initalizing a tournament"""
        Tournament.counter += 1
        self.id = Tournament.counter

        self.name_tournament = name_tournament
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_rounds = number_rounds
        self.rounds = []
        self.description = description
        self.players = []

        # add tournaments to the list of tournament
        Tournament.all_tournaments.append(self)

    @staticmethod
    def save_data_tournament(filename="data_tournament.json"):
        """Save tournament data to a JSON file.

        Args:
            filename (str, optional): Name of the JSON file. Defaults to "data_tournament.json".

        Returns:
            bool:
                - `True` if the data was saved successfully.
                - `False` if the save operation failed.

        Raises:
            IOError: If an error occurs while writing to the file.ta.
        """
        # file path to data_tournament.json
        file_path = os.path.join(os.getcwd(), filename)

        try:
            # Write updated data to file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    [tournament.__dict__ for tournament in Tournament.all_tournaments], file, indent=4, sort_keys=True
                )
                return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    @staticmethod
    def load_from_file(filename="data_tournament.json"):
        """
        Loads tournaments from a JSON file and repopulates the tournaments list.

        Args:
            filename (str, optional): The file name to load tournaments from. Defaults to "data_tournament.json".
        """
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            Tournament.all_tournaments = []
            for tournament_data in data:
                tournament = Tournament(
                    tournament_data["name_tournament"],
                    tournament_data["location"],
                    tournament_data["start_date"],
                    tournament_data["end_date"],
                    tournament_data["number_rounds"],
                    tournament_data["description"],
                )
                tournament.players = tournament_data.get("rounds", [])
                tournament.players = tournament_data.get("players", [])
                tournament.id = tournament_data["id"]

    @staticmethod
    def get_tournament_data(tournament_id):
        """Searches for and returns tournament information based on registration ID
        Args:
           registration_ID (str): registration ID of searched tournament.

        Returns:
            dict or None:
                - A dictionary containing the tournament's information if found:
                    -"id" (int) :
                    - "name_tournament" (str): Name of the tournament.
                    - "location" (str): Tournament location.
                    - "start_date" (int): Tournament start date.
                    - "end_date" (int): Tournament end date.
                    - "number_rounds" (int): Number of rounds of the tournament.
                    - "description" (str): Tournament description.
                    - "list_rounds" (list): Tournament round lists.
                - `None` if no tournament matches the name provided.

        Raises:
            ValueError: If the name is empty or invalid."""
        for tournament in Tournament.all_tournaments:
            if tournament.id == tournament_id:
                return {
                    "name_tournament": tournament.name_tournament,
                    "location": tournament.location,
                    "start_date": tournament.start_date,
                    "end_date": tournament.end_date,
                    "number_rounds": tournament.number_rounds,
                    "rounds": [],
                    "description": tournament.description,
                    "players": [],
                }

        raise ValueError("No tournament found with this id")
