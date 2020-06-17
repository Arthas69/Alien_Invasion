import sys
from random import randint

import pygame

from game.settings import Settings
from game.ship import Ship
from game.bullet import Bullet
from game.alien import Alien
from game.star import Star


class AlienInvasion:
    """ Overall class to manage game assets and behavior """

    def __init__(self):
        """ Initialize the game and creates game resources"""
        pygame.init()

        self.settings = Settings()

        # for windowed mode
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # for the fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._populate_sky()
        self._create_fleet()

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """ Respond to keypresses and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Respond to keypresses """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Respond to key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """ Update images on the screen and flip to the new screen """
        self.screen.fill(self.settings.bg_color)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.stars.draw(self.screen)
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _create_alien(self, alien_number, row_number):
        """ Create an alien and place it in the row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Double indent from left side of the screen for every even row
        # indent_width = alien_width if row_number % 2 == 0 else 2 * alien_width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """ Create the fleet of aliens """
        # Create and alien and finds a number of aliens in the row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        # Defying the number of alien to fill all available space in a row
        available_space_in_row = self.settings.screen_width - 2 * alien_width
        number_aliens_in_row = available_space_in_row // (2 * alien_width)
        # Determine a number of rows of alien to fit the screen
        available_space_for_rows = self.settings.screen_height - ship_height - (5 * alien_height)
        number_of_rows = available_space_for_rows // (2 * alien_height)

        # Creates the fleet of aliens
        for row_number in range(number_of_rows):
            for alien_number in range(number_aliens_in_row):
                self._create_alien(alien_number, row_number)

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets """
        # Update bullet position
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update the position of all aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached the edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _populate_sky(self):
        for _ in range(self.settings.star_count):
            star = Star(self)
            star_width, star_height = star.rect.size
            star.rect.x = randint(star_width, self.settings.screen_width - star_width)
            star.rect.y = randint(star_height, self.settings.screen_height - star_height)
            self.stars.add(star)


if __name__ == '__main__':
    # Create game instance and run it
    ai = AlienInvasion()
    ai.run_game()
