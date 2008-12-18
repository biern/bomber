# -*- coding: utf-8 -*-
import logging
from copy import copy
from ConfigParser import ConfigParser

def list_remove(list, value):
    """ Returns True if object was removed, False if it wasn't found """ 
    try:
        list.remove(value)
        return True
    except ValueError:
        return False

def config_to_dict(configParser):
    res = {}
    for section in configParser.sections():
        tmp = {}
        for var, val in configParser.items(section):
            tmp[var] = val
        res[section] = tmp
        
    return res

def parse_dict(options, parsers, log=None):
    """ Parses options in dict "options" according
    to parser functions in dict "parsers", returns
    parsed dict """
    options = copy(options)
    if not log: 
        log = logging.getLogger("options-parser")
        
    for key, value in options.items():
        #If parser does not exist for the key, continue
        if not parsers.get(key, False): continue
        try:
            options[key] = parsers[key](value)
        except Exception, msg:
            log.warning("Error while parsing option %s, value %s, message: %s"
                        % (key, value, msg))
    return options

def load_config(paths, default_values, parsers):
    if type(paths) == str:
        paths = [paths]
    log = logging.getLogger('config_loader')
    config = copy(default_values)
    configParser = ConfigParser()
    if not configParser.read(*paths):
        log.warning("None of the config files was loaded (paths:\n %s)"
                    % paths )
    loaded = config_to_dict(configParser)
    config.update(loaded)
    for section, options in config.items():
        for key, value in options.items():
            try:
                config[section][key] = parsers.get(key, lambda s: s)(value)
            except Exception, msg:
                log.error("Error while parsing option %s from section %section, message: %s"
                          % (key, section, msg) )
                
    return config