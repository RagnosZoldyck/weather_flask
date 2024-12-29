from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "7f2250971fc96adc34d3f69b42bcfeb0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Route for the main website
@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # Fetch weather data from OpenWeatherMap API
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                weather_data = {"error": "City not found"}
    return render_template("index.html", weather=weather_data)

# API to fetch weather data (can be consumed by the website or other clients)
@app.route("/api/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "City not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

