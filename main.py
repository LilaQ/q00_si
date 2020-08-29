import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from cpu import getPC, getVRAM, cpu_8080, loadROM, memory, getREGS, getSP, getFLAGS, loadSI


def ppu(screen, surface):
    pa = pygame.PixelArray(surface)
    vram = getVRAM()
    for y in range(256):
        for x in range(224):
            white = vram[y*0x20+x//8] >> (7-(x % 8)) & 1
            if white != 0:
                pa[y,x] = (255, 255, 255)
            else:
                pa[y,x] = (0, 0, 0)
    del pa
    surface = pygame.transform.scale(surface, (512, 448))
    screen.blit(surface, (0,0))


def main():
    #print("*** TEST: cpu_tests/TST8080.COM", end="\r")
    #loadROM("TST8080.COM")
    loadSI()

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
    vram = getVRAM()
    for y in range(256):
    	for x in range(224):
            white = vram[y*0x20+x//8] >> (7-(x % 8)) & 1
            if white != 0:
                pa[y,x] = (255, 255, 255)
            else:
                pa[y,x] = (0, 0, 0)
    del pa
    surface = pygame.transform.scale(surface, (512, 448))
    screen.blit(surface, (0,0))
     
    # define a variable to control the main loop
    running = True
     
    # main loop
    cnt = 0
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        #   step PPU
        #if c % 1996800 == 0:
        if cnt > 1996800:
            ppu(screen, surface)
            pygame.display.update()
            cnt = cnt - 1996800
        #   step CPU    
        # print("PC: " + "{:04X}".format(getPC()) + ", AF: " + "{:02X}".format(getREGS().A) + "{:02X}".format((getFLAGS().S << 7) | (getFLAGS().Z << 6) | (getFLAGS().A << 4) | (getFLAGS().P << 2) | (1 << 1) | (getFLAGS().C)) + ", BC: " + "{:02X}".format(getREGS().B) + "{:02X}".format(getREGS().C) + ", DE: " + "{:02X}".format(getREGS().D) + "{:02X}".format(getREGS().E) + ", HL: " + "{:02X}".format(getREGS().H) + "{:02X}".format(getREGS().L) + ", SP: " + "{:04X}".format(getSP()) + ", CYC: " + str(cnt) + "\t(" + "{:02X}".format(memory[getPC()]) + " " + "{:02X}".format(memory[getPC()+1]) + " " + "{:02X}".format(memory[getPC()+2]) + " " + "{:02X}".format(memory[getPC()+3]) + ")\t(" + "{:02X}".format(memory[(getREGS().H<<8)|getREGS().L]) + ") (" + "{:04X}".format((getREGS().H<<8)|getREGS().L) + ")")
        # if getPC() == 0x0000:
        #     exit(1)
        # if getPC() == 5:
        #     if getREGS().C == 2:
        #         print(chr(getREGS().E))
        #     elif getREGS().C == 9:
        #         v = (getREGS().D << 8) | getREGS().E
        #         while chr(memory[v]) != "$":
        #             print(chr(memory[v]), end="")
        #             v = v + 1
        cnt = cnt + cpu_8080[memory[getPC()]]()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
    main()