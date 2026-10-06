# Three-Tier Task Tracker (DevOps practice project)

| Tier | Tech | Folder | Port |
|------|------|--------|------|
| Frontend | Vite (vanilla JS) built to static files, served by Nginx | `frontend/` | 80 in container |
| Backend | Python 3.12 + Flask + Gunicorn | `backend/` | 5000 |
| Database | PostgreSQL 16 | `db/init.sql` | 5432 |

No Ansible, Terraform or Kubernetes. Only Docker, Docker Compose, GitHub Actions and Jenkins.

## What you write yourself
- [ ] `frontend/Dockerfile` (multi-stage: node build, then nginx serving `dist/`)
- [ ] `backend/Dockerfile`
- [ ] `docker-compose.yml` (services: frontend, backend, db)
- [ ] `.github/workflows/ci.yml`
- [ ] `Jenkinsfile`
- [ ] `.dockerignore` files

## Commands your pipelines will need

**Backend** (in `backend/`, Python 3.12)
- Install: `pip install -r requirements-dev.txt`
- Lint: `flake8 .`
- Test: `pytest`
- Production run: `gunicorn -b 0.0.0.0:5000 app:app`

**Frontend** (in `frontend/`, Node 20)
- Install: `npm install` (or `npm ci` after you commit the lock file)
- Test: `npm test`
- Build: `npm run build` (output in `dist/`)

**Database**
- Image: `postgres:16`
- Mount `db/init.sql` to `/docker-entrypoint-initdb.d/init.sql` (runs on first start only)
- Needs env vars: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

**Smoke test** after `docker compose up -d`: `./scripts/smoke_test.sh http://localhost:8080`

## Wiring notes
- Backend env vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` (see `.env.example`). `DB_HOST` should be the compose service name of the database.
- `frontend/nginx.conf` proxies `/api/` to `http://backend:5000`, so your compose service for the backend must be named `backend`.
- Map the frontend container port 80 to host 8080 to match the smoke test.
- The backend can start before Postgres is ready. Add a `healthcheck` on the db and `depends_on` with `condition: service_healthy` (`pg_isready -U $POSTGRES_USER`).
- Use a named volume for `/var/lib/postgresql/data`.

## API
- `GET /api/health`, `GET /api/health/db`
- `GET /api/tasks`, `POST /api/tasks` (`{"title": "..."}`)
- `PATCH /api/tasks/<id>` toggles done, `DELETE /api/tasks/<id>`

## Pipeline ideas to practice
1. Lint + test both tiers (run in parallel)
2. Build Docker images, tag with the commit SHA
3. Push to Docker Hub (store credentials as GitHub secrets / Jenkins credentials)
4. Deploy with `docker compose up -d` and run the smoke test
5. Add a `develop` vs `main` branch rule, or a manual approval step in Jenkins
