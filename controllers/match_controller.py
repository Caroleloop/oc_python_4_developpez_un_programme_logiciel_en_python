import os
import json


from models.match_model import Match
from views.utile import display_message


class MatchController:
    def __init__(self):
        """Controller to manage matches"""
        self.match_model = Match

    def create_match(self, player_1, player_2):
        """Create a new match instance and initialize scores."""
        self.match_model(player_1, player_2)
        display_message(f"Match créé entre {player_1} et {player_2}.")

    @staticmethod
    def match_result(player1, player2, result, match):
        """Gives the results of the match:
        the winner receives 1 point,
        the loser receives 0 points,
        in the event of a draw each receives 0.5 points.

        Results: “1” if player1 wins, “2” if player2 wins, “draw” for a tie
        """
        if result == "1":
            player1[1] += 1
        elif result == "2":
            player2[1] += 1
        elif result == "draw":
            player1[1] += 0.5
            player2[1] += 0.5
        else:
            raise ValueError("Invalid result: must be '1', '2' ou 'draw'")

        match[0] = player1
        match[1] = player2

    @staticmethod
    def save_scores_to_json(self, filename="data_tournament.json"):
        """Saves scores in a JSON file."""
        try:
            # Load existing scores if any
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as file:
                    players_data = json.load(file)
            else:
                display_message("File not found.")
                return

            # Update existing scores with new scores
            for player in players_data:
                full_name = f"{player['first_name']} {player['last_name']}"
                if full_name in self.scores:
                    player["score"] += self.scores[full_name]

            # Save updated scores
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(players_data, file, indent=4)
            display_message("Scores recorded with success!")
        except Exception as e:
            display_message(f"Error when recording scores : {e}")

    @staticmethod
    def update_player_score(player_id, score, filename="data_players.json"):
        """Updates a player's score in data_players.json"""
        if not os.path.exists(filename):
            display_message("File data_players.json not found.")
            return

        # Load player data
        with open(filename, "r", encoding="utf-8") as file:
            players_data = json.load(file)

        # Find the player and update his score
        for player in players_data:
            if player["id"] == player_id:
                player["score"] += score
                break
        else:
            print(f"Player with ID {player_id} not found.")
            return

        # Save changes
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(players_data, file, indent=4)

    def charger_matchs_joues(self):
        """Charge les matchs déjà joués depuis un fichier JSON."""
        try:
            with open(self.fichier_json, "r") as file:
                data = json.load(file)
                matchs_joues = set()
                for round in data.get("rounds", []):
                    for match in round:
                        matchs_joues.add(tuple(match))
                return matchs_joues
        except (FileNotFoundError, json.JSONDecodeError):
            return set()


if __name__ == "__main__":
    controller = MatchController("Magnus", "Hikaru")
    controller.match_result("1")  # Magnus gagne
    controller.save_scores_to_json(controller.scores)
