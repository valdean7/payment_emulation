### 1. Instalar a biblioteca `payment_emulation`:

```{.bash}
pip install payment_emulation
```

### 2. Adicione em `INSTALLED_APPS`: 

```{.py3}
INSTALLED_APPS = [
    ...
    'payment_emulation',
]
```

### 3. Realize as Migrações:

```{.bash}
python manage.py migrate
```