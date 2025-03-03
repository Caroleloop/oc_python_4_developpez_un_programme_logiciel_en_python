import random
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self):
        self.view = TournamentView()

    def tournament_management(self):
        while True:
            choix = self.view.display_tournament_menu()
            if choix == "1":
                self.tournament_list()
            elif choix == "2":
                self.create_tournament()
            elif choix == "3":
                self.manage_tournament()
            elif choix == "4":
                self.modify_tournament()
            elif choix == "5":
                self.delete_tournament()
            elif choix == "6":
                break
            else:
                print("Choix invalide.")

    def tournament_list(self):
        print("Affichage de la liste des tournois... (à implémenter)")

    def create_tournament(self):
        print("Création d’un tournoi... (à implémenter)")

    def manage_tournament(self):
        print("Gestion du tournoi... (à implémenter)")

    def modify_tournament(self):
        print("Modification d’un tournoi... (à implémenter)")

    def delete_tournament(self):
        print("Suppression d’un tournoi... (à implémenter)")

    def update_of_participating_players(self, player):
        """
        Adds or updates a player in the tournament participants list.

        Args:
            player (Player): An instance of the Player class representing the player to be added.
        """
        pass

    def shuffle_player(self):
        """
        Randomly shuffles the list of players to avoid any bias in pair formation.
        """
        if len(self.players_list) > 1:
            random.shuffle(self.players_list)
        return self.players_list

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
