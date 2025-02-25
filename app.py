from flask import Flask, request, Response
import requests

app = Flask(__name__)

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

@app.route("/", methods=["GET"])
def get_ip():
    headers = request.headers
    ipv4 = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    ipv6 = request.headers.get("X-Client-IP", "NO_IPv6")

    # Get location data
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
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
        </head>
        <body>
            <h1>Gustavo Migliorini Arruda IP checker</h1>
            <p>Your IPv4: {ipv4 or 'NO_IPv4'}</p>
            <p>Your IPv6: {ipv6}</p>
            <p><strong>Location:</strong> {city}, {country}</p>
            
            <h2>Your IP Location on the Map</h2>
            <div id="map" style="height: 400px;"></div>

            <script>
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

    # Handle curl headers
    if "IPv4" in headers:
        return Response((ipv4 if ipv4 else "NO_IPv4") + "\n")
    elif "IPv6" in headers:
        return Response((ipv6 if ipv6 != "NO_IPv6" else "NO_IPv6") + "\n")
    else:
        return Response((ipv6 if ipv6 != "NO_IPv6" else ipv4) + "\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)