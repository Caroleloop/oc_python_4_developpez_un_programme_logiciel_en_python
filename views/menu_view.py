class MenuView:
    def display_main_menu(self):
        print("\nWelcome to the tournament!")
        print("1. Player management")
        print("2. tournaments management")
        print("3. View reports")
        print("4. Exit")

        while True:
            choice = input("Your choice: ")
            if choice in {"1", "2", "3", "4"}:
                return choice
            print("Invalid choice, please enter a number between 1 and 4.")

    def get_input(self, message):
        return input(message).strip()

    def display_message(self, message):
        print(message)
