import json

from netbox import NetBoxClient

nb = NetBoxClient(
    # base_url="http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
    base_url="http://127.0.0.1:8000/",
    token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318",
)

# ret = nb.dcim.sites.all()
# ret = nb.ipam.prefixes.all()
# print(json.dumps(ret.data, indent=4))
# ret = nb.ipam.ip_addresses.all()
# print(json.dumps(ret.data, indent=4))

# ret = nb.ipam.ip_range.available_ips.list(1)
# print(json.dumps(ret.data, indent=4))

# ret = nb.circuits.circuit_terminations.all()
ret = nb.dcim.interfaces.update(1624, type="40gbase-x-qsfpp")
# ret = nb.ipam.ip_ranges.update(1, start_address='192.168.4.10/24', end_address='192.168.4.50/24')
# ret = nb.ipam.ip_ranges.update(1, start_address='aaaaa', end_address='192.168.4.50/24')
print(json.dumps(ret.data, indent=4))

# b_terminations = [{"object_type": "dcim.interface", "object_id": 1639}]
#
# ret = nb.dcim.cables.update(133, b_terminations=b_terminations)
# print(ret)
