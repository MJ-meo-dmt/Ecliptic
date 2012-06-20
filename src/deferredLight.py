###########################################
### Light class for deferred lighting   ###
### 23/12/11                            ###
###########################################

from panda3d.core import Shader, NodePath, Vec3, DepthTestAttrib, RenderAttrib, ColorBlendAttrib, DepthWriteAttrib, CullFaceAttrib, Vec4
from direct.gui.DirectGui import *
from pandac.PandaModules import GraphicsPipe, ShaderAttrib, Shader, RenderState, Texture, GraphicsOutput, FrameBufferProperties, WindowProperties
from panda3d.core import *
from pandac.PandaModules import Lens
from math import pi,sin,cos
from direct.interval.IntervalGlobal import *
import random

from globals import *

PICK_TAG = 'pickable'
FILM_SIZE = Vec2(1500,1500)
SHADOW_BIAS = Vec3(7,7,7)

class DeferredLight(NodePath):

    def __init__(self, shadows, vizparent, num, movement, buffer_system, parent, geom, vizgeom, light_type, color, pos, scale, style, attenuation, energy, Kd, Ks, follow=None, lshader_tag="Shading pass" ):
        NodePath.__init__(self, 'light')
        
        self.vizparent = vizparent        
        self.num = num
        self.movement = movement
        self.scale = scale
        self.attenuation = attenuation
        self.initial_attenuation = attenuation
        self.style = style
        self.parent = parent
        
        self.energy = energy
        
        self.shadows = shadows
         
        self.attenuation = Vec3(energy,scale,1)

        light = loader.loadModel(geom)
        light.setPos(pos)
 
        self.vizparent.setPos(pos)
         
        light.setScale(scale)

        light.reparentTo(RENDER_NODES['LIGHTS'])
        
        light.setTag(SHADER_TAGS['compute light'], "True")
        light.setShaderInput("shadows_on", Vec3(shadows,0,0))
        light.setShaderInput("random", loader.loadTexture("../assets/textures/noise_random.jpg"))

        light.setShaderInput("albedo", BUFFER_SYSTEM['main'].albedo_map)
        light.setShaderInput("depth", BUFFER_SYSTEM['main'].depth_map)
        light.setShaderInput("normal", BUFFER_SYSTEM['main'].normal_map)
        light.setShaderInput("specular", BUFFER_SYSTEM['main'].specular_map)
        light.setShaderInput("misc", BUFFER_SYSTEM['main'].misc_map)
        light.setShaderInput("shadowsource", BUFFER_SYSTEM['main'].shadow_cube)
                
        light.setShaderInput("power", energy)
        light.setShaderInput("lightradius", scale)
        
        light.setShaderInput("attrcolor", color)
                
        light.setShaderInput("cubemap", BUFFER_SYSTEM['main'].reflection_cube_texture)
                
        if(light_type == "directionnal"):
            light.setShaderInput("dirlight", Vec3(1,1,1))
        elif(light_type == "point"):
            light.setShaderInput("dirlight", Vec3(0,0,0))
                   
        light.setShaderInput("Kd", Kd)
        light.setShaderInput("Ks", Ks)
        light.setShaderInput("camera",BUFFER_SYSTEM['main'].light_cam)
        #light.setShaderInput("light", light)
        light.setShaderInput("origin", WORLD['origin'])
        light.setShaderInput("light", BUFFER_SYSTEM['main'].light_cam)
        #light.setShaderInput("a", buffer_system.depth_map_shadows)
        #light.setShaderInput("shadowcam", buffer_system.shadow_cam)
        #light.setShaderInput("push", Vec3(1,1,1))

        light.setShaderInput("attenuation_params",self.attenuation)
        
        print(self.attenuation)
        
        self.follow = follow
        
        
        taskMgr.add(self.update,"update_light"+num)

        #light.setShaderInput("strauss_params",self.smoothness, self.metalness, self.transparency)
        
        self.light = light

        if(self.style == 'dazzle_light'):
            self.dazzle_light()
            
        if(self.style == 'dazzle_strong'):
            self.dazzle_strong()
            
        if(self.style == 'horror_movie'):
            print("horror")
            self.horror_light()

    def apply_shader(self, node, shader):
        node.setShader(Shader.load(shader))
        for name, value in self.inputs.items():
            self.node.setShaderInput(name, value)
    
    def set_attenuation(self, factor):
        self.attenuation = factor 
        
    def horror_light(self):
        Sequence(
                Func(self.dazzle_light),
                Wait(random.uniform(1,2)),
                Func(self.shut_light),
                Wait(random.uniform(1,2)),
                Func(self.activate_light),
                ).loop()
        
    def dazzle_light(self):
        Sequence(
                Wait(random.uniform(0.1,0.2)),
                Func(self.set_attenuation,Vec3(random.uniform(0,10),self.initial_attenuation.y, self.initial_attenuation.z)),
                ).loop()
                    
    def dazzle_strong(self):
        Sequence(
                Wait(random.uniform(0.1,0.2)),
                Func(self.set_attenuation,Vec3(self.initial_attenuation.x,random.uniform(0,10), self.initial_attenuation.z)),
                ).loop()
        
    def activate_light(self):
        self.light.show()
        self.vizparent.show()
        
    def shut_light(self):
        self.light.hide()
        self.vizparent.hide()

    def update(self,task):
        self.light.setShaderInput("power", self.energy)
        if self.follow != None:
            self.light.setPos(self.follow.getPos(render))
        self.vizparent.setPos(self.light.getPos())
        #self.attenuation = Vec3(self.world.smoothness, self.world.metalness, self.world.quadratic)
        self.light.setPos(self.vizparent.getPos(render))
        return task.cont
        
        
        
