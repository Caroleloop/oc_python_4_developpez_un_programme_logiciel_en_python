import datetime


class Round:
    counter_round = 1

    def __init__(self, name_round):
        """initalizing a round"""
        self.id = Round.counter_round
        Round.counter_round += 1
        self.name_round = name_round
        self.start_time = None
        self.end_time = None
        self.matchs = []

    def start_time(self):
        """
        Marks the start of a round by recording the start time.

        Return :
            start_time (str): Round end date and time (format 'YYYY-MM-DD HH:MM').
        """
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def end_time(self):
        """
        Marks the end of a tour by recording the end time.

        Return :
            end_time (str): Round end date and time (format 'YYYY-MM-DD HH:MM').
        """
        self.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
