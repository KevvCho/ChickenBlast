import pygame
from modo import *
from personaje import *
from proyectil import *
from mapa import *
from animacion import *
from GUI.GUI_form_main import *


FPS = 60

# Dimensiones de la ventana
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Inicialización de Pygame
pygame.init()

# Creación de la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chicken Blast")
windows_icon = pygame.image.load("sprites\extra\icon.png").convert_alpha()
pygame.display.set_icon(windows_icon)



background_menu = pygame.image.load("sprites/extra/bg.png").convert_alpha()
background_menu = pygame.transform.scale(background_menu, (screen.get_width(),screen.get_height()))

# Posición inicial del sprite
sprite_x = SCREEN_WIDTH - 800
sprite_y = SCREEN_HEIGHT - 180

# Creación del reloj para controlar los FPS
clock = pygame.time.Clock()

# Jugador
scale_factor = 0.8
mover_izquierda = False
mover_izquierda = False
game_over_time = 0

# Proyectil
proyectil_group = pygame.sprite.Group()
shoot_cooldown = 0
proyectil = Proyectil(screen, 0, -500, "jugador")

# Dash aereo
posicion_click = 0

# Score
score_enem_static = 10
score_enem_anim = 50
score_enem_boss = 300

# Fuente texto
pygame.font.init()
main_font = pygame.font.SysFont("Humanst521 BT", 25)
score_font = pygame.font.SysFont("Courier Normal", 35)

# Mapa
current_map = "menu"
screen_scroll = 0

# Musica
volumen = 0.05
lista_canciones = generar_lista_canciones()
cambiar_canciones(current_map, lista_canciones)

# Menu
start_game = False
form_menu = FormMenu(screen, 300, 20, 600, 550, (204,226,225), "Yellow", -1, True)


