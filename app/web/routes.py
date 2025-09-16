from datetime import datetime
from flask import render_template, request, redirect, abort
from sqlalchemy import or_

from ..extensions import db
from ..models import Url, Click
from . import web_bp


@web_bp.get("/")
def home():
    return render_template("index.html")


@web_bp.post("/shorten")
def shorten_form():
    long_url = request.form.get("long_url")
    if not long_url:
        abort(400, description="Invalid URL")
    from ..utils import generate_short_code

    code = generate_short_code(long_url)
    url = Url(long_url=long_url, short_code=code)
    db.session.add(url)
    db.session.commit()
    return f"Shortened URL: <a href='/{url.short_code}'>{request.host_url}{url.short_code}</a>"


@web_bp.get("/<code_or_alias>")
def redirect_short(code_or_alias: str):
    u = Url.query.filter(or_(Url.short_code == code_or_alias, Url.custom_alias == code_or_alias)).first()
    if not u or (u.expires_at and u.expires_at < datetime.utcnow()):
        abort(404, description="URL not found")
    u.clicks += 1
    click = Click(
        url_id=u.id,
        referrer=request.referrer,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.remote_addr,
    )
    db.session.add(click)
    db.session.commit()
    return redirect(u.long_url)


