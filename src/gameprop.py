###  GAME PROPS - OBJECTS  ###

#

from pandac.PandaModules import *
from panda3d.core import *









#----------------------------------------------------------------------#

## This will move i guess

#sensorNP = render.attachNewNode("SENSORS")
# Will have to make one for each and parent it under render or world or something.


# Base object class
class GameObject():
    
    """
    GameObject Class:
    
    Base class for game objects.
    """
    
    def __init__(self):
	
	self.objectName = ""
	self.objectType = ""
	self.objectTriggers = ""
	self.objectArea = ""
	self.objectPickable = ""
	self.objectNeeds = ""
	self.objectStatus = False
	self.objectSoundON = ""
	self.objectSoundOFF = ""
	self.objectStyle = ""
	self.objectPhysics = 0.0
	self.objectParent = ""
	
	self.objectPosition = Point3(0, 0, 0)
	self.objectHpr = VBase3(0, 0, 0)


class SENSOR(GameObject):
    
    """
    SENOR Class:
    
    Object class for SENSORS, constructed from the tag system /
    Then parented to the master NodePath for sensors.
    """
    
    def __init__(self, _world, _model, object):
	
	# Init the base class
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('SENSOR')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set the object Area
	self.objectArea = self.object.getTag('AREA')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	
	# Here we add something like, if the object is setup,
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.sensorNP)
	
	
	
class DOOR(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base world
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('DOOR')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.doorNP)
	
	
class PLAYER(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base world
	self._world = _world
	
	# Set the object
	self.object = object	
	
	# Add a object name
	self.objectName = self.object.getTag('PLAYER')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.playerNP)
	
	

class TRIGGER(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('TRIGGER')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.triggerNP)
	
	

class LIGHT(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('LIGHT')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	## LIGHT SPECIFICS ##
	
	# Floats 0.0 - 1.0
	self.lightRed = self.object.getTag('LIGHT_RED')
	self.lightGreen = self.object.getTag('LIGHT_GREEN')
	self.lightBlue = self.object.getTag('LIGHT_BLUE')
	
	# Maybe add flag here to check if vis or invis.
	# Parent it to the master NodePath for it
	self.object.reparentTo(self._world.visLightsNP)



class ITEM(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('ITEM')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.itemNP)
	
	

class SCREEN(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('SCREEN')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.screenNP)
	
	

class PARTICLES(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('PARTICLES')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.particlesNP)
	
	

class SUIT(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('SUIT')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.suitNP)
	
	

class DECOR(GameObject):
    
    def __init__(self, _world, _model, object):
	GameObject.__init__(self)
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('DECOR')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Triggers
	self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Set if pickable: bool
	self.objectPickable = self.object.getTag('PICKABLE')
	
	# Set the object needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Set the object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Set the ON sound for the object
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Set the OFF sound for the object
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.decorNP)
	
	

