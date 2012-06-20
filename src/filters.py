###########################################
### Filter system for deferred lighting ###
### 12/23/11 original                   ###
### 01/21/12 updated                    ###
### 05/18/12 ecliptic space version     ###
###########################################

from pandac.PandaModules import *
from panda3d.core import *
from direct.filter.FilterManager import *
from direct.gui.DirectGui import *

from globals import *

# TODO -70 fps with filters

FAR_CLIP = 50000
NEAR_CLIP = 10

FOG_COLOR = Vec4(0,0,0,1)
FOG_POWER = Vec4(.1,.1,1,1) # (red, blue, gray, extinguish)

BLOOM = False
COLOR_CORRECTION = True
DOF = False
FOG = False
FXAA = False
PARTICLES  = False
SSAO = False

CASTER_POS = Vec3(-0,-1000,-500)
VL_BLUR = 8
VL_CLEAR_COLOR = Vec4(0.7, 0.6, 0.5, 1)
VL_PARAMS = (64,  1/32.0, .99, .99)

class FilterSystem():

    def __init__(self, _base, world, buffer_system):
        
        self.power = Vec3(1,1,0)
        
        self.world = world
        self._base = _base
        
        #self.activate_gui()
        
        self.bias2 = 1
        
        self.blur = 0.5
        self.aperture = 0.1
        self.focus = 0.5
        self.near = 0.1
        self.far = 0.8
        self.focal = 0.5
        self.exposure = 0.5
        self.bloomfactor = 0.1
        
        self.bool_fxaa = 0
        self.last_map = None
        
        self.filterMan = FilterManager(base.win, base.cam)
        self.card = CardMaker('Compositing quad')
        self.card.setFrameFullscreenQuad()
        self.finalQuad = render2d.attachNewNode(self.card.generate())
        
        
        self.resolution_x = 1024
        self.resolution_y = 768
        self.make_initial_pass()
        
        self.original_map = buffer_system.light_map
        self.last_map = self.original_map
        
        # Particles pass
        if(PARTICLES):
            particles_comp_map = Texture()
            quad = self.filterMan.renderQuadInto(colortex = particles_comp_map)
            quad.setShader(loader.loadShader("particles_comp.cg"))
            quad.setShaderInput("color", self.last_map)
            #quad.setShaderInput("camera", self.world.buffer_system.transparency_cam )
            quad.setShaderInput("particles", buffer_system.transparency_map)
            quad.setShaderInput("particles_depth", buffer_system.transparency_depth_map)
            quad.setShaderInput("scene_depth", buffer_system.depth_map)
            self.last_map = particles_comp_map
        
        
            
            
        # Linearize depth pass
        if(DOF or COLOR_CORRECTION):
            self.lineardepth_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = self.lineardepth_map)
            quad.setShader(loader.loadShader("shaders/depth_linear.cg"))
            quad.setShaderInput("depthnonlinear", buffer_system.depth_map)
            quad.setShaderInput("clipplanes", Vec3(NEAR_CLIP,FAR_CLIP,0))
            quad.setShaderInput("camera", buffer_system.light_cam)
            self.lindepthmap = quad
                        
        # Bloom filter
        if(BLOOM):
            # Create emit map
            emit_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = emit_map)
            quad.setShader(loader.loadShader("shaders/create_emit.cg"))
            quad.setShaderInput("emitmap", buffer_system.misc_map)
            quad.setShaderInput("albedomap", buffer_system.albedo_map)
            # Horizontal blur pass
            hblur_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = hblur_map)
            quad.setShader(loader.loadShader("shaders/hblur.cg"))
            quad.setShaderInput("color", emit_map)
            # Vertical blur pass
            vblur_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = vblur_map)
            quad.setShader(loader.loadShader("shaders/vblur.cg"))
            quad.setShaderInput("color", hblur_map)
            # Bloom pass
            hdr_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = hdr_map)
            quad.setShader(loader.loadShader("shaders/hdr.cg"))
            quad.setShaderInput("color", self.last_map)
            quad.setShaderInput("bloom_map", vblur_map)
            quad.setShaderInput("hdr_params", Vec3(0.5,0.5,0))
            self.hdr = quad
            self.last_map = hdr_map
            
        # DOF filter
        if(DOF):
            dof_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = dof_map)
            quad.setShader(loader.loadShader("shaders/dof.cg"))
            quad.setShaderInput("color", self.last_map)
            quad.setShaderInput("depth", buffer_system.depth_map)
            quad.setShaderInput("preblurmap", self.last_map)
            quad.setShaderInput("camera", buffer_system.light_cam)
            quad.setShaderInput("clipplanes", Vec3(50,500,0))
            self.dof = quad
            self.last_map = dof_map
        
        # Color perspective filter # 
        if(COLOR_CORRECTION):
            colpersp_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = colpersp_map)
            quad.setShader(loader.loadShader("shaders/col_persp.cg"))
            quad.setShaderInput("lineardepth", self.lineardepth_map)        
            quad.setShaderInput("originalmap", self.last_map)        
            quad.setShaderInput("fogcolor", FOG_COLOR)        
            quad.setShaderInput("power", FOG_POWER)   
            self.last_map = colpersp_map 
        
        # FXAA filter
        if(FXAA):
            self.fxaa_map = Texture()
            quad = self.filterMan.renderQuadInto(div=1,mul=1,align=1,colortex = self.fxaa_map)
            quad.setShader(loader.loadShader("shaders/fxaa.cg"))
            quad.setShaderInput("color", self.last_map)
            self.last_map = self.fxaa_map
               
        self.make_final_pass() 
        taskMgr.add(self.update,"update")
        
    def make_initial_pass(self):
        self.map_A = Texture()
        self.map_B = Texture()
                
    def make_final_pass(self):
        self.finalQuad.setShader(loader.loadShader("composite.cg"))
        self.finalQuad.setShaderInput("mapA", self.last_map) 
        self.finalQuad.setShaderInput("mapB", self.last_map) 
        self.finalQuad.setShaderInput("power", self.power)
            
    #def setBias(self): self.bias2 = self.bias_slider['value']
    def setAperture(self): self.aperture = self.aperture_slider['value']
    def setBlur(self): self.blur = self.blur_slider['value']
    def setFocus(self): self.focus = self.focus_slider['value']
    def setExposure(self): self.exposure = self.exposure_slider['value']
    def setBloomfactor(self): self.bloomfactor = self.bloomfactor_slider['value']
    def setBrightmax(self): self.world.brightmax = self.brightmax_slider['value']
    def setNear(self): self.near = self.near_slider['value']
    def setFar(self): self.far = self.far_slider['value']
    def setFocal(self): self.focal = self.focal_slider['value']
    def setFxaa(self,status):
        if status:
            self.bool_fxaa = 1
        else:
            self.bool_fxaa = 0
    def update(self, task):
        RENDER_NODES['LIGHTS'].setShaderInput("dofparams", Vec4(self.near,self.focal,self.far, self.blur))
        #print(self.blur)
        if(DOF):
            self.dof.setShaderInput("params", Vec3(self.exposure,self.aperture,self.focus))
            self.dof.setShaderInput("resolution", Vec3(1024, 768,0))
        if(DOF or COLOR_CORRECTION):
            self.lindepthmap.setShaderInput("dofparams", Vec4(self.near,self.focal,self.far, self.blur))
        if(BLOOM):
            self.hdr.setShaderInput("hdr_params", Vec3(0.5,0.5,0))
        return task.cont
    
    ### GUI tout pourri ###
    def activate_gui(self):
        self.near_slider = DirectSlider(range = (0,1), value = 0.1, pageSize=0.1, text = "shadows", text_scale = 0.1,command = self.setNear)
        self.near_slider.setPos(0.7,0,0.9)
        self.near_slider.setScale(0.5)
        self.focal_slider = DirectSlider(range = (0,10), value = 0.5, pageSize=0.1, text = "ambiant", text_scale = 0.1,command = self.setFocal)
        self.focal_slider.setPos(0.7,0,0.7)
        self.focal_slider.setScale(0.5)
        self.far_slider = DirectSlider(range = (0,1), value = 0.8, pageSize=0.1, text = "ward", text_scale = 0.1,command = self.setFar)
        self.far_slider.setPos(0.7,0,0.5)
        self.far_slider.setScale(0.5)
        
        self.blur_slider = DirectSlider(range = (0,1), value = 0.1, pageSize=0.1, text = "reflection", text_scale = 0.1,command = self.setBlur)
        self.blur_slider.setPos(-0.7,0,0.9)
        self.blur_slider.setScale(0.5)
        
        self.aperture_slider = DirectSlider(range = (0,1), value = 0.2, pageSize=0.1, text = "aperture", text_scale = 0.1,command = self.setAperture)
        self.aperture_slider.setPos(-0.7,0,0.8)
        self.aperture_slider.setScale(0.5)

        self.focus_slider = DirectSlider(range = (0,1), value = 0, pageSize=0.1, text = "focus", text_scale = 0.1,command = self.setFocus)
        self.focus_slider.setPos(-0.7,0,0.6)
        self.focus_slider.setScale(0.5)

        self.exposure_slider = DirectSlider(range = (0.0,0.5), value = 0.8, pageSize=0.1, text = "blur", text_scale = 0.1,command = self.setExposure)
        self.exposure_slider.setPos(-0.7,0,0.4)
        self.exposure_slider.setScale(0.5)

        self.bloomfactor_slider = DirectSlider(range = (0.0,5), value = 0.1, pageSize=0.1, text = "bloomfactor", text_scale = 0.1,command = self.setBloomfactor)
        self.bloomfactor_slider.setPos(-0.7,0,0.2)
        self.bloomfactor_slider.setScale(0.5)

        self.brightmax_slider = DirectSlider(range = (0.000002,1), value = 0, pageSize=0.1, text = "bias", text_scale = 0.1,command = self.setBrightmax)
        self.brightmax_slider.setPos(-0.7,0,0.0)
        self.brightmax_slider.setScale(0.5)
        
        b = DirectCheckButton(text = "Fxaa" ,scale=.05,command=self.setFxaa)
        b.setPos(-1.0,-1.0,-0.6)
        
        self.a = self.aperture_slider
        self.b = self.focus_slider
        self.c = self.exposure_slider
        self.d = self.bloomfactor_slider
        self.e = self.brightmax_slider
        self.i = self.blur_slider
        self.j = b
        
        #self.k = self.bias_slider
        self.sliders_list = [self.near_slider, self.focal_slider, self.far_slider, self.blur_slider, self.aperture_slider, self.focus_slider, self.exposure_slider, self.bloomfactor_slider, self.brightmax_slider, b]
