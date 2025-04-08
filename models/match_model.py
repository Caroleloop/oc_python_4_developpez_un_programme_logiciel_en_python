class Match:
    def __init__(self, player_1, player_2):
        """Initializes a match between two players.

        Args:
            player_1 (Player): First player of the match.
            player_2 (Player): Second player of the match.

        Attributes:
            player_1 (Player): Player playing with white pieces.
            player_2 (Player): Player playing with black pieces.
            scores (dict): Dictionary containing the players as keys and their scores (float) as values,
            initialized to 0.
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self.scores = {player_1: 0, player_2: 0}
        self.round

    @property
    def finished(self):
        """Checks if the match is finished.

        Returns:
            bool:
                - `True` if at least one of the players has a score greater than 0.
                - `False` if the match has not been played yet (both scores are 0).
        """
        sum_scores = 0
        for _, score in self.scores.items():
            sum_scores += score

        if sum_scores == 0:
            return False

        return True
