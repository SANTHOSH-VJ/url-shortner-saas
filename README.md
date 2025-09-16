URL Shortener SaaS (Refactored)

Modernized Flask + React URL shortener with RESTful API, SQLAlchemy ORM, migrations, authentication, analytics, QR codes, and containerized deployment.

Features:
- REST API with Blueprints: create short URLs, resolve, analytics, QR
- ORM models (User, Url, Click, ApiKey) with Flask-Migrate
- API key authentication and basic signup to generate keys
- Custom aliases, expiration dates, click tracking with referrer/UA/IP
- React frontend (Vite) and Nginx for static hosting + API proxy
- Docker/Docker Compose for local dev: app, MySQL, frontend, nginx
- CI workflow (GitHub Actions) for build checks

Quick Start (Docker Compose):
1. docker compose up -d --build
2. App API at http://localhost:5000, Frontend at http://localhost:8080

Environment Variables:
- DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
- SECRET_KEY, DATABASE_URL (optional; overrides individual DB vars)

Database Migrations:
- Install deps: pip install -r requirements.txt
- Export env vars (see docker-compose.yml defaults)
- Initialize: flask db init
- Generate: flask db migrate -m "init"
- Apply: flask db upgrade

API Examples:
- Create URL: POST /api/v1/urls {"long_url":"https://example.com","custom_alias":"my-link"}
- Get URL: GET /api/v1/urls/{code_or_alias}
- Analytics: GET /api/v1/urls/{code_or_alias}/analytics
- QR: GET /api/v1/urls/{code_or_alias}/qr
- Signup: POST /api/v1/auth/signup {"email":"a@b.com","password":"pass"}
- Create API Key: POST /api/v1/auth/apikeys {"email":"a@b.com","password":"pass"}
  - Use key via header: X-API-Key: <key>

Local Dev (without Docker):
1. python -m venv .venv && .venv\Scripts\activate (Windows)
2. pip install -r requirements.txt
3. Set env vars (DB_*, SECRET_KEY)
4. flask run

Project Structure:
```
app/
  __init__.py, config.py, extensions.py, models.py, utils.py, errors.py
  api/, auth/, web/
frontend/ (React Vite app)
wsgi.py, Dockerfile, docker-compose.yml, Procfile
```
