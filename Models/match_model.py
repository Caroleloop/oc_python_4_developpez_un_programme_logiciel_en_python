class Match:
    def __init__(self, player_1, player_2):
        """Initializes a match between two players.

        Args:
            player1 (Player): First player of the match.
            player2 (Player): Second player in the match.

        Attributes:
            player1 (Player): Player playing with white pieces.
            player2 (Player): Player playing with black pieces.
            score_player1 (float): Player 1's score (initialized to 0).
            score_player2 (float): Player 2's score (initialized to 0).
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self.scores = {player_1: 0, player_2: 0}
