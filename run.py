import pygame
from pygame.locals import *
from constants import *
from grid import Grid
from node import NodeGroup, NodeShadow
from copy import deepcopy
#node modes:  "create", "move", "delete", "connect"

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.probenode = NodeShadow()
        self.nodegroup = NodeGroup()
        self.selectedNode = None
        self.selectedNodes = []
        self.mode = "create"
        #self.path = None
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.grid.toggle()
                if event.key == K_RIGHTBRACKET:
                    self.probenode.increaseRadius()
                if event.key == K_LEFTBRACKET:
                    self.probenode.decreaseRadius()
                if event.key == K_LEFT:
                    self.grid.fade()
                elif event.key == K_RIGHT:
                    self.grid.unfade()
                    
                if event.key == K_1:
                    self.mode = "create"
                    self.probenode = NodeShadow()
                    self.selectedNode = None
                    self.selectedNodes = []
                    self.nodegroup.normalize()
                    
                if event.key == K_2:
                    self.mode = "move"
                    self.selectedNode = None
                    self.selectedNodes = []
                    self.nodegroup.normalize()
                    self.probenode = None
                    
                if event.key == K_3:
                    self.mode = "delete"
                    self.probenode = None

                if event.key == K_4:
                    self.mode = "connect"
                    self.selectedNode = None
                    self.selectedNodes = []
                    self.nodegroup.normalize()
                    self.probenode = None
                    
                if event.key == K_DELETE:
                    if self.mode == "delete":
                        for node in self.selectedNodes:
                            self.nodegroup.delete(node)
                            
            elif event.type == MOUSEBUTTONDOWN:
                if self.mode == "move":
                    x, y = pygame.mouse.get_pos()
                    node = self.nodegroup.getNode(x, y)
                    if node is not None:
                        copynode = deepcopy(node)
                        self.probenode = node
                        #self.probenode = NodeShadow()
                        #self.probenode.x = copynode.x
                        #self.probenode.y = copynode.y
                        #self.probenode.radius = copynode.radius
                        #self.probenode.color = copynode.color
                        #self.nodegroup.delete(node)
                elif self.mode == "connect":
                    x, y = pygame.mouse.get_pos()
                    self.selectedNode = self.nodegroup.getNode(x, y)
                    #if self.selectedNode is not None:
                    #    pass
                        
            elif event.type == MOUSEBUTTONUP:
                if self.mode == "create":
                    x, y = pygame.mouse.get_pos()
                    self.nodegroup.add(x, y, self.probenode.radius)
                elif self.mode == "delete":
                    #print("delete")
                    x, y = pygame.mouse.get_pos()
                    self.selectedNode = self.nodegroup.getNode(x, y)
                    if self.selectedNode is not None:
                        self.selectedNode.color = YELLOW
                        self.selectedNodes.append(self.selectedNode)
                    #print(self.selectedNode)
                elif self.mode == "move":
                    if self.probenode is not None:
                        #x, y = pygame.mouse.get_pos()
                        #self.nodegroup.add(x, y, self.probenode.radius)
                        self.probenode = None
                elif self.mode == "connect":
                    if self.selectedNode is not None:
                        x, y = pygame.mouse.get_pos()
                        node = self.nodegroup.getNode(x, y)
                        if node is not None:
                            if node != self.selectedNode:
                                self.selectedNode.addNeighbor(node)
                                node.addNeighbor(self.selectedNode)
                                self.selectedNode = None
                    
        self.checkMouseEvents()
        
    def checkMouseEvents(self):
        #if pygame.mouse.get_focused():
        #    print(pygame.mouse.get_pos())
        pass
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.grid.render(self.screen)

        self.nodegroup.render(self.screen)

        if self.probenode is not None:
            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.probenode.updatePosition(x, y)
                self.probenode.render(self.screen)

        if self.mode == "connect":
            if self.selectedNode is not None:
                x, y = pygame.mouse.get_pos()
                x = round(x / TILEWIDTH)*TILEWIDTH
                y = round(y / TILEHEIGHT)*TILEHEIGHT
                pygame.draw.line(self.screen, WHITE, (self.selectedNode.x, self.selectedNode.y), (x, y), 1)
                
        pygame.display.update()



if __name__ == "__main__":
    game = GameController()
    while True:
        game.update()
