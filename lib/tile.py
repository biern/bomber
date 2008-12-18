# -*- coding: utf-8 -*-
import logging

class Tile(object):
    """ Abstract class defining necessary properties for each ingame object"""
    log = logging.getLogger("tile_object")
    background = False
    offset_x = offset_y = 0
    direction = "down"
    speed = 0
    action = 'none'
    __priority = 5 # drawing priority, use 'drawing_priority' property instead of this
    __name = "" # name is used by a render engine to load display data of the object
    __priority_name = {
                     'lowest':1,
                     'low':3,
                     'normal':5,
                     'high':7,
                     'highest':9,
                     }
    
    def __init__(self, x, y, board, add=True):
        self.x = x
        self.y = y
        self.board = board
        if self.background:
            self.drawing_priority = -1
        if add:
            self.add_to_board()
    
    def add_to_board(self):
        self.board.add_tile(self)
    
    def remove_from_board(self):
        self.board.remove_tile(self)
    
    #-Properties-------------------------------------------------------------------
     
    def get_name(self):
        if not self.__name:
            return self.__class__.__name__.lower()
        return self.__name
    
    def set_name(self, name):
        if name != name.lower():
            self.log.warning("Name '%s' contains uppercase letters, they will be lowered!" % name)
            name = name.lower()
        self.__name = name
    
    def set_drawing_priority(self, priority):
        if type(priority) == int:
            self.__priority = priority
        elif type(priority) == str:
            try:
                self.__priority = self.__priority_name[priority]
            except KeyError:
                self.log.warning("Priority name '%s' not found, using default" 
                                 % priority)
                self.__priority = 5
    
    def get_drawing_priority(self):
        return self.__priority

    name = property(get_name, set_name)
    
    #FIXME: Sort this property - it should work when setting static
    # class variable as well, but it does not
    drawing_priority = property(get_drawing_priority, set_drawing_priority)
    
    