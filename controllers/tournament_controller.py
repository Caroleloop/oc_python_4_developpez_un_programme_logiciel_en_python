import datetime
from views.tournament_view import TournamentView
from models.tournament_model import Tournament
from models.player_model import Player
from controllers.match_controller import MatchController
from controllers.round_controller import RoundController
from controllers.player_controller import PlayerController
from views.utile import get_input, display_message


class TournamentController:
    def __init__(self, tournaments, players):
        """Initializes the TournamentController with tournament and player data.

        Args:
            tournaments (list): List of existing Tournament instances.
            players (list): List of existing Player instances.

        Attributes:
            view (TournamentView): View for tournament-related user interactions.
            model (Tournament): Tournament model class.
            player_model (Player): Player model class.
            match_controller (MatchController): Match controller class.
            round_controller (RoundController): Instance of RoundController.
            player_controller (PlayerController): Player controller class.
        """
        self.view = TournamentView()
        self.model = Tournament
        self.player_model = Player
        self.match_controller = MatchController
        self.round_controller = RoundController()
        self.player_controller = PlayerController
        Tournament.all_tournaments = tournaments
        Player.all_players = players
        # self.past_matches = set()

    def tournament_management(self):
        """Displays the tournament menu and handles user choices."""
        while True:
            choice = self.view.display_tournament_menu()
            if choice == "1-1":
                self.create_tournament()
            elif choice == "1-2":
                self.add_players_to_the_tournament()
            elif choice == "1-3":
                self.delete_player_to_the_tournament()
            elif choice == "2-1":
                self.round_controller.create_first_round()
            elif choice == "2-2":
                self.score_update()
            elif choice == "2-3":
                self.round_controller.create_another_round()
            elif choice == "3":
                self.modify_tournament()
            elif choice == "4":
                self.delete_tournament()
            elif choice == "5":
                self.display_tournament()
            elif choice == "6":
                break
            else:
                print("choice invalide.")

    def create_tournament(self):
        """Creates a new tournament and optionally adds players."""
        name_tournament = get_input("\tTournament name: ").strip()
        location = get_input("\tTournament location: ").strip()
        start_date = get_input("\tStart date of the tournament:").strip()
        while True:
            number_rounds_input = get_input("\tNumber of tournament rounds (default: 4): ").strip()

            if not number_rounds_input:
                number_rounds = 4
                break

            try:
                number_rounds = int(number_rounds_input)
                if number_rounds < 4:
                    number_rounds = 4
                break
            except ValueError:
                print("Please enter a valid number.")

        description = get_input("\tTournament description: ").strip()

        tournament = Tournament(name_tournament, location, start_date, "", number_rounds, description)
        Tournament.save_data_tournament()

        add_player = get_input("\n\tDo you want to add players to the tournament? (y/n):")
        if add_player == "y":
            self.add_players_to_the_tournament(tournament)
        else:
            display_message("\n\tYou can add players later using the 'Add players' option.")

    def add_players_to_the_tournament(self, tournament=None):
        """Adds players to a specified tournament.

        Args:
            tournament (Tournament, optional): Tournament to add players to.
                If None, prompts user to select one.
        """
        if tournament is None:
            tournament = Tournament.tournament_id()
            if tournament is None:
                display_message("Action cancelled.")
                return

        display_message(f"Add players to tournament: {tournament.name_tournament} (ID: {tournament.id}).")
        display_message("Enter the IDs of the players to be added (type 'end' to finish).")

        while True:
            player_id = get_input("Player ID to be added: ").strip()

            if player_id.lower() == "end":
                break  # Exits the loop if the user types “end”.
            try:
                player_id = int(player_id)
            except ValueError:
                display_message("Invalid input. Please enter a number or 'end' to quit.")
            # Check if the player exists
            player = next((p for p in Player.all_players if p.id == player_id), None)

            if not player:
                display_message(f"Player with ID {player_id} not found.")
                continue

            # Check if the player is already registered
            if any(p_id == player_id for p_id in tournament.players):
                display_message(f"Player {player_id} is already registered in this tournament.")
                continue

                # Add player to tournament
            tournament.players.append(player_id)
            display_message(f"Player ID: {player_id} added successfully.")

        # Save changes in data_tournaments.json
        Tournament.save_data_tournament()
        display_message("All players have been added to the tournament.")

    def delete_player_to_the_tournament(self, tournament=None):
        """Removes a player from a tournament.

        Args:
            tournament (Tournament, optional): Tournament to remove the player from.
                If None, prompts user to select one.
        """
        if tournament is None:
            tournament = Tournament.tournament_id()
            if tournament is None:
                display_message("Action cancelled.")
                return

        display_message(f"Delete players to tournament: {tournament.name_tournament} (ID: {tournament.id}).")

        for player_id in tournament.players:
            player = next((p for p in Player.all_players if p.id == player_id), None)
            if player:
                display_message(f"ID: {player.id} | Last name: {player.last_name}  | First name: {player.first_name}")

        player_id = int(get_input("Quel est l'id du joueur à supprimer?:").strip())
        print(player_id)
        # Check if the player exists

        if player_id not in tournament.players:
            display_message("\nJoueur non trouvé dans ce tournoi.")
            return

        player = next((p for p in Player.all_players if p.id == player_id), None)
        if not player:
            display_message("\nJoueur non trouvé dans la base de données.")
            return

        # Request confirmation
        confirmation = (
            get_input(f"\nAre you sure you want to delete {player.last_name} {player.first_name}? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation == "y":
            tournament.players.remove(player_id)
            display_message("\nPlayer successfully deleted.")
        else:
            display_message("\nDeletion cancelled.")

        Tournament.save_data_tournament()

    def end_of_tournament(self):
        """Sets the end date of a tournament."""
        tournament = Tournament.tournament_id()
        if tournament.start_date:
            display_message("The tournament has already begun.")
            return

        tournament.end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        Tournament.save_data_tournament()

        display_message(f"The tournament '{tournament.name_tournament}' ended on {tournament.start_date}.")

    def modify_tournament(self):
        """Modifies the details of an existing tournament.

        Prompts user to enter new values or leave fields blank
        to keep existing information.
        """
        tournament = Tournament.tournament_id()

        # Display current information
        display_message(
            f"\nModifying tournament:\n\t "
            f"ID: {tournament.id}\n\t"
            f"Tournament name: {tournament.name_tournament}\n\t"
            f"Tournament location: {tournament.location}\n\t"
            f"Start date: {tournament.start_date}\n\t"
            f"Number of tournament rounds: {tournament.number_rounds}\n\t"
            f"Tournament description: {tournament.description}\n\t"
        )
        display_message("Leave blank to keep the current value.")

        # Request new information
        new_name_tournament = get_input(f"New name tournament ({tournament.name_tournament}): ").strip()
        new_location = get_input(f"New location ({tournament.location}): ").strip()
        new_start_date = get_input(f"New start_date ({tournament.start_date}): ").strip()
        new_number_rounds = get_input(f"New number rounds ({tournament.number_rounds}): ").strip()
        new_description = get_input(f"New description ({tournament.description}): ").strip()

        # Update information if a new value is provided
        if new_name_tournament:
            tournament.name_tournament = new_name_tournament
        if new_location:
            tournament.location = new_location
        if new_start_date:
            tournament.start_date = new_start_date
        if new_number_rounds:
            tournament.number_rounds = int(new_number_rounds)
        if new_description:
            tournament.description = new_description

        # Save modifications
        Tournament.save_data_tournament()
        display_message("Tournament successfully updated.")

    def delete_tournament(self):
        """Deletes a tournament by its ID after confirmation."""
        tournament = Tournament.tournament_id()

        # Request confirmation
        confirmation = (
            get_input(f"Are you sure you want to delete the tournament with the ID {tournament.id}? (y/n): ")
            .strip()
            .lower()
        )

        if confirmation == "y":
            for i, t in enumerate(Tournament.all_tournaments):
                if t.id == tournament.id:
                    del Tournament.all_tournaments[i]
            Tournament.save_data_tournament()
            display_message("Tournament successfully deleted.")
        else:
            display_message("Deletion cancelled.")
        pass

    def score_update(self, tournament=None):
        """
        Updates player scores for matches in the current round.

        Args:
            tournament (Tournament, optional): Tournament whose scores are to be updated.
                If None, user is prompted to choose one.
        """
        tournament = Tournament.tournament_id()
        if not tournament.rounds:
            display_message("No round found for this tournament.")
            return

        current_round = next((r for r in tournament.rounds if not r["end_date_round"]), None)

        if not current_round:
            display_message("All rounds have been completed.")
            return

        display_message(f" Update scores for  {current_round['name']} (ID: {current_round['id']})")

        for match in current_round["matches"]:
            player1, player2, colors = match
            display_message(f"Match between  {player1[0]} and {player2[0]}")

            valid_responses = ["1", "2", "draw"]
            result = None

            while result not in valid_responses:
                result = get_input(
                    f"Result  (1: Player  {player1[0]} wins, 2: Player  {player2[0]} wins, draw: equality) : "
                )
                if result not in valid_responses:
                    display_message("Invalid input. Please enter '1', '2', or 'draw'.")

            try:
                self.match_controller.match_result(player1, player2, result, match)
                self.match_controller.update_player_score(player1[0], player1[1])
                self.match_controller.update_player_score(player2[0], player2[1])
            except ValueError as e:
                display_message(str(e))
                return

        display_message("Scores updated and round over!\n")

        self.end_tournament(tournament)
        Tournament.save_data_tournament()

    @staticmethod
    def display_tournament():
        """Displays all tournament data: players, rounds, matches, and results."""
        Player.load_data_players()
        Tournament.load_data_tournaments()

        for tournament in Tournament.all_tournaments:
            display_message(
                f"\n\n\tID: {tournament.id}\n\t"
                f"Tournament name: {tournament.name_tournament}\n\t"
                f"Tournament location: {tournament.location}\n\t"
                f"Start date: {tournament.start_date}\n\t"
                f"Number of tournament rounds: {tournament.number_rounds}\n\t"
                f"Tournament description: {tournament.description}\n\t"
                f"End date: {tournament.end_date}"
            )
            display_message("\tPlayers: ")
            for player_id in tournament.players:
                player = next((p for p in Player.all_players if p.id == player_id), None)
                if player:
                    display_message(
                        f"\t\tID: {player.id}\n\t"
                        f"\tLast name: {player.last_name}\n\t"
                        f"\tFirst name: {player.first_name}\n\t"
                        f"\tBirthdate: {player.birthdate}\n\t"
                        f"\tNational chess identifier: {player.national_chess_identifier}\n\t"
                        f"\tScore: {player.score}\n"
                    )
                else:
                    display_message(f"\t\t- Player ID {player_id} not found.")

            display_message("\tRounds: ")
            for round_ in tournament.rounds:
                display_message(
                    f"\t\t{round_['name']}:\n "
                    f"\t\tStart round: {round_['start_date_round']}\n"
                    f"\t\tEnd round: {round_['end_date_round']}"
                )
                display_message("\t\tMatches: ")
                for match in round_["matches"]:
                    player1, player2, color = match
                    player1_info = next((p for p in Player.all_players if p.id == player1[0]), None)
                    player2_info = next((p for p in Player.all_players if p.id == player2[0]), None)

                    color_info = color[0]
                    color1 = "white" if color_info.get(str(player1_info.id)) == "white" else "black"
                    color2 = "white" if color_info.get(str(player2_info.id)) == "white" else "black"

                    if player1_info and player2_info:

                        display_message(
                            f"\t\t\t{player1_info.first_name} {player1_info.last_name} "
                            f"(ID: {player1_info.id}), color: {color1}, score: {player1[1]}  vs "
                            f"{player2_info.first_name} {player2_info.last_name} "
                            f"(ID: {player2_info.id}), color: {color2}, score: {player2[1]} "
                        )
                    else:
                        display_message("\t\t\t- Invalid player data.")

    @staticmethod
    def end_tournament(tournament):
        """Ends a tournament if its last round has been completed.

        Args:
            tournament (Tournament): Tournament instance to check and close.
        """
        if not tournament.rounds:
            display_message("No round found for this tournament.")
            return

        # Find the last round in progress (the one that doesn't yet have an end date)
        current_round = next((r for r in tournament.rounds if not r["end_date_round"]), None)

        if not current_round:
            display_message("\nAll rounds have already been completed.")
            return

        # Mark the end of the round
        current_round["end_date_round"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Check if this is the last round of the tournament
        if current_round["id"] == tournament.number_rounds:
            tournament.end_date = current_round["end_date_round"]
            display_message(f"\nThe tournament '{tournament.name_tournament}' is finished!")
        else:
            display_message(f"{current_round['name']} finished. The tournament continues.")
