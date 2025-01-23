### 1. Instalar a biblioteca Payment Emulation:

```{.bash}
pip install {{ vars.lib_name }}
```

### 2. Adicione em `INSTALLED_APPS`: 

```{.py3}
INSTALLED_APPS = [
    ...
    '{{ vars.installed_apps }}',
]
```

### 3. Realize as migrações:

```{.bash}
python manage.py migrate
```
