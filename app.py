from flask import Flask, request, jsonify
from flask_cors import CORS
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "c32672cb0b9744b3830720673eea690e"

@app.route("/", methods=["POST"])
def index():
    # Support JSON and form-data
    number = request.json.get("phone") if request.is_json else request.form.get("phone")

    if not number:
        return jsonify({"error": "Missing 'phone' field"}), 400

    try:
        parsed_number = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        region_code = phonenumbers.region_code_for_number(parsed_number)
        query_location = f"{location}, {region_code}"

        geocoder_api = OpenCageGeocode(API_KEY)
        results = geocoder_api.geocode(query_location)

        if results and len(results):
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            return jsonify({
                "number": number,
                "location": location,
                "carrier": carrier_name,
                "latitude": lat,
                "longitude": lng
            })

        return jsonify({"error": "Location not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Invalid phone number or API issue: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
