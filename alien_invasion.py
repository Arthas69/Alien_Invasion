import sys
from random import randint
from time import sleep

import pygame

from game.bullet import Bullet
from game.alien import Alien
from game.settings import Settings
from game.ship import Ship
from game.star import Star
from utils.game_stats import GameStats
from utils.button import Button


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

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._populate_sky()
        self._create_fleet()

        self.play_button = Button(self, 'Play')

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            self._check_events()

            if self.stats.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """ Respond to key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """ Start a new game if the player clicks Play """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_game()

    def _check_bullet_alien_collisions(self):
        """ Respond for bullet-alien collisions """
        # Remove any bullet and alien that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached the edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottoms(self):
        """ Check if any aliens have reached the bottom of the screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat it the same as if the ship got hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

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

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _populate_sky(self):
        """ Place stars on the sky """
        for _ in range(self.settings.star_count):
            star = Star(self)
            star_width, star_height = star.rect.size
            star.rect.x = randint(star_width, self.settings.screen_width - star_width)
            star.rect.y = randint(star_height, self.settings.screen_height - star_height)
            self.stars.add(star)

    def _start_game(self):
        """ Start the game if key pressed or mouse clicked """
        if not self.stats.game_active:
            # Reset the game stats
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien """
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Clear the screen from remaining aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            # Create new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """ Check if the fleet is at an edge, then update the position of all aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottoms()

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets """
        # Update bullet position
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_screen(self):
        """ Update images on the screen and flip to the new screen """
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Create game instance and run it
    ai = AlienInvasion()
    ai.run_game()
