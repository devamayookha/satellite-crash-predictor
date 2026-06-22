from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

from risk_logic import assess_risk

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    result = assess_risk(
        altitude_obj1_km=float(data["altitude1"]),
        altitude_obj2_km=float(data["altitude2"]),
        relative_velocity_kms=float(data["velocity"]),
        miss_distance_km=float(data["miss_distance"]),
        object_size_category=data["size_category"],
        time_to_closest_approach_hours=float(data["time_to_approach"]),
    )

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)