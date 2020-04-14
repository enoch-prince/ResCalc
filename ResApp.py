#!/usr/bin/env 
# Import the pygame library and initialise the game engine
import pygame
import UI

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


def main():
    # -------- Main Program Loop -----------
    index = 0
    prev_millis = pygame.time.get_ticks()
    UI.create_window()
    UI.change_bg(index)
    while True:
        # change bg every 30sec
        if (pygame.time.get_ticks() - prev_millis) >= 30000:
            if index >= 1:
                index = 0
            else:
                index += 1
            prev_millis = pygame.time.get_ticks()
        UI.change_bg(index)
        UI.show()
        # --- Limit to 25 frames per second
        clock.tick(25)


if __name__ == '__main__':
    main()