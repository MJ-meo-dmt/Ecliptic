###  GAME PROPS - OBJECTS  ###
"""
GAME PROPS:

Handles the creation of the objects parsed from the egg_file.

Basically each object class here will set the object up in panda,
as it were in blender, with all it's properties.
"""

# System imports


# Panda imports
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.bullet import *
from math import *
from direct.showbase.DirectObject import DirectObject


# Game imports
from globals import *
from deferredLight import *
from eventcomponent import *


#----------------------------------------------------------------------#

# This will handle all object setups from the egg file.


# Base object class
class baseObject():
    
    """
    baseObject Class:
    
    Base class for game objects.
    """
    
    def __init__(self):
    
        self.name = ""
        self.triggers = ""
        self.area = 0
        self.pickable = ""
        self.needs = ""
        self.status = ""
        self.soundON = ""
        self.soundOFF = ""
        self.style = ""
        self.physics = ""
        self.mass = 0.0
        self.parent = ""

        self.position = Point3(0, 0, 0)
        self.hpr = VBase3(0, 0, 0)
        self.scale = VBase3(0, 0, 0)

class GameObject(baseObject):
    
    def __init__(self, _model, object):
        
        baseObject.__init__(self)
       
        self.object = object
        self.event = False
    
        name = ''
        self.type = 'DECOR'
        
        for i in OBJECTS_TYPES:
            if self.object.hasTag(i):
                self.type = i
                name = self.object.getTag(i)
                
                if i in EVENT_LIST:
                    self.event = EVENT[i]
                    
                else:
                    pass
        
        print "Object Event: ",self.event
        
        self.name = name
        self.triggers = self.object.getTag('triggers')
        self.area = self.object.getTag('area')
        self.pickable = self.object.getTag('pickable')
        self.needs = self.object.getTag('needs')
        self.status = self.object.getTag('status')
        self.soundON = self.object.getTag('soundON')
        self.soundOFF = self.object.getTag('soundOFF')
        self.style = self.object.getTag('style')
        self.physics = self.object.getTag('physics')
        self.mass = self.object.getTag('mass')
        self.parent = self.object.getTag('parent')
        
        self.shadows = 0

        self.position = self.object.getPos(_model)
        self.hpr = self.object.getHpr(_model)
        self.scale = self.object.getScale(_model)
        
        ## TESTING
        self.bodyNP = False
        print "Outside: ", self.bodyNP
        if self.physics:
            self.set_physics()
        print "Outside After: ", self.bodyNP
        
        self.render()
        
        print(self.type)
        if self.type == 'LIGHT':
            self.create_light()
            
        taskMgr.add(self.update,'update'+self.name)
        
    def update(self,task):
        if self.shadows == 1:
            BUFFER_SYSTEM['main'].shadow_cube.setPos(self.object.getPos())
        return task.cont

    def render(self):

        self.object.reparentTo(GAMEPLAY_NODES[self.type])


    ### Method for setting up the object's physics. ###
    def set_physics(self):
        
        Physics = self.physics
        Mass = self.mass

        # Get the geom node
        objectNode = self.object.node()
        objectGeom = objectNode.getGeom(0)
            
        # Setup the bullet mesh
        objectMesh = BulletTriangleMesh()
        objectMesh.addGeom(objectGeom)

        # Setup a static object
        if Physics == 'static':
            body = BulletRigidBodyNode('Bullet '+self.name)
            self.bodyNP = BULLET_NODES['STATICS'].attachNewNode(body)
            shape = BulletTriangleMeshShape(objectMesh, dynamic=False)
            self.bodyNP.node().setKinematic(True)
            self.bodyNP.node().addShape(shape)
            self.bodyNP.node().setMass(0)
            self.bodyNP.setCollideMask(BitMask32.allOn())
            print "inside IF 1: ", self.bodyNP
            # Attach the static object to the _physics world
            return PHYSICS['WORLD'].attachRigidBody(body), self.bodyNP

        # Setup a Dynamic object
        if Physics == 'dynamic':
            body = BulletRigidBodyNode('Bullet '+self.name)
            self.bodyNP = BULLET_NODES['DYNAMICS'].attachNewNode(body)
            shape = BulletTriangleMeshShape(objectMesh, dynamic=True)
            self.bodyNP.node().addShape(shape)
            self.bodyNP.node().setMass(Mass)
            self.bodyNP.setCollideMask(BitMask32.allOn())
            print "inside IF 2: ", self.bodyNP
            # Attach the dynamic object to the _physics world
            return PHYSICS['WORLD'].attachRigidBody(body), self.bodyNP

        # Setup a Ghost object
        if Physics == 'ghost':
            ghost = BulletGhostNode('Ghost_sensor '+self.name)
            shape = BulletTriangleMeshShape(objectMesh, dynamic=False)
            ghost.addShape(shape)
            self.bodyNP = BULLET_NODES['GHOSTS'].attachNewNode(ghost)
            self.bodyNP.setPos(self.position)
            self.bodyNP.setCollideMask(BitMask32(0x0f))
            print "inside IF 3: ", self.bodyNP
            # Attach the ghost object to the _physics world
            return PHYSICS['WORLD'].attachGhost(ghost)
        
        
    
    ### Setup lights ###
    def create_light(self):

        distance = float(self.object.getTag('distance'))
        energy = float(self.object.getTag('energy'))
        color = COLORS[self.object.getTag('color')]
        
        self.shadows = 0
        if bool(self.object.getTag('shadows')) == True :
            self.shadows = 1
                    
        light = DeferredLight(
            shadows=self.shadows,
            vizparent=self.object,
            num=str(WORLD['CLASS'].num_lights),
            movement=True,
            buffer_system=BUFFER_SYSTEM['main'],
            parent=RENDER_NODES['LIGHTS'],   
            geom="../assets/models/sphere_simple2",
            vizgeom="../assets/models/cube",
            light_type="point",
            color=color,
            pos=self.position,
            scale=distance,
            style=self.object.getTag('simple_light'),
            attenuation=Vec3(1, 1, 1),
            energy = energy,
            Kd=Vec3(1,1,1),
            Ks=Vec3(1,1,1),
            follow=self.object
        )

