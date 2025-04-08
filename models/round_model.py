import datetime


class Round:
    counter_round = 1

    def __init__(self, name_round):
        """
        Initializes a round with the given name.

        Args:
            name_round (str): The name of the round (e.g., "Round 1").
        """
        self.id = Round.counter_round
        Round.counter_round += 1
        self.name_round = name_round
        self.start_time = None
        self.end_time = None
        self.matchs = []

    def start_time(self):
        """
        Marks the start of the round by recording the start time.

        Returns:
            str: The start time in the format 'YYYY-MM-DD HH:MM'.
        """
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def end_time(self):
        """
        Marks the end of the round by recording the end time.

        Returns:
            str: The end time in the format 'YYYY-MM-DD HH:MM'.
        """
        self.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
