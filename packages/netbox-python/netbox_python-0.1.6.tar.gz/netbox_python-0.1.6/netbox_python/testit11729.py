import json

from netbox import NetBoxClient

nb = NetBoxClient(
    base_url="http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
)

data = [
    {
        "device": 124,
    },
]
data = [
    {
        "name": "ti1-1",
    },
]

# ret = nb.dcim.interfaces.update(1640, name="ti1-1")
ret = nb.ipam.prefixes dcim.interfaces.update(1640, device=124)
# ret = nb.dcim.interfaces.update(1640, device=123)
print(ret.response.status_code)
print(ret.data)
