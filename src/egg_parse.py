## This file will parse egg files for TAG's.

# System imports


# Panda imports
from panda3d.core import *
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject

# Game imports
from globals import *
from gameprop import *


#----------------------------------------------------------------------#

# Main egg parser.

class Parse():
    
    def __init__(self, _base, _world, _model):
	# Base class
	self._base = _base
	
	# Base world
	self._world = _world
	
	# Keep track of num_of_objects
	num_sensors = 0
	num_doors = 0
	num_triggers = 0
	num_lights = 0
	num_items = 0
	num_particles = 0
	
	# Get the model to be parsed:
	self.model = _model
	
	# Find all the objects inside the egg file, and save them.
	self.objects = self.model.findAllMatches('**')
	
	
	# Now check all objects and then init the class for that tag:
	for object in self.objects:
	    
	    if object.hasTag('SENSOR'):
		OBJECTS[object.getTag('SENSOR')] = SENSOR(self._world, self.model, object)
		num_sensors += 1
		
	    if object.hasTag('DOOR'):
		OBJECTS[object.getTag('DOOR')] = DOOR(self._world, self.model, object)
		num_doors += 1
		
	    if object.hasTag('PLAYER'):
		OBJECTS[object.getTag('PLAYER')] = PLAYER(self._world, self.model, object)
		
	    if object.hasTag('TRIGGER'):
		OBJECTS[object.getTag('TRIGGER')] = TRIGGER(self._world, self.model, object)
		num_triggers += 1
		
	    if object.hasTag('LIGHT'):
		OBJECTS[object.getTag('LIGHT')] = LIGHT(self._world, self.model, object)
		num_lights += 1
		
	    if object.hasTag('ITEM'):
		OBJECTS[object.getTag('ITEM')] = ITEM(self._world, self.model, object)
		num_items += 1
		
	    if object.hasTag('SCREEN'):
		OBJECTS[object.getTag('SCREEN')] = SCREEN(self._world, self.model, object)
		
	    if object.hasTag('PARTICLES'):
		OBJECTS[object.getTag('PARTICLES')] = PARTICLES(self._world, self.model, object)
		num_particles += 1
		
	    if object.hasTag('SUIT'):
		OBJECTS[object.getTag('SUIT')] = SUIT(self._world, self.model, object)
		
	    if object.hasTag('DECOR'):
		OBJECTS[object.getTag('DECOR')] = DECOR(self._world, self.model, object)
		
		
		
	

