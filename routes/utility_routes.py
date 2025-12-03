from flask import Blueprint, jsonify

utility_bp = Blueprint("utility_bp", __name__)

@utility_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "message": "Backend & routes are working fine!"
    })
