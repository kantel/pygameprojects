# coding=utf-8

# Minimales PyGame-Grundgerüst
# Als Template für alle Python/PyGame-Projekte zu verwenden

import pygame as pg
import os

# Einige nützliche Konstanten
WIDTH = 640
HEIGHT = 480
FPS = 60   # Framerate

# Pygame initialisieren und das Fenster und die Hintergrundfarbe festlegen
pg.init()
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("🐍 Hällo Wörld! 🐍")
background = pg.Surface(win.get_size())
background = background.convert()
background.fill((0, 80, 125))
clock = pg.time.Clock()


# Assets laden
# Hier wird der Pfad zum Verzeichnis des ».py«-Files gesetzt
# Erspart einem das Herumgehample in TextMate mit dem os.getcwd()
# und os.path.join()
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

keep_going = True
while keep_going:
    # Framerate feslegen
    clock.tick(FPS)
    # Eingabe verarbeiten (Input Events)
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            keep_going = False

    # Update

    # Draw
    win.blit(background, (0, 0))
    
    # Wenn *alles* gezeichnet ist
    pg.display.flip()

print("I did it, Babe!")
pg.quit()          