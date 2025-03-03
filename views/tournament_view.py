class TournamentView:
    def display_tournament_menu(self):
        print("\nTournament management")
        print("1. Tournaments list")
        print("2. Create a tournament")
        print("3. Starting / Resuming a tournament")
        print("4. Modifying a tournament")
        print("5. Delete a tournament")
        print("6. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4", "5", "6"}:
                return choice
            print("Invalid choice, please enter a number between 1 and 6.")
