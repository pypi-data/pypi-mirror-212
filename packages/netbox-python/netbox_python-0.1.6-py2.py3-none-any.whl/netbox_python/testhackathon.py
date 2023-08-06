import json

from netbox import NetBoxClient

nb = NetBoxClient(
    base_url="https://richtest2.cloud.netboxapp.com/",
    token="bcc217a54d6cc3555f8bfac4585d62f57896e7a0",
)

# nb = NetBoxClient(
#     base_url="http://127.0.0.1:8000/", token="bcc217a54d6cc3555f8bfac4585d62f57896e7a0"
# )

ret = nb.dcim.devices.render_config(107)

print(f"status code: {ret.response.status_code}")
print(json.dumps(ret.data, indent=4))
print("\n--- content ---\n")
print(ret.data["content"])
