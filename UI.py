""" A class for creating the UI for the ResCalc App 
    Copyright 2017, Enoch Prince, princealva11@gmail.com, All rights reserved.
"""
import pygame

from logic import EventHandler, load_image

# Initialize pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)  # 30,30,30 for light
BROWN = (77, 39, 0)  # 114,60,5 for light
RED = (128, 0, 0)  # 255,0,0 for light
ORANGE = (222, 111, 0)  # 255,130,0 for light
YELLOW = (222, 222, 0)  # 255,255,0 for light
GREEN = (0, 128, 0)  # 0,255,0 for light
BLUE = (0, 0, 140)  # 0,0,255 for light
VIOLET = (102, 0, 102)  # 128,0,128 for light
GREY = (128, 128, 128)  # 178,178,178 for light
WHITE = (255, 255, 255)
GOLD = (212, 175, 0)  # 212,175,0 for light 240, 198, 0
SILVER = (192, 192, 192)  # 212,212,212 for light

# Set some Parameters
WIDTH = 800
HEIGHT = 500
BACKGROUND = []
eventHandler = EventHandler()


def create_window():
    global temp_surf, surface, menubar, res_image, \
        four_band_resistor, five_band_resistor, colorPalette

    windowSize = (WIDTH, HEIGHT)
    window = pygame.display.set_mode(windowSize)
    icon = load_image('icon.jpg')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('ResCalc v1.0.0')
    surface = pygame.display.get_surface()
    temp_surf = pygame.Surface(windowSize)
    window.fill(GREY)

    menubar = Menubar((0, 0), (100, 20), ('ResType', '4 Band', '5 Band'))
    res_image = load_image('res2.png')
    
    four_band_resistor = Resistor()
    five_band_resistor = Resistor('5 band')
    
    colorPalette = ColorPalette((175, 130))
    colorPalette.createColors()
    
    eventHandler.textOutput.set_text_color(BLUE)


# Load necessary Images
def load_bg_images():
    for i in range(2):
        img = load_image('bg%s.jpg' % i)
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        BACKGROUND.append(img)


def draw(d, s, pos):
    # --- Drawing code should go here. s->source, d->destination
    # First, clear the screen to grey.
    d.fill(GREY)
    d.blit(s, pos)


def change_bg(i):
    if not BACKGROUND:
        load_bg_images()
    draw(temp_surf, BACKGROUND[i], (0, 0))


def show():
    # display the menubar
    menubar.display()

    # check which option has been clicked: 4 band or 5 band
    if not menubar.fiveBandSelected:
        temp_surf.blit(res_image, (195, 200))
        four_band_resistor.respond_to_event()
        four_band_resistor.show()
        if four_band_resistor.band_isClicked:
            colorPalette.isShown = True
            if colorPalette.colorSelected:
                pass
        else:
            colorPalette.isShown = False
        colorPalette.respond_to_event()
        colorPalette.showPalette()
        
        if eventHandler.textInput.ENTER_KEY_PRESSED:
            four_band_resistor.getColorCodeFromRes(eventHandler.textInput.get_text())
            #print("Enter key pressed")
        
        four_band_resistor.calculate()

    else:
        temp_surf.blit(res_image, (195, 200))
        five_band_resistor.respond_to_event()
        five_band_resistor.show()
        if five_band_resistor.band_isClicked:
            colorPalette.isShown = True
        else:
            colorPalette.isShown = False
        colorPalette.respond_to_event()
        colorPalette.showPalette()
        five_band_resistor.calculate()

    # --- Blit the text onto the screen --- #
    if eventHandler.textOutput.clicked:
        if not menubar.fiveBandSelected: # to disable text input for 5 band resistor
            temp_surf.blit(eventHandler.textInput.get_surface(), (195 + 170, 200 + 78 + 30))
        else:
            temp_surf.blit(eventHandler.textOutput.get_surface(), (195 + 170, 200 + 78 + 30))
    else:
        temp_surf.blit(eventHandler.textOutput.get_surface(), (195 + 170, 200 + 78 + 30))
    # --- Go ahead and update the screen with what we've drawn --- #
    draw(surface, temp_surf, (0, 0))
    pygame.display.update()


def mouse_hover(rect):
    eventHandler.eventLoop()
    # print(eventHandler.mousePosition)
    if rect.collidepoint(eventHandler.mousePosition):
        return True


