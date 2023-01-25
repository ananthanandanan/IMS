# Docker Settings

## Setup docker for development

### Create .evn file

- In the env file add the following test variables

```bash
DEBUG=1
SECRET_KEY=secret
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_NAME=postgres
DJANGO_USER=postgres
DJANGO_PASSWORD=postgres
```

- In settings.py depending on the database you are using, add the following

```python
## SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

## PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DJANGO_NAME"),
            "USER": os.environ.get("DJANGO_USER"),
            "PASSWORD": os.environ.get("DJANGO_PASSWORD"),
            "HOST": "db",
            "PORT": "5432",
        }
    }
```

- In entrypoint.sh uncomment the following based on the database you are using

```bash
## SQLite
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb

## PostgreSQL
python3 manage.py makemigrations members buildings userlog
python3 manage.py migrate
```
