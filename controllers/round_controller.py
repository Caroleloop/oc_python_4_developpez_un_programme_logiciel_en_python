class RoundController:
    def create_round(self, name_round, start_time, end_time):
        """
        Creates a new round and initializes its matches.

        Args:
            name (str): round name (e.g. "Round 1”).
            start_date_time (str): Round start date and time (format 'YYYY-MM-DD HH:MM').
        """
        round_data = {"name": name_round, "start_time": start_time, "end_time": end_time, "matches": []}
        return round_data

    def sort_players_score(self):
        pass

    def initialize_current_round(self, tournament):
        """Initialise l'attribut current_round si inexistant."""
        if not hasattr(tournament, "current_round"):
            tournament.current_round = 1
