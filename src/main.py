#!/usr/bin/python

"""
See LICENSE in main folder.
---------------------------


* This file contains the main class and methods to start the game.


---------------------------
Developers:

- MJ-meo-dmt
"""

# System imports
import sys
import os

# Panda Engine imports
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("",
"""
    window-title Ecliptic - Space
    fullscreen 0
    win-size 1024 768
    cursor-hidden 0
    sync-video 0
    show-frame-rate-meter 1
    show-buffers 0
    basic-shaders-only 1
    compressed-textures 1
    force-parasite-buffer 1
    prefer-parasite-buffer 1

"""
)
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.filter.FilterManager import *

# Game imports
from world import *
from player import *
from gamelogic import *
from globals import *
from physics import *
from buffers import *
from filters import *

#----------------------------------------------------------------------#

class Main(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        # reinitialize display
        self.render = render
        self.render.setState(RenderState.makeEmpty())
        #base.cam.node().setActive(0)

        print "Running game..."

        # Needs fix
        # Hide the cursor
        props = WindowProperties() 
        props.setCursorHidden(True) 
        self.win.requestProperties(props)

        # Master Instances
        WORLD['CLASS']   = World()
        PHYSICS['CLASS'] = Physics()
        #PLAYER['CLASS']  = Player()

        BUFFER_SYSTEM['main'] = BufferSystem(base)
        
        self.FilterClass = FilterSystem(base, self, BUFFER_SYSTEM['main'])

        

        # init the main methods
        self.init_player()
        self.init_world()
        
        
        BUFFER_SYSTEM['main'].render()
        
        # Event Instances
        #self.SensorEvent = SensorEvent(self)
        self.messenger.send('Sen')

        # Debug: Show the scene graph.
        #self.render.ls()
        #print sys.getsizeof(OBJECTS)
        #for i in OBJECTS['SENSOR']:
        #	print i

         ### DEBUG ###
        ### DISPLAY CUSTOM TEXTURE FROM BUFFERS ###
        #filterMan = FilterManager(base.win, base.cam)
        #original_map = Texture()
        #finalQuad = filterMan.renderSceneInto(colortex = original_map)
        #finalQuad.setShader(loader.loadShader("shaders/display_texture.cg"))
        #finalQuad.setShaderInput('color',BUFFER_SYSTEM['main'].light_map)
        ### DEBUG ###
        
    def init_world(self):

        self.level1 = Level("Level1", "../assets/models/NewRoom.egg")

    def init_player(self):

        PLAYER['CLASS'] = MakePlayer()


game = Main()
game.run()



#### QUICK THOUGHTS :P














