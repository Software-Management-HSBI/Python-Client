import pygame
import sys

from Multiplayer.client import Client
from Gamefiles.game import Game
from Multiplayer.button import Button
from Visuals.colors import Colors

pygame.init()
client = Client()

# In diesen Methoden werden unsere Aufrufe fuer die verschiedenen Modi aufgerufen, sie sind die Aktionen der Buttons
# TODO: Das ist alles noch etwas Spaghetti-Code-Artig, irgendwie refactoren.
def start_game():
    Game()

# TODO: Bis jetzt ist nur der Singleplayer-Button nutzbar, weil wir noch keine andere Modi haben, d. h. hier dann aktualisieren
def options():
    pass

def multiplayer():
    pass

width = 1024
height = 768
title = "Wakaliwood Gaming"

start_Button = Button(400, 75, 200, 50, "Start", color=Colors.GREEN, action=start_game)
options_Button = Button(400, 375, 200, 50, "Optionen", color=Colors.YELLOW, action=options)
multiplayer_Button = Button(400, 675, 200, 50, "Mehrspieler", color=Colors.BLUE, action=multiplayer)

buttons = [start_Button, options_Button, multiplayer_Button]

# TODO: Hier soll das Menu implementiert werden, also verschiedene Knoepfe fuer Singleplayer, Multiplayer, Einstellungen etc.
class Menu:

    background_image = pygame.image.load("assets/racer.jpg")

    def __init__(self):
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(title)
        self.menu_loop()

    # Hier soll ueberprueft werden, ob ein neuer Modus ausgewaehlt wurde. Default ist immer das Main-Menu
    def menu_loop(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.action:
                                    button.action()


            self.screen.blit(self.background_image, (0, 0))

            for button in buttons:
                button.draw(self.screen)

            pygame.display.flip()



