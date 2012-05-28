#!/usr/bin/python

# System imports
import sys, math, os

# Panda imports
from panda3d.core import *
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from panda3d.core import BitMask32
from panda3d.bullet import ZUp
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from direct.showbase.InputStateGlobal import inputState

# Game imports
from devconfig import *
from globals import *


#---------------------------------------------------------------------#

## Main Player Class.
class Player(object):
    """
    Player Class:
        
    This class handels all "Players" in game (Actors)
        
    @method addEntity: Use this to add a created entity to the global entity Dict{}
    """
 
    def __init__(self): 	    
	pass
        # These are players and other entities
	
    def addEntity(self, entityKey, entityObject):
	"""
	@param entityKey: Pref the name of the entity
	@param entityObject: Pref the name of the created entity
	"""
	# Add entity to the global enity dict{}
	ENTITY[entityKey] = entityObject
	

## MakePlayer Class

# Will move this class under physics.py so that we have some order.
class MakePlayer(DirectObject):
        
    """
    MakePlayer Class:
        
    This class handels the creation of Players.
    Players will be stored in the Entity dict.
    """
    def __init__(self, _base, _physics, _world, name):

	"""
	constructor:
                
	@param name: String_name, for the Player - In game.
	@param entityName: String_name for the PC - Player in ENTITY /
	    dict{} for all uses in code.
	"""
	
	# Base class
	self._base = _base
	
	# Base Physics
	self._physics = _physics
	
	# Base World
	self._world = _world
	
	# Setup Player name
	self.playerName = name
                
	# Setup Player inventory
	self.playerDataStorage = [] # May change
	
	## ADD MOUSE LOOK TASK TO TASKMGR
	taskMgr.add(self.mouseLook, 'camera')
	
	# Crouch Flag
	self.crouching = False
	
	# Mouse look
	self.omega = 0.0
	
	# Setup player input
	self.accept('space', self.doJump)
	self.accept('c', self.doCrouch) # We need to fix the height
	self.accept( "escape",sys.exit ) 
	inputState.watchWithModifiers('forward', 'w')
	inputState.watchWithModifiers('left', 'a')
	inputState.watchWithModifiers('reverse', 's')
	inputState.watchWithModifiers('right', 'd')
	inputState.watchWithModifiers('turnLeft', 'q')
	inputState.watchWithModifiers('turnRight', 'e')
	
	# Camera Setup for player
	# Get the screen size for the camera controller
	self.winXhalf = base.win.getXSize()/2 
	self.winYhalf = base.win.getYSize()/2
	
	## SETUP CHARACTER AND CHARACTER SHAPE
	# Setup Shape
	h = 1.75
	w = 0.4
	shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

	self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
	self.characterNP = self._world.playerNP.attachNewNode(self.character)
	self.characterNP.setPos(-4, 0, 1.8) # May need some tweaking
	self.characterNP.setCollideMask(BitMask32.allOn())
	
	# Attach the character to the base _Physics
	self._physics.world.attachCharacter(self.character)
	
	# Reparent the camera to the player
	base.camera.reparentTo(self.characterNP) 
	base.camera.setPos(0,0,1.7) 
	base.camLens.setNearFar(camNear,camFar)
	base.camLens.setFov(camFov) 
	base.disableMouse()
	
	
    # Handle player jumping
    def doJump(self):
	self.character.setMaxJumpHeight(2.3)
	self.character.setJumpSpeed(4.5)
	self.character.doJump()
    
    
    # Handle player crouch.
    def doCrouch(self):
	self.crouching = not self.crouching
	sz = self.crouching and 0.6 or 1.0

	self.characterNP.setScale(Vec3(1, 1, sz))
    
    def mouseLook(self, task):
	dt = globalClock.getDt()
	# Handle mouse
	md = base.win.getPointer(0) 
	x = md.getX() 
	y = md.getY() 
	
	if base.win.movePointer(0, self.winXhalf, self.winYhalf): 
		self.omega = (x - self.winXhalf)*-mouseSpeed
		base.camera.setP( clampScalar(-90,90, base.camera.getP() - (y - self.winYhalf)*0.1) ) 
	self.processInput(dt)
	return task.cont
    
    # Handle player input
    def processInput(self, dt):
	speed = Vec3(0, 0, 0)
	
	#@param PCSpeed: Player move speed under devconfig.py
	if inputState.isSet('forward'): speed.setY( PCSpeed)
	if inputState.isSet('reverse'): speed.setY(-PCSpeed)
	if inputState.isSet('left'):    speed.setX(-PCSpeed)
	if inputState.isSet('right'):   speed.setX( PCSpeed)
	
	self.character.setAngularMovement(self.omega)
	self.character.setLinearMovement(speed, True)

