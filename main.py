import pygame as pg
from pygame.color import THECOLORS
import asyncio
from random import randint
#некоректны livecells возможно с закольцовкой проблемы
#start settings

screenWidth = 1400
screenHeight = 700
synFieldValue = 200.0
timeAmongFrames = 0
dimmingLight = 2 #decreases sun value under livecells
shadows = True

#end settings

startPoints = set()
fieldValues = set()
status = True
pause = False
frames  = 0
checkSecond = False
#buttons

exitButton = pg.Rect(10,10,20,20)
renewButton = pg.Rect(10,40,20,20)
pauseButton = pg.Rect(40,10,20,20)
plusButton = pg.Rect(220,130,20,20)
minusButton = pg.Rect(10,130,20,20)

pg.init()
screen = pg.display.set_mode((screenWidth,screenHeight))
pg.display.set_caption('VirtualTrees', 'images/icon.png')
screen.fill(THECOLORS['white'])

#fonts
f1 = pg.font.Font(None,24)

class Field:
    def __init__(self):
        global fieldValues
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.staticValues = set()

        for width in range(self.screenWidth//10):
            for height in range(self.screenHeight//10):
                rect = (width*10,height*10,synFieldValue) 
                self.staticValues.add(rect)
       

    def drawField(self):
        global fieldValues
        global dimmingLight
        global synFieldValue

        self.allRects = self.staticValues
        if shadows:
            for livevalue in fieldValues:
                values = {(x,y,sun//dimmingLight) for x,y,sun in self.allRects if x==livevalue[0] and y>livevalue[1] and (x,y) not in fieldValues}
                self.allRects.difference_update(set(values))
                self.allRects.update(set(values))
                for value in values:
                    pg.draw.rect(screen,(0+value[2],0+value[2],0+value[2]),pg.Rect(value[0],value[1],10,10))

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

    def startGrow(self):
        global startPoints
        global fieldValues
        global screenWidth
        global screenHeight

        self.time +=1 #counter of time
        self.clearNewCells = set()
        for cell in self.newCells:
            sun = 100 #заглушка епта
            chromosome = cell[2]
            x = cell[0]
            for counter,gen in enumerate(chromosome): #add new cells
                if gen<8:
                    if (cell[0]+10)>screenWidth:
                        x = -10
                    if (cell[0]-10)<0:
                        x = screenWidth+10

                    if counter == 0 and ((x-10,cell[1]) not in fieldValues) and (0<cell[1]<screenHeight): #закольцевать карту
                        self.clearNewCells.add((x-10,cell[1],self.genomValues[gen],sun,100))

                    if counter == 1 and ((x,cell[1]+10) not in fieldValues) and (0<cell[1]<screenHeight):
                        self.clearNewCells.add((x,cell[1]+10,self.genomValues[gen],sun,100))

                    if counter == 2 and ((x+10,cell[1],0) not in fieldValues) and (0<cell[1]<screenHeight):
                        self.clearNewCells.add((x+10,cell[1],self.genomValues[gen],sun,100))

                    if counter == 3 and ((x,cell[1]-10) not in fieldValues) and (0<cell[1]<screenHeight):
                        self.clearNewCells.add((x,cell[1]-10,self.genomValues[gen],sun,100))
                    else:
                        continue

                elif gen>8:
                    self.longLife = gen*3
                else:
                    self.longLife = 0 
                    continue           
        self.cells.update(self.newCells)
        self.newCells = self.clearNewCells  

        for cell in self.cells:
            rect = pg.Rect(cell[0], cell[1],10,10)
            pg.draw.rect(screen,self.color,rect)

        for cell in self.newCells:
            if self.genomValues.index(cell[2])==0:
                rect = pg.Rect(cell[0], cell[1],10,10)
                pg.draw.rect(screen,THECOLORS['brown'],rect)

        if self.time >= self.longLife: #kill old tree
            for cell in self.newCells:
                if self.genomValues.index(cell[2])==0 and ((cell[0],cell[1]) not in fieldValues): #seeds have to be with gen 0
                    startPoints.add((cell[0],690,self.genomValues))
                    
            fieldValues.difference_update({(x,y) for x,y,*rest in self.cells})
            self.cells = set()
            self.status = False

    def returnData(self):
        global startPoints
        global fieldValues
        data = {(x,y) for x,y,*rest in self.cells}
        data2 = {(x,y) for x,y,*rest in self.newCells} 
        fieldValues.update(data2)       
        fieldValues.update(data) 
        fieldValues.update(startPoints)

class Genom:
    def __init__(self):
        #genom structure [[left,up,right,bottom],....]
        self.genom = ((randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),
                      (randint(0,15),randint(0,15),randint(0,15),randint(0,15)),)

async def Simuation():

    def makeMutations(genomValues):
        genomValues = list(genomValues)
        newGenom = [[0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]
        chance = randint(0,3)
        if chance == 0:
            randChromosome = randint(0,7)
            randGen = randint(0,3)
            randValue = randint(0,15)
            for chr,chromosome in enumerate(genomValues):
                for g,gen in enumerate(chromosome):
                    if chr == randChromosome and g == randGen:
                        newGenom[chr][g] = randValue
                    else:
                        newGenom[chr][g] = gen
            for chr,chromosome in enumerate(newGenom):
                newGenom[chr] = tuple(chromosome)
            newGenom = tuple(newGenom)
            return newGenom
        else:
            pass

    global plusButton
    global minusButton
    global startPoints
    global fieldValues
    global synFieldValue
    global timeAmongFrames
    global renewButton
    global exitButton
    global status
    global f1
    global pauseButton
    global pause
    global frames
    global checkSecond
    
    sun = synFieldValue 
    trees = []
    counter = 0
    stabileFrame = 0

    while True:
        frames+=1
        screen.fill(THECOLORS['white']) #renew screen

        pg.draw.rect(screen,(255,255,0),renewButton)
        pg.draw.rect(screen,(255,0,0),exitButton)
        pg.draw.rect(screen,(0,255,0),pauseButton)
        pg.draw.rect(screen,(255,0,0),minusButton)
        pg.draw.rect(screen,(0,255,0),plusButton)

        text1 = f1.render(f'Trees number: {len(trees)}',1,(0,0,0))
        text2 = f1.render(f'Step: {counter}',1,(0,0,0))
        text4 = f1.render(f'Time among frames: {round(timeAmongFrames,1)}',1,(0,0,0))

        if checkSecond == True:
            stabileFrame = frames//5
            checkSecond = False
            frames = 0
        
        text3 = f1.render(f'FPS: {stabileFrame}',1,(0,0,0))
        screen.blit(text1, (10,70))
        screen.blit(text2, (10,90))         
        screen.blit(text3, (10,110))
        screen.blit(text4, (30,130))
        
        if pause == False:
            counter+=1
            if trees == [] or status == False:
                trees = []
                counter = 0
                genomValues = Genom().genom
                field = Field()
                startPoints = set()
                fieldValues = set()
                tree = Tree(genomValues = genomValues, place = (700,690))
                trees.append(tree)

            for tree in trees:       
                if tree.status == True:
                    tree.returnData()
                else:
                    trees.remove(tree) #delete old trees
            
            for tree in trees:
                tree.startGrow()

            field.drawField()

            for cell in startPoints:
                newGenom = makeMutations(cell[2])
                if newGenom:
                    tree = Tree(genomValues=newGenom, place=(cell[0],cell[1]))
                else:
                    tree = Tree(genomValues=cell[2], place=(cell[0],cell[1]))
                trees.append(tree)
            startPoints = set()

            pg.display.flip()
            await asyncio.sleep(timeAmongFrames)
        else:
            await asyncio.sleep(0.1)

async def GetFPS():
    global frames
    global checkSecond
    while True:
        await asyncio.sleep(5)
        checkSecond = True
        
async def CheckEvents():
    global timeAmongFrames
    global renewButton
    global exitButton
    global status
    global pauseButton
    global pause
    global plusButton
    global minusButton
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if renewButton.collidepoint(event.pos):
                    status = False
                if exitButton.collidepoint(event.pos):
                    running = False
                if pauseButton.collidepoint(event.pos):
                    if pause == False:
                        pause = True
                    else:
                       pause = False
                if minusButton.collidepoint(event.pos):
                    if timeAmongFrames>0:
                        timeAmongFrames -= 0.1
                if plusButton.collidepoint(event.pos):
                    timeAmongFrames += 0.1
                
                await asyncio.sleep(0.01)
                status = True

        await asyncio.sleep(0.01)
    pg.quit()

async def main():
    await asyncio.gather(CheckEvents(), Simuation(),GetFPS())

asyncio.run(main())