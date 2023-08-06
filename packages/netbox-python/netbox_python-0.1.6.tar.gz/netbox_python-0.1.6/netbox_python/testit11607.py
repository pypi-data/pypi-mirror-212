import requests

payload = [{"id": 28, "custom_fields": {"cable": {"id": 59}}}]
headers = {
    "Authorization": "Token bd316de5adff1f3cd1d2e28bb0a326ff72d0b318",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
r = requests.patch(
    "http://127.0.0.1:8000/api/circuits/circuits/", json=payload, headers=headers
)
print(r.status_code)
