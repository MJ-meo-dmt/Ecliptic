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
	
