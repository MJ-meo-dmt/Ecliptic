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
	self.world.setGravity(Vec3(0, 0, worldGravity))
	
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
	
	# test the class test
	self.test = MakeObject(self, 'Box1', 'b', 1.0)
	
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
	
	### Setup model = collision model from egg file. ###
	# Collision model #
	colmodel = loader.loadModel('../assets/models/hallway.col.egg') # load model 
	
	solids_collection = BulletHelper.fromCollisionSolids(colmodel); # retrieve all solids found in the .egg file
	
	solid_main = render.attachNewNode('conteneur solides') # master node containing all our solids
	for solid in solids_collection: # for each solid found in solids collection
	    solid.node().setMass(0.0) # set zero mass / not affected by gravity
	    solid.node().setKinematic(True)
	    #solid.setCollideMask(BitMask32.allOn())
	    self.world.attachRigidBody(solid.node()) # attach solid to bullet world
	    solid.reparentTo(solid_main) # parent solid to master node
	
	# Display model #
	vismodel = loader.loadModel('../assets/models/hallway.1.egg') # visual model
	vismodel.reparentTo(render)
	
	
    
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
	
	# Write a class for pick able objects so that we instance the object in the world and if picked up we change that instance or del it then create new one, then same again when dropped
	
	
	bodyA = base.camera
	
	
	if self.pickTest == False:
	    self.test.bodyNP.wrtReparentTo(bodyA)
	    #self.test.bodyNP.copyTo(bodyA)
	    #self.test.worldNP
	    #bodyB.setPos(0, 2, 0)
	    self.test.bodyNP.node().setMass(0.0)
	    #self.test.bodyNP.setScale(1)
	    self.test.bodyNP.setCollideMask(BitMask32.allOff())
	    self.pickTest = True
	    
	    
	elif self.pickTest == True:
	    self.test.bodyNP.wrtReparentTo(self.worldNP)
	    self.test.bodyNP.node().setMass(1.0)
	    self.test.bodyNP.setCollideMask(BitMask32.allOn())
	   #bodyB.setPos(bodyPos)
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
    
    
class MakeObject(object):
    
    """
    MakeObject Class:
    
    Handles the creation for moveable objects in the physics world, also these will be objects
    the player could pick up, depending on mass (have to make check for this inside the picker method)
    
    @param w: self from Physics Class inorder to use things from it
    @param name: Object name
    @param shapeCheck: The type of shape to be use for the object, 'b' = BoxShape, 's' = SphereShape
    @param sx: shape x Vec3, scale = 0.5 default
    @param sy: shape y Vec3, scale = 0.5 default
    @param sz: shape z Vec3, scale = 0.5 default
    @param sr: shape radius for spheres = 3 default
    
    """
    
    def __init__(self, w, name, shapeCheck, mass=0.0, sx=0.5, sy=0.5, sz=0.5, sr=3):
	"""
	Constructor:
	
	"""
	# This is self, from the instance under Physics class
	self.mainWorld = w
	
	# Give the object a name
	self.name = name
	self.mass = mass
	
	# This is param settin 'b' = BoxShape, 's' = SphereShape
	self.shapeCheck = shapeCheck
	# Keeper for the final choice on shape
	self.makeShape = ''
	
	# Types of shapes
	boxShape = BulletBoxShape(Vec3(sx, sy, sz))
	sphereShape = BulletSphereShape(sr)
	
	if shapeCheck == 'b':
	    self.makeShape = boxShape
	    
	
	# Sphere shapes don't seem to work now... :P how cares...
	elif shapeCheck == 's':
	    self.makeShape = sphereShape
	
	
	# Create the body
	self.body = BulletRigidBodyNode(self.name)
	self.bodyNP = self.mainWorld.worldNP.attachNewNode(self.body)
	self.bodyNP.node().addShape(self.makeShape)
	self.bodyNP.node().setMass(mass)
	self.bodyNP.node().setDeactivationEnabled(False)
	self.bodyNP.setCollideMask(BitMask32.allOn())
	self.bodyNP.setPos(0, 0, 0)

	# Add a visual to the solid body
	visNP = loader.loadModel('../assets/models/box.egg')
	#visNP.setScale(0.5, 0.5, 0.5)
	visNP.clearModelNodes()
	visNP.reparentTo(self.bodyNP)
	
	# Finally add this object to the mainPhysics world
	self.mainWorld.world.attachRigidBody(self.body)
    
    
    
    
    
    
    
    
    
    
    
    
    
	
