from views.menu_view import MenuView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController
from models.player_model import Player
from models.tournament_model import Tournament


class TournoiApp:
    def __init__(self):
        self.menu_view = MenuView
        self.report_controller = ReportController()

        self.players = Player.load_data_players()
        self.tournaments = Tournament.load_data_tournaments()
        self.player_controller = PlayerController(self.players)
        self.tournament_controller = TournamentController(self.tournaments, self.players)
        self.report_controller = ReportController()

    def run(self):
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
    app = TournoiApp()
    app.run()
