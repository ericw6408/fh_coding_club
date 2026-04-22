import machine
from time import sleep as delay



# class to handle joystick positions

class Joystick():
    def __init__(self,pinx:machine.ADC,piny:machine.ADC):
        initialx = pinx.read_u16()
        initialy = piny.read_u16()
        
        initialx /= (65536/100) # offset is as a pct
        initialy /= (65536/100)
        
        self.x_offset = (50 - round(initialx,2))
        self.y_offset = (50 - round(initialy,2))
        self.x_pin = pinx
        self.y_pin = piny
        
    def get_pos(self)->list:
        # returns a list of [x_pct,y_pct] AFTER applying the offset.
        
        # since read_u16 returns a linearly scaling value from 0 to 100, then:
        x_pct = round(((self.x_pin.read_u16() / 65536) * 100) + self.x_offset,2)
        
        y_pct = round(((self.y_pin.read_u16() / 65536) * 100) + self.y_offset,2)
        
        return (x_pct,y_pct)
    
    def get_x(self):
        return round(((self.x_pin.read_u16() * 100) / 65536) + self.x_offset,2)

    def get_y(self):
        return round(((self.y_pin.read_u16() * 100) / 65536) + self.y_offset,2)

