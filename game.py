import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from buttons import Button , Back_Button
from ship import Ship
from bullet import Bullet
from alien import Alien

pygame.init()
pygame.mixer.init()

# Load the sound files.
bullet_sfx = pygame.mixer.Sound('assets/sounds/bullet-hit.wav')
ship_hit_sfx = pygame.mixer.Sound('assets/sounds/player-ship-destroyed.wav')
level_increase_sfx = pygame.mixer.Sound('assets/sounds/level-completion.wav')
alien_explosion_sfx = pygame.mixer.Sound('assets/sounds/alien-explosion.wav')
button_click_sfx = pygame.mixer.Sound('assets/sounds/button-click.wav')
game_intro_pressed_sfx = pygame.mixer.Sound('assets/sounds/game-intro-pressed.wav')

# Set the volume of the sound files.
bullet_sfx.set_volume(0.1)
ship_hit_sfx.set_volume(0.1)
level_increase_sfx.set_volume(0.7)
alien_explosion_sfx.set_volume(0.1)
button_click_sfx.set_volume(0.2)
game_intro_pressed_sfx.set_volume(0.3)

#* Code for Pre Main Menu screen.
# Set up the display
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()

# Display icon and caption for the game.
icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption("Galactic Alien Annihilation")

# Set up the font
font = pygame.font.Font(None, 36)

