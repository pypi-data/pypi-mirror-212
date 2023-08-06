import json

from netbox import NetBoxClient

nb = NetBoxClient(
    base_url="http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
)

group_id = 2
while group_id < 60:
    ret = nb.ipam.fhrp_groups.create(protocol="vrrp2", group_id=group_id)
    group_id += 1

print(ret.response.status_code)
print(ret.data)
