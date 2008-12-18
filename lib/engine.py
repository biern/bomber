# -*- coding: utf-8 -*-
""" Template class from which other engines should (only should) inherit """

class Engine(object):
    """ Abstract class """
    name = "none"
    def __init__(self):
        """ Load some settings (if any) """
        pass
    
    def onModLoaded(self, mod):
        """ This is the best place to load all mod data (ie. sprites)
        and get rid of the previous one if any, also get types of input
        events requested by the mod """
        pass
    
    def draw(self, board):
        """ Making the game actually appear on the screen """
        pass
        
    def get_input(self):
        """Returns dict of captured events
        example:
            {'pressed':['a','b','left_control'], 'released:'['x','c']', 'mouse':[32,80]}
         """
        return {}
    
    def onQuit(self):
        """ Perform some cleanup here if necessary """
        pass
    
    def control_fps(self, fps):
        """ Should sleep/wait just enough to make the game run with given fps """
        pass
