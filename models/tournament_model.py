import json
import os


class Tournament:
    counter = 0
    all_tournaments = []

    def __init__(
        self, name_tournament, location, start_date, end_date=(""), number_rounds=4, description="", current_round=1
    ):
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
        self.current_round = current_round
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
            # tournaments_data = [tournament.__dict__ for tournament in Tournament.all_tournaments]
            # Write updated data to file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    [tournament.__dict__ for tournament in Tournament.all_tournaments], file, indent=4, sort_keys=True
                )

            # with open(file_path, "w", encoding="utf-8") as file:
            #     json.dump(tournaments_data, file, indent=4, sort_keys=True)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    @staticmethod
    def load_data_tournaments(filename="data_tournament.json"):
        """
        Loads tournaments from a JSON file and repopulates the tournaments list.

        Args:
            filename (str, optional): The file name to load tournaments from. Defaults to "data_tournament.json".
        """
        Tournament.all_tournaments.clear()
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))
        if not os.path.exists(filename):
            print("No data file found. Returning an empty list.")
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Tournament.all_tournaments = []

            for tournament_data in data:
                tournament = Tournament(
                    name_tournament=tournament_data["name_tournament"],
                    location=tournament_data["location"],
                    start_date=tournament_data["start_date"],
                    end_date=tournament_data.get("end_date", ""),
                    number_rounds=tournament_data["number_rounds"],
                    description=tournament_data["description"],
                    current_round=tournament_data.get("current_round", 0),
                )
                tournament.end_date = tournament_data.get("end_date", "0000-00-00")
                tournament.rounds = tournament_data.get("rounds", [])
                tournament.players = tournament_data.get("players", [])
                tournament.id = tournament_data["id"]

            # return Tournament.all_tournaments
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading player data: {e}")
            return []
        return Tournament.all_tournaments

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
                    "id": tournament.id,
                    "name_tournament": tournament.name_tournament,
                    "location": tournament.location,
                    "start_date": tournament.start_date,
                    "end_date": tournament.end_date,
                    "number_rounds": tournament.number_rounds,
                    "rounds": tournament.rounds,
                    "description": tournament.description,
                    "players": tournament.players,
                }

        raise ValueError("No tournament found with this id")
