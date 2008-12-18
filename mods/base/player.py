from lib.utils import list_remove

class Player(object):
    owns = []
    states = [] # list of strings, similar to rules
    
    # These are assigned by mod instance and shouldn't
    # be used from player class (they might dissappear someday :):
    controls = {} # Maps key to action
    config = {} # Config dict
    # 
    def __init__(self, name):
        self.name = name
        
    def action_requested(self, action, released=False):
        """ This should handle every action that player can do """
        print "Requested action %s" % action,
        if released:
            print "R",
        print ""
        pass
    
    def add_object(self, o):
        self.owns.append(o)
        
    def remove_object(self, o):
        return list_remove(self.owns, o)
    
    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)
            
    def remove_state(self, state):
        return list_remove(self.states, state)
    
    def set_states(self, states):
        self.states = states