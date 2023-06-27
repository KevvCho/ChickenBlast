from pygame.locals import *
from GUI.GUI_button import *
from GUI.GUI_button_image import *
from GUI.GUI_form import *

class FormNiveles(Form):
    def __init__(self, screen, x, y, w, h, volumen, color_background, color_border = "BLACK", border_size = -1, active=True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)

        self.volumen = volumen
        self.font = pygame.font.SysFont("Courier Normal", 25)
        # niveles
        self.board = pygame.image.load("sprites/extra/board.png").convert_alpha()
        self.board = pygame.transform.scale(self.board, (560,500))
        self.mapatuto = Button_Image(self._slave, x, y, 180, 40, 270, 80, "sprites/extra/tutorial.png", self.btn_click_nivel, "mapatuto")
        self.mapa1 = Button_Image(self._slave, x, y, 180, 130, 270, 80, "sprites/extra/nivel1.png", self.btn_click_nivel, "mapa1")
        self.mapa2 = Button_Image(self._slave, x, y, 180, 220, 270, 80, "sprites/extra/nivel2.png", self.btn_click_nivel, "mapa2")
        self.mapa3 = Button_Image(self._slave, x, y, 180, 310, 270, 80, "sprites/extra/nivel3.png", self.btn_click_nivel, "mapa3")
        self.mapa4 = Button_Image(self._slave, x, y, 180, 400, 270, 80, "sprites/extra/boss.png", self.btn_click_nivel, "mapa4")
        self.btn_back = Button_Image(self._slave, x, y, 70, 400, 70, 70, "sprites/extra/back.png", self.btn_click_back, "a")



        self.lista_widgets.append(self.mapatuto)
        self.lista_widgets.append(self.mapa1)
        self.lista_widgets.append(self.mapa2)
        self.lista_widgets.append(self.mapa3)
        self.lista_widgets.append(self.mapa4)
        self.lista_widgets.append(self.btn_back)
    
    def render(self):
        self._slave.fill(self._color_background)
        self._slave.blit(self.board, (20,20))

    def btn_click_back(self, texto):
        self.close()

    def btn_click_nivel(self, texto):
        self.padre.nivel = texto
        self.close()
