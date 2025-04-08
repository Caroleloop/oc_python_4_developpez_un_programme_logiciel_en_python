class TournamentView:
    def display_tournament_menu(self):
        """
         Displays the main menu for tournament management and handles user selection of an action.

        Available options:
        1. Create a tournament
        2. Start / Resume a tournament
        3. Modify a tournament
        4. Delete a tournament
        5. Display a tournament
        6. Return to the main menu

        Returns:
            str: The user's selection as a string (e.g., "1", "2", etc.), or the return value of submenus.
        """
        print("\nTournament management")
        print("1. Create a tournament")
        print("2. Starting / Resuming a tournament")
        print("3. Modifying a tournament")
        print("4. Delete a tournament")
        print("5. Display tournament")
        print("6. Return to main menu")

        while True:
            choice = input("Your choice: ")
            if choice in {"3", "4", "5", "6"}:
                return choice
            elif choice == "1":
                return self.display_create_a_tournament()
            elif choice == "2":
                return self.display_starting_resuming()

            print("\nInvalid choice, please enter a number between 1 and 6.")

    def display_create_a_tournament(self):
        """
         Displays the sub-menu for creating a tournament and handles user selection of an action.

        Available options:
        1. Tournament information (name, location, etc.)
        2. Add players
        3. Delete a player
        4. Return to the previous menu

        Returns:
            str: The user's selection as a string (e.g., "1-1", "1-2" for sub-options).
            str: The return value of the main menu if the user selects to go back.
        """
        print("\nCreate a tournament")
        print("1. Tournament information (name, location, ...)")
        print("2. Add players")
        print("3. Delete player")
        print("4. Return to previous menu")

        while True:
            sub_choice = input("Your choice: ")
            if sub_choice in {"1", "2", "3"}:
                return f"1-{sub_choice}"
            elif sub_choice == "4":
                return self.display_tournament_menu()
            print("\nInvalid choice, please enter a number between 1 and 4.")

    def display_starting_resuming(self):
        """
        Displays the sub-menu for starting or resuming a tournament and handles user selection of an action.

        Available options:
        1. Create Round 1
        2. Update scores
        3. Create another round
        4. Return to the main menu

        Returns:
            str: The user's selection as a string (e.g., "2-1", "2-2" for sub-options).
            str: The return value of the main menu if the user selects to go back.
        """
        print("\nStarting / Resuming a tournament")
        print("1. Create Round 1")
        print("2. Score update")
        print("3. Create another round")
        print("4. Revenir au menu principal ")

        while True:
            sub_choice = input("Your choice: ")
            if sub_choice in {"1", "2", "3"}:
                return f"2-{sub_choice}"
            elif sub_choice == "4":
                return self.display_tournament_menu()
            print("\nInvalid choice, please enter a number between 1 and 4.")
