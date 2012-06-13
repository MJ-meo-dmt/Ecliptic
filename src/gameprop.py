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
from math import *
from direct.showbase.DirectObject import DirectObject


# Game imports
from globals import *


#----------------------------------------------------------------------#

# This will handle all object setups from the egg file.


# Base object class
class baseObject(DirectObject):
    
    """
    baseObject Class:
    
    Base class for game objects.
    """
    
    def __init__(self):
    
	self.objectName = ""
	self.objectTriggers = ""
	self.objectArea = 0
	self.objectPicker = ""
	self.objectNeeds = ""
	self.objectStatus = ""
	self.objectSoundON = ""
	self.objectSoundOFF = ""
	self.objectStyle = ""
	self.objectPhysics = ""
	self.objectMass = 0.0
	self.objectParent = ""
    
	##  LIGHTS
	self.lightType = ""
	self.lightRed = 0.0
	self.lightGreen = 0.0
	self.lightBlue = 0.0
	self.lightPower = 0.0
    
	self.objectPosition = Point3(0, 0, 0)
	self.objectHpr = VBase3(0, 0, 0)
	self.objectScale = VBase3(0, 0, 0)
    



class GameObject(baseObject):
    
    
    def __init__(self, _base, _physics, _world, _model, object):
	
        
        # __init__ the base class
        baseObject.__init__(self)
        
        # Base 
        self._base = _base
        
        # Base Physics
        self._physics = _physics
        
        # Base World
        self._world = _world
        
        # Get the object
        self.object = object
	
	################################################
        ###### Get the <TAG's> from the egg file #######
	################################################
	
	# Get the correct Name for the object
	self.tagList = ['ROOM', 'SENSOR', 'DOOR', 'PLAYER', 'TRIGGER', 'LIGHT',
		'ITEM', 'SCREEN', 'PARTICLES', 'SUIT', 'DECOR']

	name = ''
	self.objectType = None
	for i in self.tagList:
	    if self.object.hasTag(i):
		self.objectType = i
		name = self.object.getTag(i)
		
	    
        
        # Get object name
        self.objectName = name
	print 'Object name: ',self.objectName, ' have been made.'
	
        # Get object triggers
        self.objectTriggers = self.object.getTag('TRIGGERS')
	
	# Get object Area
	self.objectArea = self.object.getTag('AREA')
	
	# is object Pickable
	self.objectPicker = self.object.getTag('PICKER')
	
	# Get object Needs
	self.objectNeeds = self.object.getTag('NEEDS')
	
	# Get object Status
	self.objectStatus = self.object.getTag('STATUS')
	
	# Get object SoundON
	self.objectSoundON = self.object.getTag('SOUNDON')
	
	# Get object SoundOFF
	self.objectSoundOFF = self.object.getTag('SOUNDOFF')
	
	# Get object Style
	self.objectStyle = self.object.getTag('STYLE')
	
	# Get object Physics
	self.objectPhysics = self.object.getTag('PHYSICS')
	
	# Get object Mass
	self.objectMass = self.object.getTag('MASS')
	
	# Get object Parent
	self.objectParent = self.object.getTag('PARENT')
	
	### GET OBJECT LOC, ROT, SCALE ###
	self.objectPosition = self.object.getPos(_model)
	self.objectHpr = self.object.getHpr(_model)
	self.objectScale = self.object.getScale(_model)
	
	################################################
	
	
	### LIGHT SPECIFICS ###
	if self.objectType == 'LIGHT':
	    
	    ### LIGHTS SETTINGS ###
	    # Type, Red, green, blue, power
	    self.lightType = self.object.getTag('TYPE')
	    self.lightRed = self.object.getTag('RED')
	    self.lightGreen = self.object.getTag('GREEN')
	    self.lightBlue = self.object.getTag('BLUE')
	    self.lightPower = self.object.getTag('POWER')
	    self.setLights()
	
	
	###### INNER OBJECT SETUPS ######
	# Setup object physics
	if self.object.hasTag('PHYSICS'):
	    self.setObjectPhysics()
	
	# Setup object RenderNode
	self.setRenderNode()
	
    ### Set the object's render node ###
    def setRenderNode(self):
	
	# Reparent Reference dict
	setRenderNP = {}
	###
	setRenderNP['ROOM'] = self._world.roomNP
	setRenderNP['SENSOR'] = self._world.sensorNP
	setRenderNP['DOOR'] = self._world.doorNP
	setRenderNP['PLAYER'] = self._world.playerNP
	setRenderNP['TRIGGER'] = self._world.triggerNP
	setRenderNP['LIGHT'] = self._world.lightNP
	setRenderNP['ITEM'] = self._world.itemNP
	setRenderNP['SCREEN'] = self._world.screenNP
	setRenderNP['PARTICLES'] = self._world.particleNP
	setRenderNP['SUIT'] = self._world.suitNP
	setRenderNP['DECOR'] = self._world.decorNP
	###
	
	# Get the correct NP
	for tag in self.tagList:
	    
	    if self.object.hasTag(tag):
		
		return self.object.reparentTo(setRenderNP[tag])
	
	
    ### Setup the object's physics body ###
    def setObjectPhysics(self):
	"""
	Method for setting up the object's physics.
	Counts for SENSOR's aswell.
	"""
	
	Physics = self.objectPhysics
	Mass = 0.0#self.objectMass
	
	# Get the geom node
	objectNode = self.object.node()
	objectGeom = objectNode.getGeom(0)
	    
	# Setup the bullet mesh
	objectMesh = BulletTriangleMesh()
	objectMesh.addGeom(objectGeom)
	
	# Setup a static object
	if Physics == 'STATIC':
	    
	    body = BulletRigidBodyNode('Bullet '+self.objectName)
	    self.bodyNP = self._world.staticNP.attachNewNode(body)
	    shape = BulletTriangleMeshShape(objectMesh, dynamic=False)
	    self.bodyNP.node().setKinematic(True)
	    self.bodyNP.node().addShape(shape)
	    self.bodyNP.node().setMass(Mass)
	    self.bodyNP.setCollideMask(BitMask32.allOn())
	    
	    # Attach the static object to the _physics world
	    return self._physics.world.attachRigidBody(body)
	
	# Setup a Dynamic object
	if Physics == 'DYNAMIC':
	    
	    body = BulletRigidBodyNode('Bullet '+self.objectName)
	    self.bodyNP = self._world.dynamicNP.attachNewNode(body)
	    shape = BulletTriangleMeshShape(objectMesh, dynamic=True)
	    self.bodyNP.node().addShape(shape)
	    self.bodyNP.node().setMass(Mass)
	    self.bodyNP.setCollideMask(BitMask32.allOn())
	    
	    # Attach the dynamic object to the _physics world
	    return self._physics.world.attachRigidBody(body)
	
	# Setup a Ghost object
	if Physics == 'GHOST':
	    
	    ghost = BulletGhostNode('Ghost_sensor '+self.objectName)
	    shape = BulletTriangleMeshShape(objectMesh, dynamic=False)
	    ghost.addShape(shape)
	    self.ghostNP = self._world.sensorNP.attachNewNode(ghost)
	    self.ghostNP.setPos(self.objectPosition)
	    self.ghostNP.setCollideMask(BitMask32(0x0f))
	    
	    # Attach the ghost object to the _physics world
	    return self._physics.world.attachGhost(ghost)
	
    
    ### Setup lights ###
    def setLights(self):
	
	if self.lightType == 'POINT':
	    
	    # Testing light: Remove if done
	    ############################################
	    # Setup lights for the level
	    plight = PointLight('plight')
	    plight.setColor(VBase4(0.7, 0.7, 0.7, 1))
	    plnp = render.attachNewNode(plight)
	    plnp.setPos(0, 0, 8)
	    render.setLight(plnp)
	    ############################################
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

