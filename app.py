from flask import Flask, request, Response, jsonify, send_from_directory
import requests, os

app = Flask(__name__, static_folder="static")

def get_ip_info(ip):
    """Fetch IP geolocation data from ipinfo.io"""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        location = data.get("loc", "0,0")  # Latitude, Longitude
        city = data.get("city", "Unknown City")
        country = data.get("country", "Unknown Country")
        return location, city, country
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return "0,0", "Unknown City", "Unknown Country"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

@app.route("/", methods=["GET"])
def get_ip():
    headers = request.headers
    # Smart IPv4 detection (works inside Docker & behind proxy)
    ipv4 = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    location, city, country = get_ip_info(ipv4)
    user_agent = headers.get("User-Agent", "").lower()
    is_curl = "curl" in user_agent
    if not is_curl:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="robots" content="noindex, nofollow">
            <title>Gustavo Migliorini Arruda IP checker</title>
            <link rel="stylesheet" href="/static/leaflet.css" />
            <script src="/static/leaflet.js"></script>
        </head>
        <body>
            <h1>Gustavo Migliorini Arruda IP checker</h1>
            <p>Your IPv4: {ipv4 or 'NO_IPv4'}</p>
            <p><strong>Location:</strong> {city}, {country}</p>
            <p>Your IPv6: <span id="ipv6_label">Click the button to check</span></p>
            <button onclick="fetchIPv6()">Get IPv6</button>
            <h2>Your IP Location on the Map</h2>
            <div id="map" style="height: 400px;"></div>
            <script>
                function fetchIPv6() {{
                    fetch("https://api64.ipify.org?format=json")
                    .then(response => response.json())
                    .then(data => {{
                        if (data.ip.includes(".")) {{ // If response contains IPv4
                            document.getElementById("ipv6_label").textContent = "No IPv6";
                        }} else {{
                            document.getElementById("ipv6_label").textContent = data.ip;
                        }}
                    }})
                    .catch(error => {{
                        console.error("Error fetching IPv6:", error);
                        document.getElementById("ipv6_label").textContent = "Failed to get IPv6";
                    }});
                }}
                var map = L.map('map').setView([{location}], 10);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);
                L.marker([{location}]).addTo(map)
                    .bindPopup("Your Location: {city}, {country}")
                    .openPopup();
            </script>
        </body>
        </html>
        """
        return Response(html_content, mimetype="text/html")
    return Response(ipv4 + "\n")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