def mouse_click(rect):
    if mouse_hover(rect) and eventHandler.clicked:
        return True


class Resistor(pygame.sprite.Sprite):
    BAND_WIDTH, BAND_HEIGHT = 25, 62
    BAND_POS_X, BAND_POS_Y = 317, 209
    GAP = 10
    five_band_isCreated = False
    band_isClicked = False

    def __init__(self, restype=None):
        super().__init__()
        self.resistance = 0.0
        self.tolerance = 0
        self.multiplier = 0
        self.multiplier_alpha_part = ''
        self.res_surf = pygame.Rect((self.BAND_POS_X, self.BAND_POS_Y),
                                    (self.BAND_WIDTH * 5 + self.GAP * 5, self.BAND_HEIGHT))
        self.band = []
        for i in range(5):
            self.band.append(Band((self.BAND_POS_X, self.BAND_POS_Y), (self.BAND_WIDTH, self.BAND_HEIGHT)))

        self.colorPalette = ColorPalette((175, 130))
        self.colorPalette.createColors()

        if restype is not None:
            if '5' or 'five' in restype:
                self.create_5_band_resistor()
                self.five_band_isCreated = True
        else:
            self.create_4_band_resistor()
            self.five_band_isCreated = False
            
    def create_4_band_resistor(self):
        self.band[0].x = self.BAND_POS_X
        self.band[1].x = self.BAND_POS_X + self.BAND_WIDTH + self.GAP * 2
        self.band[2].x = self.band[1].x + self.BAND_WIDTH + self.GAP * 2
        self.band[3].x = self.band[2].x + self.BAND_WIDTH + (self.GAP * 3.5)
        for band in self.band:
            band.y = self.BAND_POS_Y

    def create_5_band_resistor(self):
        self.band[0].x = self.BAND_POS_X
        self.band[1].x = self.BAND_POS_X + self.BAND_WIDTH + self.GAP
        self.band[2].x = self.band[1].x + self.BAND_WIDTH + self.GAP
        self.band[3].x = self.band[2].x + self.BAND_WIDTH + self.GAP
        self.band[4].x = self.band[3].x + self.BAND_WIDTH + (self.GAP * 2)
        for band in self.band:
            band.y = self.BAND_POS_Y

    def show(self):
        if self.five_band_isCreated:
            temp_surf.fill((110, 90, 0), self.res_surf)
            temp_surf.fill(self.band[0].color, self.band[0])
            temp_surf.fill(self.band[1].color, self.band[1])
            temp_surf.fill(self.band[2].color, self.band[2])
            temp_surf.fill(self.band[3].color, self.band[3])
            temp_surf.fill(self.band[4].color, self.band[4])
        else:
            temp_surf.fill((110, 90, 0), self.res_surf)
            temp_surf.fill(self.band[0].color, self.band[0])
            temp_surf.fill(self.band[1].color, self.band[1])
            temp_surf.fill(self.band[2].color, self.band[2])
            temp_surf.fill(self.band[3].color, self.band[3])

        self.colorPalette.showPalette()

    def respond_to_event(self):
        if self.five_band_isCreated:
            self.band[4].respond_to_event()
            self.colorPalette.respond_to_event()
            if self.band_isClicked:
                self.colorPalette.isShown = True
            else:
                self.colorPalette.isShown = False
            if self.band[4].hovered:
                # highlight the band's color
                self.band[4].color = self.band[4].highlight_color(self.band[4].color)
            else:
                self.band[4].color = self.band[4].dehighlight_color(self.band[4].color)

            if self.band[4].clicked:
                self.band_isClicked = True
                # highlight the band's color
                self.band[4].color = self.band[4].highlight_color(self.band[4].color)
                if self.colorPalette.colorSelected:
                    for colorRect in self.colorPalette.colorRect:
                        if colorRect.clicked:
                            self.band[4].color = colorRect.color
                            self.band[4].value = colorRect.value
            if not mouse_hover(self.band[4]) and eventHandler.clicked:
                self.band[4].color = self.band[4].dehighlight_color(self.band[4].color)
                self.band[4].clicked = False

        self.colorPalette.respond_to_event()
        if self.band_isClicked:
            self.colorPalette.isShown = True
        else:
            self.colorPalette.isShown = False

        for i in range(4):
            self.band[i].respond_to_event()
            if self.band[i].hovered:
                # highlight the band's color
                self.band[i].color = self.band[i].highlight_color(self.band[i].color)
            else:
                self.band[i].color = self.band[i].dehighlight_color(self.band[i].color)

            if self.band[i].clicked:
                # band color should remain highlighted
                self.band[i].color = self.band[i].highlight_color(self.band[i].color)
                # set a flag to display the color palette
                self.band_isClicked = True
                if self.colorPalette.colorSelected:
                    for colorRect in self.colorPalette.colorRect:
                        if colorRect.clicked:
                            # change the band's color to that which is selected from the color palette
                            self.band[i].color = colorRect.color
                            self.band[i].value = colorRect.value

            # dehighlight the band when deselected
            if not mouse_hover(self.band[i]) and eventHandler.clicked:
                self.band[i].color = self.band[i].dehighlight_color(self.band[i].color)
                self.band[i].clicked = False

        if not mouse_hover(self.res_surf) and eventHandler.clicked:
            # when user clicks outside the resistor image
            self.band_isClicked = False

            for i in range(5):
                # check if the clicked flag is set to true
                if self.band[i].clicked:
                    # reset it to false
                    self.band[i].clicked = False
                    # dehighlight all the highlighted colors
                    self.band[i].color = self.band[i].dehighlight_color(self.band[i].color)

            for colorRect in self.colorPalette.colorRect:
                # check for clicked flags for any of the colorRects and disable it
                if colorRect.clicked:
                    colorRect.clicked = False
            
            if mouse_click(eventHandler.textOutputRect):
                eventHandler.textInput.input_string = "{0:.1f}".format(self.resistance) + self.multiplier_alpha_part 
                eventHandler.textOutput.clicked = True
            
            if not mouse_hover(eventHandler.textOutputRect) and eventHandler.clicked:
                eventHandler.textOutput.clicked = False

    def calculate(self):
        if self.five_band_isCreated:
            for band in self.band:
                if self.band.index(band) == 0:
                    self.resistance += (band.value * 100)
                if self.band.index(band) == 1:
                    self.resistance += (band.value * 10)
                if self.band.index(band) == 2:
                    self.resistance += band.value
                if self.band.index(band) == 3:
                    if 1 <= band.value <= 3:
                        self.multiplier_alpha_part = 'K'
                        self.multiplier = 0.01 if band.value is 1 else 0.1 \
                            if band.value is 2 else 1
                    elif 4 <= band.value <= 6:
                        self.multiplier_alpha_part = 'M'
                        self.multiplier = 0.01 if band.value is 4 else 0.1 \
                            if band.value is 5 else 1
                    elif 7 <= band.value <= 9:
                        self.multiplier_alpha_part = 'G'
                        self.multiplier = 0.01 if band.value is 7 else 0.1 if band.value is 8 else 1
                    elif band.value is 10 or band.value is 11:
                        self.multiplier = 0.1 if band.value is 10 else 0.01
                    else:
                        self.multiplier = 10 ** band.value
                        self.multiplier_alpha_part = ''
                if self.band.index(band) == 4:
                    self.tolerance = 5 if band.value is 10 else 10 \
                        if band.value is 11 else 0.5 if band.value is 5 else 0.25 \
                        if band.value is 6 else 0.1 if band.value is 7 else 0.05 \
                        if band.value is 8 else 1 if band.value is 1 else 2 \
                        if band.value is 2 else 0

        else:
            for band in self.band:
                if self.band.index(band) == 0:
                    self.resistance += (band.value * 10)
                if self.band.index(band) == 1:
                    self.resistance += band.value
                if self.band.index(band) == 2:
                    if 2 <= band.value <= 4:
                        self.multiplier_alpha_part = 'K'
                        self.multiplier = 0.1 if band.value is 2 else 1 \
                            if band.value is 3 else 10
                    elif 5 <= band.value <= 7:
                        self.multiplier_alpha_part = 'M'
                        self.multiplier = 0.1 if band.value is 5 else 1 \
                            if band.value is 6 else 10
                    elif band.value is 8 or band.value is 9:
                        self.multiplier_alpha_part = 'G'
                        self.multiplier = 0.1 if band.value is 8 else 1
                    elif band.value is 10 or band.value is 11:
                        self.multiplier = 0.1 if band.value is 10 else 0.01
                    else:
                        self.multiplier = 10 ** band.value
                        self.multiplier_alpha_part = ' '
                if self.band.index(band) is 3:
                    self.tolerance = 5 if band.value is 10 else 10 \
                        if band.value is 11 else 0.5 if band.value is 5 else 0.25 \
                        if band.value is 6 else 0.1 if band.value is 7 else 0.05 \
                        if band.value is 8 else 1 if band.value is 1 else 2 \
                        if band.value is 2 else 0

        self.resistance *= self.multiplier
        # print(self.five_band_isCreated)
        eventHandler.textOutput.set_output_string("{0:.1f}".format(self.resistance) + self.multiplier_alpha_part
                                                  + u"\u03A9 " + str(self.tolerance) + "%")

        # --- Process Text outputs --- #
        eventHandler.textOutput.update()
        eventHandler.textOutputRect = eventHandler.textOutput.get_text_rect(308, 365)
        # eventHandler.textOutputRect = textOutputRect
        
        self.resistance = 0
        self.multiplier = 0
        self.tolerance = 0

    def getColorCodeFromRes(self, resistance):
        """ The Resistance Parameter must be a String type """
        resistance = resistance.strip()
        reslist = list(resistance)
        #print(reslist)
        if not self.five_band_isCreated:       
            for index, numstr in enumerate(reslist):
                if index == 0:
                    if len(reslist) is 1:
                        # set the 1st and 3rd bands to black
                        self.band[1].color = self.colorPalette.COLORS[int(numstr)]
                        self.band[1].value = int(numstr)
                        self.band[0].color = BLACK
                        self.band[0].value = 0
                        self.band[2].color = BLACK
                        self.band[2].value = 0
                        break
                    else:
                        self.band[index].color = self.colorPalette.COLORS[int(numstr)]
                        self.band[index].value = int(numstr)
                    #print(numstr)
                # check for the 2nd index
                elif index == 1:
                    if numstr.isdigit():
                        if len(reslist) is 2:
                            # set the 3rd band to Black
                            self.band[2].color = BLACK
                            self.band[2].value = 0
                        
                        self.band[1].color = self.colorPalette.COLORS[int(numstr)]
                        self.band[1].value = int(numstr)  
                        #print("2nd: "+ numstr)                   
                    elif numstr.isalpha():
                        self.band[1].color = BLACK
                        self.band[1].value = 0
                        self.changeBandColor(numstr, 2, -1) # 3rd band will change
                    elif numstr is '.':
                        if "k" or "K" or "M" or "m" or "g" or "G" not in reslist:
                            # then resistance is in the form 1.0, 1.0K etc, so set the 3rd band to Gold
                            self.band[2].color = GOLD
                            self.band[2].value = 0.1
                # check for the 3rd index
                elif index == 2:
                    if numstr.isdigit():
                        # check if the previous index is a dot
                        if reslist[index-1] is '.':
                            self.band[1].color = self.colorPalette.COLORS[int(numstr)]
                            self.band[1].value = int(numstr)
                        # band is a brown as long as it's a 4-band resistor
                        else:
                            self.band[2].color = BROWN
                            self.band[2].value = 1
                            #print("3rd: "+ numstr)
                    elif numstr.isalpha():
                        self.changeBandColor(numstr, 2, 0) # 3rd band will change
                    elif numstr is '.':
                        # then resistance will be in the form 10.0, etc
                        self.band[2].color = BLACK
                        self.band[2].value = 0
                # check for the 4th index  
                elif index == 3:
                    if numstr.isalpha():
                        if '.' in reslist:
                            # resistance will be in the form 2.7k, etc
                            self.changeBandColor(numstr, 2, -1) #change the 3rd band to Red
                        else:
                            self.changeBandColor(numstr, 2, 1)
                    if numstr is '.':
                        continue  
                # set the last band to default to a tolerance of 5%
                self.band[3].color = GOLD
                self.band[3].value = 10
        else:
            for index, numstr in enumerate(reslist):
                pass

    def changeBandColor(self, s, bi, ci):
        if s is 'K' or s is 'k':
            self.band[bi].color = self.colorPalette.COLORS[3+ci]
            self.band[bi].value = 3+ci
        if s is 'M' or s is 'm':
            self.band[bi].color = self.colorPalette.COLORS[6+ci]
            self.band[bi].value = 6+ci
        if s is 'G' or s is 'g':
            self.band[bi].color = self.colorPalette.COLORS[9+ci]
            self.band[bi].value = 9+ci

