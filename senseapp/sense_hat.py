from sense_hat import SenseHat as PiSenseHat

class SenseHat:

    hat = None
    settings = None
    display_bussy = False
    
    def __init__(self, settings):
        self.settings = settings
        self.hat = PiSenseHat()
        self.update_rotation(settings.get("rotation"))
        self.update_low_light(settings.get("low_light"))

    def get_sensor_values(self):
        return  {
            "humidity": self.hat.get_humidity(),
            "temperature": self.hat.get_temperature(),
            "pressure": self.hat.get_pressure()
        }
    
    def display(self, text, color = None, speed = None):
        if not color: color = [255, 255, 255]
        if not speed: speed = self.settings.get("display_speed")
        self.display_bussy = True
        self.hat.show_message(text, text_colour=color, scroll_speed=speed)
        self.display_bussy = False
        self.update_rotation(self.settings.get("rotation"))

    def update_rotation(self, value):
        # Don't update the rotation while 'show_message' is active. It buffers the rotation and resets it to the bufferd value when done...
        # https://github.com/astro-pi/python-sense-hat/blob/9a37f0923ce8dbde69514c3b8d58d30de01c9ee7/sense_hat/sense_hat.py#L466
        if(not self.display_bussy):  
            self.hat.set_rotation(value, False)
    
    def update_low_light(self, value):
        self.hat.low_light = value