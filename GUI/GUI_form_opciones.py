import pygame, sqlite3
from pygame.locals import *
from GUI.GUI_button import *
from GUI.GUI_button_image import *
from GUI.GUI_form import *
from GUI.GUI_label import *
from GUI.GUI_slider import *
from GUI.GUI_textbox import *
from GUI.GUI_widget import *
from GUI.GUI_form_score import *

class FormOpciones(Form):
    def __init__(self, screen, x, y, w, h, volumen, color_background, color_border = "BLACK", border_size = -1, active=True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)

        self.volumen = volumen
        self.dic_score = self.leer_puntajes()

        # Opciones
        self.font = pygame.font.SysFont("Courier Normal", 35)
        self.slider = pygame.image.load("sprites/extra/slider.png").convert_alpha()
        self.slider = pygame.transform.scale(self.slider, (430,100))
        self.board = pygame.image.load("sprites/extra/board.png").convert_alpha()
        self.board = pygame.transform.scale(self.board, (560,500))
        self.txtbox = TextBox(self._slave, x, y, 90, 125, 150, 30, "Gray", "White", "Red", "Blue", 2,font="Comic Sans", font_size=15, font_color="BLACK")
        self.btn_submit = Button_Image(self._slave, x, y, 260, 120, 40, 40, "sprites/extra/button submit.png", self.btn_click_submit, "a")
        self.label_volumen = Label(self._slave, 90, 190, 110, 50,"20%", "Courier Normal", 30, "White", "sprites/extra/Table.png")
        self.slider_volumen = Slider(self._slave, x, y, 110, 290, 380, 10, self.volumen, "Blue", "White")
        self.btn_back = Button_Image(self._slave, x, y, 70, 400, 70, 70, "sprites/extra/back.png", self.btn_click_back, "a")
        self.btn_scores = Button_Image(self._slave, x, y, 430, 400, 70, 70, "sprites/extra/leaderboard.png", self.btn_scores_click, "a")

        self.lista_widgets.append(self.txtbox)
        self.lista_widgets.append(self.btn_submit)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_back)
        self.lista_widgets.append(self.btn_scores)

        self.musica_text = self.font.render("Musica", False, "White")
        self.nombre_jugador = self.font.render("Cambiar nombre", False, "White")
    
    def render(self):
        self._slave.fill(self._color_background)
        self._slave.blit(self.board, (20,20))
        self._slave.blit(self.slider, (90,250))
        self._slave.blit(self.musica_text, (220,200))
        self._slave.blit(self.nombre_jugador, (310,130))
        self.update_volumen()

    def update_volumen(self):
        self.volumen = self.slider_volumen.value
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)

    def btn_click_back(self, texto):
        self.close()

    def btn_scores_click(self, texto):
        form_puntaje = FormMenuScore(self._master, 350, 20, 500, 550, (220,0,220), "White", True, "sprites/extra/Window.png", self.dic_score, 100, 10, 10)
        self.show_dialog(form_puntaje)

    
    def btn_click_submit(self,texto):
      
        self.padre.nombre = self.txtbox.get_text()
    
    def leer_puntajes(self):
        puntajes_dict = []

        # Establecer una conexión con la base de datos y obtener los puntajes
        try:
            conexion = sqlite3.connect('puntajes.db')
            cursor = conexion.cursor()

            cursor.execute('SELECT jugador, score FROM puntajes ORDER BY score DESC LIMIT 3')
            puntajes = cursor.fetchall()

            conexion.close()

            # Convertir los puntajes en una lista de diccionarios
            for puntaje in puntajes:
                puntajes_dict.append({"Jugador": puntaje[0], "Score": puntaje[1]})
        except:
            pass

        return puntajes_dict