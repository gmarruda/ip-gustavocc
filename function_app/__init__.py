import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = req.headers
    ipv4 = req.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    ipv6 = req.headers.get("X-Client-IP", "NO_IPv6")

    # Detecting curl (by checking User-Agent)
    user_agent = headers.get("User-Agent", "").lower()
    is_curl = "curl" in user_agent

    if not is_curl:
        # HTML Response for Browsers
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
        return func.HttpResponse(html_content, mimetype="text/html")

    # Handling curl requests
    ipv4_requested = headers.get("IPv4")
    ipv6_requested = headers.get("IPv6")

    if ipv4_requested:
        return func.HttpResponse(ipv4 if ipv4 else "NO_IPv4")
    elif ipv6_requested:
        return func.HttpResponse(ipv6 if ipv6 != "NO_IPv6" else "NO_IPv6")
    else:
        # Default: prefer IPv6 if available, otherwise return IPv4
        return func.HttpResponse(ipv6 if ipv6 != "NO_IPv6" else ipv4)