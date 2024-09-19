import pygame
import config.screen as conf_screen
import sys

DARKEN_FACTOR = 0.3

# Fonction pour afficher le menu principal
def show_menu(screen):
    path = "assets/UI/menu/"
    # Charger l'image de fond
    background = pygame.image.load(path + "menu_background.png")
    background = pygame.transform.scale(background, (conf_screen.WIDTH_SCREEN, conf_screen.HEIGHT_SCREEN))


    # Charger les images des boutons
    button_play_img = pygame.image.load(path + "play_button.png")
    button_quit_img = pygame.image.load(path + "exit_button.png")
    
    button_play_img = pygame.transform.scale(button_play_img, (button_play_img.get_width() // 10, button_play_img.get_height() // 10))
    button_quit_img = pygame.transform.scale(button_quit_img, (button_quit_img.get_width() // 10, button_quit_img.get_height() // 10))

    # Définir les positions des boutons
    button_play_rect = button_play_img.get_rect(center=(conf_screen.WIDTH_SCREEN*(2/9), conf_screen.HEIGHT_SCREEN*(9/10)))
    button_quit_rect = button_quit_img.get_rect(center=(conf_screen.WIDTH_SCREEN*(7/9), conf_screen.HEIGHT_SCREEN*(9/10)))

    # Fonction pour vérifier si un bouton est cliqué
    def check_button_click(mouse_pos, button_rect):
        if button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def check_button_hover(mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)
    
    # Fonction pour appliquer un filtre de couleur assombrissant
    def darken_image(image, factor):
        # Créer une nouvelle surface pour l'image assombrie
        darkened_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        darkened_image.blit(image, (0, 0))  # Copier l'image originale sur la nouvelle surface

        # Appliquer l'effet d'assombrissement en multipliant les valeurs des pixels
        for x in range(darkened_image.get_width()):
            for y in range(darkened_image.get_height()):
                r, g, b, a = darkened_image.get_at((x, y))
                # Calculer les nouvelles valeurs RGB
                r = int(r * (1 - factor))
                g = int(g * (1 - factor))
                b = int(b * (1 - factor))
                darkened_image.set_at((x, y), (r, g, b, a))
        
        return darkened_image

    # Boucle pour gérer le menu
    while True:
        
        mouse_pos = pygame.mouse.get_pos()
        # Appliquer l'effet d'assombrissement si la souris survole un bouton
        if check_button_hover(mouse_pos, button_play_rect):
            play_img = darken_image(button_play_img, DARKEN_FACTOR)
        else:
            play_img = button_play_img

        if check_button_hover(mouse_pos, button_quit_rect):
            quit_img = darken_image(button_quit_img, DARKEN_FACTOR)
        else:
            quit_img = button_quit_img

        # Dessiner l'image de fond et les boutons
        screen.blit(background, (0, 0))  # Dessiner l'image de fond
        screen.blit(play_img, button_play_rect)  # Dessiner le bouton Jouer (assombri ou non)
        screen.blit(quit_img, button_quit_rect)  # Dessiner le bouton Quitter (assombri ou non)
        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Vérifier si on clique sur "Jouer"
                if check_button_click(mouse_pos, button_play_rect):
                    print("Lancement du jeu")
                    return "play"  # Retourne une valeur pour indiquer que le jeu doit démarrer

                # Vérifier si on clique sur "Quitter"
                if check_button_click(mouse_pos, button_quit_rect):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()