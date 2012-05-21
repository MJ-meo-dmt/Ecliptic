#!/usr/bin/python

# System imports
import sys, time, math

# Panda imports
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletSphereShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletTriangleMesh
from pandac.PandaModules import CollisionNode, CollisionSphere
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletHelper
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import BulletHingeConstraint
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import BitMask32
from panda3d.core import Point3
from panda3d.bullet import ZUp
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

# Game imports
from globals import *
from devconfig import *
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
	taskMgr.add(self.mouseLook, 'camera')
	
	# Setup player input
	self.accept('space', self.doJump)
	self.accept('c', self.doCrouch) # We need to fix the height
	self.accept('f1', self.showDebug)
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
                
	# Reparent the camera to the player
	base.camera.reparentTo(ENTITY['PC'].entityPlayer) 
	base.camera.setPos(0,0,1.7) 
	base.camLens.setNearFar(camNear,camFar)
	base.camLens.setFov(camFov) 
	base.disableMouse()
	
	# Omega for heading
	self.omega = 0.0
	
	# Setup the player and player physics
	self.char = ''
	self.setup_player()
	
	# Setup test World
	self.box = ''
	self.hinge = ''
	self.pickTest = False
	self.accept('e', self.playerPickup)
	self.setup_world()
	
    
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
	
	# Handle mouse
	md = base.win.getPointer(0) 
	x = md.getX() 
	y = md.getY() 
	
	if base.win.movePointer(0, self.winXhalf, self.winYhalf): 
		self.omega = (x - self.winXhalf)*-mouseSpeed
		base.camera.setP( clampScalar(-90,90, base.camera.getP() - (y - self.winYhalf)*0.1) ) 
	
	return task.cont
    
    # Handle player input
    def processInput(self, dt):
	speed = Vec3(0, 0, 0)
	#self.omega = 0.0

	if inputState.isSet('forward'): speed.setY( 2.0)
	if inputState.isSet('reverse'): speed.setY(-2.0)
	if inputState.isSet('left'):    speed.setX(-2.0)
	if inputState.isSet('right'):   speed.setX( 2.0)
	
	self.character.setAngularMovement(self.omega)
	self.character.setLinearMovement(speed, True)
    
    
    def setup_world(self):
	
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
	
	# Box A
	shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

	bodyA = BulletRigidBodyNode('Box A')
	bodyNP = self.worldNP.attachNewNode(bodyA)
	bodyNP.node().addShape(shape)
	bodyNP.node().setMass(0.4)
	bodyNP.node().setDeactivationEnabled(False)
	bodyNP.setCollideMask(BitMask32.allOn())
	bodyNP.setPos(-4, -5, 3)
	
	visNP = loader.loadModel('../assets/models/box.egg')
	visNP.setScale(0.5, 0.5, 0.5)
	visNP.clearModelNodes()
	visNP.reparentTo(bodyNP)
	
	self.box = bodyNP
	self.world.attachRigidBody(bodyA)
    
    # Setup the player physics
    def setup_player(self):
	
	# Character
	self.crouching = False

	h = 1.75
	w = 0.4
	shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

	self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
	self.characterNP = self.worldNP.attachNewNode(self.character)
	#self.characterNP.setMass(1.0)
	self.characterNP.setPos(-4, 0, 1.8)
	#self.characterNP.setH(45)
	self.characterNP.setCollideMask(BitMask32.allOn())
	self.world.attachCharacter(self.character)
	
	self.char = self.characterNP

	self.actorNP = ENTITY['PC'].entityPlayer
	self.actorNP.reparentTo(self.characterNP)
	self.actorNP.setScale(0.3048) # 1ft = 0.3048m
	#self.actorNP.setH(180)
	self.actorNP.setPos(0, 0, 0)
	
	## This isn't working so great.  Since I tried it with hingeConstraint but thats only between two rigid bodies.
	# Although I found something in the manual that I want to try.
    def playerPickup(self):
	
	bodyA = base.camera
	bodyB = self.box
	
	grab = bodyA.attachNewNode('grab')
	grab.setPos(0, 2, 1)
	
	print bodyA
	
	if self.pickTest == False:
	    bodyB.reparentTo(bodyA)
	    bodyB.setPos(0, 2, 0)
	    bodyB.node().setMass(0.0)
	    self.pickTest = True
	    
	    
	elif self.pickTest == True:
	    bodyPos = bodyA.getPos() + 1
	    bodyB.reparentTo(self.worldNP)
	    bodyB.setPos(bodyPos)
	    self.pickTest = False
	
    # Simulate Physics
    def update(self, task):
	
	dt = globalClock.getDt()
	self.processInput(dt)
	self.world.doPhysics(dt, 4, 1./270.)
	
	return task.cont
    
    # Enable/Disable debug
    def showDebug(self):
	
	# To enable debug
	self.debugNode = BulletDebugNode('Debug')
	self.debugNode.showBoundingBoxes(False)
	self.debugNode.showNormals(False)
	self.debugNode.showWireframe(True)
	self.debugNode.showConstraints(True)
	self.debugNP = render.attachNewNode(self.debugNode)
	self.debugNP.show()
	
	# Add the debug node to the physics world
	self.world.setDebugNode(self.debugNP.node())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
	
