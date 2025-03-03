from views.menu_view import MenuView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


class TournoiApp:
    def __init__(self):
        self.menu_view = MenuView()
        self.joueur_controller = PlayerController()
        self.tournoi_controller = TournamentController()
        self.rapport_controller = ReportController()

    def run(self):
        while True:
            choix = self.menu_view.display_main_menu()
            if choix == "1":
                self.joueur_controller.players_management()
            elif choix == "2":
                self.tournoi_controller.tournament_management()
            elif choix == "3":
                self.rapport_controller.display_reports()
            elif choix == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    app = TournoiApp()
    app.run()
