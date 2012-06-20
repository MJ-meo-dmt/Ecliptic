# Event component:
# Add to the GameObject Class depending on type.

from globals import *

class SensorEvent():
    
    pass 
    
class DoorEvent():
    
    pass 
    
class PlayerEvent():
    
    pass 

class TriggerEvent():
    
    pass 
    
class LightEvent():
    
    pass
    
class ItemEvent():
    
    pass 
    
class ScreenEvent():
    
    pass 
    
class ParticleEvent():
    
    pass 
    
class SuitEvent():
    
    pass 
    

EVENT['SENSOR'] = SensorEvent()
EVENT['DOOR'] = DoorEvent()
EVENT['PLAYER'] = PlayerEvent()
EVENT['TRIGGER'] = TriggerEvent()
EVENT['LIGHT'] = LightEvent()
EVENT['ITEM'] = ItemEvent()
EVENT['SCREEN'] = ScreenEvent()
EVENT['PARTICLES'] = ParticleEvent()
EVENT['SUIT'] = SuitEvent()


