import json

from netbox import NetBoxClient

nb = NetBoxClient(
    base_url="http://127.0.0.1:8000/", token="c9b7ce896053a4af79299eca0fbbe9a400747e8e"
)

data = [
    {
        "user": 2,
    },
]

# ret = nb.dcim.interfaces.update(1640, name="ti1-1")
ret = nb.users.tokens.create(user=2)
print(ret.response.status_code)
print(ret.data)
