import pygame
from pygame.locals import *

from GUI.GUI_button import *
#No se instancia. Es la base de la jerarquia
class Form(Widget):
    def __init__(self, screen, x,y,w,h, color_background,color_border = "Black", border_size = -1, active = True):
        super().__init__(screen, x,y,w,h, color_background, color_border, border_size)
        self._slave = pygame.Surface((w,h))
        self.slave_rect = self._slave.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active
        self.lista_widgets = []
        self.volumen = 0.05
        self.nivel = ""
        self.nombre = ""
        self.pausa = False
        self.quit = False
        self.hijo = None
        self.dialog_result = None
        self.padre = None
    
    def show_dialog(self, formulario):
        self.hijo = formulario
        self.hijo.padre = self

    def close(self):
        self.padre.hijo = None

    def verificar_dialog_result(self):
        return self.hijo == None or self.hijo.dialog_result != None
 
    def render(self):
        pass
    
    def update_volumen(self):
        pygame.mixer.music.set_volume(self.volumen)
    
    def update(self, lista_eventos):

        if self.nivel != "":
            self.active = False

        if self.active:
            if self.verificar_dialog_result():
                if self.active:
                    self.draw()
                    self.render()
                    for widget in self.lista_widgets:
                        widget.update(lista_eventos)
            else:
                self.hijo.update(lista_eventos)
        
    
