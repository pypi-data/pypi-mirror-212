import json

from netbox import NetBoxClient

nb = NetBoxClient(
    base_url="http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
)

data = [
    {
        "device_role": 1,
        "device_type": 6,
        "site": 24,
        "rack": 39,
        "face": "front",
        "position": 11,
    },
    {
        "device_role": 1,
        "device_type": 6,
        "site": 24,
        "rack": 39,
        "face": "front",
        "position": 12,
    },
]


ret = nb.dcim.devices.create(data)
print(ret.response.status_code)
print(ret.response.text)
print(ret.data)
