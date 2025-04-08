class MenuView:
    def display_main_menu():
        """
        Displays the main menu and allows the user to select one of the available options.

        Available options:
        1. Player management
        2. Tournament management
        3. View reports
        4. Exit

        Returns:
            str: The user's choice as a string (e.g., "1", "2", etc.).
        """
        print("\nWelcome to the chess tournament program.")
        print("1. Player management")
        print("2. Tournaments management")
        print("3. View reports")
        print("4. Exit")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4"}:
                return choice
            print("Invalid choice, please enter a number between 1 and 4.")
