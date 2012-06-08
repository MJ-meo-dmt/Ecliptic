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
    
    def __init__(self, _base, _world):
	
	# Base Class
	self._base = _base
	
	# Base World
	self._world = _world
	
	## Setup a bullet world.
	
	# World Node (MAIN)
	self.worldNP = render.attachNewNode('World')
	
	# World
	self.world = BulletWorld()
	self.world.setGravity(Vec3(0, 0, worldGravity))
	
	# Add the simulation method to the taskmgr
	taskMgr.add(self.update, 'update')
	
	# Setup test World
	self.box = ''
	self.hinge = ''
	self.pickTest = False
	self.sensor = ''
	
	# test the class test
	self.test = MakeObject(self, 'Box1', 'b', 20.0)
	self.test.bodyNP.setPos(0, 1, 1)
	
	
	pos = 1
	
	#for x in range(5):
	    #x = MakeObject(self, 'box', 'b', 5.0)
	    #pos += 1
	    #x.bodyNP.setPos(0, 0, pos)
	
	
	self.accept('e', self.playerPickup)
	self.accept('f1', self.showDebug)
	self.setup_world()
	#taskMgr.add(self.checkGhost, 'checkGhost')

    
    
    def setup_world(self):
	
	#############################################
	##
	##  GROUND FOR TESTING 
	#############################################
	pass
	# Ground
	#shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

	#np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
	#np.node().addShape(shape)
	#np.setPos(0, 0, 0)
	#np.setCollideMask(BitMask32.allOn())

	#self.world.attachRigidBody(np.node())
	
	##############################################
	##############################################
	
	
	
	########################
	# FIXED :D  - Still simple atm.
	########################
    def playerPickup(self):
	
	# Write a class for pick able objects so that we instance the object in the world and if picked up we change that instance or del it then create new one, then same again when dropped
	
	
	bodyA = base.camera
	
	# Will have to make a pick up mask so that it collides with walls and floors and w/e else.. except with the player
	if self.pickTest == False:
	    self.test.bodyNP.wrtReparentTo(bodyA)
	    #self.test.bodyNP.copyTo(bodyA)
	    #self.test.worldNP
	    #bodyB.setPos(0, 2, 0)
	    self.test.bodyNP.node().setMass(0.0)
	    #self.test.bodyNP.setScale(1)
	    #self.test.bodyNP.setCollideMask(BitMask32.allOn())
	    self.pickTest = True
	    
	    
	elif self.pickTest == True:
	    self.test.bodyNP.wrtReparentTo(self.worldNP)
	    self.test.bodyNP.node().setMass(20.0)
	    #self.test.bodyNP.setCollideMask(BitMask32.allOn())
	   #bodyB.setPos(bodyPos)
	    self.pickTest = False
	
    # Simulate Physics
    def update(self, task):
	
	dt = globalClock.getDt()
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
	    
	
	# Sphere shapes don't seem to work now... :P who cares...
	elif shapeCheck == 's':
	    self.makeShape = sphereShape
	
	
	# Create the body
	self.body = BulletRigidBodyNode(self.name)
	self.bodyNP = self.mainWorld.worldNP.attachNewNode(self.body)
	self.bodyNP.node().addShape(self.makeShape)
	self.bodyNP.node().setMass(mass)
	self.bodyNP.node().setDeactivationEnabled(False)
	self.bodyNP.setCollideMask(BitMask32.allOn())
	

	# Add a visual to the solid body
	visNP = loader.loadModel('../assets/models/box.egg')
	#visNP.setScale(0.5, 0.5, 0.5)
	visNP.clearModelNodes()
	visNP.reparentTo(self.bodyNP)
	
	# Finally add this object to the mainPhysics world
	self.mainWorld.world.attachRigidBody(self.body)
    
    
    
    
    
    
    
    
    
    
    
    
    
	
