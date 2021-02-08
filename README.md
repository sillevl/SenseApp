# SenseAPP

Turn your Raspberry Pi into an IoT device using the Raspberry Pi Sense Hat and this project.

## API

Socket connection `/tmp/senseapp.sock`

### Sensor value updates

Every time new sensorvalues are availabe, updates will automatically be send to all clients.

```json
{
    "humidity": 22.098386764526367,
    "temperature": 38.38396453857422,
    "pressure": 1008.396728515625
}
```

### Get information

#### System info

To get the systeminformation you need to send the a `get` message to the application, containing an array of the wanted values

```json
{
    "get": ["system_info"]
}
```

#### Current settings

In order to get the current settings, the following request can be send to the application.

```json
{
    "get": ["settings"]
}
```

#### Combining requests

You can combine multiple information requests in a single request. The responses will be send sepparatly.

```json
{
    "get": ["settings", "system_info"]
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
