## Manipulando seeds utilizando o CLI

Uma forma simples de lidar com as seeds é através do uso da interface de linha de comando (CLI).
Veja abaixo as formas de se lidar com estas manipulações.

### Apagar seeds

Caso queira apagar as seeds existentes use o seguinte comando:

```{.bash .copy}
python manage.py deleteseeds
```

![deleteseeds](assets/img/deleteseeds.png)

Também é possível apagar seeds específicas utilizando a flag `-n` ou `--name`:

```{.bash .copy}
python manage.py deleteseeds --name probatus
```

![deleteseeds name](assets/img/deleteseeds_name.png)

Caso o nome informado da seed não for encontrado ocasionará a seguinte resposta:

![deleteseeds not found](assets/img/deleteseeds_not_found.png)

???+ Info

    Quando for apagar uma seeds especifica, o nome que for passado pode ser com letras maiusculas ou minusculas,
    contanto que o nome esteja correto irá funcionar.

### Criar seeds

Para criar as seeds use o seguinte comando:

```{.bash .copy}
python manage.py createseeds
```

![createseeds](assets/img/createseeds.png)

???+ Info
    Ao criar as seeds, se já existir alguma criada, só será criada as seeds que estão faltando.

### Definir saldo

A única seed que pode ser definida um novo saldo é a seed `PROBATUS`.
Quando uma transação é feita usando-a, o `amount` é deduzido do `balance`,
e consequentemente, o valor do saldo diminuirá. Para definir um novo valor (valor padrão: 99999),
use o seguinte comando:

```{.bash .copy}
python manage.py setbalance
```

![setbalance default](assets/img/setbalance_default.png)

Também é possível definir um valor desejado usando a flag `-b` ou `--balance`:

```{.bash .copy}
python manage.py setbalance --balance 10000
```

![setbalance value](assets/img/setbalance_value.png)

Caso a seed `PROBATUS` não exista ocasionará a seguinte resposta:

![setbalance not created](assets/img/setbalance_not_created.png)