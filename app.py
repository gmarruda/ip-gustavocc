from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_ip():
    headers = request.headers
    ipv4 = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    ipv6 = request.headers.get("X-Client-IP", "NO_IPv6")

    user_agent = headers.get("User-Agent", "").lower()
    is_curl = "curl" in user_agent

    if not is_curl:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gustavo Migliorini Arruda IP checker</title>
        </head>
        <body>
            <h1>Gustavo Migliorini Arruda IP checker</h1>
            <p>Your IPv4: {ipv4 or 'NO_IPv4'}</p>
            <p>Your IPv6: {ipv6}</p>
        </body>
        </html>
        """
        return Response(html_content, mimetype="text/html")

    # Handle curl headers
    if "ipv4" in headers:
        return Response((ipv4 if ipv4 else "NO_IPv4") + "\n")
    elif "ipv6" in headers:
        return Response((ipv6 if ipv6 != "NO_IPv6" else "NO_IPv6") + "\n")
    else:
        return Response((ipv6 if ipv6 != "NO_IPv6" else ipv4) + "\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)