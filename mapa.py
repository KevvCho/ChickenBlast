import pygame,csv
from pygame import mixer
from personaje import *
from modo import creador_logs

COLS = 520
ROWS = 20
TILE_SIZE = 32

class World():
    def __init__(self, screen, map):
        self.screen = screen
        self.goal_list = []
        self.obstacle_list = []
        self.decoration_list = []
        self.damage_list = []
        self.item_hp_list = []
        self.item_score_list = []
        self.enemy_group = []
        self.current_map = map
        self.bg = pygame.image.load(f"sprites/bgs/default.png").convert_alpha()
        self.map_width = self.bg.get_width()

    def generar_tiles(self, screen, map, scale_factor, TILE_SIZE, ROWS, COLS, SCREEN_WIDTH, SCREEN_HEIGHT):

        # Crear grupos de enemigos
        enemy_group_stat = pygame.sprite.Group()
        enemy_group_anim = pygame.sprite.Group()
        enemy_group_boss = pygame.sprite.Group()

        # Obtener las texturas
        img_list = cargar_imagenes_tiles(TILE_SIZE)

        # Cargar el mundo a partir del csv
        data = cargar_mundo(map, ROWS, COLS)

        # Fondo del nivel
        self.bg = cargar_fondo(map, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Longitud del fondo
        self.map_width = self.bg.get_width()

        # Longitud del nivel
        self.level_length = len(data[0])

        # Asignacion de tile por numero
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile > -1:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 3:
                        self.damage_list.append(tile_data)
                    if tile != -1 and tile < 15:
                        self.obstacle_list.append(tile_data)
                    if tile >= 15 and tile < 32 and tile != 28 and tile != 30:
                        self.decoration_list.append(tile_data)
                    elif tile == 28:
                        self.item_score_list.append(tile_data)
                    elif tile == 30:
                        self.item_hp_list.append(tile_data)
                    elif tile == 32:
                        self.goal_list.append(tile_data)
                    elif tile == 33:
                        enemy = Personaje(screen, "enemigo_boss", x * TILE_SIZE, y * TILE_SIZE, 2,3, scale_factor, self)
                        enemy.hp = 10
                        enemy_group_boss.add(enemy)
                    elif tile == 34:
                        enemy = Personaje(screen, "enemigo_static", x * TILE_SIZE, y * TILE_SIZE, 2,3, scale_factor, self)
                        enemy_group_stat.add(enemy)
                    elif tile == 35:
                        enemy = Personaje(screen, "enemigo_anim", x * TILE_SIZE, y * TILE_SIZE, 2,3, scale_factor, self)
                        enemy_group_anim.add(enemy)

        # Agregar enemigos a sus respectivos grupos
        self.enemy_group.append(enemy_group_boss)
        self.enemy_group.append(enemy_group_stat)
        self.enemy_group.append(enemy_group_anim)
        

    # Bliteo de las tiles en la pantalla
    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.damage_list:
            screen.blit(tile[0], tile[1])
        for tile in self.goal_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])    
        for tile in self.decoration_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.item_hp_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.item_score_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            
            
    # Bliteo del fondo
    def draw_bg(self, screen, screen_scroll):
        screen.fill((0,100,100))
        for i in range (20):
            screen.blit(self.bg, ((i * self.map_width) - screen_scroll, 0))

# Se encarga de cargar todas las tiles en la carpeta indicada
def cargar_imagenes_tiles(TILE_SIZE) -> list:
    img_list = []
    for x in range(36):
        img = pygame.image.load(f'sprites/tiles/{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    return img_list


# Carga el fondo segun el mapa indicado y de no haberlo carga una imagen en negro
def cargar_fondo(map, SCREEN_WIDTH, SCREEN_HEIGHT):

    try:
        bg = pygame.image.load(f"sprites/bgs/{map}.png").convert_alpha()
    except:
        bg = pygame.image.load(f"sprites/bgs/default.png").convert_alpha()
    
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH * 2, SCREEN_HEIGHT))
    

    return bg

# Devuelve un mapa vacio para poder ser cargado nuevamente
def resetear_mapa(ROWS, COLS) -> list:
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    return world_data

# Genera un mapa vacio y a partir del csv con el nombre del mapa genera 
# una lista con sus respectivos x,y
def cargar_mundo(current_map, ROWS, COLS):

    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    try:
        if current_map != "menu":
            with open(f'Mapas/{current_map}.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
    except Exception as e:
        creador_logs(e)

    return world_data
    
# Elige la cancion del nivel y devuelve el grupo de enemigos en el nivel
def generar_nivel(screen, world, current_map, scale_factor, SCREEN_WIDTH, SCREEN_HEIGHT):

    lista_canciones = generar_lista_canciones()

    
    world.current_map = current_map
    world.generar_tiles(screen, world.current_map, scale_factor, TILE_SIZE, ROWS, COLS, SCREEN_WIDTH, SCREEN_HEIGHT)
    enemy_group = world.enemy_group
    cambiar_canciones(world.current_map, lista_canciones)

    return enemy_group

# Cambia la cancion del nivel seleccionado, en caso de no haberlo carga un archivo sin sonido
def cambiar_canciones(map, lista_canciones):

    cancion = ""
    if map == "mapatuto":
        cancion = lista_canciones[0][0]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "mapa1":
        cancion = lista_canciones[0][1]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "mapa2":
        cancion = lista_canciones[0][2]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "mapa3":
        cancion = lista_canciones[0][3]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "mapa4":
        cancion = lista_canciones[0][4]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "menu":
        cancion = lista_canciones[1][0]
        mixer.music.load(cancion)
        mixer.music.play(-1)
    elif map == "cutscene":
        cancion = lista_canciones[1][1]
        mixer.music.load(cancion)
        mixer.music.play()
    elif map == "ending":
        cancion = lista_canciones[1][2]
        mixer.music.load(cancion)
        mixer.music.play()
    else:
        cancion = "Musica/silence.mp3"
        mixer.music.load(cancion)
        mixer.music.play(-1)
    
    
# Busca canciones en la lista seleccionada y devuelve una lista con niveles y extras
def generar_lista_canciones() -> list:

    lista_canciones = []

    lista_niveles = []
    for i in range(5):
        cancion = f"Musica/map{i}.mp3"
        lista_niveles.append(cancion)

    lista_canciones.append(lista_niveles)
    
    lista_extra = []
    for i in range(3):
        cancion = f"Musica/extra{i+1}.mp3"
        lista_extra.append(cancion)

    lista_canciones.append(lista_extra)
    
    
    return lista_canciones
    
