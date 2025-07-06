from flask import Flask, request, jsonify, render_template
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/locate', methods=['POST'])
def locate_number():
    data = request.json
    number = data.get("number")

    try:
        parsed_number = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed_number, 'en')
        operator = carrier.name_for_number(parsed_number, 'en')
        timezones = timezone.time_zones_for_number(parsed_number)

        return jsonify({
            "success": True,
            "location": location,
            "carrier": operator,
            "timezones": list(timezones)
        })

    except:
        return jsonify({"success": False, "message": "Invalid number"}), 400

if __name__ == '__main__':
    app.run()
