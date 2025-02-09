class Tournament:
    def __init__(self,
                 name_tournament,
                 location,
                 start_date,
                 end_date,
                 nomber_rounds,
                 description
                 ):
        '''initalizing a tournament'''
        self.name_tournament = name_tournament
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.nomber_rounds = nomber_rounds
        self.description = description

    def add_palyer(self):
        '''ajouer un joueur au tournois'''
        pass

    def generate_pairs_round_one(self):
        '''generates pairs for round 1'''
        pass

    def generate_pairs_other_rounds(self):
        '''generates pairs for other rounds'''
        pass

    def add_round(self):
        '''add a round to the tournament'''
        pass

    def update_scores(self):
        '''update scores'''
        pass
