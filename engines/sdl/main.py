# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from ConfigParser import ConfigParser
from copy import copy
import os
import logging

from lib.globals import MOD_DIR
from lib.engine import Engine
from lib.utils import config_to_dict, parse_dict
from sprite import Sprite

#TODO: Use image for background instead of tile objects - it costs loads of cpu work

class SDLEngine(Engine):
    log = logging.getLogger("SDLEngine")
    
    #===============================================================================
    #    Input Handling Part
    #===============================================================================        
            
    def get_input(self):
        res = {}
        pygame.event.pump()
#        mods = pygame.key.get_mods()
        up = pygame.event.get(KEYUP)
        down = pygame.event.get(KEYDOWN)
        res['keyup'] = [pygame.key.name(e.key) for e in up]
        res['keydown'] = [pygame.key.name(e.key) for e in down]
        # get rid of unwanted events
        # if it isn't called, event queue will be blocked
        pygame.event.get()
        return res

    #===============================================================================
    #    Renderer Part
    #===============================================================================

    #-Default config values and their parsers--------------------------------------
    size_parser = lambda s: [int(i) for i in s.split('x')]
    config_defaults = {
                       'resolution':'0x0', # 0x0 for auto
                       'fullscreen':'0',
                       'tile-size':'32',
                       'board-size':'10x10',
                    }
    config_parser = {
                     'resolution':size_parser,
                     'fullscreen': lambda s: int(s),
                     'tile-size': lambda s: int(s),
#                     'board-size': size_parser,
                     }
    
    anim_defaults = {
                'frames':'1',
                'size':config_defaults['tile-size']+'x'+config_defaults['tile-size'], 
                'sequence':'1', #TODO: should default to 1 ... n , n=frames_number
                'repeat':'1',
                }
    anim_parser = {
                   'frames': lambda s: int(s),
                   'size': size_parser,
                   'sequence': lambda s: [int(i) for i in s.split()],
                   'repeat': lambda s: int(s),
                   }
    #------------------------------------------------------------------------------ 
    format = 'anim'
    store_sprite_in = "sdl_sprite"
    name = 'sdl'
    media = {}
    directions = {
                  'l':'left',
                  'r':'right',
                  'u':'up',
                  'd':'down'
                  }
    #------------------------------------------------------------------------------
    clock = pygame.time.Clock() 
    def __init__(self):
        super(SDLEngine, self).__init__()
        self.load_config()
    
    #-Callbacks-------------------------------------------------------------------- 
    
    def onModLoaded(self, mod):
        """ Inits pygame display and loads all data """
        self.load_config(mod)
        self.init_display(mod)
        self.load_data(mod)
        self.mod = mod
    
    #-Initialization--------------------------------------------------------------- 
    
    def load_config(self, mod=None):
        """ Loads config :-) May be called without mod argument to set up
         initial settings"""
        pre_config = copy(self.config_defaults)
        #if mod is defined update pre_config with mod specific settings
        if mod:
            mod_specific_config = ConfigParser()
            if not mod_specific_config.read(os.path.join(self.data_path(mod), 'settings.ini')):
                self.log.warning("Config file '%s' not found, using default settings"
                                 % os.path.join(self.data_path(mod), 'settings.ini')) 
            mod_specific_config = config_to_dict(mod_specific_config) 
            pre_config.update(mod_specific_config.get('main',{}))

        # Parsing config
        pre_config = parse_dict(pre_config, self.config_parser, self.log)
        
        # Other mod options (already parsed by mod)
        if mod:
            mod_config = mod.get_config()
            try:
                pre_config['board-size'] = mod_config['board']['size']
            except KeyError:
                self.log.critical("Attribute 'size' in section 'board' of mod config"
                                  "not found, using default. Weird things may happen")
        
        self.config = pre_config
        self.log.debug("Configuration loaded")
    
    def init_display(self, mod):
        """ """
        flags = 0
        self.display_size = self.calculate_display_size(mod)
        if self.config.get('fullscreen', 0):
            flags |= FULLSCREEN | HWSURFACE | DOUBLEBUF
            resolution = self.config['resolution']
            # Is resolution set to auto ? 
            if not (resolution[0] or resolution[1] ):
                resolution = self.display_size
            self.screen = pygame.display.set_mode(resolution, flags)
        else:
            self.screen = pygame.display.set_mode(self.display_size, flags)
        pygame.display.set_caption(getattr(mod, 'full_name', 'No mod loaded'))
    
    
    def calculate_display_size(self, mod):
        """ Returns size of the surface that will be used for game. 
        Should be called after engine/mod config is loaded """
        size = [0,0]
        size[0] = self.config['board-size'][0] * self.config['tile-size']
        size[1] = self.config['board-size'][1] * self.config['tile-size']
        return size
        
    #-Data handling---------------------------------------------------------------- 
    def data_path(self, mod):
        return os.path.join(MOD_DIR(mod), self.name)
    
    def load_data(self, mod):
        """ Loads all animations for mod """
        # Get list of all files to load
        # Currently loads all *.png files in data folder,
        self.log.debug("Loading data...")
        data_dir = self.data_path(mod)
        files = []
        try:
            files = [file for file in os.listdir(data_dir) if file.endswith(self.format)]
        except OSError:
            self.log.error("Data directory (%s) for mod not found!"
                           % data_dir)
        for filename in files:
            object_name = filename.rsplit('.')[0]
            self.log.debug("Loading data for '%s'..." % object_name)
            self.media[object_name] = {}
            #setting up parser for .anim file
            config = self.load_anim_config(os.path.join(data_dir, filename))
            #storing images and config for each action
            for action in config.keys():
                #TODO: New image loading function (loading images from one file)
                self.media[object_name][action] = self.get_images_for_action(object_name, action, data_dir)
                self.media[object_name][action]['config'] = config[action]
                
        self.log.debug("Loading data finished")
    
    def load_anim_config(self, path_to_file):
        """ Returns a readymade, parsed config dict loaded from path_to_file """
        self.log.debug("\tLoading configuration...")
        #TODO: Generating sprite classes on the fly from config ?
        #Loading config from file
        configParser = ConfigParser()
        configParser.read(path_to_file)
        #Making it a dictionary
        dicted = config_to_dict(configParser)
        # Setting up result config dict
        config = {}
        for action, options in dicted.items():
            # each action's options are made a copy of default ones 
            config[action] = copy(self.anim_defaults)
            # then we update it with values from loaded config file
            config[action].update(options)
            # parsing options
            config[action] = parse_dict(config[action], self.anim_parser, self.log)

        return config

    
    def get_images_for_action(self, name, action, data_dir):
        """ Returns dict of images, ready to store 
        format: result[direction][frame] -> img"""
        self.log.debug("\tLoading action '%s'..." % action)
        prefix = name + '_' + action
        
        #Setting up result dict
        result = {}
        for k, v in self.directions.items():
            result[v] = {}
        
        files = sorted([f for f in os.listdir(data_dir) if f.startswith(prefix)])
            
        #TODO:checking for shortened file names
        #action = 'none', direction = 'down'
        #if action == 'none':
        #load_files = [f for f in files if f.rsplit('.')[0].rsplit('_')[0] == name]
        
        for file in files:
            try:
                #the rest of the string should include: _direction_part
                tmp = file[len(prefix):].rsplit('.')[0] # part between prefix and extension
                el = tmp[1:].split('_')
                # checking if filename is correct
                if len(el) != 2: 
                    self.log.warning('File %s not loaded, reason: Wrong filename (Wrong underscores number)!' % file)
                    continue
                direction = el[0]
                if direction not in self.directions.keys():
                    self.log.warning('File %s not loaded, reason: Wrong filename ("%s" is not a valid direction)!' 
                                     % (file, direction))
                    continue
                frame = 1
                try:
                    frame = int(el[1])
                except ValueError:
                    self.log.warning('File %s not loaded, reason: Wrong filename (frame number should be int, but got "%s!")' 
                                     % (file, el[1]))
                    continue
                #finally, saving result image
                result[self.directions[direction]][frame] = pygame.image.load(os.path.join(data_dir, file)).convert_alpha()
