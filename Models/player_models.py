import json
import os


class Player:
    def __init__(self,
                 last_name,
                 first_name,
                 birthdate,
                 national_chess_identifier):
        '''Initializes player data'''
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_chess_identifier = national_chess_identifier

    def full_name_player(self):
        '''Defines the player's first and last name as a
        representation of the player object'''
        return self.first_name + " " + self.last_name

    def data_player(self):
        '''Creation of a Python dictionary containing player data'''
        data = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
            "national_chess_identifier": self.national_chess_identifier
        }
        return data

    def save_data_player(self):
        '''Saves player data in JSON file'''
        file_path = os.path.join(os.getcwd(), 'data_player.json')

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    players_data = json.load(file)  # Load existing data
                except json.JSONDecodeError:
                    players_data = {}  # If the file is empty or corrupted
        else:
            players_data = {}

        # Find the next unique identifier (player_1, player_2, ...)
        next_id = "player_{}".format(len(players_data) + 1)

        # Add the player under his unique identifier
        players_data[next_id] = self.data_player()

        # Write updated data to file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(players_data, file, indent=4, ensure_ascii=False)

    def get_player_data(self):
        '''Recover player data'''
        pass

    def add_data_new_player(self):
        '''Add a new player data'''
        pass


if __name__ == "__main__":
    player1 = Player("Truc", "Matine", "1990-12-01", "BC12345")
    name = player1.full_name_player()
    data = player1.save_data_player()
    print(name)
