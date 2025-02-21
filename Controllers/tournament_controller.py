class TournamentController:
    def update_of_participating_players(self, player):
        """
        Adds or updates a player in the tournament participants list.

        Args:
            player (Player): An instance of the Player class representing the player to be added.
        """
        pass

    def mix_player(self):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
        """
        pass

    def create_pairs_round_1(self):
        """
        Generates player pairs for the first round according to random order.

        Returns:
            list[tuple]: A list of tuples containing the player pairs.
        """
        pass

    def creation_pairs_other_rounds(self):
        """
        Generates player pairs for subsequent rounds based on scores.

        Returns:
            list[tuple]: A list of tuples representing player pairs.
        """
        pass

    def draw_white_black(self, player1, player2):
        """
        Randomly determines which player will play with the white or black pieces.

        Args:
            player1 (Player): First player of the pair.
            player2 (Player): Second player of the pair.

        Returns:
            tuple: (Player, Player) where the first element is the player with the white pieces.
        """
        pass

    def update_score(self, player, points):
        """
        Updates the player's score after a match.
        Gives the results of the match: the winner receives 1 point, the loser receives 0 points,
        in the event of a draw each receives 0.5 points.

        Args:
            player (Player): The player whose score is to be updated.
            points (float): Number of points obtained (1 for a win, 0.5 for a draw, 0 for a loss).

        Results: “1” if player1 wins,
                 “2” if player2 wins,
                 “draw” for a tie
        """
        pass
