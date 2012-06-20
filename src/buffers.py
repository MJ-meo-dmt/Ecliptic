###########################################
### Buffer system for deferred lighting ###
### 23/12/11                            ###
###########################################

from globals import *

from pandac.PandaModules import GraphicsPipe, ShaderAttrib, Shader, RenderState, Texture, GraphicsOutput, FrameBufferProperties, WindowProperties
from panda3d.core import *
from math import *

CG_NORMALMAP = "shaders/normal_map.cg"
CG_LIGHT = "shaders/def_light.cg"
SHADOW_MAP_SIZE = 512

# TODO CUSTOM SCREEN RESOLUTION

class BufferSystem():

    def __init__(self, _base):
        
        self._base = _base
        
        self._base.cam.node().setActive(0)
        
        # window properties
        self.winprops = WindowProperties.size(base.win.getXSize(),base.win.getYSize())
        self.props = FrameBufferProperties()
        self.props.setDepthBits(1)
        self.props.setColorBits(1) 
        self.props.setAlphaBits(1) 
        
        # buffers creation
        self.geom_buffer = self.make_FBO("geom buffer",3)
        self.light_buffer = self.make_FBO("light buffer",0)
        self.transparency_buffer = self.make_FBO("transparency buffer",0)
        
        # cameras creation
        self.geom_cam = self._base.makeCamera(self.geom_buffer)
        self.light_cam = self._base.makeCamera(self.light_buffer)
        self.transparency_cam = self._base.makeCamera(self.transparency_buffer)
        
        # cameras setup
        self.geom_cam.node().getDisplayRegion(0).setClearColorActive(1) 
        self.geom_cam.node().getDisplayRegion(0).setClearColor(Vec4(1,0,0,1)) 
        self.geom_cam.node().getDisplayRegion(0).setClearDepthActive(1) 
        
        self.light_cam.node().getDisplayRegion(0).setClearColorActive(1) 
        self.geom_cam.node().getDisplayRegion(0).setClearColor(Vec4(0,1,0,1)) 
        self.light_cam.node().getDisplayRegion(0).setClearDepthActive(1) 
        
        self.transparency_cam.node().getDisplayRegion(0).setClearColorActive(1) 
        self.transparency_cam.node().getDisplayRegion(0).setClearDepthActive(1) 
        
        self.geom_cam.node().getLens().setNear(0.1)
        self.light_cam.node().getLens().setNear(0.1)
        self.transparency_cam.node().getLens().setNear(0.1)
        
        self.geom_cam.node().getLens().setFov(90)
        self.light_cam.node().getLens().setFov(90)
        self._base.cam.node().getLens().setFov(90)
        self.transparency_cam.node().getLens().setFov(90)
                
        # cameras masks
        self.geom_mask = BitMask32(1)
        self.light_mask = BitMask32(2)    
        self.transparency_mask = BitMask32(4) 
        
        self.light_cam.node().setCameraMask(self.light_mask)
        self.geom_cam.node().setCameraMask(self.geom_mask)
        self.transparency_cam.node().setCameraMask(self.transparency_mask)
        
        RENDER_NODES['LIGHTS'].hide(self.geom_mask)
        RENDER_NODES['GEOMS'].hide(self.light_mask)
        RENDER_NODES['TRANSPS'].hide(self.geom_mask)
        
        # link cameras
        self.geom_cam.node().setScene(RENDER_NODES['GEOMS'])
        self.light_cam.node().setScene(RENDER_NODES['LIGHTS'])
        self.transparency_cam.node().setScene(RENDER_NODES['TRANSPS'])
        
        # buffers rendering order
        self.light_buffer.setSort(0)
        self.geom_buffer.setSort(-50)
        self.transparency_buffer.setSort(50)
        self._base.win.setSort(-100)   

        # shadows cube creation
        self.shadow_cube = RENDER_NODES['GEOMS'].attachNewNode("cubemap")
        self.shadow_cube.setPos(0, 0, 0)
        buffer_cube_shadow = self._base.win.makeCubeMap("cube 1", 512, self.shadow_cube, camera_mask = self.geom_mask, to_ram = False, fbp = self.props)
        self.shadow_cube_texture = buffer_cube_shadow.getTexture()

        cameras = []
        for camera in self.shadow_cube.getChildren():
            cameras.append(camera)
            camera.node().getLens().setFov(90)
            camera.node().getLens().setNearFar(0.1 ,10.0)
            camera.node().setCameraMask(self.geom_mask)
            cameraInit = NodePath(PandaNode("cube camera initiator"))
            cameraInit.setShader(Shader.load('shaders/point_lights_cube.sha'))
            cameraInit.setShaderInput("light2", self.shadow_cube)
            cameraInit.setShaderInput("lightCamera", camera)
            cameraInit.setShaderInput("lensFar", Vec4(camera.node().getLens().getFar()))
            cameraInit.setShaderInput("transparency", Vec4(1))
            camera.node().setInitialState(cameraInit.getState())
            
        # reflections cube creation                    
        self.reflection_cube = RENDER_NODES['GEOMS'].attachNewNode("cubemap pivot")
        self.buffer_reflection_cube = self._base.win.makeCubeMap("cube 2", 512, self.reflection_cube, camera_mask = self.geom_mask, to_ram = False, fbp = self.props)
        self.reflection_cube_texture = self.buffer_reflection_cube.getTexture()

        for camera in self.reflection_cube.getChildren():
            camera.node().getLens().setNearFar(0.1 ,500.0)

        # shader rendering normal maps
        normal_shader = ShaderAttrib.make()
        normal_shader = normal_shader.setShader(Shader.load(CG_NORMALMAP))

        # shader rendering light
        light_shader = ShaderAttrib.make()
        light_shader = light_shader.setShader(Shader.load(CG_LIGHT))
        
        # link states with cameras
        self.geom_cam.node().setTagStateKey(SHADER_TAGS['g-buffer'])
        self.geom_cam.node().setTagState("True", RenderState.make(normal_shader))
        self.light_cam.node().setTagStateKey(SHADER_TAGS['compute light'])
        self.light_cam.node().setTagState("True", RenderState.make(light_shader))
        
        # render textures creation
        self.albedo_map = Texture()
        self.normal_map = Texture()
        self.depth_map = Texture()  
        self.specular_map = Texture()
        self.misc_map = Texture()
        self.light_map = Texture()
        self.transparency_map = Texture() 
        self.transparency_depth_map = Texture()
             
        # render textures   
        self.transparency_buffer.addRenderTexture(self.transparency_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPColor)
        self.transparency_buffer.addRenderTexture(self.transparency_depth_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPDepth)
        
        self.geom_buffer.addRenderTexture(self.normal_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPColor)
        self.geom_buffer.addRenderTexture(self.depth_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPDepth)
        self.geom_buffer.addRenderTexture(self.albedo_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPAuxRgba0)      
        self.geom_buffer.addRenderTexture(self.specular_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPAuxRgba1)
        self.geom_buffer.addRenderTexture(self.misc_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPAuxRgba2)
        
        self.light_buffer.addRenderTexture(self.light_map, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPColor)  
 
        taskMgr.add(self.update,'update reflections cubemap')
    
    ## TODO move this to renderer class
    def render(self):

        RENDER_NODES['GEOMS'].setTag(SHADER_TAGS['g-buffer'], "True")
        RENDER_NODES['GEOMS'].setShaderInput("modifier",Vec3(0,0,0))
        RENDER_NODES['GEOMS'].setShaderInput('camera', base.camera)
        RENDER_NODES['GEOMS'].setShaderInput("light", BUFFER_SYSTEM['main'].shadow_cube)
        RENDER_NODES['GEOMS'].setShaderInput("light2", BUFFER_SYSTEM['main'].shadow_cube)
        RENDER_NODES['GEOMS'].setShaderInput("projDepthmap", BUFFER_SYSTEM['main'].shadow_cube_texture)
        RENDER_NODES['GEOMS'].setShaderInput("textureDims", Vec4(32))
        RENDER_NODES['GEOMS'].setShaderInput("smoothSamples", Vec4(1))
        RENDER_NODES['GEOMS'].setShaderInput("lensFar", Vec4(10))
        RENDER_NODES['GEOMS'].setShaderInput("lensNear", Vec4(0.01))
        RENDER_NODES['GEOMS'].setShaderInput("penumbra", 0.00003)
        RENDER_NODES['GEOMS'].setShaderInput("depthOffset", 0.1)
        RENDER_NODES['GEOMS'].setShaderInput("a", BUFFER_SYSTEM['main'].shadow_cube)
        
    def update(self,task):
        #self.reflection_cube.setPos(self._base.camera.getPos())
        #self.reflection_cube.setHpr(self._base.camera.getHpr())
        return task.cont

    def make_FBO(self, name, auxrgba):
        self.props.setAuxRgba(auxrgba)
        return base.graphicsEngine.makeOutput(
             self._base.pipe, name, 0,
             self.props, self.winprops,
             GraphicsPipe.BFRefuseWindow,
             self._base.win.getGsg(), self._base.win)