# Render both the texts.
text1 = font.render("This game was developed by Arnab Narayan Bose", True, (230, 230, 230))
text1_rect = text1.get_rect(center=(WIDTH // 4.5, HEIGHT - text1.get_height() // 1))

text2 = font.render("© 2023 All Rights Reserved", True, (230, 230, 230))
text2_rect = text2.get_rect(center=(WIDTH // 1.15, HEIGHT - text2.get_height() // 1))

# Render the exit text
exit_text = font.render('Press any key to enter', True, (230, 230, 230), 'black')
exit_text_rect = exit_text.get_rect()
exit_text_rect.center = (WIDTH // 2, HEIGHT // 2)

# Variables for blinking effect
blink = True
blink_speed = 1000  # Speed of blinking in milliseconds
last_blink = pygame.time.get_ticks()
# Start blinking after 1 second.
start_blink_at = pygame.time.get_ticks() + 200  
# Add these lines before your game loop
secret_message = font.render("HEY! YOU, DO WANT TO PLAY THE GAME OR NOT!?", True, (230, 230, 230), 'black')
secret_message_rect = secret_message.get_rect()
secret_message_rect.center = (WIDTH // 2, HEIGHT // 4)
show_secret_message_at = pygame.time.get_ticks() + 3_600_000  # 1 hr in milliseconds.
show_secret_message = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            game_intro_pressed_sfx.play()
            sleep(0.1)
            running = False

    now = pygame.time.get_ticks()

    # Check if it's time to show the secret message
    if now >= show_secret_message_at:
        show_secret_message = True

    # Fill the window with a white background
    window.fill('black')

    # Blinking effect for the text.
    if now - last_blink >= blink_speed and now >= start_blink_at:
        last_blink = now
        blink = not blink

    # Draw the text onto the window
    window.blit(text1, text1_rect)
    #window.blit(text2, text2_rect)
    if blink:
        window.blit(exit_text, exit_text_rect)

    # Draw the secret message
    if show_secret_message:
        window.blit(secret_message, secret_message_rect)

    # Flip the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

#* Code for Main Menu class.
class MainMenu:
    def __init__(self, window):
        self.window = window
        """Initialize the main menu and create the resources."""
        pygame.init()

        # Set a timer for playing the main menu theme
        pygame.time.set_timer(pygame.USEREVENT, 250)  # 1000 ms = 1 s; 100 ms = 0.1 s

        # Set up some constants
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        
        # Display icon and caption for the game.
        icon = pygame.image.load('icon.ico')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Galactic Alien Annihilation")
                
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)  
        self.button_width, self.button_height = 162, 66
        self.button_y_gap = 100
        self.button_x = (self.screen_width - self.button_width) / 2

        # Create a Surface for the title
        font = pygame.font.Font('assets/fonts/Doctor Glitch.otf', 52)
        self.title_surface = font.render("Galactic  Alien  Annihilation", True, (255, 255, 255))

        # Set up a color
        self.color = (255, 255, 255)

        self.buttons = [
            self.Button(self.button_x, self.screen_height / 2 - self.button_height / 2 - self.button_y_gap, self.button_width, self.button_height, "New Game", 'lime', self.start_game),
            self.Button(self.button_x, self.screen_height / 2 - self.button_height / 2, self.button_width, self.button_height, "Keybinds", 'gold', self.open_options),
            self.Button(self.button_x, self.screen_height / 2 - self.button_height / 2 + self.button_y_gap, self.button_width, self.button_height, "Quit", 'crimson', self.quit_game),
        ]
    
    class Button:
        def __init__(self, x, y, width, height, text, color, command):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.command = command

        def draw(self, screen, font):
            pygame.draw.rect(screen, self.color, self.rect)
            text_surface = font.render(self.text, True, (0, 0, 0))
            screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) / 2, 
                                       self.rect.y + (self.rect.height - text_surface.get_height()) / 2))

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.command()
                    button_click_sfx.play()

    def start_game(self):
        # Create a new and run it.
        button_click_sfx.play()
        pygame.mixer.music.fadeout(2000)  # 1000 ms = 1 s
        gai = Galactic_Alien_Annihilation(self.window)
        gai.run_game(window)
        
    def open_options(self):
        options = Options(menu,window)
        options.run(window)

    def quit_game(self):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
        else:  
            button_click_sfx.play()
            sleep(0.1)
            sys.exit()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.KEYDOWN and 
                                                                                                                    event.key == pygame.K_e):
                    self.quit_game()
                elif event.type == pygame.USEREVENT:
                    # Play the Main_menu theme
                    pygame.mixer.music.load('assets/music/main_menu.mp3')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(loops=-1, fade_ms=2011) # 1000 ms = 1 s.
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        pygame.mixer.music.stop()
                        
                for button in self.buttons:
                    button.handle_event(event)

            # Load the background0.
            self.screen.fill('white')
            image = pygame.image.load('assets/images/background0.png').convert()
            self.screen.blit(image, (0, 0))
            
            for button in self.buttons:
                button.draw(self.screen, self.font)
            # Draw the title in the center of the screen.
            self.screen.blit(self.title_surface, ((self.screen_width - self.title_surface.get_width()) / 2, 50))
            
            pygame.display.flip()

# Sub-code for the options menu.
class Options:
    def __init__(self, menu, window):
        self.menu = menu
        self.window = window
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.Font(None, 36)
        # Back button
        self.back_button = self.menu.Button(self.screen.get_rect().width / 2 - 81,
                                            self.screen.get_rect().height - 100, 162, 66,
                                            "Back", (251, 106, 0), self.back_to_main,)
        button_click_sfx.play()
       
    # Give function to all the things in the option window.
    def back_to_main(self):
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        button_click_sfx.play()
        self.menu.main()
    
    def run(self, window):
        self.window = window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.back_button.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        pygame.mixer.music.unload()
                    if event.key == pygame.K_e:  
                        sys.exit()

            self.screen.fill('white')
            image = pygame.image.load('assets/images/background0.png').convert()
            self.screen.blit(image, (0, 0))
            self.back_button.draw(self.screen, self.font)

            self.font = pygame.font.Font(None, 30)  
            self.title_surface = self.font.render('A/D - To move left and right', True, (255, 255, 255))  
            msg0_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 6.1, self.screen.get_rect().height / 8))
            self.screen.blit(self.title_surface, msg0_rect)
            
            self.title_surface = self.font.render('Space - To shoot bullets', True, (255, 255, 255))  
            msg1_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 6.5, self.screen.get_rect().height / 5))
            self.screen.blit(self.title_surface, msg1_rect)

            self.title_surface = self.font.render('E - To exit the game quickly', True, (255, 255, 255))  
            msg2_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 6, self.screen.get_rect().height / 3.6))
            self.screen.blit(self.title_surface, msg2_rect)

            self.title_surface = self.font.render('Escape - To show pause menu (in game)', True, (255, 255, 255))  
            msg3_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 4.72, self.screen.get_rect().height / 2.8))
            self.screen.blit(self.title_surface, msg3_rect)

            self.title_surface = self.font.render('M - Stop music playback temporarily', True, (255, 255, 255))  
            msg4_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 5, self.screen.get_rect().height / 2.3))
            self.screen.blit(self.title_surface, msg4_rect)

            pygame.display.flip()
            
            # Display icon and caption for the game.
            icon = pygame.image.load('icon.ico')
            pygame.display.set_icon(icon)
            pygame.display.set_caption("Galactic Alien Annihilation")

