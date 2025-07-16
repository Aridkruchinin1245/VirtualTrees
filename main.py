import pygame as pg
from pygame.color import THECOLORS
import asyncio
from random import randint
startPoints = set()

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
        self.newCells = set()
        self.time = 0
        self.longLife = 0
        self.status = True
        
        for tup in fieldValues:
            if tup[0] == place[0]+10 and tup[1] == place[1]: #поиск sun зная x,y
                self.sun = tup[2]

        self.newCells.add((place[0],place[1],self.genomValues[0],100,100))
        self.cells.add((place[0],place[1],self.genomValues[0],100,100)) #genom 0 always starts
        pg.draw.rect(screen, self.color, self.startPoint)
        pg.display.update()

    def startGrow(self):
        global startPoints
        self.time +=1 #counter of time
        newCells = set() # set with points of grow
        for cell in self.newCells:
            sun = 100
            self.counter = 0
            chromosome = cell[2]
                
            for gen in chromosome:
                if gen<8:
                    if self.counter == 0 and not (cell[0]-10,cell[1],self.genomValues,sun,100) in self.cells:
                        newCells.add((cell[0]-10,cell[1],self.genomValues[gen],sun,100))

                    elif self.counter == 1 and not (cell[0],cell[1]+10,self.genomValues,sun,100) in self.cells:
                        newCells.add((cell[0],cell[1]+10,self.genomValues[gen],sun,100))

                    elif self.counter == 2 and not (cell[0]+10,cell[1],self.genomValues,sun,100) in self.cells:
                        newCells.add((cell[0]+10,cell[1],self.genomValues[gen],sun,100))

                    elif self.counter == 3 and not (cell[0],cell[1]-10,self.genomValues,sun,100) in self.cells:
                        newCells.add((cell[0],cell[1]-10,self.genomValues[gen],sun,100))
                elif gen>8:
                    self.longLife = gen*3
                else:
                    self.longLife = 0
                self.counter+=1
                
        self.cells.update(self.newCells)
        self.newCells = newCells
        for cell in self.newCells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            #pg.draw.rect(screen,THECOLORS['brown'],rect)

        for cell in self.cells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            pg.draw.rect(screen,self.color,rect)

        if self.time > self.longLife:
            self.status = False
            for cell in newCells:
                startPoints.add((cell[0],690,self.genomValues))
        pg.display.flip

class Genom():
    def __init__(self):
        #genom structure [[left,up,right,bottom],....]
        self.genom = ((randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),
                      (randint(0,16),randint(0,16),randint(0,16),randint(0,16)),)

async def Simuation():
    global startPoints
    
    print(startPoints)
    sun = 100 #this parameter changes the sun value
    field = Field(sun)
    field.drawField()
    trees = []
    while True:
        if trees == []:
            sun = 100 #this parameter changes the sun value
            genomValues = Genom().genom
            tree = Tree(genomValues = genomValues, place = (700,690), fieldValues=field.rects)
            trees.append(tree)
            startPoints = set()
            pg.display.update()

        screen.fill(THECOLORS['white'])
        field.drawField()
            
        for tree in trees:
            if tree.status == True:
                tree.startGrow()
            else:
                trees.remove(tree)
        delete = set()
        for cell in startPoints:
            delete.add(cell)
            tree = Tree(genomValues=cell[2], place=(cell[0],cell[1]), fieldValues=field.rects)
            trees.append(tree)
        startPoints = startPoints-delete
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