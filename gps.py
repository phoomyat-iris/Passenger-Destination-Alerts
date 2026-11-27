from flask import Flask, render_template, request 
from geopy.distance import geodesic

bus_stop = { 
        "Jurong East": {
            "coordinates": (1.3333800691519504, 103.74231863722021),
            "number": 1
        },
        "Clementi": {
            "coordinates": (1.309968767268852, 103.77747439304167),
            "number": 2
        },
        "SP": {
            "coordinates": (1.3113737561885968, 103.77864648204583),
            "number": 3
        },
        "Buona Vista": {
            "coordinates": (1.3066748717130419, 103.79097782557754),
            "number": 4
        },
        "Commonwealth": {
            "coordinates": (1.3042141572794765, 103.79836534941028),
            "number": 5
        },
        "Queenstown": {
            "coordinates": (1.2944989484691487, 103.80606427530621),
            "number": 6
        }
        
    }

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gps", methods=["POST"])
def receive_gps():

    data = request.get_json()

    lat  = data["lat"]
    long = data["long"]

    print("\nCurrent GPS coordinates:")
    print("Latitude:", lat)
    print("Longitude:", long)

    location = (float(lat), float(long))

    for stop_name, stop_gps in bus_stop.items():

        dist = geodesic(location, stop_gps["coordinates"])

        if dist.meters <= 25:
            print(f"\nCurrent location at: {stop_name}")
            print(f"Distance to {stop_name}: {dist.meters:.2f} m")
            print(f"Tolerance value= 25m\n")
            break

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)