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
from panda3d.bullet import *
from direct.showbase.InputStateGlobal import inputState

# Game imports
from devconfig import *
from globals import *
from gui import *


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
    def __init__(self):

        """
        constructor:
                    
        @param name: String_name, for the Player - In game.
        @param entityName: String_name for the PC - Player in ENTITY /
        dict{} for all uses in code.
        
        """
        
        
                   
        self.direction = Vec3(0,0,0)
        self.angular_direction = Vec3(0,0,0)
        self.speed = 1
        self.angular_speed = 3
        
        # Setup Player inventory
        self.playerDataStorage = [] # May change
    
        ## ADD MOUSE LOOK TASK TO TASKMGR
        #taskMgr.add(self.look, 'camera')
    
        # Crouch Flag
        self.crouching = False
    
        # Mouse look
        self.omega = 0.0
    
        # Setup player input
        self.accept('space', self.jump)
        self.accept('c', self.crouch) # We need to fix the height
        self.accept( "escape",sys.exit ) 
        
        self.accept('arrow_up', self.up )
        self.accept('arrow_down', self.down )
        self.accept('arrow_left', self.left )
        self.accept('arrow_right', self.right)
        
        self.accept("arrow_up-up", self.idle, ["up"])
        self.accept("arrow_down-up", self.idle, ["down"])
        self.accept("arrow_left-up", self.idle, ["left"])
        self.accept("arrow_right-up", self.idle, ["right"])
        
        #inputState.watchWithModifiers('forward', 'w')
        #inputState.watchWithModifiers('left', 'a')
        #inputState.watchWithModifiers('reverse', 's')
        #inputState.watchWithModifiers('right', 'd')
        #inputState.watchWithModifiers('turnLeft', 'q')
        #inputState.watchWithModifiers('turnRight', 'e')
        #inputState.watchWithModifiers('turnRight', 'e')
    
        # Camera Setup for player
        # Get the screen size for the camera controller
        self.winXhalf = base.win.getXSize()/2 
        self.winYhalf = base.win.getYSize()/2
    
        ## SETUP CHARACTER AND CHARACTER SHAPE
        # Setup Shape
        
        # units = meters
        # body height : 1.8 meters
        # eyes line : 1.8 - 0.11 meters = 1.69 meters
        # h is distance between the centers of the 2 spheres
        # w is radius of the spheres
        
        # 1.8 = 0.3 + 1.2 + 0.3
        # center : 1.8/2 = 0.9
        # camera height : 1.69-0.9 = 0.79
        
        h = 1.2
        w = 0.3
        
        # Player needs different setup saam as bullet character controller.
        # Atm force gets added onto the node making it ballich
        shape = BulletCapsuleShape(w, h , ZUp)
        
        node = BulletRigidBodyNode('Box')
        node.setMass(1.0)
        node.addShape(shape)
        self.node = node
        node.setAngularDamping(10)

        np = GAMEPLAY_NODES['PLAYER'].attachNewNode(node)
        np.setPos(0, 0, 1)
        
        self.arm = np.attachNewNode('arm')
        self.arm.setPos(0,0,0.2)
        
        self.np = np
         
        PHYSICS['WORLD'].attachRigidBody(node)

        #self.character = BulletCharacterControllerNode(shape, 1, 'Player')
        #-------------------------------------------------------------------#
        # PLAYER GRAVITY SETTINGS AND FALL SPEED #
        #self.character.setGravity(0.87)
        #self.character.setFallSpeed(0.3)
        #
        #-------------------------------------------------------------------#
    
        #self.characterNP = GAMEPLAY_NODES['PLAYER'].attachNewNode(self.character)
        #self.characterNP.setPos(0, 0, 2) # May need some tweaking
        #self.characterNP.setCollideMask(BitMask32.allOn())
        
        
        # Attach the character to the base _Physics
        #PHYSICS['WORLD'].attachCharacter(self.character)
        
        # Reparent the camera to the player
        #base.camera.reparentTo(self.np) 
        #base.camera.setPos(0,0,0.79) 
        #base.camLens.setNearFar(camNear,camFar)
        base.camLens.setFov(90) 
        base.disableMouse()
        gui = Crosshair()
        
        self.arm = loader.loadModel('../assets/models/test.egg')
        screens = self.arm.findAllMatches('**')
        self.arm_screen = None
        rot = 0
        pos = 0
        for screen in screens :
            if screen.hasTag('screen'):
                self.arm_screen = screen
                rot = screen.getHpr()
                pos = screen.getPos()
                print("rotation"+str(rot))
         
        self.actor = Actor('../assets/models/test.egg', {'anim1':'../assets/models/test-Anim0.egg'})
        self.actor.reparentTo(self.np)
        self.actor.loop('anim1')
        self.actor.setPos(.0,-0.1,0.4)
        self.actor.setH(180)
        self.actor.node().setBounds(OmniBoundingVolume())
        self.actor.node().setFinal(True)
        #self.actor.setTwoSided(True)
        #self.actor.reparentTo(self.world.buffer_system.geom_cam)
        #self.actor.hide(self.world.buffer_system.light_mask)
        
        # attach smth to hand 
        
        picker = self.actor.exposeJoint(None,"modelRoot","hand_picker")
        
        arm_bone = self.actor.exposeJoint(None,"modelRoot","screen_picker")
        
        self.arm_screen.reparentTo(arm_bone)
        self.arm_screen.setH(self.arm_screen.getH()+90)
        self.temp_animate = self.arm_screen

        self.picker = picker
        
        taskMgr.add(self.update,'update player position')
        
        # Player Debug:
        #print ""
        #print "Player Character controller settings: "
        #print ""
        #print "Character Gravity: ", self.character.getGravity()
        #print "Character Max Slope: ",self.character.getMaxSlope()
        #print ""
        
         
    def up(self):
        self.direction += Vec3(0,1,0)
        self.angular_direction += Vec3(1,0,0)
        
    def down(self):
        self.direction += Vec3(0,-1,0)
        
    def left(self):
        self.direction += Vec3(-1,0,0)
            
    def right(self):
        self.direction += Vec3(1,0,0)
        
    def idle(self, key):
        
        if(key == "up"):
            self.direction -= Vec3(0,1,0)
            self.angular_direction -= Vec3(1,0,0)
        elif(key == "down"):
            self.direction -= Vec3(0,-1,0)
        elif(key == "left"):
            self.direction -= Vec3(-1,0,0)
        elif(key == "right"):
            self.direction -= Vec3(1,0,0)
        
        
    # Handle player jumping
    def jump(self):
        self.character.setMaxJumpHeight(2.3)
        self.character.setJumpSpeed(4.5)
        self.character.doJump()
   
    # Handle player crouch. <Buged to shit>
    def crouch(self):
        self.crouching = not self.crouching
        sz = self.crouching and 0.6 or 1.0
        #self.character.getShape().setLocalScale(Vec3(1, 1, sz))
        self.characterNP.setScale(Vec3(1, 1, sz) * 0.3048)
        #self.characterNP.setPos(0, 0, -1 * sz)
    
    # Handle player mouse
    def look(self, task):
        dt = globalClock.getDt()
        # Handle mouse
        md = base.win.getPointer(0) 
        x = md.getX() 
        y = md.getY() 
        if base.win.movePointer(0, self.winXhalf, self.winYhalf): 
            self.omega = (x - self.winXhalf)*-mouseSpeed
            base.camera.setP( (clampScalar(-90,90, base.camera.getP() - (y - self.winYhalf)*0.09)) ) 
        self.processInput(dt)
        return task.cont
    
    def update(self,task):
        dt = globalClock.getDt()
        
        self.np.setPos(self.np,self.direction * dt * self.speed)
        
        base.camera.setPos(self.np.getPos()+ Vec3(0,0,0.79))
        
        md = base.win.getPointer(0) 
        x = md.getX() 
        y = md.getY() 
        if base.win.movePointer(0, self.winXhalf, self.winYhalf): 
            base.camera.setP(base.camera.getP() - (y - self.winYhalf)*dt*self.angular_speed)
            self.np.setH(self.np.getH() - (x - self.winXhalf)*dt*self.angular_speed)
        
        base.camera.setH(self.np.getH())
        base.camera.setR(self.np.getR())
        
        self.node.setAngularFactor(0)
        self.node.setAngularVelocity(0)
        
        BUFFER_SYSTEM['main'].reflection_cube.setPos(base.camera.getPos())
        BUFFER_SYSTEM['main'].reflection_cube.setHpr(base.camera.getHpr())
         
        return task.cont
        
    # Handle player input
    def processInput(self, dt):
        print(self.direction)
        speed = Vec3(0, 0, 0)
        
        #@param PCSpeed: Player move speed under devconfig.py
        if inputState.isSet('forward'): speed.setY( PCSpeed)
        if inputState.isSet('reverse'): speed.setY(-PCSpeed)
        if inputState.isSet('left'):    speed.setX(-PCSpeed)
        if inputState.isSet('right'):   speed.setX( PCSpeed)
        
        
        self.character.setAngularMovement(self.omega)
        self.character.setLinearMovement(speed, True)

