from datetime import datetime, timedelta
from flask import request, jsonify, current_app, url_for, send_file
from sqlalchemy.exc import IntegrityError
from io import BytesIO

from ..extensions import db
from ..models import Url, Click, ApiKey, User
from ..utils import generate_short_code, generate_qr_png_bytes
from . import api_bp


def _auth_api_key() -> User | None:
    api_key_value = request.headers.get("X-API-Key") or request.args.get("api_key")
    if not api_key_value:
        return None
    api_key = ApiKey.query.filter_by(key=api_key_value, is_active=True).first()
    if not api_key:
        return None
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        return None
    return api_key.user


@api_bp.post("/urls")
def create_short_url():
    auth_user = _auth_api_key()
    data = request.get_json(silent=True) or {}
    long_url = data.get("long_url")
    custom_alias = data.get("custom_alias")
    expires_in_days = data.get("expires_in_days")

    if not long_url:
        return jsonify({"error": "long_url is required"}), 400

    short_code = generate_short_code(long_url)
    expires_at = (
        datetime.utcnow() + timedelta(days=int(expires_in_days)) if expires_in_days else None
    )
    url = Url(
        user_id=auth_user.id if auth_user else None,
        long_url=long_url,
        short_code=short_code,
        custom_alias=custom_alias or None,
        expires_at=expires_at,
    )
    try:
        db.session.add(url)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "custom_alias or generated code already exists"}), 409

    short_path = url.custom_alias or url.short_code
    short_url = request.host_url.rstrip("/") + "/" + short_path
    return jsonify({
        "id": url.id,
        "short_url": short_url,
        "short_code": short_path,
        "long_url": url.long_url,
        "expires_at": url.expires_at.isoformat() if url.expires_at else None,
        "created_at": url.created_at.isoformat(),
    }), 201


@api_bp.get("/urls/<code_or_alias>")
def get_url(code_or_alias: str):
    url = Url.query.filter((Url.short_code == code_or_alias) | (Url.custom_alias == code_or_alias)).first()
    if not url:
        return jsonify({"error": "not_found"}), 404
    return jsonify({
        "id": url.id,
        "long_url": url.long_url,
        "short_code": url.custom_alias or url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at.isoformat(),
        "expires_at": url.expires_at.isoformat() if url.expires_at else None,
    })


@api_bp.get("/urls/<code_or_alias>/analytics")
def url_analytics(code_or_alias: str):
    url = Url.query.filter((Url.short_code == code_or_alias) | (Url.custom_alias == code_or_alias)).first()
    if not url:
        return jsonify({"error": "not_found"}), 404

    clicks = [
        {
            "id": c.id,
            "created_at": c.created_at.isoformat(),
            "referrer": c.referrer,
            "user_agent": c.user_agent,
            "country": c.country,
            "ip_address": c.ip_address,
        }
        for c in url.click_events[-100:]
    ]

    return jsonify({
        "id": url.id,
        "total_clicks": url.clicks,
        "recent_clicks": clicks,
    })


@api_bp.get("/urls/<code_or_alias>/qr")
def url_qr(code_or_alias: str):
    url = Url.query.filter((Url.short_code == code_or_alias) | (Url.custom_alias == code_or_alias)).first()
    if not url:
        return jsonify({"error": "not_found"}), 404
    short_path = url.custom_alias or url.short_code
    short_url = request.host_url.rstrip("/") + "/" + short_path
    png_bytes = generate_qr_png_bytes(short_url)
    return send_file(BytesIO(png_bytes), mimetype="image/png")


