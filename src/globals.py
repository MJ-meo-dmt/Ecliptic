#!/usr/bin/python

#######################################################################

# Here I keep all the Dict{}

#######################################################################

# Numbers of things

# Keeps levels
LEVELS = {}

# Keeps Players, entities
ENTITY = {}

# Keeps Stations (May move levels into this one? not sure yet.)
STATIONS = {}

# Event Components
EVENT_LIST = ['SENSOR', 'DOOR', 'PLAYER', 'TRIGGER', 'LIGHT','ITEM', 'SCREEN', 'PARTICLES', 'SUIT']

# Keeps all objects found in egg files with instance to class
OBJECTS = {}
OBJECTS['ROOM'] = {}
OBJECTS['SENSOR'] = {}
OBJECTS['DOOR'] = {}
OBJECTS['PLAYER'] = {}
OBJECTS['TRIGGER'] = {}
OBJECTS['LIGHT'] = {}
OBJECTS['ITEM'] = {}
OBJECTS['SCREEN'] = {}
OBJECTS['PARTICLES'] = {}
OBJECTS['SUIT'] = {}
OBJECTS['DECOR'] = {}
OBJECTS_TYPES = ['ROOM', 'SENSOR', 'DOOR', 'PLAYER', 'TRIGGER', 'LIGHT','ITEM', 'SCREEN', 'PARTICLES', 'SUIT', 'DECOR']

META = {}

BASE = {}

# Master nodes
GAMEPLAY_NODES = {}
RENDER_NODES = {}
BULLET_NODES = {}

# Buffer
BUFFER_SYSTEM = {}

# Shader globals
SHADER_TAGS = {}
SHADER_TAGS['g-buffer'] = 'g-buffer pass'
SHADER_TAGS['compute light'] = 'compute lights pass'

# Graphics
COLORS = {}
COLORS['red'] = (1,0,0,1)
COLORS['green'] = (0,1,0,1)
COLORS['blue'] = (0,0,1,1)
COLORS['white'] = (1,1,1,1)

# Game globals
WORLD = {}
PLAYER = {}
PHYSICS = {}

# Files globals
PATHS = {}
PATHS['models'] = 'ressources/assets/models/'
PATHS['shaders'] = 'ressources/shaders/'
PATHS['textures'] = 'ressources/assets/textures'

# Game configuration
CONFIG = {}
CONFIG['resolutionX'] = 1024
CONFIG['resolutionY'] = 768
CONFIG['bloomPower'] = 0.5

