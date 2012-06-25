## This file will parse egg files for TAG's.

# System imports


# Panda imports
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

# Game imports
from globals import *
from gameprop import *
from eventcomponent import *


#----------------------------------------------------------------------#

# Main egg parser.
# For all visual objects
class ParseMain(NodePath):
        
    """
    Parse Class:
    
    Handles the parsing of egg files.
    Sorts each object/Node found into a specific object/Type
    
    Constructor:
    @param _model: The egg file to be parsed, send from world.py under MakeLevel.
    """
    
    def __init__(self, _model):
        NodePath.__init__(self, 'object')
                
        # Keep track of num_of_objects
        num_sensors = 0
        num_doors = 0
        num_triggers = 0
        num_lights = 0
        num_items = 0
        num_particles = 0
        
        # Get the model to be parsed:
        self._model = _model
        
        # Find all the objects inside the egg file, and save them.
        self.objects = self._model.findAllMatches('**')
        
        # Now check all objects and then init the class for that tag:
        for object in self.objects:
            for _type in OBJECTS_TYPES :
                if object.hasTag(_type):
                    OBJECTS[_type][object.getTag(_type)] = GameObject(self._model, object)
                    
                    
