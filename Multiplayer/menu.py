import pygame
import sys

from Multiplayer.button import Button
from Multiplayer.client import Client
from Gamefiles.game import Game
from Visuals.colors import Colors

import globals as gl

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

title = "Wakaliwood Gaming"

start_Button = Button(50, 50, 200, 50, "Start", color=Colors.GREEN, action=start_game)
options_Button = Button(gl.width - 250, 50, 200, 50, "Optionen", color=Colors.YELLOW, action=options)
multiplayer_Button = Button(50, gl.height - 100, 200, 50, "Mehrspieler", color=Colors.BLUE, action=multiplayer)
quit_Button = Button(gl.width - 250, gl.height - 100, 200, 50, "Beenden", color=Colors.WHITE, action=sys.exit)

buttons = [start_Button, options_Button, multiplayer_Button, quit_Button]

# TODO: Hier soll das Menu implementiert werden, also verschiedene Knoepfe fuer Singleplayer, Multiplayer, Einstellungen etc.
class Menu:

    background_image = pygame.image.load("assets/racer.jpg")

    def __init__(self):
        gl.screen = pygame.display.set_mode([gl.width, gl.height])
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


            gl.screen.blit(self.background_image, (0, 0))

            for button in buttons:
                button.draw(gl.screen)

            pygame.display.flip()
