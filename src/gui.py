#!/usr/bin/python

# System imports

# Panda imports
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import * 
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib


# Game imports


#----------------------------------------------------------------------#


# Player Crosshair
class Crosshair(DirectObject):
	def __init__(self):
		self.crosshair = OnscreenImage('../assets/gui/crosshair3.png', (0, 0, 0) )
		self.crosshair.setScale(0.03)
		self.crosshair.setTransparency(TransparencyAttrib.MAlpha, 0)

