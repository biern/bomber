# -*- coding: utf-8 -*-

import random

from lib.mod import Mod
from lib.tile import Tile
from lib.board import Board

class Pointer(Tile):
    drawing_priority = 9

class Bomb(Tile):
    action = 'ticking'
    drawing_priority = 5

class Grid(Tile):
    background = True

class TestMod(Mod):
    full_name = 'Bombastik Bomberman'
    quit = False
    def __init__(self):
        super(TestMod, self).__init__()
        self.add_bomb = False
        self.board = Board(self.config['board']['size'])

        x, y = self.board.get_size()
        for i in range(x):
            for j in range(y):
                Grid(i,j,self.board)
                
        self.pointer = Pointer(1,1,self.board)
        print "Press escape to quit"
        print "Use arrow keys to move"
        print "Enter to add a bomb"
        print "1 to add 100 bombs"
        print "r to remove all bombs"
    
    def handle_input(self, input):
        for key in input.get('keydown',[]):
            if key == 'escape':
                self.quit = True
            if key == 'return':
                self.add_bomb = True
            if key == 'up':
                self.pointer.y -= 1
            if key == 'down':
                self.pointer.y += 1
            if key == 'left':
                self.pointer.x -=1
            if key == 'right':
                self.pointer.x += 1
            if key == 'r':
                for tile in self.board.get_tiles_of_type(Bomb):
                    tile.remove_from_board()
                print "Removing bombs"
            if key == '1':
                for i in range(99):
                    Bomb(random.randint(0,self.board.width-1),random.randint(0,self.board.height-1), self.board)
                print "Adding 100 bombs"
        
                    
    def update(self):
        if self.add_bomb:
            Bomb(self.pointer.x, self.pointer.y, self.board)
            self.add_bomb = False
        return self.quit


mod = TestMod