# Code for the main game.
class Galactic_Alien_Annihilation:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self, window):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.window = window
        self.pause_menu = False
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Display icon and caption for the game.
        icon = pygame.image.load('icon.ico')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Galactic Alien Annihilation")

        # Create an instance to store the game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")
        self.exit_button = Back_Button(self, "Back")

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #* Create an alien and find the number of aliens in a row.
        # Spacing between each alien is qual to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (1 * alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropiately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            if not self.pause_menu:
                alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self, window):
        """Start the main loop for the game."""
        self.window = window
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all the aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Load the sound.
            ship_hit_sfx.play()
            
            # Pause.
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all the aliens in the fleet."""
        if not self.pause_menu:
            self._check_fleet_edges()
            self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        if not self.pause_menu:
            # Update bullets positions.
            self.bullets.update()

        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisons()

    def _check_bullet_alien_collisons(self):
        """Respond to bullet-alien collisions."""
        if not self.pause_menu:
            # Remove any bullets and aliens that have collided.
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.pause_menu:
            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
                alien_explosion_sfx.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            level_increase_sfx.play()
            self.sb.prep_level()

    def _check_events(self):
        """Respond to all keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                if event.key == pygame.K_m:
                        pygame.mixer.music.unload()
                # Event handling for pause menu.
                if event.key == pygame.K_ESCAPE:
                    if self.stats.game_active:
                        if self.pause_menu:
                            self.pause_menu = False
                            pygame.mouse.set_visible(False)
                            pygame.mixer.music.unpause()
                        else:
                            self.pause_menu = True
                            pygame.mouse.set_visible(True)
                            pygame.mixer.music.pause()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # Check for play button.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # Check for back button.
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_back_button(mouse_pos)
            # Check for the buttons displayed in pause menu.
                if self.pause_menu:
                    if self.back.collidepoint(event.pos):
                        button_click_sfx.play()
                        self.menu = MainMenu(self.window)
                        self.menu.main()
                    elif self.reset.collidepoint(event.pos):
                        button_click_sfx.play()
                        gai = Galactic_Alien_Annihilation(self.window)
                        gai.run_game(window)
    
    # Buttons for the screen of the game.
    def _check_back_button(self, mouse_pos):
        """Return to main menu when the player clicks Return."""
        if self.exit_button.rect.collidepoint(mouse_pos):
            button_click_sfx.play()
            self.menu = MainMenu(self.window)
            self.menu.main()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            button_click_sfx.play()
            pygame.mixer.music.load('assets/music/game.mp3')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            # Reset the game's settings.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_e:
                sys.exit()
        if not self.pause_menu:
            if event.key == pygame.K_d:
                self.ship.moving_right = True
            elif event.key == pygame.K_a:
                self.ship.moving_left = True
            if self.stats.game_active:
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()
                    bullet_sfx.play()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def draw_pause(self): 
        """Draw the things that will be displayed in the pause menu"""
        pygame.draw.rect(self.surface, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
        pygame.draw.rect(self.surface, (255, 255, 255), [382, 180, 600, 50], 0, 69)
        self.reset = pygame.draw.rect(self.surface, (220, 20, 10), [542, 280, 280, 50], 0, 0)
        self.back = pygame.draw.rect(self.surface, (251, 106, 0), [542, 355, 280, 50], 0, 0)

        #* Texts for the Pause menu.
        # Pause menu
        self.font = pygame.font.Font(None, 32)  
        self.title_surface = self.font.render("Game is currently paused: press Esc to resume", True, (0, 0, 0))  
        msg_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 2, self.screen.get_rect().height / 3.75))
        self.surface.blit(self.title_surface, msg_rect)

        # Reset button
        self.font = pygame.font.Font(None, 40)  
        self.title_surface = self.font.render("Restart", True, (0, 0, 0))  
        msg_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 2, self.screen.get_rect().height / 2.52))
        self.surface.blit(self.title_surface, msg_rect)

        # Back button
        self.font = pygame.font.Font(None, 40) 
        self.title_surface = self.font.render("Back", True, (0, 0, 0))  
        msg_rect = self.title_surface.get_rect(center=(self.screen.get_rect().width / 2, self.screen.get_rect().height / 2.03))
        self.surface.blit(self.title_surface, msg_rect)

        self.screen.blit(self.surface, (0, 0))
        return self.reset, self.back
    
    def _update_screen(self):
        """Update images on the screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.exit_button.draw_button()

        if self.pause_menu:
            self.draw_pause()

        pygame.display.flip()

if __name__ == "__main__":
    menu = MainMenu(window)
    menu.main()