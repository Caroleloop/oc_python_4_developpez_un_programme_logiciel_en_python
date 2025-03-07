class TournamentView:
    def display_tournament_menu(self):
        print("\nTournament management")
        print("1. Create a tournament")
        print("2. Starting / Resuming a tournament")
        print("3. Modifying a tournament")
        print("4. Delete a tournament")
        print("5. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4", "5"}:
                return choice
            print("\nInvalid choice, please enter a number between 1 and 5.")
