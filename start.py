# -*- coding: utf-8 -*-
import lib.logger # should be called first to set up logging configuration
import profile
from lib.game import Game

g = Game()
g.set_engine('sdl')
g.set_mod('test')
g.start()