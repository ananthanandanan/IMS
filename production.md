## Django settings for production

- We need to set few things for production environment. Especially since we are using docker and docker-compose. 

- Create .env file in the root directory of the project. We can do this by adding the following lines to `.env` file.

```
ALLOWED_HOSTS=your_domain_name
POSTGRES_NAME=your_postgres_name
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
...
## We can add more, like secret key, DEBUG, etc.
```

- We need to set `DEBUG` to `False` while setting up production environment variables.

- We need to set `ALLOWED_HOSTS` to `['*']` in `settings.py` file. Or depending on our domain name, for example: `['example.com']`.


- We need to set `DATABASES` in `settings.py` file. Mainly because we will be using postgresql database.

```python
DATABASES = {

    "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ.get("POSTGRES_NAME"),
    "USER": os.environ.get("POSTGRES_USER"),
    "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "HOST": "db",
    "PORT": "5432",

    }
}
```

- Define the MEDIA_ROOT and MEDIA_URL in `settings.py` file. We can do this by adding the following lines to `settings.py` file.

```python
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

- We also need to add some security settings. We can do this by adding the following lines to `settings.py` file. For always running in
https, csrf token etc.

```python

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
```

