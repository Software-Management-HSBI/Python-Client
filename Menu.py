import pygame
import Background

from client import Client
from Standard_Config import Game
from button import Button

pygame.init()

client = Client()

width = 1024
height = 768
title = "Wakaliwood Gaming"

# TODO: Hier soll das Menu implementiert werden, also verschiedene Knoepfe fuer Singleplayer, Multiplayer, Einstellungen etc.
class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(title)

    # Hier soll ueberprueft werden, ob ein neuer Modus ausgewaehlt wurde. Default ist immer das Main-Menu
    def menu_loop(self):

        self.current_mode = "main"
        loop = True
        while loop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    
            if self.current_mode == "main":
                self.draw_menu()
            elif self.current_mode == "single":
                Game()
            pygame.display.update()

    # Soll das Startmenu zeichnen und einen Knopf fuer das Starten vom Singleplayer besitzen
    # TODO: Hier muessen dann noch die anderen Knoepfe fuer die verschiedenen Modi hin
    def draw_menu(self):
        Background.init_background(self.screen)

        start_button = Button(200, 150, 100, 50, "Singleplayer starten")
        button_check = True
        while button_check:
            for event in pygame.event.get():
                start_button.handle_event(event)
            
            start_button.draw(self.screen)


