import pygame
from constants import *

class Node(object):
    def __init__(self, x, y, radius=8):
        self.x = round(x / TILEWIDTH)*TILEWIDTH
        self.y = round(y / TILEHEIGHT)*TILEHEIGHT
        self.color = RED
        self.radius = radius
        self.neighbors = []

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def updatePosition(self, x, y):
        self.x = round(x / TILEWIDTH)*TILEWIDTH
        self.y = round(y / TILEHEIGHT)*TILEHEIGHT
        
    def addNeighbor(self, node):
        self.neighbors.append(node)

    def removeNeighbor(self, node):
        if node in self.neighbors:
            self.neighbors.remove(node)
            
    def increaseRadius(self):
        self.radius += 1

    def decreaseRadius(self):
        self.radius -= 1
        if self.radius == 0: self.radius = 1

    def renderPathToNeighbors(self, screen):
        for neighbor in self.neighbors:
            pygame.draw.line(screen, WHITE, (self.x, self.y), (neighbor.x, neighbor.y), 2)
            
    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class NodeGroup(object):
    def __init__(self):
        self.nodes = []

    def add(self, x, y, radius):
        node = self.getNode(x, y)
        if node is None:
            self.nodes.append(Node(x, y, radius))

    def delete(self, node):
        for n in self.nodes:
            n.removeNeighbor(node)
        if node in self.nodes:
            self.nodes.remove(node)
        
    def getNode(self, x, y):
        x = round(x / TILEWIDTH)*TILEWIDTH
        y = round(y / TILEHEIGHT)*TILEHEIGHT
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node
        return None

    def normalize(self):
        for node in self.nodes:
            node.color = RED
    
    def render(self, screen):
        for node in self.nodes:
            node.renderPathToNeighbors(screen)
        for node in self.nodes:
            node.render(screen)

            
class NodeShadow(Node):
    def __init__(self):
        Node.__init__(self, 0, 0)
        self.color = (212, 138, 138)
        
    #def render(self, screen):
    #    self.x = round(x / TILEWIDTH)*TILEWIDTH
    #    self.y = round(y / TILEHEIGHT)*TILEHEIGHT
        #self.x = x
        #self.y = y
    #    Node.render(self, screen)
