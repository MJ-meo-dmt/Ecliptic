###  GAME PROPS - OBJECTS  ###
"""
GAME PROPS:

Handles the creation of the objects parsed from the egg_file.

Basically each object class here will set the object up in panda,
as it were in blender, with all it's properties.
"""

# System imports


# Panda imports
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.bullet import *
from panda3d.core import BitMask32


# Game imports
from globals import *


#----------------------------------------------------------------------#

# This will handle all object setups from the egg file.


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
	self.objectBitMask = 0
	self.objectParent = ""
	
	self.objectPosition = Point3(0, 0, 0)
	self.objectHpr = VBase3(0, 0, 0)
	self.objectScale = VBase3(0, 0, 0)


class FLOOR(GameObject):
    
    
    def __init__(self, _physics, _world, _model, object):
	
	# Init the base class
	GameObject.__init__(self)
	
	# Base Physics
	self._physics = _physics
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('FLOOR')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Area
	self.objectArea = self.object.getTag('AREA')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = float(self.object.getTag('PHYSICS'))
	
	# Set the object BitMask
	self.objectBitMask = self.object.getTag('BITMASK')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# ----------------------------------------- #
	# Adding the solid shape to the wall #
	
	solid_collection = BulletHelper.fromCollisionSolids(self.object)
	
	# Search the model for the <collide>
	for solid in solid_collection:
	    
	    solid.node().setMass(self.objectPhysics)
	    solid.setCollideMask(BitMask32.allOn())
	    self._physics.world.attachRigidBody(solid.node()) # attach solid to bullet world
	    solid.reparentTo(self._world.floorNP)
	
	# Attach the visual of the object
	self.object.reparentTo(self._world.floorNP)
	self.object.setPos(self.objectPosition)
	self.object.setHpr(self.objectHpr)
	
	
class WALL(GameObject):
    
    def __init__(self, _physics, _world, _model, object):
	
	# Init the base class
	GameObject.__init__(self)
	
	# Base Physics
	self._physics = _physics
	
	# Base World
	self._world = _world
	
	# Set the object
	self.object = object
	
	# Add a object name
	self.objectName = self.object.getTag('WALL')
	
	# Set the object Type
	self.objectType = self.object.getTag('TYPE')
	
	# Set the object Area
	self.objectArea = self.object.getTag('AREA')
	
	# Set the object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Set the object physics
	self.objectPhysics = float(self.object.getTag('PHYSICS'))
	
	# Set the object BitMask
	self.objectBitMask = self.object.getTag('BITMASK')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# ----------------------------------------- #
	# Adding the solid shape to the wall #
	
	solid_collection = BulletHelper.fromCollisionSolids(self.object)
	
	# Search the model for the <collide>
	for solid in solid_collection:
	    
	    solid.node().setMass(self.objectPhysics)
	    solid.setCollideMask(BitMask32.allOn())
	    self._physics.world.attachRigidBody(solid.node()) # attach solid to bullet world
	    solid.reparentTo(self._world.wallNP)
	
	# Attach the visual of the object
	self.object.reparentTo(self._world.wallNP)
	self.object.setPos(self.objectPosition)
	self.object.setHpr(self.objectHpr)
	

class SENSOR(GameObject):
    
    """
    SENSOR Class:
    
    Object class for SENSOR's, constructed from the tag system /
    Then parented to the master NodePath for sensors.
    """
    
    def __init__(self, _physics, _world, _model, object):
	
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
	self.object.setPos(self.objectPosition)
	self.object.setHpr(self.objectHpr)
	
	
	
class DOOR(GameObject):
    
    def __init__(self, _physics, _world, _model, object):
	GameObject.__init__(self)
	
	# Base Physics
	self._physics = _physics
	
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
	self.objectPhysics = float(self.object.getTag('PHYSICS'))
	
	# Set the object BitMask
	self.objectBitMask = self.object.getTag('BITMASK')
	
	# Set the object parent: In means the object this object belongs too
	self.objectParent = self.object.getTag('PARENT')
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# ----------------------------------------- #
	# Adding the solid shape to the wall #
	
	solid_collection = BulletHelper.fromCollisionSolids(self.object)
	
	# Search the model for the <collide>
	for solid in solid_collection:
	    
	    solid.node().setMass(self.objectPhysics)
	    solid.setCollideMask(BitMask32.allOn())
	    self._physics.world.attachRigidBody(solid.node()) # attach solid to bullet world
	    solid.reparentTo(self._world.doorNP)
	
	# Set the position and rotation
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	
	# Parent it to the master NodePath for it
	
	self.object.reparentTo(self._world.doorNP)
	self.object.setPos(self.objectPosition)
	self.object.setHpr(self.objectHpr)
	
	
	#-------------------------------------------------------------#
	# Object Functions
	
	
	
	
class PLAYER(GameObject):
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
	self.lightPower = self.object.getTag('LIGHT_POWER')
	
	# Maybe add flag here to check if vis or invis.
	# Parent it to the master NodePath for it
	self.object.reparentTo(self._world.visLightsNP)



class ITEM(GameObject):
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
    
    def __init__(self, _physics, _world, _model, object):
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
	
	

