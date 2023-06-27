import pygame, os

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,screen,x,y, chartype):
        super().__init__()
        self.screen = screen
        self.speed = 15
        self.index = 0
        self.chartype = chartype
        self.flip = False
        self.animation_list = []
        self.frame = 0
        self.update_time = pygame.time.get_ticks()
        num_frames = len(os.listdir(f"sprites/{self.chartype}/proyectil"))
        for i in range(num_frames):
            img = pygame.image.load(f"sprites/{self.chartype}/proyectil/{i}.png")
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.alpha = 300
        self.on_screen = False
        self.is_moving = False
        
    
    def update(self, screen_width, last_position, obstacle_list):
        
        if not self.is_moving:
            if last_position == "left":
                self.flip = True
            else:
                self.flip = False
            self.is_moving = True

        if self.flip:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        for tile in obstacle_list:
            if tile[1].colliderect(self.rect):
                self.rect.y = 1200
        if self.rect.x < -20 or self.rect.x > screen_width-100: 
                self.rect.y = 1200

        self.alpha -= 7
        self.image.set_alpha(self.alpha)
        self.update_animation()
        self.draw()

    
    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-5, self.rect.y, self.image.get_width(), self.image.get_height()))
        

    def update_animation(self):

        animation_cooldown = 20
        self.image = self.animation_list[self.frame]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
        
        if self.frame >= len(self.animation_list):
            self.frame = 0