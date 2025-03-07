class PlayerView:
    def display_player_menu(self):
        print("\nPlayer management")
        print("1. Add a player")
        print("2. Modify a player")
        print("3. Delete a player")
        print("4. Display players")
        print("5. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4", "5"}:
                return choice
            print("\nInvalid choice, please enter a number between 1 and 5.")
