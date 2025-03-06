from views.report_view import ReportView


class ReportController:
    def __init__(self):
        self.view = ReportView()

    def display_reports(self):
        while True:
            choice = self.view.display_report_menu()
            if choice == "1":
                self.list_players()
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

    def list_players(self):
        print("Displaying list of players... (to be implemented)")

    def list_tournaments(self):
        print("Displaying list of tournaments... (to be implemented)")

    def tournament_details(self):
        print("Displaying tournament details... (to be implemented)")

    def list_tournament_players(self):
        print("Displaying tournament players... (to be implemented)")

    def list_rounds_and_matches(self):
        print("Displaying tournament rounds and matches... (to be implemented)")