########################## Bucle principal del juego ###################################
running = True
while running:
    

    current_time = pygame.time.get_ticks()
    lista_eventos = pygame.event.get()

    # Menu
    if start_game == False:
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                running = False       
        
        #screen.fill("Black")
        screen.blit(background_menu, (0,0))
        form_menu.update(lista_eventos)
        if form_menu.nivel != "":
            world = World(screen, current_map)
            enemy_group = generar_nivel(screen,world, form_menu.nivel, scale_factor, SCREEN_WIDTH, SCREEN_HEIGHT)
            jugador = Personaje(screen, "jugador", sprite_x, sprite_y, 5,3, scale_factor, world)
            jugador.nombre = form_menu.nombre
            start_game = True
        
        if form_menu.quit == True:
            running = False


    # Inicio del juego
    else:
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    world.current_map = "menu"
                    cambiar_canciones(world.current_map, lista_canciones)          
                    start_game = False
                    form_menu.active = True
                    form_menu.nivel = ""
                if event.key == pygame.K_TAB:
                    cambiar_modo()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    jugador.bandera_proyectil = True
                if event.button == 3:
                    jugador.light_dash = True
                    posicion_click = event.pos

        keys = pygame.key.get_pressed()

        # Dibujar nivel
        world.draw_bg(screen, jugador.camera_x)
        world.draw(screen, jugador.screen_scroll)


        # Enemigos en grupo
        #Boss
        for enemigo in enemy_group[0]:
            if enemigo.alive:
                enemigo.ai_movement(jugador.screen_scroll, world.obstacle_list, scale_factor)
                enemigo.update_animation(70)
                enemigo.draw(5, 20)
            if proyectil.rect.colliderect(enemigo.rect):
                proyectil.rect.y = 1200
                enemigo.hp -= 1
            if enemigo.hp == 0:
                enemigo.alive = False
                enemigo.kill()
                jugador.score += score_enem_boss
                jugador.level_cleared = True
            if enemigo.rect.colliderect(jugador.rect):
                if jugador.hit_count == 0:
                    jugador.hit = True
                    jugador.hp -= 1

        # Enemigo estatico
        for enemigo in enemy_group[1]:
            if enemigo.alive:
                enemigo.ai_move(False, False, jugador.screen_scroll)
                enemigo.update_animation(20)
                enemigo.draw()
            if proyectil.rect.colliderect(enemigo.rect):
                proyectil.rect.y = 1200
                enemigo.hp -= 1
            if enemigo.hp == 0:
                enemigo.alive = False
                jugador.score += score_enem_static
                enemigo.kill()
            if enemigo.rect.colliderect(jugador.rect):
                if jugador.light_dash:
                    enemigo.hp = 0
                elif jugador.hit_count == 0:
                    jugador.hit = True
                    jugador.hp -= 1

        # Enemigo en movimiento
        for enemigo in enemy_group[2]:
            if enemigo.alive:
                enemigo.ai_movement(jugador.screen_scroll, world.obstacle_list, scale_factor)
                enemigo.update_animation(70)
                enemigo.draw(15, 15)
            if proyectil.rect.colliderect(enemigo.rect):
                proyectil.rect.y = 1200
                enemigo.hp -= 1
            if enemigo.hp == 0:
                enemigo.alive = False
                jugador.score += score_enem_anim
                enemigo.kill()
            if enemigo.rect.colliderect(jugador.rect):
                if jugador.light_dash:
                    enemigo.hp = 0
                elif jugador.hit_count == 0:
                    jugador.hit = True
                    jugador.hp -= 1
                    

        # Lanzar proyectil
        if jugador.bandera_proyectil:
            if shoot_cooldown == 0:
                jugador.lista_sonidos[5].play()
                shoot_cooldown = 10
                proyectil = Proyectil(screen, jugador.rect.centerx, jugador.rect.centery, "jugador")
                proyectil_group.add(proyectil)
                proyectil.on_screen = True

                if proyectil.on_screen:
                    jugador.bandera_proyectil = False     
            shoot_cooldown -= 1

        if proyectil.on_screen:
            proyectil.update(SCREEN_WIDTH, jugador.last_position, world.obstacle_list)
            

        # Actualizacion jugador
        jugador.update(world, posicion_click,SCREEN_WIDTH)


        # Score Jugador
        jugador_score = score_font.render(f"Score: {jugador.score}", False, "White")
        screen.blit(jugador_score, (20,SCREEN_HEIGHT- 40))
        

         # Vida jugador
        if jugador.hp == 0:
            jugador.alive = False
            jugador.screen_scroll = 0
            if game_over_time > FPS * 2:
                current_map = world.current_map
                world = World(screen, current_map)
                enemy_group = generar_nivel(screen, world, current_map, scale_factor, SCREEN_WIDTH, SCREEN_HEIGHT)
                jugador = Personaje(screen, "jugador", sprite_x, sprite_y, 5,3, scale_factor, world)
                game_over_time = 0
            game_over_time = game_over(screen, game_over_time)

        # Final nivel
        if jugador.level_cleared == True:
            jugador.screen_scroll = 0
            jugador.hit_count += 1
            if jugador.hit_count == 1:
                jugador.lista_sonidos[0].play()
            if jugador.hit_count > FPS * 2:
                jugador.guardar_puntaje()
                world.current_map = "menu"
                cambiar_canciones("menu", lista_canciones)          
                start_game = False
                form_menu.active = True
                form_menu.nivel = ""
            jugador.draw_follow()
            jugador.update_action(8)
            jugador.update_animation(40)

        # Debug mode
        if get_mode():
            camera_debug = main_font.render(f"camera_x:{int(jugador.camera_x)}", False, (0, 0, 0), "White")
            sprite_x_debug = main_font.render(f"sprite_x:{jugador.rect.x}", False, (0, 0, 0), "White")
            sprite_y_debug = main_font.render(f"sprite_y:{jugador.rect.y}", False, (0, 0, 0), "White")
            jumping_debug = main_font.render(f"is_jumping:{jugador.is_jumping}", False, (0, 0, 0), "White")
            speed_debug = main_font.render(f"sprite_speed:{jugador.speed}", False, (0, 0, 0), "White")
            bandera_proyectil_debug = main_font.render(f"bandera_proyectil:{jugador.bandera_proyectil}", False, (0, 0, 0), "White")
            screen.blit(camera_debug, (1030,0))
            screen.blit(sprite_x_debug, (1030,20))
            screen.blit(sprite_y_debug, (1030,40))
            screen.blit(speed_debug, (1030,60))
            screen.blit(jumping_debug, (1030,80))
            screen.blit(bandera_proyectil_debug, (1000,100))
            pygame.draw.rect(screen, "Green", jugador.rect, 2)

            # Reset position
            if keys[pygame.K_l]:
                jugador.rect.x = SCREEN_WIDTH - 800
                jugador.rect.y = SCREEN_HEIGHT - 220
                jugador.jump_velocity = 0
                jugador.dy = 0
                jugador.dx = 0
                jugador.is_jumping = False

            # Reset nivel
            if keys[pygame.K_p]:
                reset_debug = main_font.render("RESET", False, (0, 0, 0), "Red")
                screen.blit(reset_debug, (SCREEN_WIDTH/2,60))
                current_map = world.current_map
                world = World(screen, current_map)
                enemy_group = generar_nivel(screen, world, current_map, scale_factor, SCREEN_WIDTH, SCREEN_HEIGHT)
                jugador = Personaje(screen, "jugador", sprite_x, sprite_y, 5,3, scale_factor, world)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    print(f"Posicion actual del mouse: X :{mouse_pos[0]} Y: {mouse_pos[1]}")
                    pygame.draw.rect(screen, "Yellow", proyectil.rect, 2)

            for tile in world.obstacle_list:
                pygame.draw.rect(screen, "White", tile[1], 2)
            for tile in world.damage_list:
                pygame.draw.rect(screen, "Red", tile[1], 2)
            for tile in world.goal_list:
                pygame.draw.rect(screen, "Cyan", tile[1], 2)

            for enemigo in enemy_group[0]:
                pygame.draw.rect(screen, "Red", enemigo, 2)
            for enemigo in enemy_group[1]:
                pygame.draw.rect(screen, "Red", enemigo, 2)
            for enemigo in enemy_group[2]:
                pygame.draw.rect(screen, "Red", enemigo, 2)


    # Actualiza la ventana
    pygame.display.flip()

    # Controla los FPS deljuego
    clock.tick(FPS)

# Cierra Pygame al salir del juego
pygame.quit()