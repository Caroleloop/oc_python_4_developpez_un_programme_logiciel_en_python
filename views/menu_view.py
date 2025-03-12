class MenuView:
    def display_main_menu():
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
