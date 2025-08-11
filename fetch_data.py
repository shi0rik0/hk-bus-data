import requests
import json

TRACKED_CTB_ROUTES = [
    "798",
    "A29",
]


def fetch_kmb_data():
    # route
    response_route = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/route/")
    data_route = response_route.json()
    data_route = data_route["data"]
    data_route.sort(key=lambda x: (x["route"], x["bound"], x["service_type"]))

    with open("kmb_routes.json", "w", encoding="utf-8") as f:
        json.dump(data_route, f, indent=4, ensure_ascii=False)

    # stop
    response_stop = requests.get("https://data.etabus.gov.hk/v1/transport/kmb/stop/")
    data_stop = response_stop.json()
    data_stop = data_stop["data"]
    data_stop.sort(key=lambda x: x["stop"])

    with open("kmb_stops.json", "w", encoding="utf-8") as f:
        json.dump(data_stop, f, indent=4, ensure_ascii=False)

    # route-stop
    response_route_stop = requests.get(
        "https://data.etabus.gov.hk/v1/transport/kmb/route-stop"
    )
    data_route_stop = response_route_stop.json()
    data_route_stop = data_route_stop["data"]
    data_route_stop.sort(
        key=lambda x: (x["route"], x["bound"], x["service_type"], int(x["seq"]))
    )

    with open("kmb_route_stops.json", "w", encoding="utf-8") as f:
        json.dump(data_route_stop, f, indent=4, ensure_ascii=False)

    # route-stop-ex
    for i in data_route_stop:
        i["stop_name_tc"] = next(
            (j["name_tc"] for j in data_stop if j["stop"] == i["stop"]), None
        )

    with open("kmb_route_stops_ex.json", "w", encoding="utf-8") as f:
        json.dump(data_route_stop, f, indent=4, ensure_ascii=False)


def fetch_ctb_data():
    # route
    response_route = requests.get(
        "https://rt.data.gov.hk/v2/transport/citybus/route/CTB"
    )
    data_route = response_route.json()
    data_route = data_route["data"]
    data_route.sort(key=lambda x: x["route"])

    with open("ctb_routes.json", "w", encoding="utf-8") as f:
        json.dump(data_route, f, indent=4, ensure_ascii=False)

    # route-stop
    data_route_stop = []
    for route in TRACKED_CTB_ROUTES:
        for dir in ["inbound", "outbound"]:
            response_route_stop = requests.get(
                f"https://rt.data.gov.hk/v2/transport/citybus/route-stop/CTB/{route}/{dir}"
            )
            data = response_route_stop.json()
            data_route_stop.extend(data["data"])
    stops = set(i["stop"] for i in data_route_stop)
    stop_names = {}
    for stop in stops:
        response_stop = requests.get(
            f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop}"
        )
        data = response_stop.json()
        stop_names[stop] = data["data"]["name_tc"]
    for i in data_route_stop:
        i["stop_name_tc"] = stop_names[i["stop"]]
        del i["data_timestamp"]
    data_route_stop.sort(key=lambda x: (x["route"], x["dir"], int(x["seq"])))

    with open("ctb_route_stops.json", "w", encoding="utf-8") as f:
        json.dump(data_route_stop, f, indent=4, ensure_ascii=False)


fetch_kmb_data()
fetch_ctb_data()
