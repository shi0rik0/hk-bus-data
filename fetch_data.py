import requests
import json

response = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/route/")
data_route = response.json()
data_route = data_route["data"]
data_route.sort(key=lambda x: (x["route"], x["bound"], x["service_type"]))

with open("kmb_routes.json", "w", encoding="utf-8") as f:
    json.dump(data_route, f, indent=4, ensure_ascii=False)

response = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/stop/")
data_stop = response.json()
data_stop = data_stop["data"]
data_stop.sort(key=lambda x: x["stop"])

with open("kmb_stops.json", "w", encoding="utf-8") as f:
    json.dump(data_stop, f, indent=4, ensure_ascii=False)

response = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/route-stop")
data_route_stop = response.json()

data_route_stop = data_route_stop["data"]
data_route_stop.sort(
    key=lambda x: (x["route"], x["bound"], x["service_type"], int(x["seq"]))
)

with open("kmb_route_stops.json", "w", encoding="utf-8") as f:
    json.dump(data_route_stop, f, indent=4, ensure_ascii=False)

for i in data_route_stop:
    i["stop_name_tc"] = next(
        (j["name_tc"] for j in data_stop if j["stop"] == i["stop"]), None
    )

with open("kmb_route_stops_ex.json", "w", encoding="utf-8") as f:
    json.dump(data_route_stop, f, indent=4, ensure_ascii=False)
