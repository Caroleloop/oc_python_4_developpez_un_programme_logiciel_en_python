import json
import os
from utile.utile import get_input, display_message


class Tournament:
    counter = 0
    all_tournaments = []

    def __init__(
        self, name_tournament, location, start_date, end_date=(""), number_rounds=4, description="", current_round=0
    ):
        """
        Initializes a tournament with the given attributes.

        Args:
            name_tournament (str): The name of the tournament.
            location (str): The location where the tournament is held.
            start_date (str): The start date of the tournament (format: YYYY-MM-DD).
            end_date (str, optional): The end date of the tournament (format: YYYY-MM-DD). Defaults to an empty string.
            number_rounds (int, optional): The number of rounds in the tournament. Defaults to 4.
            description (str, optional): A description of the tournament. Defaults to an empty string.
            current_round (int, optional): The current round of the tournament. Defaults to 0.
        """
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
        """
        Saves tournament data to a JSON file.

        Args:
            filename (str, optional): The name of the file to save the data to. Defaults to "data_tournament.json".

        Returns:
            bool:
                - `True` if the data was saved successfully.
                - `False` if the save operation failed.

        Raises:
            IOError: If an error occurs while writing to the file.
        """
        # file path to data_tournament.json
        file_path = os.path.join(os.getcwd(), filename)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    [tournament.__dict__ for tournament in Tournament.all_tournaments], file, indent=4, sort_keys=True
                )

            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    @staticmethod
    def load_data_tournaments(filename="data_tournament.json"):
        """
        Loads tournaments from a JSON file and repopulates the list of tournaments.

        Args:
            filename (str, optional): The file name to load tournaments from. Defaults to "data_tournament.json".

        Returns:
            list: A list of all tournaments loaded from the file, or an empty list if loading failed.
        """
        Tournament.all_tournaments.clear()
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))
        if not os.path.exists(filename):
            print("No data file found. Returning an empty list.")
            return []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

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
            Tournament.counter = max((t.id for t in Tournament.all_tournaments), default=0)

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading player data: {e}")
            return []
        return Tournament.all_tournaments

    @staticmethod
    def get_tournament_data(tournament_id):
        """
        Retrieves the data of a specific tournament by its ID.

        Args:
            tournament_id (int): The ID of the tournament to search for.

        Returns:
            dict: A dictionary containing the tournament's information if found.

        Raises:
            ValueError: If no tournament is found with the provided ID.
        """
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

    @staticmethod
    def tournament_id():
        """
        Prompts the user to select a tournament by its ID.

        Returns:
            Tournament or None: The selected tournament, or `None` if no tournament is selected.
        """
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
