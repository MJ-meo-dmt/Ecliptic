#!/usr/bin/python

# System imports
import sys, time, math

# Panda imports
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletTriangleMesh
from pandac.PandaModules import CollisionNode, CollisionSphere
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletGhostNode
from panda3d.core import BitMask32
from panda3d.bullet import ZUp
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

# Game imports
from globals import *

#---------------------------------------------------------------------#


## Main Physics Class
class Physics(DirectObject):
    
    """
    Physics Class:
    
    Handles the all Physics
    """
    
    def __init__(self):
	
	## Setup a bullet world.
	
	# World Node (MAIN)
	self.worldNP = render.attachNewNode('World')
	
	# World
	self.world = BulletWorld()
	self.world.setGravity(Vec3(0, 0, -9.81))
	
	# Add the simulation method to the taskmgr
	taskMgr.add(self.update, 'update')
	
	# Setup player input
	self.accept('space', self.doJump)
	self.accept('c', self.doCrouch) # We need to fix the height
	inputState.watchWithModifiers('forward', 'w')
	inputState.watchWithModifiers('left', 'a')
	inputState.watchWithModifiers('reverse', 's')
	inputState.watchWithModifiers('right', 'd')
	inputState.watchWithModifiers('turnLeft', 'q')
	inputState.watchWithModifiers('turnRight', 'e')
	
	# Setup the player and player physics
	self.setup_player()
    
    # Handle player jumping
    def doJump(self):
	self.character.setMaxJumpHeight(5.0)
	self.character.setJumpSpeed(8.0)
	self.character.doJump()
    
    
    # Handle player crouch.
    def doCrouch(self):
	self.crouching = not self.crouching
	sz = self.crouching and 0.6 or 1.0

	self.characterNP.setScale(Vec3(1, 1, sz))
    
    
    # Handle player input
    def processInput(self, dt):
	speed = Vec3(0, 0, 0)
	omega = 0.0

	if inputState.isSet('forward'): speed.setY( 2.0)
	if inputState.isSet('reverse'): speed.setY(-2.0)
	if inputState.isSet('left'):    speed.setX(-2.0)
	if inputState.isSet('right'):   speed.setX( 2.0)
	if inputState.isSet('turnLeft'):  omega =  120.0
	if inputState.isSet('turnRight'): omega = -120.0

	self.character.setAngularMovement(omega)
	self.character.setLinearMovement(speed, True)
    
    
    # Setup the player physics
    def setup_player(self):
	
	#############################################
	##
	##  GROUND FOR TESTING 
	#############################################
	
	# Ground
	shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

	np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
	np.node().addShape(shape)
	np.setPos(0, 0, 0)
	np.setCollideMask(BitMask32.allOn())

	self.world.attachRigidBody(np.node())
	
	##############################################
	##############################################
	
	# Character
	self.crouching = False

	h = 1.75
	w = 0.4
	shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

	self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
	#self.character.setMass(1.0)
	self.characterNP = self.worldNP.attachNewNode(self.character)
	self.characterNP.setPos(-2, 0, 14)
	#self.characterNP.setH(45)
	self.characterNP.setCollideMask(BitMask32.allOn())
	self.world.attachCharacter(self.character)

	self.actorNP = ENTITY['PC'].entityPlayer
	self.actorNP.reparentTo(self.characterNP)
	self.actorNP.setScale(0.3048) # 1ft = 0.3048m
	#self.actorNP.setH(180)
	self.actorNP.setPos(0, 0, 0)
	
    # Simulate Physics
    def update(self, task):
	
	dt = globalClock.getDt()
	self.processInput(dt)
	self.world.doPhysics(dt, 4, 1./270.)
	
	return task.cont
    
    # Enable/Disable debug
    def _debug(self):
	
	# To enable debug
	self.debugNode = BulletDebugNode('Debug')
	self.debugNode.showBoundingBoxes(False)
	self.debugNode.showNormals(False)
	self.debugNP = render.attachNewNode(self.debugNode)
	self.debugNP.show()
	
	# Add the debug node to the physics world
	self.world.setDebugNode(self.debugNP.node())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
	
