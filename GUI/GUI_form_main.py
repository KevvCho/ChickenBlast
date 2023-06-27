import pygame
from pygame.locals import *
from GUI.GUI_button_image import *
from GUI.GUI_form import *
from GUI.GUI_form_opciones import *
from GUI.GUI_form_niveles import *

class FormMenu(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border = "BLACK", border_size = -1, active=True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)

        pygame.mixer.init()
        
        # Menu

        self.board = pygame.image.load("sprites/extra/board.png").convert_alpha()
        self.board = pygame.transform.scale(self.board, (560,500))
        self.logo = pygame.image.load("sprites/extra/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (290,150))
        self.btn_play = Button_Image(self._slave, x, y, 110, 160, 390, 109, "sprites/extra/menu1.png", self.btn_click_play, "a")
        self.btn_options = Button_Image(self._slave, x, y, 110, 270, 390, 109, "sprites/extra/menu2.png", self.btn_click_opciones, "a")
        self.btn_quit = Button_Image(self._slave, x, y, 110, 380, 390, 109, "sprites/extra/menu3.png", self.btn_click_quit, "a")

        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.btn_options)
        self.lista_widgets.append(self.btn_quit)

    
    def render(self):
        self._slave.fill(self._color_background)
        self._slave.blit(self.board, (20,20))
        self._slave.blit(self.logo, (150,20))
        self.update_volumen()
        
    def btn_click_play(self, lista_eventos):
        form_opciones = FormNiveles(self._master, 300, 20, 600, 550, self.volumen, (204,226,225), "Magenta", -1, True)
        self.show_dialog(form_opciones)

    def btn_click_opciones(self, lista_eventos):
        form_opciones = FormOpciones(self._master, 300, 20, 600, 550, self.volumen, (204,226,225), "Magenta", -1, True)
        self.show_dialog(form_opciones)
    
    def btn_click_quit(self, lista_eventos):
        self.quit = True