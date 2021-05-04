# SenseAPP

Turn your Raspberry Pi into an IoT device using the Raspberry Pi Sense Hat and this project.

## API

Socket connection `/tmp/senseapp.sock`

### Sensor value updates

Every time new sensorvalues are availabe, updates will automatically be send to all clients.

```json
{
  "sensor_values": {
    "humidity": 27.164823532104492,
    "temperature": 36.82665252685547,
    "pressure": 1035.015625
  }
}
```

### Get information

#### Version

To get the systeminformation you need to send the a `get` message to the application, containing an array of the wanted values

```json
{
    "get": ["version"]
}
```

#### Current settings

In order to get the current settings, the following request can be send to the application.

```json
{
    "get": ["settings"]
}
```

### Update settings

To update settings, you can send a `post` message containing one or more settings to be updated.

```json
{
  "post": { 
      "settings": { 
          "brightness": 255,
          "low_light": true,
          "rotation": 90
       }
    }
}
```

## Default settings

These are the default settings. All settings can be updated using the API.

```json
{
    "wanted_temperature": 36.0,
    "wanted_temperature_range": 1.0,
    "brightness": 255,
    "low_light": false,
    "display_speed": 0.075,
    "rotation": 180
}
```
