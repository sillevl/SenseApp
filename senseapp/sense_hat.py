from sense_hat import SenseHat as PiSenseHat

class SenseHat:

    hat = None
    settings = None
    
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
        self.hat.show_message(text, text_colour=color, scroll_speed=speed)

    def update_rotation(self, value):
        self.hat.rotation = value
    
    def update_low_light(self, value):
        self.hat.low_light = value