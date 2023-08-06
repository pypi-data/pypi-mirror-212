import json

import pynetbox
from netbox import NetBoxClient

nbpy = pynetbox.api(
    "http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
)
nb = NetBoxClient(
    # base_url="http://127.0.0.1:8000/", token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318"
    base_url="http://127.0.0.1:8000/",
    token="bd316de5adff1f3cd1d2e28bb0a326ff72d0b318",
)

site = nbpy.dcim.sites.create(
    name="test", slug="test", status="active", custom_fields={"cfsitetest": "ttt"}
)
# ret = nb.dcim.sites.update(24, custom_fields={"cfsitetest": "ttt", })
# print(json.dumps(ret.data, indent=4))
