import pygame, sys, time
from settings import *
from buttonClass import *

class App:
    def __init__(self):
        pygame.init()
        ''' add music for fun
        pygame.mixer.music.load('lastgoodbye.mp3')
        '''
        pygame.mixer.music.play(0)
        self.window=pygame.display.set_mode((WIDTH,HEIGHT))
        self.running=True
        self.grid=board
        self.solvedGrid=solved_board
        self.selected=None
        self.mousePos=None
        self.state="playing"
        self.string="PRESS SPACE TO ACTIVATE SOLVER"
        self.col=BLACK
        self.playingButtons=[]
        self.menuButtons=[]
        self.endButtons=[]
        self.lockCells=[]
        self.load()
        self.click=None
        self.font=pygame.font.SysFont("comicsans",40)
        

    def run(self):
        start=time.time()
        while self.running:
            if self.state=="playing":
                play_time=round(time.time()-start)
                
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            
        pygame.quit()
        sys.exit()


###########PLAYING##########################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
                
            if event.type==pygame.MOUSEBUTTONDOWN:
                selected=self.mouseOnGrid()
                buttonSelected=self.playingButtons[0].update(self.mousePos)
                if selected:
                    self.selected=selected
                else:
                    self.selected=None
                

            if event.type==pygame.KEYDOWN:
                if self.selected!=None and self.selected not in self.lockCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]]=int(event.unicode)
                    if event.key==pygame.K_h:
                        self.grid[self.selected[1]][self.selected[0]]=self.solvedGrid[self.selected[1]][self.selected[0]]    
                    if event.key==pygame.K_BACKSPACE:
                        self.grid[self.selected[1]][self.selected[0]]=0
                    

                if event.key==pygame.K_SPACE:
                    solved=self.solver(self.grid)
                    if solved:
                        print("Solving")

                if event.key==pygame.K_DELETE:
                    self.clear()
                    self.string="PLAY AGAIN!"
                    self.col=BLACK
                    pygame.display.update()
                if event.key==pygame.K_e:
                    flag=0
                    for i in range(0,9):
                        for j in range(0,9):
                            if self.grid[i][j]!=self.solvedGrid[i][j]:
                                flag=1
                                break
                        if flag==1:
                            break
                    if flag==1:
                        self.string="LOSE"
                        self.col=CRIMSON
                        pygame.display.update()
                    else:
                        self.string="WIN"
                        self.col=GREEN
                        pygame.display.update()
                        
                    
                
                    

             

    def playing_update(self):
        self.mousePos=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        for button in self.playingButtons:
            button.update(self.mousePos)

    def playing_draw(self):
        self.window.fill(PINK)
        for button in self.playingButtons:
            button.draw(self.window)
            button.addText(self.window)
                    
        if self.selected:
            self.drawSelection(self.window,self.selected)

        self.shadeLockedCells(self.window,self.lockCells)
        
        self.drawNumbers(self.window)        
        self.instruction(self.window,self.string,self.col)
        self.drawContainer(self.window)
        pygame.display.update()


##############PLAYING#########################

##############SUDOKU SOLVE####################
        
    def empty(self,grid):
        for i in range(0,9):
            for j in range(0,9):
                if self.grid[j][i]==0:
                    return (j,i)
        return None

    def valid(self,grid,num,pos):
        for i in range(0,9):
            if self.grid[i][pos[1]]==num and i!=pos[0]:
                return False
            if self.grid[pos[0]][i]==num and i!=pos[1]:
                return False
        x=pos[0]//3
        y=pos[1]//3

        for i in range(x*3,x*3+3):
            for j in range(y*3,y*3+3):
                if self.grid[i][j]==num and pos!=(i,j):
                    return False
        return True
    
    def solver(self,grid):
        find=self.empty(self.grid)
        if not find:
            return True
        r,c= find
        for num in range(1,10):
            if self.valid(self.grid,num,(r,c)):
                self.drawSelection(self.window,(c,r))
                self.drawNumbers(self.window)
                self.grid[r][c]=num
                pygame.time.delay(30)
                pygame.display.update()
                
                if self.solver(self.grid):
                    return True
                else:
                    self.grid[r][c]=0
                    self.drawNumbers(self.window)
                    pygame.time.delay(30)
                    pygame.display.update()
        return False
        

    
     
##############SUDOKU SOLVE####################


###############HELPERS#########################

    def shadeLockedCells(self,window,locked):
        for cell in locked:
            pygame.draw.rect(window,LOCKEDCELLCOLOUR,(cell[0]*cellsize+gridPos[0],cell[1]*cellsize+gridPos[1],cellsize,cellsize))

    def instruction(self,window,string,col):
        pos=[50,550]
        self.textToScreen(window,string,pos,col)
        
    def drawNumbers(self,window):
        for i in range(0,9):
            for j in range(0,9):
                num=self.grid[j][i]
                if num!=0:
                    pos=[i*cellsize+gridPos[0]+cellsize/2.5,j*cellsize+gridPos[1]+cellsize/4]
                    self.textToScreen(window,str(num),pos)

    def drawSelection(self,window,pos,color=CRIMSON):
        pygame.draw.rect(window, WHITE,(pos[0]*cellsize+gridPos[0],pos[1]*cellsize+gridPos[1],cellsize,cellsize))
        pygame.draw.rect(window, color,(pos[0]*cellsize+gridPos[0],pos[1]*cellsize+gridPos[1],cellsize,cellsize),4)
        
    def drawContainer(self,window):
        pygame.draw.rect(window,BLACK,(gridPos[0],gridPos[1],WIDTH-150,HEIGHT-150),2)
        for i in range(9):
            thickness=1
            if i%3==0:
                thickness=2
            pygame.draw.line(window,BLACK,(gridPos[0]+i*cellsize,gridPos[1]),(gridPos[0]+i*cellsize,gridPos[1]+450),thickness)
            pygame.draw.line(window,BLACK,(gridPos[0],gridPos[1]+i*cellsize),(gridPos[0]+450,gridPos[1]+i*cellsize),thickness)
               
    def clear(self):
        keep=self.lockCells
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if [j,i] not in self.lockCells:
                    self.grid[i][j]=0

    def mouseOnGrid(self):
        if self.mousePos[0]<gridPos[0] or self.mousePos[1]<gridPos[1] or self.mousePos[0]>gridPos[0]+gridSize or self.mousePos[1]>gridPos[1]+gridSize:
            return False
        else:
            box_x=(self.mousePos[0]-gridPos[0])//cellsize
            box_y=(self.mousePos[1]-gridPos[1])//cellsize
            return (box_x,box_y)
        
    def textToScreen(self,window,text,pos,color=BLACK):
        font=self.font.render(text,False,color)
        window.blit(font,pos)
        window.blit(font,pos)

    def loadButtons(self):
        self.playingButtons.append(Button(260,20,80,30,"Solve!"))
        
    def load(self):
        self.loadButtons()

        #locked cells
        for i,col in enumerate(self.grid):
            for j,num in enumerate(col):
                if num!=0:
                    self.lockCells.append([j,i])
        
        
    def isInt(self,string):
        try:
            int(string)
            return True
        except:
            return False
