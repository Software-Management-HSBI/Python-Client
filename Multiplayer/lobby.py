import pygame

import globals as gl
from Visuals.colors import Colors
from Multiplayer.button import Button


class Lobby:
    lobby_image = pygame.image.load("assets/lobby.jpg")

    def __init__(self):
        # TODO: Hier wird dann statt dieser Liste eine Liste aller Spieler vom Server genommen
        self.player_list = ["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"]
        self.player_buttons = []

        # Erstelle Bereitschafts-Buttons für jeden Spieler
        self.button_width, self.button_height = 200, 50
        self.button_spacing = 20
        self.initial_button_y = 50
        self.create_buttons()
        self.lobby_loop()

    def create_buttons(self):
        for i, player in enumerate(self.player_list):
            button_x = (gl.width - self.button_width) // 2
            button_y = self.initial_button_y + i * (self.button_height + self.button_spacing)

            button = Button(button_x, button_y, self.button_width, self.button_height, f"{player}\n Bereit",
                            color=Colors.RED, hover_color=Colors.LIGHT_RED)
            self.player_buttons.append(button)

    def lobby_loop(self):
        running = True
        ready = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if gl.client.sio.connected:
                        gl.client.disconnect()
                    running = False

                # Ueberpruefe, ob ein Button angeklickt wurde
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.player_buttons:
                        if button.rect.collidepoint(event.pos):
                            if not ready:
                                # TODO: Hier kommt dann der Bereitschaftscheck hin,
                                #  maybe eine Methode vom Server die das macht?
                                button.color = Colors.GREEN
                                button.hover_color = Colors.LIGHT_GREEN
                                # gl.client.ready()
                                ready = not ready
                            else:
                                button.color = Colors.RED
                                button.hover_color = Colors.LIGHT_RED
                                ready = not ready
                                # gl.client.not_ready()

            # Hintergrund zeichnen
            gl.screen.blit(self.lobby_image, (0, 0))

            # Zeichne die Buttons
            for button in self.player_buttons:
                button.draw(gl.screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)
