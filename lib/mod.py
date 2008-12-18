# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import logging
import os
from copy import copy

from utils import config_to_dict, parse_dict
from board import Board

class Mod(object):
    """ Base class for all mods. Defines necessary interface and provieds
    some basic functions"""
    # name is overwritten by the directory name of a mod,
    # while loading mod, since it is used to get mod path
    name = 'not_set'
    #full name can contain any characters
    full_name = 'Default mod v 0.000'
    default_config = {
                      'board': {'size':'10x10'}
                      }
    config_parser = {
                     'board': {
                               'size': lambda s: [int(i) for i in s.split('x')],
                               },
                     }
    config_filename = 'settings.ini'
    log = logging.getLogger('mod')
    board = Board((10,10))
    def __init__(self):
        """ Loads some data """
        # Loading mod config file
        self.quit = False
        self.load_config()
    
    #-Callbacks-------------------------------------------------------------------- 
    def onNewGame(self, *args, **kwargs):
        """ Parsing args, loading maps etc """
        pass
    
    #--Necessary Interface--------------------------------------------------------- 
    def dir(self):
        return "mods/%s" % self.name
        
    def get_board(self):
        """ Returns board object """
        return self.board
    
    def handle_input(self, input):
        """ Result of InputEngine.get_input() goes here. 
        Generates necessary events """
        #Printing keys
        for key, item in input.items():
            if 'escape' in item:
                self.quit = True
            if not item: continue
            print key, ':',
            for key_name in item:
                print key_name,',',
            print ""

    
    def update(self):
        """ Perform collision detection, handle events, check rules, etc,
         return True to quit the game """
        return self.quit
    
    def get_config(self):
        """ Returns parsed 'settings.ini' """
        return self.config
    
    #-Helper functions------------------------------------------------------------- 
    
    def load_config(self):
        path = os.path.join(self.dir(), self.config_filename)
        configParser = ConfigParser()
        configParser.read(path)
        if not os.path.exists(path):
            self.log.warning("Warning, mod config file not found (%s), using default settings" % path)
        # Parsing all data strings
        self.config = copy(self.default_config)
        self.config.update(config_to_dict(configParser))
        for section in self.config.keys():
            self.config[section] = parse_dict(self.config[section],
                                              self.config_parser.get(section, {}),
                                              self.log)
        
        self.log.debug("Configuration loaded")

    def check_collisions(self):
        """ Checks collisions between all tiles on board,
        calls callbacks for collisions"""
        pass