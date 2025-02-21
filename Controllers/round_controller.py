class RoundController:
    def create_round(self, name_round, start_time):
        """
        Creates a new round and initializes its matches.

        Args:
            name (str): round name (e.g. "Round 1”).
            start_date_time (str): Round start date and time (format 'YYYY-MM-DD HH:MM').
        """
        pass

    def create_liste_match(self, pairs):
        """
        Generates the match list for a given round.

        Args:
            pairs (list[tuple]): List of player pairs.

        Returns:
            list[Match]: List of Match objects corresponding to matches in the round.
        """
        pass

    def sort_players_score(self):
        pass
