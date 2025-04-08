class PlayerView:
    def display_player_menu(self):
        """
        Displays the player management menu and handles user selection of an action.

        Available options:
        1. Add a player
        2. Modify a player
        3. Delete a player
        4. Display players
        5. Return to the main menu

        Returns:
            str: The user's choice as a string (e.g., "1", "2", etc.).
        """
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
