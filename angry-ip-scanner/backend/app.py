from flask import Flask, request, jsonify
from scanner import ping, scan_ports, get_ip_location

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    ip = data.get("ip")
    start_port = data.get("start_port", 1)
    end_port = data.get("end_port", 1024)

    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = {
        "ip": ip,
        "is_alive": ping(ip),
        "open_ports": scan_ports(ip, start_port, end_port),
        "location": get_ip_location(ip),
    }
    import json
import csv

def save_scan_results(result):
    """Save scan results to a file (both JSON and CSV)."""
    # Save as JSON
    with open("scan_results.json", "a") as json_file:
        json.dump(result, json_file, indent=4)
        json_file.write(",\n")

    # Save as CSV
    with open("scan_results.csv", "a", newline="") as csv_file:
        fieldnames = ["ip", "is_alive", "open_ports", "city", "region", "country", "isp"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header only if the file is empty
        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            "ip": result["ip"],
            "is_alive": result["is_alive"],
            "open_ports": ", ".join(map(str, result["open_ports"])),
            "city": result["location"]["city"],
            "region": result["location"]["region"],
            "country": result["location"]["country"],
            "isp": result["location"]["isp"]
        })

@app.route("/scan", methods=["POST"])
def scan():
    data = request.json
    ip = data.get("ip")
    start_port = data.get("start_port", 1)
    end_port = data.get("end_port", 1024)

    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = {
        "ip": ip,
        "is_alive": ping(ip),
        "open_ports": scan_ports(ip, start_port, end_port),
        "location": get_ip_location(ip),
    }

    save_scan_results(result)  # Save the results

    return jsonify(result)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
