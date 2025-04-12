from flask import jsonify


def health_check():
    print("health check")
    return jsonify(status="healthy"), 200

