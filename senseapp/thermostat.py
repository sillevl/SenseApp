
class Thermostat:
    
    def __init__(self, wanted_temperature, range=25):
        self.wanted_tempeature = wanted_temperature
        self.range = range

    def update(self, temperature):
        self.temperature = temperature
        return {
            "heating": self.is_heating(),
            "cooling": self.is_cooling()
        }

    def is_heating(self):
        return self.temperature < self.wanted_tempeature - self.range / 2

    def is_cooling(self):
        return self.temperature > self.wanted_tempeature + self.range / 2