class Band(pygame.Rect):
    def __init__(self, pos, size):
        # size = 25, 62
        super(Band, self).__init__(pos, size)
        self.x, self.y = pos
        self.width, self.height = size
        self.color = BLACK
        self.value = 0
        self.clicked = False
        self.clickable = True
        self.hovered = None

    def respond_to_event(self):
        self.hovered = False
        if mouse_hover(self) and self.clickable:
            self.hovered = True
        if mouse_click(self) and self.clickable:
            self.clicked = True

    def disable(self):
        self.clickable = False
    
    def enable(self):
        self.clickable = True if not self.clickable else False

    @staticmethod
    def highlight_color(color):
        if color == BLACK:
            return 30, 30, 30
        elif color == BROWN:
            return 114, 60, 5
        elif color == RED:
            return 200, 0, 0
        elif color == ORANGE:
            return 255, 130, 0
        elif color == YELLOW:
            return 255, 255, 30
        elif color == GREEN:
            return 0, 200, 0
        elif color == BLUE:
            return 0, 0, 255
        elif color == VIOLET:
            return 128, 0, 128
        elif color == GREY:
            return 160, 160, 160
        elif color == SILVER:
            return 200, 200, 200
        elif color == GOLD:
            return 240, 198, 0
        else:
            return color

    @staticmethod
    def dehighlight_color(color):
        if color == (30, 30, 30):
            return BLACK
        elif color == (114, 60, 5):
            return BROWN
        elif color == (200, 0, 0):
            return RED
        elif color == (255, 130, 0):
            return ORANGE
        elif color == (255, 255, 30):
            return YELLOW
        elif color == (0, 200, 0):
            return GREEN
        elif color == (0, 0, 255):
            return BLUE
        elif color == (128, 0, 128):
            return VIOLET
        elif color == (160, 160, 160):
            return GREY
        elif color == (200, 200, 200):
            return SILVER
        elif color == (240, 198, 0):
            return GOLD
        else:
            return color


