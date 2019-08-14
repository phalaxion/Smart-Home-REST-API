# Device Registry Service

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all devices

**Definitions**

`GET /devices`

**Response**

- `200 OK` on success

```json
[
    {
        "identifier": "ceiling-light",
        "name": "Ceiling Light",
        "device_type": "switch",
        "controller_gateway": "192.168.0.2"
    },
    {
        "identifier": "air-conditioner",
        "name": "Air Conditioner",
        "device_type": "aircon",
        "controller_gateway": "192.168.0.2"
    }
]
```

### Registering

**Definition**

`POST /devices`

**Arguements**

- `"identifier":string` a globally unique identifier for this device
- `"name":string` a human friendly name for this device
- `"device_type":string` the type of device as understood by the user
- `"controller_gateway":string` the IP address of the device's controller

If a device with the given identifier already exists, the existing deivce will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "identifier": "ceiling-light",
    "name": "Ceiling Light",
    "device_type": "switch",
    "controller_gateway": "192.168.0.2"
}
```

## Lookup device details

`GET /devices/<identifer>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "identifier": "ceiling-light",
    "name": "Ceiling Light",
    "device_type": "switch",
    "controller_gateway": "192.168.0.2"
}
```

## Delete a device

**Definition**

`DELETE /devices/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `204 No Content` delete happened successfully
