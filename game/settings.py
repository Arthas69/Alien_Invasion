from random import randint

class Settings:
    """ A class to store all settings for Alien Invasion """

    def __init__(self):
        """ Initialize the game's settings """
        # Screen settings
        self.screen_width = 1200  # Ширина экрана
        self.screen_height = 800  # Высота экрана
        self.bg_color = (0, 0, 255)  # Цвет фона

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Star settings
        self.star_count = randint(10, 20)
