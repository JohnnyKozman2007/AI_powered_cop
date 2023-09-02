import os
from pygame.locals import *
import pygame
from queue import PriorityQueue
from map_generator import make_map 
from tkinter import messagebox
from tile import Tile
import time
import random
import numpy
import tensorflow 
from tensorflow.keras.models import load_model


pygame.init()
class Player(pygame.sprite.Sprite):
    x = 44
    y = 44
    speed = 10

    def __init__(self,groups):
        super().__init__(groups)
    def get_rect_dim(self,image,pos):
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.rect = self.rect
    def moveRight(self):
        self.x = self.x + self.speed
 
    def moveLeft(self):
        self.x = self.x - self.speed
 
    def moveUp(self):
        self.y = self.y - self.speed
 
    def moveDown(self):
        self.y = self.y + self.speed


class Enemy(pygame.sprite.Sprite):
    x = 2*40
    y = 1*40
    speed = 40
    start = False

    def __init__(self,groups,image,x,y):
        super().__init__(groups)
        self.get_rect_dim(image)
        self.x = x
        self.y = y
        self.pos = False
    def get_rect_dim(self,image,pos=(2*40,18*40)):
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.rect = self.rect
    def get_neighbours(self,pos):
        neighbours = []
        for i in range(-1,2):
            for x in range(-1,2):
                if not [pos[0]+i,pos[1]+x] in Tile.tiles:
                    if not pos[0]+i <= 0 and not pos[0]+i >= 30 and not pos[1]+x <= 0 and not pos[1]+x >= 30:
                        #print(9,not pos[0]+i < 0,not pos[0]+i >= 30)
                            neighbours.append([pos[0]+i,pos[1]+x])
        return neighbours
    def preform_move(self,pos):

        if pos[0] > self.x//40:
            self.moveRight()
        elif pos[0] < self.x//40:
            self.moveLeft()    
        if pos[1] > self.y//40:
            self.moveDown()
        elif pos[1] < self.y//40:
            self.moveUp()     
        #self.border()
    def change_position(self):
        #print('changing')
        if not self.pos :
            pos = (self.x//40,self.y//40)
        else:
            pos = self.pos
        next_to = self.get_neighbours(pos)
        
        #print(next_to)
        pos = next_to[random.randint(0,len(next_to)-1)]
        self.preform_move(pos)
        #print(pos)
        self.pos = pos
        return pos

    def moveRight(self):
        self.x = self.x + 40
 
    def moveLeft(self):
        self.x = self.x - 40
 
    def moveUp(self):
        self.y = self.y - 40
 
    def moveDown(self):
        self.y = self.y + 40
    def show(self,window,pos):
        window.blit(self.image,(pos[0]*40,pos[1]*40))




class Maze:
    def __init__(self):
       self.M = 30
       self.N = 20
       self.maze = make_map(self.M,self.N)
       self.visible_sprites = pygame.sprite.Group()

    def overview(self):
        map = []
        for i in range(30):
            for x in range(20):
                map.append([i,x])
    def draw(self,display_surf,image_surf):
       bx = 0
       by = 0
       street = pygame.image.load("street.png").convert()
       for i in range(0,self.M*self.N):
           
           if self.maze[ bx + (by*self.M) ] == 1:
               #display_surf.blit(image_surf,( bx * 40 , by * 40))
               Tile(( bx * 40 , by * 40),self.visible_sprites,image_surf)
               #self.blocks.append()

           else:
               display_surf.blit(street,( bx * 40 , by * 40))
           bx = bx + 1
           if bx > self.M-1:
               bx = 0 
               by = by + 1


class App:
 
    windowWidth = 1200
    windowHeight = 800
    player = 0
 
    def __init__(self,maze = None):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.current_time = pygame.time.get_ticks()
        self.make_move_time = pygame.time.get_ticks()
        self.make_move = True
        self.close = []
        self.safes = []
        self.pattern = []
        self.safe_pos = [[1*40,18*40],[18*40,1*40],[28*40,18*40]]
        self.open = {}
        if maze:
            self.maze = maze
        else:
            self.maze = Maze()
        self.overview = self.maze.overview()
        self.player = Player(self.maze.visible_sprites)
        self.on_init()
        
        
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight))
        
        pygame.display.set_caption('AI Powered Cops ! HIDE ')
        self._running = True
        self._image_surf = pygame.image.load("cop.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()

        path = "..\\graphics\\trials"
        folders = [f for f in os.listdir(path) ]

        path_2 = "..\\graphics\\thiefs"
        folders_2 = [f for f in os.listdir(path_2) ]
        #print(folders_2)
        #print(folders)
        self.obj_1 = folders[random.randint(0,len(folders)-1)]
        self.obj_2 = folders[random.randint(0,len(folders)-1)]
        self.obj_3 = folders_2[random.randint(0,len(folders_2)-1)]
        
        self.objects = [self.obj_1,self.obj_2,self.obj_3]
        self.model = load_model("C:\\Users\\Sidho\\OneDrive\\Desktop\\cop\\thief detector.h5")
        x = 0
        for i in self.objects:
            
            try:
                img = tensorflow.keras.preprocessing.image.load_img("..\\graphics\\trials//" + i)
            except:
                img = tensorflow.keras.preprocessing.image.load_img("..\\graphics\\thiefs//" + i)

            img = tensorflow.keras.preprocessing.image.img_to_array(img)
            img = numpy.expand_dims(img, axis=0)
            result = self.model.predict(img) * 100
            if result > 50:
                self.enemy_surface = pygame.image.load("..\\graphics\\thiefs//" + i).convert()
                self.enemy_surface = pygame.transform.scale(self.enemy_surface, (40, 40))
                x = random.randint(0,len(self.safe_pos)-1)
                self.enemy = Enemy(self.maze.visible_sprites,self.enemy_surface,self.safe_pos[x][0],self.safe_pos[x][1])
                del self.safe_pos[x]
                #self.maze.visible_sprites
            else:
                self.safe_surface = pygame.image.load("..\\graphics\\trials//" + i).convert()
                self.safe_surface = pygame.transform.scale(self.safe_surface, (40, 40))

                x = random.randint(0,len(self.safe_pos)-1)
                self.safe = Enemy(self.maze.visible_sprites,self.safe_surface,self.safe_pos[x][0],self.safe_pos[x][1])
                self.safes.append(self.safe)
                del self.safe_pos[x]
                


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def get_neighbours(self,pos):
        neighbours = []
        for i in range(-1,2):
            for x in range(-1,2):
                if not [pos[0]+i,pos[1]+x] in Tile.tiles:
                    if not pos[0]+i <= 0 and not pos[0]+i >= 30 and not pos[1]+x <= 0 and not pos[1]+x >= 30:

                        #print(9,not pos[0]+i < 0,not pos[0]+i >= 30)
                        neighbours.append([pos[0]+i,pos[1]+x])
        return neighbours
    def preform_move(self,window,pos):
        #print(len(self.pattern))
        window.blit(self._image_surf,(pos[0]*40,pos[1]*40))
        self.pattern = self.pattern[:-1]
        self.player.x = pos[0]*40
        self.player.y = pos[1]*40
        # if pos[0] > self.player.x//40:
        #     self.player.moveRight()
        # elif pos[0] < self.player.x//40:
        #     self.player.moveLeft()    
        # pygame.display.update()
        # if pos[1] > self.player.y//40:
        #     self.player.moveDown()
        # elif pos[1] < self.player.y//40:
        #     self.player.moveUp()     
        self.make_move = False
        self.make_move_time = pygame.time.get_ticks()
        self.maze.visible_sprites.update()
        pygame.display.flip()
        #print(self.player.x,self.player.y)
    def dis(self,x,y):
        dist = pygame.math.Vector2(x[0], x[1]).distance_to((y[0], y[1]))
        return dist
    def make_grid(self, rows, width):
        grid = []
        for i in range(rows):
            for j in range(width):
                if [i,j] not in Tile.tiles:
                    grid.append([i,j])
                # if i == 28 and j == 19:
                #     print('made')
        return grid
    def reconstruct_path(self,came_from, current):
        if len(self.pattern) > 0:
            return
        self.pattern = []
        while current in came_from:
            current = came_from[current]
            self.pattern.append(current)
            # if current in Tile.tiles:
            #     print('disaster')
            # current_time = pygame.time.get_ticks()

            # if not self.make_move:
            #     if current_time - self.make_move_time >= 100000000000000:
            #         self.make_move = True
            #         #current_time = pygame.time.get_ticks()
            # self.make_move = False
            # self.preform_move(self._display_surf,current)
            # self.border()
            # break
        
    def a_star(self,start = False,num = 3,enemy = None):
        #print(self.open)
        #
        start = (self.player.x//40,self.player.y//40)

        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        grid = self.make_grid(30, 30)


        g_score = {tuple(spot): float("inf") for spot in grid }
        g_score[start] = 0
        f_score = {tuple(spot): float("inf") for spot in grid }
        f_score[start] = self.dis(start,enemy)#h(orig_pos.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            open_set_hash.remove(current)
            #print(current,'deleted')
            #print(current,enemy)
            if current == enemy:
                #print("arrived")
                #print(came_from)
                self.reconstruct_path(came_from, enemy)
                return
                #reconstruct_path(came_from, end, draw)
                #end.make_end()
                #return True
            
            for neighbor in self.get_neighbours(current):
                #print(neighbor in Tile.tiles)
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[tuple(neighbor)]:
                    came_from[tuple(neighbor)] = current
                    g_score[tuple(neighbor)] = temp_g_score
                    f_score[tuple(neighbor)] = temp_g_score + self.dis(start,enemy)
                    if tuple(neighbor) not in open_set_hash:
                        count += 1
                        open_set.put((f_score[tuple(neighbor)], count, tuple(neighbor)))
                        open_set_hash.add(tuple(neighbor))
                        #neighbor.make_open()


    def border(self):
        for i in self.maze.visible_sprites:
            #print(self.player.rect,i.rect)
            if self.player.rect == i.rect:
                continue
            if self.player.rect.colliderect(i.rect):
                if self.player.x-39 <= i.rect.x and self.player.x < i.rect.x:

                    overlap = i.rect.x  - self.player.x-40 
                    self.player.x += int(overlap)
                if self.player.x >= i.rect.x-40 and self.player.x > i.rect.x:

                    overlap = self.player.x  - i.rect.x-40  
                    self.player.x -= int(overlap)
                if self.player.y-40 <= i.rect.y and self.player.y < i.rect.y:

                    overlap = i.rect.y  - self.player.y-40 

                    self.player.y += int(overlap)
                if self.player.y >= i.rect.y-40 and self.player.y > i.rect.y:

                    overlap = self.player.y  - i.rect.y-40  

                    self.player.y -= int(overlap)    
    def on_render(self):
        
        self._display_surf.fill((0,0,0))
        
        self.maze.draw(self._display_surf,self._block_surf)
        #self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        #grid = self.make_grid(30,20)
        #grid = grid[random.randint(0,len(grid)-1)]


        
        #self._display_surf.blit(theApp.enemy_surface,(grid[0]*40,grid[1]*40))

        new_thief_pos = theApp.enemy.change_position()
        #theApp.enemy.preform_move(new_thief_pos)
        theApp.enemy.show(self._display_surf,new_thief_pos)

        for i in theApp.safes:
            new_safe_pos = i.change_position()

            i.show(self._display_surf,new_safe_pos)
      
            
        self.player.get_rect_dim(self._image_surf,(self.player.x,self.player.y))
        
        
        self.border()
        self.a_star(enemy = (theApp.enemy.x//40,theApp.enemy.y//40))
        if self.current_time-self.make_move_time  >= 10:
            #print('made')
            self.preform_move(self._display_surf,self.pattern[-1])

            
            
        else:
            #print('wait',self.current_time-self.make_move_time)
            self.current_time = pygame.time.get_ticks()
        #self._display_surf.blit(theApp.enemy_surface,(-40+new_thief_pos[0]*40,-40+new_thief_pos[1]*40))
        
        if theApp.enemy.x - 75 < self.player.x and theApp.enemy.x + 75 > self.player.x and theApp.enemy.y - 75 < self.player.y and theApp.enemy.y + 75 > self.player.y:
            messagebox.showinfo("showinfo", "AI wins !")
            restart()

        #print(self.enemy_surface.x,self.enemy_surface.y)
 
        self.maze.visible_sprites.update()
        pygame.display.flip()
        

 


def restart():
    new_maze = Maze()
    theApp = App(new_maze)
    theApp.on_render()
    done = False
    while not done:
        theApp.on_render()
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.event.pump()
        keys = pygame.key.get_pressed()
if __name__ == "__main__" :
    theApp = App()
    theApp.on_render()
    done = False
    while not done:
        theApp.on_render()
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.event.pump()
        keys = pygame.key.get_pressed()




        # if (keys[K_ESCAPE]):
        #     self._running = False    
        