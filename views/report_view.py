class ReportView:
    def display_report_menu(self):
        print("\nView reports")
        print("1. List of players in alphabetical order")
        print("2. List of tournaments")
        print("3. Name and date of a given tournament")
        print("4. List of tournament players in alphabetical order")
        print("5.List of tournament rounds and matches")
        print("6. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4", "5", "6"}:
                return choice
            print("Invalid choice, please enter a number between 1 and 6.")
