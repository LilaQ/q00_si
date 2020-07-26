import pygame
import numpy as np
import cpu

ins = [0x70]

def main():

	# initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    pygame.display.set_caption("[ q00.si - space invaders arcade emuladore ]")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((512,448))	# orig size is 256 / 224
    surface = pygame.Surface((256, 224))
    pa = pygame.PixelArray(surface)
    pa = cpu.getVRAM()
    del pa
    surface = pygame.transform.scale(surface, (512, 448))
    screen.blit(surface, (0,0))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        #	update display
        pygame.display.update()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()
	for el in ins:
		cpu.cpu_8080[el]()
