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
                rect = (width*10,height*10,sun,False) #(x,y,sun,condition (true alive, false died))
                self.rects.add(rect)

    def drawField(self, livecells: set):
        global fieldValues
        self.livecells = livecells
        self.newRects = set()
        
        if self.livecells != set():
            for livecell in self.livecells:
                for cell in self.rects:
                    if cell[3] == True:
                        self.newRects.add((cell[0],cell[1],0,cell[3]))
                    elif cell[0] == livecell[0] and livecell[1]<cell[1]:
                        self.newRects.add((cell[0],cell[1],cell[2]//1.5,cell[3]))
                    else:
                        self.newRects.add(cell)
        else:
            print('no livecells')
            for cell in self.rects:
                self.newRects.add(cell)

        self.rects = self.newRects
        fieldValues = self.rects


        for rectValue in self.rects:
            rect = pg.Rect(rectValue[0], rectValue[1],10,10)
            pg.draw.rect(screen,(0+rectValue[2],0+rectValue[2],0),rect) #make many yellow values
            pg.draw.rect(screen,(0,0,0),rect, width=1)
        pg.display.flip

class Tree:
    def __init__(self, genomValues: list, place: tuple):
        self.color = (randint(0,255),randint(0,255),randint(0,255))
        self.cells = set() #(x,y,genom,sun,energy)
        self.startPoint = pg.Rect(place[0],place[1],10,10)
        self.genomValues = genomValues
        self.newCells = set()
        self.time = 0
        self.longLife = 0
        self.status = True

        self.newCells.add((place[0],place[1],self.genomValues[0],100,100))
        self.cells.add((place[0],place[1],self.genomValues[0],100,100)) #genom 0 always starts
        pg.draw.rect(screen, self.color, self.startPoint)

    def startGrow(self):
        global startPoints
        global fieldValues

        self.time +=1 #counter of time
        self.clearNewCells = set()
        for cell in self.newCells:
            sun = 100 #заглушка епта
            self.counter = 0
            chromosome = cell[2]
                
            for gen in chromosome: #add new cells
                if gen<8:
                    # if (self.counter == 0) and ((cell[0]-10,cell[1],self.genomValues,sun,100) not in self.cells) and ((cell[0]-10,cell[1],0,True) not in fieldValues):
                    #     self.clearNewCells.add((cell[0]-10,cell[1],self.genomValues[gen],sun,100))

                    # elif (self.counter == 1) and ((cell[0],cell[1]+10,self.genomValues,sun,100) not in self.cells) and ((cell[0],cell[1]+10,0,True) not in fieldValues):
                    #     self.clearNewCells.add((cell[0],cell[1]+10,self.genomValues[gen],sun,100))

                    # elif (self.counter == 2) and ((cell[0]+10,cell[1],self.genomValues,sun,100) not in self.cells) and ((cell[0]+10,cell[1],0,True) not in fieldValues):
                    #     self.clearNewCells.add((cell[0]+10,cell[1],self.genomValues[gen],sun,100))

                    # elif (self.counter == 3) and  ((cell[0],cell[1]-10,self.genomValues,sun,100) not in self.cells) and ((cell[0],cell[1]-10,0,True) not in fieldValues):
                    #     self.clearNewCells.add((cell[0],cell[1]-10,self.genomValues[gen],sun,100))

                    if self.counter == 0:
                        self.clearNewCells.add((cell[0]-10,cell[1],self.genomValues[gen],sun,100))

                    elif self.counter == 1:
                        self.clearNewCells.add((cell[0],cell[1]+10,self.genomValues[gen],sun,100))

                    elif self.counter == 2:
                        self.clearNewCells.add((cell[0]+10,cell[1],self.genomValues[gen],sun,100))

                    elif self.counter == 3:
                        self.clearNewCells.add((cell[0],cell[1]-10,self.genomValues[gen],sun,100))
                elif gen>8:
                    self.longLife = gen*3
                else:
                    self.longLife = 0
                self.counter+=1             

        for cell in self.cells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            pg.draw.rect(screen,self.color,rect)

        delete = set()
        for cell in self.newCells:
            if cell in self.cells:
                delete.add(cell)
        
        self.clearNewCells.difference_update(delete) #delete fantom cells

        self.newCells = self.clearNewCells
        self.cells.update(self.clearNewCells)   

        for cell in self.newCells:
            if self.genomValues.index(cell[2])==0:
                rect = pg.Rect(cell[0], cell[1],10,10)
                pg.draw.rect(screen,THECOLORS['brown'],rect)

        if self.time > self.longLife: #kill old tree
            for cell in self.clearNewCells:
                if self.genomValues.index(cell[2])==0: #seeds have to be with gen 0
                    startPoints.add((cell[0],690,self.genomValues))
            self.status = False

    def returnData(self):
        data = set()
        for cell in self.cells:
            data.add((cell[0],cell[1],0,True)) #x,y,sun,condition
        for cell in self.newCells:
            data.add((cell[0],cell[1],0,True))

        return data

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
    global fieldValues
    sun = 200 #this parameter changes the sun value
    trees = []
    field = Field(sun)
    livecells = set()

    while True:
        
        screen.fill(THECOLORS['white']) #renew screen
        field.drawField(livecells)
        fieldValues = field.rects

        if trees == []:
            sun = 100 #this parameter changes the sun value
            genomValues = Genom().genom
            tree = Tree(genomValues = genomValues, place = (700,690))
            trees.append(tree)
            startPoints = set()
            livecells = set()

        for tree in trees:
            if tree.status == True:
                if tree.returnData:
                    livecells.update(tree.returnData()) #returns live cells
                    tree.startGrow()
                
            else:
                trees.remove(tree)

        delete = set()
        for cell in startPoints:
            delete.add(cell)
            tree = Tree(genomValues=cell[2], place=(cell[0],cell[1]))
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