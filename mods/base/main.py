# -*- coding: utf-8 -*-
from copy import copy
import logging

from lib.mod import Mod
from lib.board import Board
from lib.utils import parse_dict

from player import Player

class BaseMod(Mod):
    name = "base"
    full_name = "Base Mod"
    player_config_default = {
                             'name':'unnamed player',
    }
    default_controls = {
                        }
    log = logging.getLogger("BaseMod")
    #------------------------------------------------------------------------------
    players = [] 
    player_config_parser = {}
    def __init__(self):
        super(BaseMod, self).__init__()
        self.quit = False
    
    def onNewGame(self, *args, **kwargs):
        self.log.debug("Starting new game...")
        #loading map goes here
        players_n = 1
        self.board = Board(self.config['board']['size'])
        #End of loading map
        self.create_players(players_n)
    
    def create_players(self, n):
        """ Creates n players and saves them """
        self.log.debug("Creating players...")
        self.players_config = self.parse_players_conifg(n)
        self.players_controls = self.parse_players_controls(n)
        for i in range(n):
            p = Player(self.players_config[i]['name'])
            p.config = self.players_config[i]
            p.controls = self.players_controls[i]
            self.players.append(p)
            
            
    def parse_players_conifg(self, n):
        #Load config should be called before this
        result = []
        for i in range(1,n+1):
            key = 'player%i' % i
            player_config = {}
            player_config = copy(self.player_config_default)
            player_config.update(self.config.get(key, {}))
            player_config = parse_dict(player_config, self.player_config_parser)
            result.append(player_config)
        
        return result
    
    def parse_players_controls(self, n):
        result = []
        for i in range(1, n+1):
            key = 'player%i-controls' % i
            controls = copy(self.default_controls)
            controls.update(self.config.get(key, {}))
            #reversing dict - key is now a real key and value is action
            controls = dict([ (v,k) for k, v in controls.items()])
            result.append(controls)
        
        return result
    
    def key_down(self, key, released=False):
        """ Checks some mod controls, then sends action 
        to players according to their controls"""
        if not released:
            if key == 'escape':
                self.quit = True
            
        for p in self.players:
            act = p.controls.get(key, False)
            if act: 
                p.action_requested(act, released)
                return
    
    def key_up(self, key):
        self.key_down(key, True)
    
    def handle_input(self, input):
        for key in input.get('keydown', []):
            self.key_down(key)
        for key in input.get('keyup', []):
            self.key_up(key)
    
    def update(self):
        return self.quit
    
mod = BaseMod