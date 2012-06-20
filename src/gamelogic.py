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
    
    def __init__(self, base):
        
        self.base =base
        
        taskMgr.add(self.checkSensor, 'checkSensor')
        
        
    def checkSensor(self, task):
        
        # Get the sensor
        for sensor in OBJECTS['SENSOR']:
            
            obj = OBJECTS['SENSOR'][sensor].bodyNP
            print obj
            return obj
        
 
        return task.cont
 
        
        
        
































