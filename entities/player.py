import pygame
import config.colors as colors
import config.screen as conf_screen

GRAVITE = .8

PLAYER_IMG = pygame.Surface((50, 50))
PLAYER_IMG.fill(colors.RED)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = conf_screen.CELL_SIZE*2
        self.rect.y = conf_screen.HEIGHT_SCREEN - conf_screen.CELL_SIZE*6
        self.is_grounded = False
        self.x_current_speed = 0
        self.y_current_speed = 0
        self.move_speed = 6
        self.jump_speed = 15
        
        self.state = 1
        
        self.age = 8
        
    def update(self):        
        if not self.is_grounded:
            self.gravite()
        
        self.rect.x += self.x_current_speed
        self.rect.y += self.y_current_speed
        
        if self.rect.right > conf_screen.WIDTH_SCREEN:
            self.rect.right = conf_screen.WIDTH_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > conf_screen.HEIGHT_SCREEN:
            self.rect.bottom = conf_screen.HEIGHT_SCREEN
            self.is_grounded = True
            self.y_current_speed = 0

    def gravite(self):
        if not self.is_grounded:
            self.y_current_speed += GRAVITE

    def jump(self):
        if self.is_grounded or self.y_current_speed == 0:
            self.y_current_speed = -self.jump_speed
            self.is_grounded = False

    def move_right(self):
        self.x_current_speed = self.move_speed

    def move_left(self):
        self.x_current_speed = -self.move_speed

    def stop(self):
        self.x_current_speed = 0
        
    def update_age(self, year_elapsed):
        started_age = 16
        self.age = (year_elapsed) + started_age
        
    def update_state(self):
        if (self.age < 65):
            self.state = 3
        if (self.age < 50):
            self.state = 2
        if (self.age < 18):
            self.state = 1
            
        if (self.age >= 65):
            self.die()
            
        self.update_appearance()
        
    def update_appearance(self):
        if (self.state == 1):
            self.image = pygame.Surface((50, 50))
            self.image.fill(colors.RED)
        elif (self.state == 2):
            self.image = pygame.Surface((50, 80))
            self.image.fill(colors.GRAY)
        elif (self.state == 3):
            self.image = pygame.Surface((50, 65))
            self.image.fill(colors.BLACK)
        else: 
            self.die()
            
    def get_age(self):
        return self.age
    
    def die():
        print("You are dead")
        return;
    
    def show_age(self, screen):
        font = pygame.font.Font(None, conf_screen.CELL_SIZE*2)
        text = font.render("Âge : " + str(self.get_age()), 1, (0, 0, 255))
        text_rect = text.get_rect()
        screen.blit(text, (conf_screen.WIDTH_SCREEN - text_rect.width - (conf_screen.WIDTH_SCREEN//20), text_rect.height))
        
        image_path = "assets/UI/state/" + str(self.state) + ".png"
        image = pygame.image.load(image_path)
        
        doubled_size = (image.get_width() * 1, image.get_height() * 1)
        image = pygame.transform.scale(image, doubled_size)

        image_rect = image.get_rect()
        image_rect.center = (conf_screen.WIDTH_SCREEN - text_rect.width - (conf_screen.WIDTH_SCREEN // 15), conf_screen.CELL_SIZE * 2.5)
        screen.blit(image, image_rect.topleft)
        
            
        
        

        
