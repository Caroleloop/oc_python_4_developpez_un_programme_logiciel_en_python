from views.report_view import ReportView
from controllers.player_controller import PlayerController
from models.player_model import Player
from controllers.tournament_controller import TournamentController
from views.utile import display_message
from models.tournament_model import Tournament


class ReportController:
    def __init__(self, tournaments):
        """Initializes the ReportController.

        Args:
            tournaments (list): List of tournaments to be loaded into the application.

        Attributes:
            view (ReportView): View handler for displaying reports.
            player_controller (PlayerController): Controller for player-related operations.
            tournament_controller (TournamentController): Controller for tournament-related operations.
            player_model (Player): Player model class.
        """
        self.view = ReportView()
        self.player_controller = PlayerController
        self.tournament_controller = TournamentController
        self.player_model = Player
        Tournament.all_tournaments = tournaments

    def display_reports(self):
        """Main loop for the report menu.
        Handles user input and triggers corresponding report display methods.
        """
        while True:
            choice = self.view.display_report_menu()
            if choice == "1":
                self.list_players_in_alphabetical_order()
            elif choice == "2":
                self.list_tournaments()
            elif choice == "3":
                self.tournament_details()
            elif choice == "4":
                self.list_tournament_players()
            elif choice == "5":
                self.list_rounds_and_matches()
            elif choice == "6":
                break
            else:
                print("Invalid choice, please try again.")

    def list_players_in_alphabetical_order(self):
        """Displays the list of all players sorted alphabetically by last name."""
        players = Player.all_players
        sorted_players_by_last_name = PlayerController.sort_players_in_alphabetical_order(players)
        PlayerController.display_players(sorted_players_by_last_name)

    def list_tournaments(self):
        """Displays a list of all tournaments with key details."""
        for tournament in Tournament.all_tournaments:
            display_message(
                f"\n\n\tID: {tournament.id}\n\t"
                f"Tournament name: {tournament.name_tournament}\n\t"
                f"Tournament location: {tournament.location}\n\t"
                f"Start date: {tournament.start_date}\n\t"
                f"Number of tournament rounds: {tournament.number_rounds}\n\t"
                f"Tournament description: {tournament.description}\n\t"
                f"End date: {tournament.end_date}\n\t"
            )

    def tournament_details(self):
        """Displays basic details (name, start/end dates) of a selected tournament."""
        tournament_id = Tournament.tournament_id()

        display_message(
            f"\n\n\tID: {tournament_id.id}\n\t"
            f"Tournament name: {tournament_id.name_tournament}\n\t"
            f"Start date: {tournament_id.start_date}\n\t"
            f"End date: {tournament_id.end_date}\n\t"
        )

    def list_tournament_players(self):
        """Displays players from a selected tournament in alphabetical order."""
        tournament_id = Tournament.tournament_id()
        display_message("\tPlayers: ")
        players = []
        for player_id in tournament_id.players:
            player = next((p for p in Player.all_players if p.id == player_id), None)
            players.append(player)

        sorted_tournament_players_by_last_name = PlayerController.sort_players_in_alphabetical_order(players)
        PlayerController.display_players(sorted_tournament_players_by_last_name)

    def list_rounds_and_matches(self):
        """Displays all rounds and associated matches for a selected tournament.

        Shows each round’s start and end time, followed by match details including:
            - player names
            - player IDs
            - assigned colors
            - scores
        """
        tournament_id = Tournament.tournament_id()
        for round_ in tournament_id.rounds:
            display_message(
                f"\t\t{round_['name']}:\n "
                f"\t\tstart round: {round_['start_date_round']}\n"
                f"\t\tend round: {round_['end_date_round']}"
            )
            display_message("\t\t Matches: ")
            for match in round_["matches"]:
                player1, player2, color = match
                player1_info = next((p for p in Player.all_players if p.id == player1[0]), None)
                player2_info = next((p for p in Player.all_players if p.id == player2[0]), None)

                color_info = color[0]
                color1 = "white" if color_info.get(str(player1_info.id)) == "white" else "black"
                color2 = "white" if color_info.get(str(player2_info.id)) == "white" else "black"

                if player1_info and player2_info:

                    display_message(
                        f"\t\t\t{player1_info.first_name} {player1_info.last_name} "
                        f"(ID: {player1_info.id}), color: {color1},   score: {player1[1]}  vs "
                        f"{player2_info.first_name} {player2_info.last_name} "
                        f"(ID: {player2_info.id}), color: {color2},  score: {player2[1]} "
                    )
                else:
                    display_message("\t\t\t- Invalid player data.")
