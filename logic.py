import pygame
import os
import sys
from pygame_textinput import TextInput, TextOutput


def load_image(name):
    fullname = os.path.join('imgs', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ' + name + '\n' + str(message))
        pygame.quit()
        raise SystemExit
    # image = image.convert()
    #print(name + ' image successfully loaded!')
    return image


def closeWindow():
    pygame.quit()
    sys.exit()


class EventHandler:
    # global mousePosition, clicked
    def __init__(self):
        self.clicked = False
        self.mousePosition = list(pygame.mouse.get_pos())
        self.textInput = TextInput()
        self.textOutput = TextOutput()
        self.textOutputRect = None

    def eventLoop(self):
        # --- Get all events in a for loop
        events = pygame.event.get()
        for event in events:
            # --- If user clicked close
            if event.type == pygame.QUIT:
                closeWindow()
            # --- If the ESCAPE Key was pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    closeWindow()

            # --- if user moved the mouse
            if event.type == pygame.MOUSEMOTION:
                # get mouse position
                self.mousePosition = list(event.pos)
            # --- if user clicked one of the mouse buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                # set clicked flag true
                self.clicked = True
            else:
                self.clicked = False

        self.textInput.update(events)
        #self.textOutput.update()