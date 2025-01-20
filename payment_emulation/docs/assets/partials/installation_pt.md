### 1. Instalar a biblioteca `{{ vars.lib_name }}`:

```{.bash}
pip install {{ vars.lib_name }}
```

### 2. Adicione em `INSTALLED_APPS`: 

```{.py3}
INSTALLED_APPS = [
    ...
    '{{ vars.lib_name_sc }}',
]
```

### 3. Realize as migrações:

```{.bash}
python manage.py migrate
```
