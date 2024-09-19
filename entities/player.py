import pygame
import config.colors as colors
import config.screen as conf_screen
from enum import Enum
from pathlib import Path


GRAVITE = .8

PLAYER_IMG = pygame.Surface((50, 50))
PLAYER_IMG.fill(colors.RED)

class Action(Enum):
    WALK = "run"
    JUMP = "jump"
    IDLE = "idle"
    DIE = "death"
    
class Age(Enum):
    YOUNG = "young"
    ADULT = "adult"
    OLD = "old"
    
class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.current_action = Action.IDLE
        self.state = Age.YOUNG
        self.direction = Direction.RIGHT
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = conf_screen.CELL_SIZE * 2
        self.rect.y = conf_screen.HEIGHT_SCREEN - conf_screen.CELL_SIZE * 4
        self.is_grounded = False
        self.x_current_speed = 0
        self.y_current_speed = 0
        self.move_speed = 6
        self.jump_speed = 12
        self.age = 8
        self.state = Age.YOUNG
        self.platforms = platforms  # Liste des plateformes pour la détection de collision
        self.age = 0
        self.is_jumping = False

    def update(self, platforms):
        # Mouvements et collisions sur l'axe X
        self.rect.x += self.x_current_speed
        self.check_collision_x(platforms)

        # Appliquer la gravité seulement si le joueur n'est pas au sol
        if not self.is_grounded:
            self.gravite()
        
        if self.is_grounded and self.current_action == Action.JUMP:
            self.current_action = Action.IDLE
        
        self.rect.x += self.x_current_speed
        self.rect.y += self.y_current_speed

        # Gérer les limites de l'écran
        if self.rect.right > conf_screen.WIDTH_SCREEN:
            self.rect.right = conf_screen.WIDTH_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        # Si le joueur tombe en dehors de l'écran, il est remis au sol
        if self.rect.bottom > conf_screen.HEIGHT_SCREEN:
            self.rect.bottom = conf_screen.HEIGHT_SCREEN
            self.is_grounded = True
            self.y_current_speed = 0
        
        self.update_state()
        self.image = self.get_player_image()

    def gravite(self):
        """Appliquer la gravité si le joueur n'est pas au sol"""
        self.y_current_speed += GRAVITE

    def jump(self):
        """Permettre le saut seulement si le joueur est bien au sol"""
        if self.is_grounded:
            self.y_current_speed = -self.jump_speed
            self.is_grounded = False
            self.current_action = Action.JUMP

    def move_right(self):
        self.x_current_speed = self.move_speed
        self.current_action = Action.WALK
        self.direction = Direction.RIGHT

    def move_left(self):
        self.x_current_speed = -self.move_speed
        self.current_action = Action.WALK
        self.direction = Direction.LEFT

    def stop(self):
        self.x_current_speed = 0
        self.current_action = Action.IDLE

    def check_collision_x(self, platforms):
        """Vérifie et gère les collisions du joueur avec les plateformes sur l'axe X"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.x_current_speed > 0:
                    self.rect.right = platform.rect.left
                elif self.x_current_speed < 0:
                    self.rect.left = platform.rect.right

    def check_collision_y(self):
        """Vérifie et gère les collisions du joueur avec les plateformes sur l'axe Y"""
        self.is_grounded = False  # On réinitialise l'état "au sol"
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                # Si collision en tombant (le joueur touche le haut de la plateforme)
                if self.y_current_speed > 0:
                    print("collision bas")
                    self.rect.bottom = platform.rect.top
                    self.y_current_speed = 0
                    self.is_grounded = True  # Le joueur est bien au sol
                # Si collision en montant (le joueur touche le bas de la plateforme)
                elif self.y_current_speed < 0:
                    print("collision haut")
                    self.rect.top = platform.rect.bottom
                    self.y_current_speed = 0
                    
    def get_player_image(self) -> pygame.Surface:
        
        # The old player doesn't have a jump animation, so in that case we use the idle animation
        if self.current_action == Action.JUMP and self.state == Age.OLD:
            path = "assets/player/old/idle/"
            files_number = len(list(Path(path).glob("*.png")))
            image_counter = (((pygame.time.get_ticks()//100))%files_number)+1
            image = pygame.image.load(
                path + "old-idle-" + str(image_counter) + ".png"
            )
        else:
            path = "assets/player/" + self.state.value + "/" + self.current_action.value + "/"
            files_number = len(list(Path(path).glob("*.png")))
            image_counter = (((pygame.time.get_ticks()//100))%files_number)+1
            image = pygame.image.load(
                path + self.state.value + "-" + self.current_action.value + "-" + str(image_counter) + ".png"
            )
            
        old_center = self.rect.center
        self.rect = image.get_rect() 
        self.rect.center = old_center
        
        if self.direction == Direction.LEFT:
            image = pygame.transform.flip(image, True, False)
        return image

    # Reste du code inchangé
    def update_age(self, year_elapsed):
        started_age = 16
        self.age = (year_elapsed) + started_age

    def update_state(self):
        if self.age < 65:
            self.state = Age.OLD
        if self.age < 50:
            self.state = Age.ADULT
        if self.age < 18:
            self.state = Age.YOUNG

        if self.age >= 65:
            self.die()

    def get_age(self):
        return self.age

    def die(self):
        print("You are dead")
        return

    def show_age(self, screen):
        font = pygame.font.Font(None, conf_screen.CELL_SIZE * 2)
        text = font.render("Âge : " + str(self.get_age()), 1, (0, 0, 255))
        text_rect = text.get_rect()
        screen.blit(text, (conf_screen.WIDTH_SCREEN - text_rect.width - (conf_screen.WIDTH_SCREEN // 20), text_rect.height))

        image_path = "assets/UI/state/" + str(self.state.value) + ".png"
        image = pygame.image.load(image_path)

        doubled_size = (image.get_width() * 1, image.get_height() * 1)
        image = pygame.transform.scale(image, doubled_size)

        image_rect = image.get_rect()
        image_rect.center = (conf_screen.WIDTH_SCREEN - text_rect.width - (conf_screen.WIDTH_SCREEN // 15), conf_screen.CELL_SIZE * 2.5)
        screen.blit(image, image_rect.topleft)