#                print "%i%s, " % (frame, direction),
            except Exception, msg:
                self.log.warning("File %s not loaded, reason: %s" % (file, msg))
#        print ""
        return result
    
    #-Drawing----------------------------------------------------------------------
     
    def draw(self, board):
        """ Draws current boards state on screen """
        self.screen.fill((0,0,0))
        #TODO: Optimized sprite class for background tiles ?
        for tile in board.get_background_tiles():
            self.draw_tile(tile)

        for tile in board.get_tiles():
            self.draw_tile(tile)
            
        pygame.display.flip()
    
    def draw_tile(self, tile):
        img = self.get_sprite(tile).draw()
        ts = self.config['tile-size']
        #TODO: Offsets
        pos = ((tile.x+0.5)*ts-img.get_width()/2, (tile.y+0.5)*ts-img.get_height()/2)
        self.screen.blit(img, pos)
    
    def get_sprite(self, target):
        """ Gets sprite from object or generates one if not available """
        sprite = getattr(target, self.store_sprite_in, False)
        if not sprite: sprite = self.generate_sprite(target)
        return sprite
    
    
    def generate_sprite(self, target):
        """ Generates sprite for object, and sets it as object's attribute """
        data = self.media.get(target.name)
        sprite = Sprite(data, target)
        setattr(target, self.store_sprite_in, sprite)
        return sprite
    
    #-Other------------------------------------------------------------------------ 
    
    def control_fps(self, fps):
        self.clock.tick(fps)


engine = SDLEngine

""" Format of .anim files:
#TODO: Set of images for each action should live in a single png file, not in n files
[action_name]
frames: n ; obligatory field, n >= 1
sequence: 1 1 2 3 1 1 2 ; defaults to 1..n (not yet)
filename: file.png ; defaults to <object_name>_<action_name>_<direction(first letter)>.png 

example:
<bomberman.anim>

[moving]
frames: 5
sequence: 1 1 2 2 3 3 2 2 1 1 4 4 5 5 4 4
"""