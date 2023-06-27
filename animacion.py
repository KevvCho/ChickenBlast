import pygame
from personaje import *

# Muestra la pantalla de game over junto a un fondo rojo por cierta cantidad de tiempo
def game_over(screen, game_over_time):

    main_font = pygame.font.SysFont("Humanst521 BT", 50)
    game_over_text = main_font.render("Game over", False, "Black")
    
    if game_over_time < 255:
        screen.fill((100+game_over_time,0,0))
        screen.blit(game_over_text, (500,300))

    game_over_time += 1

    return game_over_time
