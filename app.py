from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)

@app.route("/api/track", methods=["POST"])
def track_number():
    data = request.get_json()
    number = data.get("phone")

    if not number:
        return jsonify({"error": "Phone number is required"}), 400

    try:
        parsed = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed, "en")
        operator = carrier.name_for_number(parsed, "en")

        return jsonify({
            "number": number,
            "location": location,
            "carrier": operator
        })
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return jsonify({"error": "Invalid number or failed to parse"}), 500

if __name__ == "__main__":
    app.run(debug=True)

