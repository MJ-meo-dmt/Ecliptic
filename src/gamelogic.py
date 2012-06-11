###  GAME LOGIC  ###

# System imports


# Panda imports
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.bullet import *



# Game imports
from globals import *

#----------------------------------------------------------------------#


class SensorEvent():
	
	def __init__(self, _base, _world, _physics):
		
		# Base Class
		self._base = _base
		
		# Base World
		self._world = _world
		
		# Base Physics
		self._physics = _physics
		
		#taskMgr.add(self.checkSensor, 'checkSensor')
		
		
	def checkSensor(self, task):
		
		sensor = OBJECTS['SENSOR']['Sensor01'].ghostNP.node()
		
		for node in sensor.getOverlappingNodes():
			print node

		if sensor.getOverlappingNode(0) == node:
			print "BAAAAAA"
		
 
		return task.cont
 
		
		
		
































