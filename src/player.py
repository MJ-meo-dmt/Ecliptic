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
	self.playerSpeed = PCSpeed # 
	self.isPlayerMoving = False # This should be used with PlayerInput.
	self.floating = False # For the jump function
                
	# Setup Player inventory
	self.playerDataStorage = [] # May change
	
                
	# Setup the Player
	self.entityPlayer = render.attachNewNode(entityName)
                
	# Setup the spawn position
	self.entityPlayer.setPos(0, 0, 0)
	
	#> Setup collision solids for the PC - Player
	'''
	# collision bits for player
	self.groundCollBit = BitMask32.bit(0) 
	self.collBitOff = BitMask32.allOff()
	
	# This way seem to bug out.
	#playerCollision = self.entityPlayer.attachCollisionSphere('PCsphere', 0,0,1, .4, self.groundCollBit, self.collBitOff)
	
	# Collision Sphere for player: cx, cy, cz, r
	self.playerColl = CollisionSphere(0, 0, 1, .4)
        self.playercollNode = CollisionNode('PCsphere')
        self.playercollNode.addSolid(self.playerColl)
        self.playercollNode.setFromCollideMask(self.groundCollBit)
        self.playercollNode.setIntoCollideMask(self.collBitOff)
        self.playercollNodePath = self.entityPlayer.attachNewNode(self.playercollNode)  # THis goes to self.playerPusher as playerCollision
	
	# This way seem to bug out.
	#self.playerGroundColNp = self.entityPlayer.attachCollisionRay( 'PCRay', 
	#							0,0,.6, 0,0,-1, 
	#				    self.groundCollBit, self.collBitOff) 
	
	# Collision Ray for player: ox, oy, oz, dx, dy, dz
	self.playerCollRay = CollisionRay(0, 0, .6, 0, 0, -1)
        self.playercollNodeRay = CollisionNode('PCRay')
        self.playercollNodeRay.addSolid(self.playerCollRay)
        self.playercollNodeRay.setFromCollideMask(self.groundCollBit)
        self.playercollNodeRay.setIntoCollideMask(self.collBitOff)
        self.playercollNodePathRay = self.entityPlayer.attachNewNode(self.playercollNodeRay)
	'''
## Player Input Class
class PlayerInput(DirectObject):
        
    """
    PlayerInput Class:
        
    Handles all the Inputs from the "PC" aka Player
    Note: Physics.py handles all PC related movement aka, keyboard+mouse
        
    """     
    def __init__(self):
	
	### SETUP KEYBOARD ###
	self.accept( "escape",sys.exit ) 
	
