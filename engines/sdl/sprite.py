# -*- coding: utf-8 -*-
import pygame


class Sprite(object):
    """ Simple object holding info vital for displaying the object properly.
    Each object, while being rendered, recieves a copy of this class if it
    doesnt posess one already. All rendering data is then gathered from from this
    class """
    notFound = False
    #TODO: Some nicer image for frames 'not found' 
    notFoundImage = pygame.Surface((20,20))
    notFoundImage.fill((255,0,0))
    def __init__(self, data, target):
        """ Target is object to represent """
        self.data = data
        if not data:
            self.notFound = True
            return
        
        self.target = target
        self.frame = 0
        self.last_action = ""
        self.last_direction = ""
        # separate variables for each sequence and its length for optimization
        # their size is constant so there's no problem :-)
        self.sequences = {}
        self.sequences_len = {}
        self.repeat = {}
        for action in data.keys():
            self.sequences[action] = data[action]['config']['sequence']
            self.sequences_len[action] = len(self.sequences[action])
            self.repeat[action] = data[action]['config']['repeat']
        
        
    def step(self, action, direction):
        """ Increases frame counter and handles animation changes """
        if self.last_action != action or self.last_direction != direction:
            self.frame = 0
            return
        else:
            self.frame += 1
            if self.frame >= self.sequences_len[action]:
                if self.repeat[action]:
                    self.frame = 0
                else:
                    self.frame -= 1
            return
    
    def draw(self):
        """ Makes the animation move beautifuly ! :-D 
        Returns surface with a current image of the object"""
        if self.notFound:
            return self.notFoundImage
        
        target = self.target          
        self.step(target.action, target.direction)
        self.last_action = target.action
        self.last_direction = target.direction
        
        try:
            return self.data[target.action][target.direction][self.sequences[target.action][self.frame]]
        except KeyError:
            return self.notFoundImage