class ColorPalette(pygame.Surface):
    isShown = False

    def __init__(self, size):
        super(ColorPalette, self).__init__(size)
        self.paletteRect = self.get_rect()
        self.pos = (320, 35)
        self.paletteRect.left, self.paletteRect.top = (50, 50)
        self.size = size
        self.colorRect = []
        self.colorSelected = False
        self.COLORS = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET, GREY, WHITE, GOLD, SILVER]

    def createColors(self):
        """ pos and size each takes a tuple """
        pos = self.pos
        gap = 5
        size = (self.size[0] - gap * 3) / 4, (self.size[0] - gap * 2) / 4
        for n in range(12):
            self.colorRect.append(Band(pos, size))

        self.colorRect[1].x = self.colorRect[0].x + self.colorRect[0].w + gap
        self.colorRect[2].x = self.colorRect[1].x + self.colorRect[1].w + gap
        self.colorRect[3].x = self.colorRect[2].x + self.colorRect[2].w + gap
        self.colorRect[5].x, self.colorRect[9].x = self.colorRect[1].x, self.colorRect[1].x
        self.colorRect[6].x, self.colorRect[10].x = self.colorRect[2].x, self.colorRect[2].x
        self.colorRect[7].x, self.colorRect[11].x = self.colorRect[3].x, self.colorRect[3].x

        self.colorRect[4].y = self.colorRect[0].y + self.colorRect[0].h + gap
        self.colorRect[5].y, self.colorRect[6].y, self.colorRect[7].y = self.colorRect[4].y, self.colorRect[4].y, \
                                                                        self.colorRect[4].y
        self.colorRect[8].y = self.colorRect[4].y + self.colorRect[4].h + gap
        self.colorRect[9].y, self.colorRect[10].y, self.colorRect[11].y = self.colorRect[8].y, self.colorRect[8].y, \
                                                                          self.colorRect[8].y
        # fill the colorRects with colors
        for colorRect in self.colorRect:
            index = self.colorRect.index(colorRect)
           
            # first get the index of the last color
            colorRect.value = len(self.COLORS) - index - 1
            #colorRect.value = self.COLORS.index(self.COLORS[-1])
            
            # return the last color and remove it from the COLOR list
            #colorRect.color = self.COLORS.pop()
            colorRect.color = self.COLORS[colorRect.value]

    def showPalette(self):
        self.fill((172, 172, 172))
        self.set_alpha(230)
        if not self.isShown:
            for colorRect in self.colorRect:
                colorRect.clicked = False
            self.fill(GREY)
            self.set_alpha(0)

        temp_surf.blit(self, self.pos)
        if self.isShown:
            for colorRect in self.colorRect:
                temp_surf.fill(colorRect.color, colorRect)

    def respond_to_event(self):
        self.colorSelected = False
        
        for colrect in self.colorRect:
            if (colrect.color is SILVER) or (colrect.color is GOLD):
                colrect.disable()
            if five_band_resistor.five_band_isCreated:
                if five_band_resistor.band[3].clicked or five_band_resistor.band[4].clicked:
                    if (colrect.color is SILVER) or (colrect.color is GOLD):
                        colrect.enable()
            if not four_band_resistor.five_band_isCreated:
                if four_band_resistor.band[2].clicked or four_band_resistor.band[3].clicked:
                    if (colrect.color is SILVER) or (colrect.color is GOLD):
                        colrect.enable()            
           
            colrect.respond_to_event()

            if colrect.hovered:
                colrect.color = colrect.highlight_color(colrect.color)
            else:
                colrect.color = colrect.dehighlight_color(colrect.color)

            if colrect.clicked:
                # set a color select flag
                if not self.colorSelected:
                    self.colorSelected = True


