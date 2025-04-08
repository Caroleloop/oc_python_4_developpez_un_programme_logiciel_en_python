class ReportView:
    def display_report_menu(self):
        """
        Displays the report menu and handles user selection for viewing different reports.

        Available options:
        1. List of players in alphabetical order
        2. List of tournaments
        3. Name and date of a specific tournament
        4. List of tournament players in alphabetical order
        5. List of tournament rounds and matches
        6. Return to the main menu

        Returns:
            str: The user's choice as a string (e.g., "1", "2", etc.).
        """
        print("\nView reports")
        print("1. List of players in alphabetical order")
        print("2. List of tournaments")
        print("3. Name and date of a given tournament")
        print("4. List of tournament players in alphabetical order")
        print("5. List of tournament rounds and matches")
        print("6. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4", "5", "6"}:
                return choice
            print("\nInvalid choice, please enter a number between 1 and 6.")
