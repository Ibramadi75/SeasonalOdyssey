import pygame
import config.colors as colors
import config.screen as conf_screen
from enum import Enum
from pathlib import Path

GRAVITE = .8

PLAYER_IMG = pygame.Surface((50, 50))
PLAYER_IMG.fill(colors.RED)

jump_sound = pygame.mixer.Sound("music/jump.wav")

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

def resize_by_removing_top(image, pixels_to_remove):
    """Resize the image by removing pixels from the top."""
    # Get the current width and height of the image
    width, height = image.get_size()
    
    # Ensure pixels_to_remove is within the height of the image
    if pixels_to_remove >= height:
        raise ValueError("Cannot remove more pixels than the height of the image")
    
    # Define the new rectangle for the resized image (removing from the top)
    new_rect = pygame.Rect(0, pixels_to_remove, width, height - pixels_to_remove)
    
    # Create a new surface with the new size
    new_image = pygame.Surface((width, height - pixels_to_remove), pygame.SRCALPHA)
    
    # Blit (copy) the relevant part of the original image onto the new surface
    new_image.blit(image, (0, 0), new_rect)
    
    return new_image

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.current_action = Action.IDLE
        self.state = Age.YOUNG
        self.direction = Direction.RIGHT
        self.image = PLAYER_IMG
        # Créer le rectangle en utilisant les attributs de l'image
        self.rect = pygame.Rect(0,0,0,0)

        self.is_grounded = False
        self.x_current_speed = 0
        self.y_current_speed = 0
        self.move_speed = 5
        self.def_move_speed = 5
        self.jump_speed = 12
        self.age = 8
        self.state = Age.YOUNG
        self.platforms = platforms  # Liste des plateformes pour la détection de collision
        self.is_jumping = False
        self.id = "terrain"
        self.is_blocked = False
        self.started_age = 15
        self.is_dead = False

    def update(self, platforms):
        if self.is_blocked:
            self.move_speed = 0
            self.jump_speed = 0
            return
        # Mouvements et collisions sur l'axe X
        self.rect.x += self.x_current_speed
        self.check_collision_x(platforms)

        # Appliquer la gravité seulement si le joueur n'est pas au sol
        if not self.is_grounded:
            self.gravite()

        if self.is_grounded and self.current_action == Action.JUMP:
            self.current_action = Action.IDLE

        # self.rect.x += self.x_current_speed
        self.rect.y += self.y_current_speed
        self.check_collision_y(platforms)

        # Gérer les limites de l'écran
        if self.rect.right > conf_screen.WIDTH_SCREEN:
            self.rect.right = conf_screen.WIDTH_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        # Si le joueur tombe en dehors de l'écran, il est remis au sol
        # if self.rect.bottom > conf_screen.HEIGHT_SCREEN:
        #     self.rect.bottom = conf_screen.HEIGHT_SCREEN
        #     self.is_grounded = True
        #     self.y_current_speed = 0
        
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
            pygame.mixer.Channel(1).play(jump_sound)

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
        for collision in platforms:
            if self.rect.colliderect(collision.rect):
                if self.x_current_speed > 0:
                    self.rect.right = collision.rect.left
                elif self.x_current_speed < 0:
                    self.rect.left = collision.rect.right

    def check_collision_y(self,platforms):
        """Vérifie et gère les collisions du joueur avec les plateformes sur l'axe Y"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Si collision en montant (le joueur touche le bas de la plateforme)
                if self.y_current_speed < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_current_speed = 0

    def get_player_image(self) -> pygame.Surface:
        # Charger l'image appropriée en fonction de l'état et de l'action
        if self.current_action == Action.JUMP and self.state == Age.OLD:
            path = "assets/player/old/idle/"
            files_number = len(list(Path(path).glob("*.png")))
            image_counter = (((pygame.time.get_ticks()//100))%files_number)+1
            image = pygame.image.load(path + "old-idle-" + str(image_counter) + ".png")
        else:
            path = "assets/player/" + self.state.value + "/" + self.current_action.value + "/"
            files_number = len(list(Path(path).glob("*.png")))
            image_counter = (((pygame.time.get_ticks()//100))%files_number)+1
            image = pygame.image.load(path + self.state.value + "-" + self.current_action.value + "-" + str(image_counter) + ".png")


        if self.state  == Age.YOUNG:
            image =  resize_by_removing_top(image,13)
        elif self.state  == Age.ADULT:
            image =  resize_by_removing_top(image,20)
        elif self.state  == Age.OLD:
            image =  resize_by_removing_top(image,58)


        # Sauvegarder le centre actuel du rect de collision pour conserver sa position après redimensionnement
        old_center = self.rect.center

        # Récupérer le rectangle de l'image
        original_rect = image.get_rect()

        # Créer un nouveau rect pour le joueur, redimensionné en largeur et en hauteur
        new_width = original_rect.width * 0.5  # Par exemple, 50% de la largeur
        new_height = original_rect.height   # Par exemple, 50% de la hauteur
        self.rect = pygame.Rect(0, 0, new_width, new_height)

        # Calculer les offsets pour centrer l'image par rapport au rect de collision
        image_offset_x = (original_rect.width - self.rect.width) // 2
        image_offset_y = (original_rect.height - self.rect.height) //2

        # Créer une surface transparente pour le sprite avec les nouvelles dimensions
        blitted_image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        blitted_image.blit(image, (-image_offset_x, -image_offset_y))

        # Assigner l'image redimensionnée avec l'offset
        self.image = blitted_image

        # Réappliquer le centre sauvegardé
        self.rect.center = old_center

        # Retourner l'image éventuellement retournée horizontalement (pour la direction)
        if self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

        return self.image

    # Reste du code inchangé
    def update_age(self, year_elapsed):
        self.age = (year_elapsed) + self.started_age

    def update_state(self):
        # if self.age < 51:
        #     self.state = Age.OLD
        #     self.def_move_speed = 3
        #     self.jump_speed = 12
        if self.age < 45:
            self.state = Age.ADULT
            self.def_move_speed = 5
            self.jump_speed = 12.3
        if self.age < 20:
            self.state = Age.YOUNG
            self.def_move_speed = 5
            self.jump_speed = 12

        if self.age >= 61:
            self.state = Age.OLD
            self.die()

    def get_age(self):
        return self.age

    def die(self):
        self.is_dead = True
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