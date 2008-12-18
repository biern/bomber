# -*- coding: utf-8 -*-
import logging
from utils import list_remove

class Board(object):
    """ Representation of the current game state.
    Consists of all ingame objects, rules, 
    messages for players, etc """
    #TODO: Messages (score, bonus, standard, ping etc)
    rules = []
    #background tiles are not subject to callbacks, also they are drawn first
    background_tiles = []
    __tiles = {}
    # list of keys
    sorted_priorities_list = [] # sorted key list for optimization
    #size of the board
    width = 10
    height = 10
    log = logging.getLogger('board')
    def __init__(self, size):
        self.width, self.height = size
    
    def get_size(self):
        return (self.width, self.height)
    
    #-Tile functions--------------------------------------------------------------- 
    
    def get_tiles(self):
        result = []
        for priority in self.sorted_priorities_list:
            try:
                result.extend(self.__tiles[priority])
            except KeyError:
                self.log.warning("Requested tileset of priority %i does not exist"
                                 % priority )
        return result
    
    def get_tiles_of_type(self, cls):
        for tile in self.get_tiles():
            if isinstance(tile, cls):
                yield tile
    
    def get_background_tiles(self):
        """ Background tiles do not recieve callbacks """
        return self.background_tiles
    
    def add_tile(self, tile):
        """ """
        if not tile.background:
            try:
                self.__tiles[tile.drawing_priority].append(tile)
            except KeyError:
                self.__add_priority_key(tile.drawing_priority)
                self.__tiles[tile.drawing_priority].append(tile)
        else:
            self.background_tiles.append(tile)
    
    def __add_priority_key(self, priority):
        """ Note that this also removes all objects with given priority """
        self.sorted_priorities_list.append(priority)
        self.sorted_priorities_list = sorted(self.sorted_priorities_list)
        self.__tiles[priority] = []

    
    def remove_tile(self, tile):
        """ Returns True if tile was removed, False if it wasn't found """
        if not tile.background:
            return any(list_remove(self.__tiles[p], tile) for p in self.sorted_priorities_list)
        else:
            return list_remove(self.get_background_tiles(), tile)
    
    #------------------------------------------------------------------------------ 
    
    def set_rules(self, rules):
        self.rules = rules
        
    def add_rule(self, rule):
        self.rules.append(rule)
    
    def remove_rule(self, rule):
        """ Returns True if rule was removed, False if it wasn't found """
        return list_remove(self.rules, rule)