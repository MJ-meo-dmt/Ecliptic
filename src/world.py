#!/usr/bin/python

# System imports
import sys, os, math

# Panda imports
from pandac.PandaModules import *
from panda3d.core import *
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from direct.task import Task
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.showbase.DirectObject import DirectObject

# Game imports
from globals import *
from egg_parse import *
#---------------------------------------------------------------------#

## World Class
class World(DirectObject):

    def __init__(self):
        
        # Origin of the world
        WORLD['origin'] = render.attachNewNode('origin')
        WORLD['origin'].setPos(0,0,0)
        
        # Rendering nodes
        RENDER_NODES['GEOMS']       = render.attachNewNode('MASTER_GEOM')
        RENDER_NODES['LIGHTS']      = render.attachNewNode('MASTER_LIGHTS')
        RENDER_NODES['TRANSPS']     = render.attachNewNode('MASTER_TRANSPARENTS')
        
        # Bullet nodes
        BULLET_NODES['MASTER']      = render.attachNewNode('MASTER_COL')
        BULLET_NODES['STATICS']     = BULLET_NODES['MASTER'].attachNewNode('STATIC_OBJECTS')
        BULLET_NODES['DYNAMICS']    = BULLET_NODES['MASTER'].attachNewNode('DYNAMIC_OBJECTS')
        BULLET_NODES['GHOSTS']      = BULLET_NODES['MASTER'].attachNewNode('GHOST_OBJECTS')
      
        # Gameplay nodes
        GAMEPLAY_NODES['SENSOR']    = RENDER_NODES['GEOMS'].attachNewNode('SENSORS')
        GAMEPLAY_NODES['DOOR']      = RENDER_NODES['GEOMS'].attachNewNode('DOORS')
        GAMEPLAY_NODES['PLAYER']    = RENDER_NODES['GEOMS'].attachNewNode('PLAYER')
        GAMEPLAY_NODES['SUIT']      = RENDER_NODES['GEOMS'].attachNewNode('SUIT')
        GAMEPLAY_NODES['TRIGGER']   = RENDER_NODES['GEOMS'].attachNewNode('TRIGGERS')
        GAMEPLAY_NODES['ITEM']      = RENDER_NODES['GEOMS'].attachNewNode('ITEMS')
        GAMEPLAY_NODES['SCREEN']    = RENDER_NODES['GEOMS'].attachNewNode('SCREENS')
        GAMEPLAY_NODES['PARTICLES'] = RENDER_NODES['GEOMS'].attachNewNode('PARTICLES')
        GAMEPLAY_NODES['DECOR']     = RENDER_NODES['GEOMS'].attachNewNode('DECORS')
        GAMEPLAY_NODES['LIGHT']     = RENDER_NODES['GEOMS'].attachNewNode('VIS_LIGHTS')
        
        # Attributes
        RENDER_NODES['LIGHTS'].node().setAttrib(DepthTestAttrib.make(RenderAttrib.MLess))
        RENDER_NODES['LIGHTS'].node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        RENDER_NODES['LIGHTS'].node().setAttrib(DepthWriteAttrib.make(DepthWriteAttrib.MOff))
        RENDER_NODES['LIGHTS'].node().setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullCounterClockwise))
        
        # 
        self.num_lights = 0
        

    def addLevel(self, levelName, levelObject):
        """
        This method adds created levels to the LEVELS dict{}

        @param levelName: String_key for the level.
        @param levelObject: The created level itself.
        """
        LEVELS[levelName] = levelObject

## Level Class
class Level():

    def __init__(self, name, model):
  
        self.name = name
        self.level = loader.loadModel(model)

        # Parse the egg model file and setup the level
        ParseMain(self.level)
