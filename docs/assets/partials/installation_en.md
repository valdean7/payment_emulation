### 1. Install the library `{{ vars.lib_name }}`:

```{.bash}
pip install {{ vars.lib_name }}
```

### 2. Add to `INSTALLED_APPS`: 

```{.py3}
INSTALLED_APPS = [
    ...
    '{{ vars.lib_name_sc }}',
]
```

### 3. Perform migrations:

```{.bash}
python manage.py migrate
```
