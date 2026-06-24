# Simple Todo — Django

A deliberately small Django app (one model, one app, plain function-based
views, Django templates) built to practice the **GitHub → Railway**
deployment pipeline.

## What it does
- Add a task
- Mark it complete / incomplete
- Delete it

That's it — no accounts, no APIs, no extra apps. Just enough Django to
exercise models, forms, templates, the admin, and static files.

## Project structure
```
simple_todo/
├── manage.py
├── requirements.txt
├── Procfile              # tells Railway how to start the app
├── core/                  # project settings/urls
└── todos/                 # the one app: model, views, forms, admin
    └── templates/todos/
└── templates/base.html
└── static/css/style.css
```

## 1. Run it locally

```bash
# from inside the simple_todo folder
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**. By default it uses a local `db.sqlite3`
file — no database setup needed.

## 2. Push it to GitHub

```bash
git init
git add .
git commit -m "Initial commit: simple Django todo app"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(`.gitignore` already excludes `db.sqlite3`, `__pycache__/`, `venv/`, etc.)

## 3. Deploy on Railway

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo** → pick this repo.
2. Railway auto-detects Python via `requirements.txt` and uses the
   `Procfile` to know how to start the app
   (`gunicorn core.wsgi`), running migrations first.
3. **Add a database (recommended):** in your Railway project, click
   **+ New** → **Database** → **PostgreSQL**. Railway automatically sets a
   `DATABASE_URL` variable on your web service, and `settings.py` is
   already wired to pick it up via `dj-database-url`. Without this step
   the app just keeps using SQLite, which works but resets whenever
   Railway redeploys/restarts the container — fine for testing, not for
   real data.
4. **Set environment variables** on your service (Settings → Variables):
   | Variable | Value |
   |---|---|
   | `SECRET_KEY` | any long random string |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | the domain Railway gives you, e.g. `yourapp.up.railway.app` |
5. **Generate a public domain:** Settings → Networking → Generate Domain.
6. Deploy. Visit the generated URL — your todo app should be live.

Every time you `git push` to `main`, Railway redeploys automatically —
that's the pipeline.

## Notes on the choices made here
- **WhiteNoise** serves CSS/JS in production so you don't need a separate
  static-file host.
- **dj-database-url** lets the same `settings.py` work with SQLite locally
  and Postgres on Railway, just by the presence/absence of `DATABASE_URL`.
- **gunicorn** is the production WSGI server (Django's own `runserver` is
  dev-only).

## Natural next steps once this works
- Add a second model (e.g. categories/tags) to practice foreign keys.
- Add user accounts so each person has their own task list.
- Swap Bootstrap-via-CDN for compiled CSS, or add Tailwind.
