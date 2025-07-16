import pygame as pg
from pygame.color import THECOLORS
import asyncio
from random import randint

pg.init()
screen = pg.display.set_mode((1400,700))
screen.fill(THECOLORS['white'])

class Field:
    def __init__(self, sun=0):
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.rects = set()
        if 0<=sun<=255:
            self.sun = sun
        else:
            raise ValueError

        for width in range(self.screenWidth//10):
            for height in range(self.screenHeight//10):
                rect = (width*10,height*10,sun)
                self.rects.add(rect)

    def drawField(self):
        for rectValue in self.rects:
            rect = pg.Rect(rectValue[0], rectValue[1],10,10)
            pg.draw.rect(screen,(255,255-rectValue[2],255-rectValue[2]),rect)
            pg.draw.rect(screen,(0,0,0),rect, width=1)
        pg.display.flip

class Tree:
    def __init__(self, genomValues: list, place: tuple, fieldValues: set):
        self.color = (randint(0,255),randint(0,255),randint(0,255))
        self.cells = set() #(x,y,genom,sun,energy)
        self.startPoint = pg.Rect(place[0],place[1],10,10)
        self.fieldValues = fieldValues
        self.genomValues = genomValues
        self.longLife = 0
        self.newCells = set()

        for tup in fieldValues:
            if tup[0] == place[0]+10 and tup[1] == place[1]: #поиск sun зная x,y
                self.sun = tup[2]
        self.newCells.add((place[0],place[1],self.genomValues[0],self.sun,100))
        self.cells.add((place[0],place[1],self.genomValues[0],self.sun,100)) #genom 0 начинает рост
        pg.draw.rect(screen, self.color, self.startPoint)
        pg.display.update()

    def startGrow(self):
        newCells = set()
        for cell in self.newCells:
            sun = 100
            self.counter = 0
            chromosome = cell[2]
            
            for gen in chromosome:
                if gen<8:
                    if self.counter == 0:
                        newCells.add((cell[0]-10,cell[1],self.genomValues[gen],sun,100))
                    elif self.counter == 1:
                        newCells.add((cell[0],cell[1]+10,self.genomValues[gen],sun,100))
                    elif self.counter == 2:
                        newCells.add((cell[0]+10,cell[1],self.genomValues[gen],sun,100))
                    elif self.counter == 3:
                        newCells.add((cell[0],cell[1]-10,self.genomValues[gen],sun,100))
                else:
                    pass 
                self.counter+=1

        self.cells.update(self.newCells)
        self.newCells = newCells
        
        print(self.newCells)
        
        for cell in self.newCells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            pg.draw.rect(screen,THECOLORS['brown'],rect)

        for cell in self.cells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            pg.draw.rect(screen,self.color,rect)


class Genom():
    def __init__(self):
        #genom structure [[left,up,right,bottom],....]
        self.genom = [(randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),]

async def Simuation():
    sun = 100 #this parameter changes the sun value
    field = Field(sun)
    field.drawField()
    genomValues = Genom().genom
    genomValues1 = Genom().genom
    genomValues2 = Genom().genom
    tree = Tree(genomValues = genomValues, place = (700,690), fieldValues=field.rects)
    tree1 = Tree(genomValues = genomValues1, place = (350,690), fieldValues=field.rects)
    tree2 = Tree(genomValues = genomValues2, place = (1050,690), fieldValues=field.rects)
    pg.display.update()
    counter = 0
    while True:
        counter+=1
        if counter == 70:
            tree.cells = set()
            counter = 0
            sun = 100 #this parameter changes the sun value
            field = Field(sun)
            field.drawField()
            genomValues = Genom().genom
            genomValues1 = Genom().genom
            genomValues2 = Genom().genom
            tree = Tree(genomValues = genomValues, place = (700,690), fieldValues=field.rects)
            tree1 = Tree(genomValues = genomValues1, place = (350,690), fieldValues=field.rects)
            tree2 = Tree(genomValues = genomValues2, place = (1050,690), fieldValues=field.rects)

            pg.display.update()
        screen.fill(THECOLORS['white'])
        field.drawField()

        tree.startGrow()
        tree1.startGrow()
        tree2.startGrow()

        pg.display.flip()

async def CheckEvents():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        await asyncio.sleep(0.01)
    pg.quit()

async def main():
    await asyncio.gather(CheckEvents(), Simuation())

asyncio.run(main())