class Menubar(pygame.Rect):
    def __init__(self, pos, size, items):
        super(Menubar, self).__init__(pos, size)
        self.pos = pos
        self.font = pygame.font.SysFont('couriernew', 14)
        self.font.set_bold(True)
        self.item = items
        self.text = []
        self.textSurface = []
        for i in self.item:
            self.text.append(self.render_text(i, BLUE, None))
        for j in range(len(self.item)):
            self.textSurface.append(self.text[j].get_rect())
        self.textSurface[1].move_ip(10, 14)
        self.textSurface[2].move_ip(10, 34)
        # self.textSurface[1].height, self.textSurface[2].height = 17, 17
        self.menuSurface = pygame.Surface((75, 50))
        self.isClicked = False
        self.isHover = False
        self.fiveBandSelected = False

    def render_text(self, item, fg_color, bg_color):
        return self.font.render(item, True, fg_color, bg_color)

    def display(self):
        if mouse_hover(self.textSurface[0]):
            self.isHover = True
            if mouse_click(self.textSurface[0]):
                self.isClicked = True
                self.menuSurface.set_alpha(150)
        else:
            self.isHover = False

        if mouse_hover(self.textSurface[1]):
            self.text[1] = self.render_text(self.item[1], RED, GREY)
        else:
            self.text[1] = self.render_text(self.item[1], BLUE, None)
        if mouse_hover(self.textSurface[2]):
            self.text[2] = self.render_text(self.item[2], RED, GREY)
        else:
            self.text[2] = self.render_text(self.item[2], BLUE, None)

        if mouse_click(self.textSurface[1]):
            # set 4 band resistor flag
            self.fiveBandSelected = False
        if mouse_click(self.textSurface[2]):
            # set 5 band resistor flag
            self.fiveBandSelected = True

        if not self.isHover:
            self.text[0] = self.render_text(self.item[0], BLUE, None)
        else:
            self.text[0] = self.render_text(self.item[0], RED, GREY)

        if not self.isClicked:
            self.menuSurface.fill(GREY)
            self.menuSurface.set_alpha(0)

        if (tuple(eventHandler.mousePosition) > self.menuSurface.get_size()) and eventHandler.clicked:
            self.isHover = False
            self.isClicked = False

        self.menuSurface.blit(self.text[1], (10, 10))
        self.menuSurface.blit(self.text[2], (10, 30))
        temp_surf.blit(self.menuSurface, (0, 12))
        temp_surf.blit(self.text[0], self.pos)
