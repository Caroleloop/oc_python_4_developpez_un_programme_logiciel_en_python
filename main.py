from views.menu_view import MenuView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from models.player_model import Player
from models.tournament_model import Tournament


class TournoiApp:
    """
    Represents the main application for managing the chess tournament.

    This class handles the initialization of views, controllers, and data related to players and tournaments.
    It manages the application's main logic, such as displaying menus and processing user inputs for player,
    tournament, and report management.
    """

    def __init__(self):
        """
        Initializes the application by creating the necessary views, controllers, and data.

        - Creates a menu view (MenuView).
        - Loads player and tournament data from predefined templates.
        - Initializes controllers for managing players, tournaments, and reports.
        """
        self.menu_view = MenuView
        self.players = Player.load_data_players()
        self.tournaments = Tournament.load_data_tournaments()
        self.player_controller = PlayerController(Player.all_players)
        self.tournament_controller = TournamentController(Tournament.all_tournaments, Player.all_players)
        self.report_controller = ReportController(Tournament.all_tournaments)

    def run(self):
        """
        Starts the main loop of the application, displaying the main menu and processing user choices.

        Based on the user's selection, the appropriate controller is invoked for managing players, tournaments,
        or reports.
        The application terminates when the user chooses the "Quit" option.
        """
        while True:
            choix = MenuView.display_main_menu()
            if choix == "1":
                self.player_controller.player_management()
            elif choix == "2":
                self.tournament_controller.tournament_management()
            elif choix == "3":
                self.report_controller.display_reports()
            elif choix == "4":
                print("Goodbye!\n")
                break
            else:
                print("\nInvalid choice, please try again.")


if __name__ == "__main__":
    """
    Initializes and runs the TournoiApp application if this script is executed directly.
    """
    app = TournoiApp()
    app.run()
