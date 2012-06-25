# Event component:
# Add to the GameObject Class depending on type.
from direct.showbase.DirectObject import DirectObject
from globals import *

class SensorEvent(DirectObject):
    
    def __init__(self, object):
        self.object = object
        
        #self.accept("Sen", self.openDoor)
        
    def openDoor(self):
        print OBJECTS['Door'][self.target].name
    
class DoorEvent():
    
    def __init__(self, object):
        self.object = object
    
class PlayerEvent():
    
    def __init__(self, object):
        self.object = object

class TriggerEvent():
    
    def __init__(self, object):
        self.object = object
        
class LightEvent():
    
    def __init__(self, object):
        self.object = object
    
class ItemEvent():
    
    def __init__(self, object):
        self.object = object 
    
class ScreenEvent():
    
    def __init__(self, object):
        self.object = object 
    
class ParticleEvent():
    
    def __init__(self, object):
        self.object = object 
    
class SuitEvent():
    
    def __init__(self, object):
        self.object = object 

