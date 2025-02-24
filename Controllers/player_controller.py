import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.player_model import Player


class PlayerController:
    def __init__(self):
        """Controller to manage players."""
        self.player_model = Player

    def add_new_player(self, last_name, first_name, birthdate, national_chess_identifier, score: int = 0):
        """Crée un joueur, le sauvegarde dans la base de données"""
        new_player = Player(last_name, first_name, birthdate, national_chess_identifier, score=0)
        new_player.save_data_players()
        return new_player

    def sort_players_by_score(self):
        """Charge les joueurs depuis le fichier et les trie par score"""
        players_data = self.player_model.load_from_file(filename="data_players.json")

        if not players_data:  # Vérifiez si players_data est vide
            print("Aucun joueur chargé.")
            return []

        sorted_players = sorted(players_data, key=lambda x: x.score, reverse=True)
        return sorted_players


if __name__ == "__main__":
    controller = PlayerController()
    sorted_players = controller.sort_players_by_score()

    for player in sorted_players:
        print(f"{player.last_name} {player.first_name} - Score: {player.score}")
