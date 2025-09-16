from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "bad_request", "message": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": "unauthorized", "message": str(e)}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "forbidden", "message": str(e)}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not_found", "message": str(e)}), 404

    @app.errorhandler(409)
    def conflict(e):
        return jsonify({"error": "conflict", "message": str(e)}), 409

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "server_error", "message": "An internal error occurred"}), 500


