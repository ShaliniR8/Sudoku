import pygame
from settings import *


class Button:
    def __init__(self,x,y,width,height,text=None,function=None,colour=(102, 0, 102),highlight=(204, 0, 204),param=None):
        self.width=width
        self.height=height
        self.image=pygame.Surface((width,height))
        self.pos=(x,y)
        self.rect=self.image.get_rect()
        self.rect.topleft=self.pos
        self.selected=function
        self.text=text
        self.font=pygame.font.SysFont('Arial', 21)
        self.colour=colour
        self.highlight=highlight
        self.function=function
        self.param=param
        self.hover=False

    def update(self,mouse):
        if self.rect.collidepoint(mouse):
            self.hover=True
        else:
            self.hover=False

    def draw(self,window):
        if self.hover:
            self.image.fill(self.highlight)
        else:
            self.image.fill(self.colour)
        window.blit(self.image,self.pos)

    def addText(self,window):
        font=self.font.render(self.text,False,WHITE)
        h=self.pos[0]+self.width/5
        v=self.pos[1]+self.height/6
        window.blit(font,(h,v))
        
        
