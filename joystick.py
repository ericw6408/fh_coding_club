import machine
from time import sleep as delay



# class to handle joystick positions

class Joystick():
    def __init__(self,pinx:machine.ADC,piny:machine.ADC,invertX = False, invertY = False):
        self.inverts = [invertX,invertY]
        initialx = pinx.read_u16()
        initialy = piny.read_u16()
        
        initialx /= (65536/100) # offset is as a pct
        initialy /= (65536/100)
        self.x_offset = 0
        self.y_offset = 0
        if self.inverts[0]:
            self.x_offset = round(initialx,2)
        else:
            self.x_offset = (50 - round(initialx,2)) 
        
        if self.inverts[1]:
            self.y_offset = round(initialy,2)
        else:
            self.x_offset = (50 - round(initialy,2))
        
        
        self.x_pin = pinx
        self.y_pin = piny
        
    
    def get_x(self):
        if self.inverts[0]:
            return 100 - round(((self.x_pin.read_u16() * 100) / 65536) + self.x_offset,2)
        else:
            return round(((self.x_pin.read_u16() * 100) / 65536) + self.x_offset,2)
    def get_y(self):
        if self.inverts[1]:
            return 100 - round(((self.y_pin.read_u16() * 100) / 65536) + self.y_offset,2)
        else:
            return round(((self.y_pin.read_u16() * 100) / 65536) + self.y_offset,2)
    
    def get_pos(self)->list:
        # returns a list of [x_pct,y_pct] AFTER applying the offset.
        
        # since read_u16 returns a linearly scaling value from 0 to 100, then:
        return [get_x(),get_y()]    
