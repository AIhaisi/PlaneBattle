import pygame
import sys

pygame.init()

#
WIDTH, HEIGHT = 512, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Explosion")


background = pygame.image.load('background.jpg').convert()
backgroundY = 0

class Explosion:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.images = []
        for i in range(9):
            image = pygame.image.load( 'explode0' + str(i+1) + '.png' ).convert_alpha()

            self.images.append(image)

        image = pygame.image.load('explode10.png').convert_alpha()
        self.images.append(image)
        image = pygame.image.load('explode11.png').convert_alpha()
        self.images.append(image)

        self.frame = 0
        self.imageFrame = 0

        self.finish = False

    def update(self):


        self.frame += 1
        self.imageFrame = (int)(self.frame / 3)

        if self.imageFrame >= len(self.images):
            self.frame = 0
            self.imageFrame = 0

            self.finish = True
            return self.finish


    def draw(self):

        if self.finish == False:
            screen.blit( self.images[self.imageFrame], (self.x - 120, self.y - 120,240,240) )



explosions = []
mousePos = [-100,-100]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mousePos = pygame.mouse.get_pos()
            e = Explosion(mousePos[0], mousePos[1])
            explosions.append(e)

    #


    # UPDATE

    for e in explosions:
        r = e.update()
        if r == True:
            explosions.remove(e)


    # RENDER

    #screen.fill(BACKGROUND_COLOR)

    #
    if backgroundY > 768:
        backgroundY = 0
    backgroundY += 0.3
    backgroundY2 = -768+backgroundY
    screen.blit(background, (0,backgroundY, 512,768))
    screen.blit(background, (0, backgroundY2, 512, 768))

    #
    for e in explosions:
        e.draw()


    pygame.display.flip()

    #
    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()

