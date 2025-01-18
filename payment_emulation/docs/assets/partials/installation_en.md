### 1. Install the library `payment_emulation`:

```{.bash}
pip install payment_emulation
```

### 2. Add to `INSTALLED_APPS`: 

```{.py3}
INSTALLED_APPS = [
    ...
    'payment_emulation',
]
```

### 3. Perform Migrations:

```{.bash}
python manage.py migrate
```