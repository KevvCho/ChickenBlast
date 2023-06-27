import pygame
from pygame.locals import *
from GUI.GUI_button import *
from GUI.GUI_button_image import *
from GUI.GUI_form import *
from GUI.GUI_label import *
from GUI.GUI_slider import *
from GUI.GUI_textbox import *
from GUI.GUI_widget import *

class FormMenuScore(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image, score, margen_y, margen_x, espacio):
        super().__init__(screen, x, y, w, h, color_background, color_border=-1, active=True)

        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image, (w,h))

        self._slave = aux_image
        self.score = score
        self._margeny_y = margen_y
        self.btn_back = Button_Image(self._slave, x, y, 30, 420, 50, 50, "sprites/extra/back.png", self.btn_click_back, "a")
        
        lbl_jugador = Label(self._slave, x=margen_x + 10, y=20, w=w/2-margen_x-10, h=50, text="Jugador",
                        font="Courier Normal", font_size=30, font_color="White", path_image="sprites/extra/bar.png")
        
        lbl_puntaje = Label(self._slave, x=margen_x + 10 + w/2 -margen_x-10, y=20, w=w/2-margen_x-10, h=50, text="Puntaje",
                        font="Courier Normal", font_size=30, font_color="White", path_image="sprites/extra/bar.png")
        
        self.lista_widgets.append(lbl_jugador)
        self.lista_widgets.append(lbl_puntaje)
        self.lista_widgets.append(self.btn_back)

        pos_inicial_y = margen_y

        for j in self.score:
            pos_inicial_x = margen_x

            for n,s in j.items():
                cadena = ""
                cadena = f"{s}"
                jugador = Label(self._slave, pos_inicial_x, pos_inicial_y , w/2-margen_x, 100, cadena, "Courier Normal", 30, "White", "sprites/extra/Table.png")
                self.lista_widgets.append(jugador)
                pos_inicial_x += w/2 - margen_x
            pos_inicial_y += 100 + espacio

    
    def btn_click_back(self, texto):
        self.close()


    def update(self, lista_eventos):
        if self.active:
            for wid in self.lista_widgets:
                wid.update(lista_eventos)
            self.draw()
