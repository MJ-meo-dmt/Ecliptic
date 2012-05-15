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

# Game imports
from collTrav import *
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
class MakePlayer(Player):
        
    """
    MakePlayer Class:
        
    This class handels the creation of Players.
    Players will be stored in the Entity dict.
    """
    def __init__(self, name, entityName='PC_player'):

	"""
	constructor:
                
	@param name: String_name, for the Player - In game.
	@param entityName: String_name for the PC - Player in ENTITY /
	    dict{} for all uses in code.
	"""
                
	# Setup Player name
	self.playerName = name
                
	# Setup Player Move Speed
	self.playerSpeed = 4 # 
	self.isPlayerMoving = False # This should be used with PlayerInput.
	self.floating = False # For the jump function
                
	# Setup Player inventory
	self.playerDataStorage = [] # May change
                
	# Setup the Player
	self.entityPlayer = render.attachNewNode(entityName)
                
	# Setup the spawn position
	self.entityPlayer.setPos(0, 0, 0)
                
	# Setup collision solid for the PC - Player
	# initialize traverser 
	base.cTrav = CollisionTraverser() 
	base.cTrav.setRespectPrevTransform(True)
	
	# collision bits 
	self.groundCollBit = BitMask32.bit(0) 
	self.collBitOff = BitMask32.allOff()
	# Player collision sphere and collider
	playerCollision = self.entityPlayer.attachCollisionSphere('PCsphere', 0,0,1, .4, self.groundCollBit, self.collBitOff) 
                
	# initialize pusher 
	self.playerPusher = CollisionHandlerPusher() 
	self.playerPusher.addCollider(playerCollision, self.entityPlayer) 
	base.cTrav.addCollider(playerCollision, self.playerPusher)
                
	# Setup player ground Ray
	self.playerGroundColNp = self.entityPlayer.attachCollisionRay( 'PCRay', 
								0,0,.6, 0,0,-1, 
					    self.groundCollBit, self.collBitOff) 
					    
	self.playerGroundHandler = CollisionHandlerGravity() 
	self.playerGroundHandler.addCollider(self.playerGroundColNp, self.entityPlayer) 
	base.cTrav.addCollider(self.playerGroundColNp, self.playerGroundHandler)
                
	base.cTrav.showCollisions(render) 
                

## Player Input Class
class PlayerInput(DirectObject):
        
    """
    PlayerInput Class:
        
    Handles all the Inputs from the "PC" aka Player
        
    """     
    def __init__(self):
                
	# Get the screen size for the camera controller
	self.winXhalf = base.win.getXSize()/2 
	self.winYhalf = base.win.getYSize()/2
                
	# Reparent the camera to the player
	base.camera.reparentTo(ENTITY['PC'].entityPlayer) 
	base.camera.setPos(0,0,1.7) 
	base.camLens.setNearFar(.1,1000)
	base.camLens.setFov(70) 
	base.disableMouse() 
                
	# Set the control maps.
	self.controlMap = {"left": 0, "right": 0, "forward": 0, "backward": 0, "jump": 0, "wheel-in": 0, "wheel-out": 0}
                
	# Add the move method to the taskman
	taskMgr.add(self.move, 'move-task')
                
	### SETUP KEYBOARD ###
	self.accept( "escape",sys.exit ) 
	self.accept("w", self.setControl, ["forward", 1])
	self.accept("a", self.setControl, ["left", 1])
	self.accept("s", self.setControl, ["backward", 1])
	self.accept("d", self.setControl, ["right", 1])
	self.accept("space", self.setControl, ["jump", 1])
                
	self.accept("w-up", self.setControl, ["forward", 0])
	self.accept("a-up", self.setControl, ["left", 0])
	self.accept("s-up", self.setControl, ["backward", 0])
	self.accept("d-up", self.setControl, ["right", 0])
	self.accept("space-up", self.setControl, ["jump", 0])
        
    def setControl(self, key, value):
	self.controlMap[key] = value
        
    # This is for calculating the jump.
    def jump(self, dt):
	# Get the "floating" from player object. 
	playerFloating = ENTITY['PC'].floating
	# Get the player - PC
	playerPc = ENTITY['PC'].entityPlayer
                
	if not playerFloating:
		playerFloating=True
		lf=LerpFunc(lambda z: playerPc.setZ(z),
			fromData = playerPc.getZ(),
			toData = playerPc.getZ()+1.0, duration = 0.7,
			blendType = 'easeOut')
		self.seq=Sequence(lf, Wait(.7))
		self.seq.start()
	elif not self.seq.isPlaying(): playerFloating=False
        
    def move(self, task):
                
	# Get the player - PC
	self.player = ENTITY['PC'].entityPlayer
	# Get the player speed
	self.playerSpeed = ENTITY['PC'].playerSpeed
                
	dt=globalClock.getDt() 
                
	# Handle mouse
	md = base.win.getPointer(0) 
	x = md.getX() 
	y = md.getY() 
	if base.win.movePointer(0, self.winXhalf, self.winYhalf): 
		self.player.setH(self.player, (x - self.winXhalf)*-0.1) 
		base.camera.setP( clampScalar(-90,90, base.camera.getP() - (y - self.winYhalf)*0.1) ) 
		
	# Move the player if the keys are pressed 
	# Forward.
	if (self.controlMap["forward"] != 0):
	    self.player.setY(self.player, self.playerSpeed * globalClock.getDt())
	# Backward.
	if (self.controlMap["backward"] != 0):
	    self.player.setY(self.player, -self.playerSpeed * globalClock.getDt())
	# Left.
	if (self.controlMap["left"] != 0):
	    self.player.setX(self.player, -self.playerSpeed * globalClock.getDt())
	# Right.
	if (self.controlMap["right"] != 0):
	    self.player.setX(self.player, self.playerSpeed * globalClock.getDt())
	# Jump
	if (self.controlMap["jump"] != 0):
	    self.jump(dt)
                
                         
	return task.cont         
