class GameStats:
    """ Track statistics for Alien Invasion """

    def __init__(self, ai_game):
        """ Initialize statistics """
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        self.high_score = 0

        # Start Alien Invasion in an active state
        self.game_active = False

    def reset_stats(self):
        """ Initialize statistics that can be changed during a game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = self.settings.manual_level if self.settings.manual_level > 1 else 1
