import pygame, os, random, sqlite3

class Personaje(pygame.sprite.Sprite):
    def __init__(self, screen, chartype, x, y, speed, hp, scale, world):
        super().__init__()
        self.world = world
        self.screen = screen
        self.chartype = chartype
        self.alive = True
        self.hp = hp
        self.hit = False
        self.hit_count = 0
        self.invencibility_frames = 255
        self.nombre = ""
        self.score = 0
        self.level_cleared = False
        self.lista_hp = []
        for i in range(4):
            hp_bar = pygame.image.load(f"sprites/hp/{i}.png").convert_alpha()
            hp_bar = pygame.transform.scale(hp_bar, (130, 30))
            self.lista_hp.append(hp_bar)
        # Pos actual icon
        self.pos_icon = pygame.image.load("sprites\extra\me.png").convert_alpha()
        self.pos_icon = pygame.transform.scale(self.pos_icon, (25, 25))
        self.pos_icon_rect = self.pos_icon.get_rect()
        self.end_icon = pygame.image.load("sprites\extra\end.png").convert_alpha()
        self.end_icon = pygame.transform.scale(self.end_icon, (30, 30))
        # Camara
        self.camera_x = 0
        self.can_touch_edge = False
        self.character_margin = 500
        self.screen_scroll = 0
        # Movimiento
        self.bandera_proyectil = False
        self.is_jumping = False
        self.crouch = False
        self.in_air = True
        self.jump_velocity = 10
        self.crouched = False
        self.dash = False
        self.light_dash = False
        self.light_dash_counter = 0
        # Sonidos
        self.lista_sonidos = []
        cantidad_sonidos = len(os.listdir(f"sfx/"))
        for i in range(cantidad_sonidos):
            sonido = pygame.mixer.Sound(f"sfx/{i}.mp3")
            sonido.set_volume(0.04)
            self.lista_sonidos.append(sonido)
        # Animacion
        self.last_position = "right"
        self.flip = False
        self.animation_list = []
        self.frame = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        if self.chartype == "jugador":
            animation_types =['idle', 'run', 'jump', 'dash', 'crouch', 'slide', 'slide_dash', 'light_dash', 'cleared', 'shoot']
        elif self.chartype == "enemigo_static":
            animation_types =['idle']
        elif self.chartype == "enemigo_anim":
            animation_types =['idle', 'run']
        elif self.chartype == "enemigo_boss":
            animation_types =['idle', 'run']
        for animation in animation_types:
            temp_list = []
            num_frames = len(os.listdir(f"sprites/{self.chartype}/{animation}"))
            for i in range(num_frames):
                img = pygame.image.load(f"sprites/{self.chartype}/{animation}/{i}.png").convert_alpha()
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.scale_by(scale)
        self.rect.center = (x, y)
        self.speed = speed
        self.dx = 0
        self.dy = 0
        # Movimiento ia
        self.move_counter = 0
        self.direction = 1
        self.idling = False
        self.idle_counter = 0
    
    # Bliteo del personaje seguido por la camara
    def draw_follow(self):

        # Cambiar posicion del sprite si esta agachado para no atravesar el suelo
        if self.crouch:
            self.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-40, self.rect.y-80, self.image.get_width(), self.image.get_height()))
        else:
            self.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-5, self.rect.y-17, self.image.get_width(), self.image.get_height()))

    # Bliteo del personaje sin seguimiento de la camara
    def draw(self, offset=5, idle_offset=1):
        if not self.idling:
            self.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -self.camera_x, self.rect.y-offset))
        else:
            self.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -self.camera_x, self.rect.y-idle_offset))
    
    def update(self, world, posicion_click, SCREEN_WIDTH):
        
        # Actualizacion del nivel
        self.world = world

        # Movimiento
        keys = pygame.key.get_pressed()
        mover_izquierda = False
        mover_derecha = False

        if self.alive and not self.level_cleared:
            self.draw_follow()
            if keys[pygame.K_a]:
                mover_izquierda = True
                self.last_position = "left"
            else:
                mover_izquierda = False

            if keys[pygame.K_d]:
                mover_derecha = True
                self.last_position = "right"
            else:
                mover_derecha = False
            
            if keys[pygame.K_w]:
                self.is_jumping = True
            
            if keys[pygame.K_s]:
                self.crouch = True
            else:
                self.crouch = False
                
            # Dash
            if keys[pygame.K_LSHIFT]:
                self.dash = True
            else:
                self.dash = False

         # Animacion
        if self.is_jumping and not self.light_dash and not self.bandera_proyectil:
            self.update_action(2)
        elif self.light_dash:
            self.update_action(7)
        elif (mover_izquierda or mover_derecha) and not self.dash and not self.crouch and not self.bandera_proyectil:
            self.update_action(1)
        elif self.dash and (mover_izquierda or mover_derecha) and not self.crouch and not self.bandera_proyectil:
            self.update_action(3)
        elif self.crouch and not self.dash and not mover_izquierda and not mover_derecha:
            self.update_action(4)
        elif self.crouch and (mover_izquierda or mover_derecha) and not self.dash:
            self.update_action(5)
        elif self.crouch and self.dash and (mover_izquierda or mover_derecha):
            self.update_action(6)
        elif self.bandera_proyectil:
            self.update_action(9)
        elif not self.level_cleared:
            self.update_action(0)
        
        self.screen_scroll = self.move(mover_izquierda, mover_derecha, posicion_click, SCREEN_WIDTH)
        
        self.camera_x -= self.screen_scroll

        self.update_animation()

        # Daño
        if self.hit:
            self.animar_daño()
            self.hit_count += 1
            if self.hit_count > 60 * 2:
                self.hit = False
                self.hit_count = 0
        else:
            self.image.set_alpha(255)

        # Fuera de mapa
        if self.rect.y > 700:
            self.hp = 0

        # Health bar
        if self.hp < 0:
            self.hp = 0
        self.screen.blit(self.lista_hp[self.hp], (1050, 562))

        # Pos actual
        if self.world.current_map != "mapa4":

            self.pos_icon_rect.x = 190
            self.pos_icon_rect.y = 5
            pygame.draw.line(self.screen, "BLUE", (200, 30), (SCREEN_WIDTH - 200, 30), 5)
            if self.camera_x < 7980:
                self.pos_icon_rect.x += self.camera_x /(self.world.level_length/(self.world.level_length/10)) 
            else:
                self.pos_icon_rect.x = 982
            self.screen.blit(self.pos_icon, self.pos_icon_rect)
            self.screen.blit(self.end_icon, (998, 2))

        
        # Movimiento camara boss
        if self.world.current_map == "mapa4":
            self.screen_scroll = 0
            self.camera_x = 0
            self.can_touch_edge = True
        else:
            self.can_touch_edge = False

        # Nombre
        if self.nombre == "":
            self.nombre = "Sin nombre"
        
    # Actualizar frames en la animacion
    def update_animation(self, animation_cooldown=20):

        # Compara tiempos de ejecucion con el actual para cambiar frame
        self.image = self.animation_list[self.action][self.frame]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
        
        if self.frame >= len(self.animation_list[self.action]):
            self.frame = 0


    def update_action(self, new_action):

        # Cambiar animacion actual por nueva
        if new_action != self.action:
            self.action = new_action
            self.frame = 0
            self.update_time = pygame.time.get_ticks()


    def move(self, mover_izquierda, mover_derecha, posicion_click, screen_width=1200):

        self.dx = 0
        self.dy = 0
        screen_scroll = 0
        

        if mover_izquierda:
            self.dx = -self.speed
            self.flip = True
            
        if mover_derecha:
            self.dx = self.speed
            self.flip = False
            
        if self.dash:
            self.speed = 8
        else:
            self.speed = 5

        # Agacharse
        if self.crouch:
            scale_factor = 0.2
            self.rect.update(self.rect.x, self.rect.y, self.image.get_width()*scale_factor,self.image.get_height()*scale_factor)
        else:
            scale_factor = 0.8
            self.rect.update(self.rect.x, self.rect.y, self.image.get_width()*scale_factor,self.image.get_height()*scale_factor)

        if self.rect.y <= 400:
            self.crouched = False

        # Saltar
        if self.is_jumping == True and self.in_air == False:
            self.jump_velocity = -11
            self.is_jumping = False
            self.in_air = True
            self.lista_sonidos[4].play()

        # Dash aereo
        if self.light_dash:
            target_x, target_y = posicion_click
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            speed = 20
            if distance != 0:
                self.dx += (dx / distance) * speed
                self.dy += (dy / distance) * speed
            self.light_dash_counter += 1
            self.jump_velocity = 0

        if self.light_dash_counter > 20:
            self.lista_sonidos[1].play()
            self.light_dash = False
            self.light_dash_counter = 0

        # Gravedad
        self.jump_velocity += 0.65

        self.dy += self.jump_velocity

        # Interaccion con tiles
        # End goal
        for tile in self.world.goal_list:
            if tile[1].colliderect(self.rect):
                self.level_cleared = True

        # Daño con pinchos
        for tile in self.world.damage_list:
            if tile[1].colliderect(self.rect):
                if self.hit_count == 0 and not self.hit:
                    self.hit = True
                    self.hp -= 1

        # Bloques solidos
        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect.x + self.dx, self.rect.y - 5, self.image.get_width()*scale_factor, self.image.get_height()*scale_factor):
                self.dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.image.get_width()*scale_factor, self.image.get_height()*scale_factor):
                if self.jump_velocity < 0:
                    self.jump_velocity = 0
                    self.dy = tile[1].bottom - self.rect.top
                elif self.jump_velocity >= 0:
                    self.jump_velocity = 0
                    self.is_jumping = False
                    self.in_air = False
                    self.rect.y = tile[1].top - self.rect.height

        # Objeto vida
        for tile in self.world.item_hp_list:
            if tile[1].colliderect(self.rect):
                if self.hp != 3:
                    self.hp += 1
                else:
                    self.score += 200
                tile[1].y = -2000
                self.lista_sonidos[3].play()
        
        # Objeto score
        for tile in self.world.item_score_list:
            if tile[1].colliderect(self.rect):
                self.score += 100
                tile[1].y = -2000
                self.lista_sonidos[2].play()
       

         # Movimiento del personaje
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Delimitar camara en mapa
        if not self.can_touch_edge:
            if (self.rect.right > screen_width - self.character_margin and
                self.camera_x < (self.world.level_length * 28.5) - screen_width) or (self.rect.left < self.character_margin and
                                                                            self.camera_x > abs(self.dx)):
                self.rect.x -= self.dx
                screen_scroll = -self.dx
            if self.rect.left + self.dx < 0 or self.rect.right + self.dx > screen_width:
                    self.dx = 0
        
        return screen_scroll
    
    # Hace al personaje semi transparente por unos segundos
    def animar_daño(self):
        
        # Animacion de daño
        if self.invencibility_frames < 100:
            self.invencibility_frames = 255
        else:
            self.invencibility_frames -= 20

        self.image.set_alpha(self.invencibility_frames)
        
        
    def ai_movement(self, scroll, obstacle_list, scale_factor):

        if self.idling == False:

            self.dy = 0
            if self.direction == 1:
                moving_right = True
            else:
                moving_right = False
            moving_left = not moving_right

            # Tiempo random para dejar de moverse
            if random.randint(1,300) == 1:
                self.idling = True

            
            self.ai_move(moving_right, moving_left, scroll)
            self.update_action(1)
            self.idle_counter = 120

            self.move_counter += 1

            # Cambiar de direccion cada cierto tiempo
            if self.move_counter > 100:
                self.move_counter = 0
                self.direction *= -1
                self.dx = 0

            # Gravedad
            self.jump_velocity += 0.65
            
            self.dy += self.jump_velocity
            self.rect.y += self.dy
        else:
            # Detener movimiento
            self.dx = 0
            self.ai_move(False, False, scroll)
            self.update_action(0)
            self.idle_counter -= 1
            if self.idle_counter <= 0:
                self.idling = False

        # Interaccion con tiles
        for tile in obstacle_list:
            if tile[1].colliderect(self.rect.x + self.dx, self.rect.y - 5, self.image.get_width()*scale_factor, self.image.get_height()*scale_factor):
                self.dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy + 15, self.image.get_width()*scale_factor, self.image.get_height()*scale_factor):
                if self.jump_velocity < 0:
                    self.jump_velocity = 0
                    self.dy = tile[1].bottom - self.rect.top
                elif self.jump_velocity >= 0:
                    self.jump_velocity = 0
                    self.rect.y = tile[1].top - self.rect.height

        
    
    def ai_move(self, mover_izquierda, mover_derecha, scroll):

       
        self.rect.x += scroll
        if mover_izquierda:
            self.dx = -self.speed
            self.flip = True

        if mover_derecha:
            self.dx = self.speed
            self.flip = False

        self.rect.x += self.dx
        self.rect.y += self.dy
    

    def guardar_puntaje(self):
        # Establecer una conexión con la base de datos y crear la tabla de puntajes
        conexion = sqlite3.connect('puntajes.db')
        cursor = conexion.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS puntajes(jugador TEXT, score INTEGER)')

        # Buscar el jugador en los puntajes existentes
        cursor.execute('SELECT * FROM puntajes WHERE jugador = ?', (self.nombre,))
        resultado = cursor.fetchone()

        if resultado:
            # Actualizar el puntaje si es mayor que el existente
            if self.score > resultado[1]:
                cursor.execute('UPDATE puntajes SET score = ? WHERE jugador = ?', (self.score, self.nombre))
        else:
            # Insertar el nuevo puntaje en la tabla de puntajes
            cursor.execute('INSERT INTO puntajes(jugador, score) VALUES(?, ?)', (self.nombre, self.score))

        conexion.commit()
        conexion.close()