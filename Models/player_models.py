class Player:
    def __init__(self,
                 last_name,
                 first_name,
                 birthdate,
                 national_chess_identifier
                 ):
        '''Initializes player data'''
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.national_chess_identifier = national_chess_identifier

    def full_name_player(self):
        '''Defines the player's first and last name as a
        representation of the player object'''
        return self.first_name + " " + self.last_name

    def save_data_player(self):
        '''saves player data in JSON file'''
        pass

    def get_player_data(self):
        '''recover player data'''
        pass

    def add_data_new_player(self):
        '''add a new player data'''
        pass
