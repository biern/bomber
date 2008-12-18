# -*- coding: utf-8 -*-
import sys
import logging

class Game(object):
    #TODO: Lots of stuff :-)
    finish = False
    mod = None
    engine = None
    FPS = 40
    log = logging.getLogger('root') 
    def __init__(self, debug=False):
        """ Actually does nothing """
        self.debug = debug
    
    def set_engine(self, engine_name):
        if self.engine:
            self.engine.onQuit()
        self.load_engine(engine_name)
    
    def set_mod(self, mod_name):
        mod = self.get_from_package('mods.%s.main' % mod_name, 'mod')
        if not mod:
            self.log.error("Couldn't load mod '%s'! See debug log for more information"
                           % mod_name)
            return False
        
        mod.name = mod_name
        self.mod = mod()
        self.log.debug("Mod '%s' loaded" % mod_name)
        self.engine.onModLoaded(self.mod)
    
    def load_engine(self, engine_name):
        engine = self.get_from_package('engines.%s.main' % engine_name, 'engine')
        if not engine:
            self.log.error("Couldn't load engine '%s', exiting" % input )
            sys.exit()
        
        self.engine = engine()
        self.log.debug("Engine '%s' loaded" % self.engine.name)
            
                
    def get_from_package(self, package_name, object_name):
        """ Returns object named 'object_name' from package if possible, else False """
        try:
            exec "from %s import %s" % (package_name, object_name)
            return eval(object_name)
        except Exception, msg:
            self.log.debug( "Couldn't import %s from package %s, reason: %s" % (object_name, package_name, msg) )
            return False
    
    def start(self):
        self.mod.onNewGame()
        self.main_loop()
        self.engine.onQuit()
    
    def main_loop(self):
        # Don't quit the game because of some exception unless in debug mode
        if not self.debug:
            while not self.finish:
                try:
                    self.mod.handle_input(self.engine.get_input())
                except Exception, msg:
                    self.log.error("Input handling raised exception, message:'%s'" 
                                   % msg)
                try:
                    self.finish = self.mod.update()
                except Exception, msg:
                    self.log.error("Mod update raised exception, message:'%s'" 
                                   % msg)
                try:
                    self.engine.draw(self.mod.get_board())
                except Exception, msg:
                    self.log.error("Engine raised exception while drawing, message:'%s'"
                                   % msg)
                try:
                    self.engine.control_fps(self.FPS)
                except Exception, msg:
                    self.log.error("Engine raised exception on fps_control, message:'%s'"
                                   % msg)
        else:
            while not self.finish:
                self.mod.handle_input(self.engine.get_input())
                self.finish = self.mod.update()
                self.engine.draw(self.mod.get_board())
                self.engine.control_fps(self.FPS)
    