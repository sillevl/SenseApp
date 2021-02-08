#!/usr/bin/python3
 
from sense_hat import SenseHat
import time
import threading
import socket,os
import json
import os.path

VERSION = "0.1.0"

READ_SENSORS_INTERVAL = 1.0

socket_file_path = "/tmp/senseapp"
settings_file = "/etc/sense-app/settings.json"

# application settings
default_settings = {
    "wanted_temperature": 36.0,
    "wanted_temperature_range": 1.0,
    "brightness": 255,
    "low_light": True,
    "display_speed": 0.075,
    "rotation": 180
}

sensor_values = None
settings = None

def main():
    print("*** SenseApp ***")
    global settings
    settings = read_settings()
    save_settings(settings)

    sense = getSense()

    read_sensor_thread = threading.Thread( target=read_sensor_values, args=(sense, ) )
    display_temperature_thread = threading.Thread( target=display_temperature, args=(sense, ))
    ipc_thread = threading.Thread( target=ipc, args=())

    read_sensor_thread.start()
    display_temperature_thread.start()
    ipc_thread.start()
    while True:
        pass

def getSense():
    sense = SenseHat()
    sense.rotation = settings["rotation"]
    sense.low_light = settings["low_light"]
    return sense

def read_sensor_values(sense):
    global sensor_values
    print("Reading sensor values")
    while True:
        # print("Read sensor values")
        values = {
            "humidity": sense.get_humidity(),
            "temperature": sense.get_temperature(),
            "pressure": sense.get_pressure()
        }
        print_sensor_values(values)
        sensor_values = values
        time.sleep(READ_SENSORS_INTERVAL)

def print_sensor_values(sensor_values):
    print("Pressure:    %s Millibars" % "{:2.1f}".format(sensor_values["pressure"]))
    print("Temperature: %s C" % "{:2.1f}".format(sensor_values["temperature"]))
    print("Humidity:    %s %%rH" % "{:2.1f}".format(sensor_values["humidity"]))

def display_temperature(sense):
    global sensor_values
    while True:
        if sensor_values:
            # Print values on led display 
            color = [0,settings["brightness"], 0]
            if sensor_values["temperature"] < settings["wanted_temperature"] - settings["wanted_temperature_range"] / 2:
                color = [0, 0, settings["brightness"]]
            elif sensor_values["temperature"] > settings["wanted_temperature"] + settings["wanted_temperature_range"] / 2:
                color = [settings["brightness"], 0, 0]
            sense.show_message("{:2.1f}C".format(sensor_values["temperature"]), text_colour=color, scroll_speed=settings["display_speed"])

        # sleep for a little bit
        time.sleep(1)

def ipc():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove(socket_file_path)
    except OSError:
        pass
    s.bind(socket_file_path)
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        if not data: break
        message = json.loads(data.decode("utf-8"))
        print(message)
        if "wanted_temperature" in message:
            set_wanted_temperature(message["wanted_temperature"])
        if "wanted_tempeature_range" in message:
            set_wanted_temperature_range(message["wanted_tempeature_range"])
        if "brightness" in message:
            set_brightness(message["brightness"])
        if "low_light" in message:
            set_low_light(message["low_light"])
        if "display_speed" in message:
            set_display_speed(message["display_speed"])
        if "rotation" in message:
            set_rotation(message["rotation"])
        # conn.send(data)
    conn.close()

def set_brightness(brightness):
    global settings
    settings["brightness"] = brightness
    save_settings(settings)

def set_wanted_temperature(temperature):
    global settings
    settings["wanted_temperature"] = temperature
    save_settings(settings)

def set_wanted_temperature_range(wanted_temperature_range):
    global settings
    settings["wanted_temperature_range"] = wanted_temperature_range
    save_settings(settings)

def set_low_light(low_light):
    global settings
    settings["low_light"] = low_light
    save_settings(settings)

def set_display_speed(display_speed):
    global settings
    settings["display_speed"] = display_speed
    save_settings(settings)

def set_rotation(rotation):
    global settings
    settings["rotation"] = rotation
    save_settings(settings)

def save_settings(settings):
    with open(settings_file, 'w') as outfile:
        json.dump(settings, outfile, indent=2)

def read_settings():
    global default_settings
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as outfile:
            json.dump(default_settings, outfile, indent=2)
    with open(settings_file) as json_file:
        data = json.load(json_file)
        settings = { **default_settings, **data }
        return settings

if __name__ == "__main__":
    main()
