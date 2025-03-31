class TournamentView:
    def display_tournament_menu(self):
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
        print("\nCreate a tournament")
        print("1. Tournament information (name, location, ...)")
        print("2. Add players")
        print("3. Create Round 1")
        print("4. Return to previous menu")

        while True:
            sub_choice = input("Your choice: ")
            if sub_choice in {"1", "2", "3"}:
                return f"1-{sub_choice}"
            elif sub_choice == "4":
                return self.display_tournament_menu()
            print("\nInvalid choice, please enter a number between 1 and 4.")

    def display_starting_resuming(self):
        print("\nStarting / Resuming a tournament")
        print("1. Start round")
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
