#!/usr/bin/python

# System imports
import sys, os

# Panda imports
from panda3d.core import *

# Game imports
from globals import *

#---------------------------------------------------------------------#


## Main Collisions Class
class Collisions(object):
    
    """
    Collisions Class:
    
    Handles all collisions
    """
    
    def __init__(self):
	
	"""
	Constuctor:
	
	Sets up all the collisions, regarding the level and the player.
	"""
	
	# Get the player entity.
	self.player = ENTITY['PC']
	
	# Start the collisions.
	base.cTrav = CollisionTraverser() 
	base.cTrav.setRespectPrevTransform(True)
	
	# initialize pusher 
	self.playerPusher = CollisionHandlerPusher() 
	self.playerPusher.addCollider(self.player.playercollNodePath, self.player.entityPlayer) 
	base.cTrav.addCollider(self.player.playercollNodePath, self.playerPusher)
	
	# initialize gravity handler and ray
	self.playerGroundHandler = CollisionHandlerGravity() 
	self.playerGroundHandler.addCollider(self.player.playercollNodePathRay, self.player.entityPlayer) 
	base.cTrav.addCollider(self.player.playercollNodePathRay, self.playerGroundHandler)
	
	##> DEBUG
	# Show the collisions
	base.cTrav.showCollisions(render)
