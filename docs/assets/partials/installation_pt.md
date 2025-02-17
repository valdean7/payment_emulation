### 1. Instalar a biblioteca Payment Emulation:

```{.bash .copy}
pip install {{ vars.lib_name }}
```

### 2. Adicione em `INSTALLED_APPS`: 

```{.python .copy}
INSTALLED_APPS = [
    ...
    '{{ vars.installed_apps }}',
]
```

### 3. Realize as migrações:

```{.bash .copy}
python manage.py migrate
```
