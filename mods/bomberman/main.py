# -*- coding: utf-8 -*-
import logging

from mods.base.main import BaseMod

class BombermanMod(BaseMod):
    name = "bomberman"
    full_name = "Bombastick Bomberman"
    log = logging.getLogger("BombermanMod")
    
mod = BombermanMod