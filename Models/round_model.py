class Round:
    def __init__(self, name_round):
        """initalizing a round"""
        self.name_round = name_round

    def creation_tour(self, name_round, start_time):
        """
        Creates a new round and initializes its matches.

        Args:
            name (str): round name (e.g. "Round 1”).
            start_date_time (str): Round start date and time (format 'YYYY-MM-DD HH:MM').
        """
        pass

    def creation_liste_match(self, pairs):
        """
        Generates the match list for a given round.

        Args:
            pairs (list[tuple]): List of player pairs.

        Returns:
            list[Match]: List of Match objects corresponding to matches in the round.
        """
        pass

    def start_round(self):
        """
        Marks the start of a round by recording the start time.
        """
        pass

    def end_round(self, date_time_end):
        """
        Marks the end of a tour by recording the end time.

        Args:
            end_round (str): Round end date and time (format 'YYYY-MM-DD HH:MM').
        """
        pass
