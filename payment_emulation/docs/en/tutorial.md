# Tutorial

## Installing the library in your project

{% include "assets/partials/installation_en.md" %}

## Pre-prepared seeds

Once you run `migrate`, 3 seeds will be created in the `Account` and `Card` models of the library. 
To retrieve this data, use the `get_seeds` method from the `PaymentSDK` class. 
Each data represented by a key will perform a specific type of transaction, and these keys are:

- `PROBATUS`: `{transaction: success, ...}`.
- `REPROBI`: `{transaction: failure, ...}`.
- `PENDENTE`: `{transaction: pending, ...}`.

See an example of how to get this data.

{% include "assets/partials/seeds.md" %}

## Managing seeds using the CLI

A simple way to handle seeds is by using the command-line interface (CLI).  
Below are the methods for performing these operations.

### Deleting seeds

If you want to delete existing seeds, use the following command:

```{.bash}
python manage.py deleteseeds
```

![deleteseeds](../assets/img/deleteseeds.png)

You can also delete specific seeds using the `-n` or `--name` flag:

```{.bash}
python manage.py deleteseeds --name probatus
```

![deleteseeds name](../assets/img/deleteseeds_name.png)

If the specified seed name is not found, the following response will appear:

![deleteseeds not found](../assets/img/deleteseeds_not_found.png)

!!! Info
    When deleting a specific seed, the name can be provided in uppercase or lowercase.
    As long as the name is correct, it will work.

### Creating seeds

To create seeds, use the following command:

```{.bash}
python manage.py createseeds
```

![createseeds](../assets/img/createseeds.png)

!!! Info
    When creating seeds, if some already exist, only the missing seeds will be created.

### Setting balance

The only seed that can have a new balance set is the `PROBATUS` seed.
When a transaction is made using it, the `amount` is deducted from the `balance`,
and consequently, the balance value will decrease. To set a new
value (default value: 99999), use the following command:


```{.bash}
python manage.py setbalance
```

![setbalance default](../assets/img/setbalance_default.png)

You can also set a desired value using the `-b` or `--balance` flag:

```{.bash}
python manage.py setbalance --balance 10000
```

![setbalance value](../assets/img/setbalance_value.png)

If the `PROBATUS` seed does not exist, the following response will appear:

![setbalance not created](../assets/img/setbalance_not_created.png)

## How to perform a transaction

Choose a seed according to the desired transaction, get the following data: 
`cpf`, `card_number`, `validity`, `cvv`, and `card_holder_name`. Then use them in the 
`payment()` method of the `PaymentSDK` class, but before using the method, you need 
to pass a list with one or more dictionaries, each containing the product data. 
Each dictionary must have the `quantity` and `unit_price` keys. It is also possible 
(and recommended) to add other keys of your preference containing product information.

- `quantity`: an `int` value indicating the quantity of the product.
- `unit_price`: a `float` indicating the product price.
- `payment()`: receives the card credentials (model `Card`) and will return a `JSON` 
response containing the result of the transaction and data related to the list of 
products passed in the class initializer. If the transaction is `transaction: success`, 
the value obtained from `quantity` multiplied by `unit_price` will be deducted from 
the `balance` of the account (model `Account`) linked to the card.

See an example of how to perform a transaction.

{% include "assets/partials/exemple_tutorial.md" %}

## How to create a new account and card

When creating an account and card, you won't need to provide all parameters, 
as some will receive `default` values. In the `Account` model, the required parameters 
will be `cpf`, `account_holder_name`, and `balance`, while in the `Card` model, the required 
parameters will be `account`, `card_holder_name`, `card_flag`, and `pin`.

- **`Account` model parameters**
    - `cpf`: receives a `str` (only digits) of a valid CPF.
    - `account_holder_name`: receives a `str` (only letters and spaces).
    - `account_number`: will receive a `default` value or can receive a `str` (only digits) of up to a maximum of 20 digits.
    - `balance`: receives an `int` or a `str` of an integer or a floating-point number with up to two decimal places.
    - `status`: will receive a choice `('AC', 'active')` as the `default` value, other choices that can be passed are `('IN', 'inactive')` and `('BL', 'blocked')`.

- **`Card` model parameters**
    - `account`: receives an instance of the `Account` model.
    - `card_holder_name`: receives a `str` (only letters and spaces).
    - `card_number`: will receive a `default` value or can receive a `str` (only digits) of up to a maximum of 16 digits.
    - `validity`: will receive a `default` value or can receive a `date`.
    - `cvv`: will receive a `default` value or can receive a `str` (only digits) of up to a maximum of 4 digits.
    - `card_flag`: receives a choice, the choices that can be passed are `VISA` (Visa), `MC` (MasterCard), `ELO` (Elo) and `OTHER` (Other).
    - `active`: receives a `bool`, `True` as the `default` value.
    - `pin`: receives a `str` (only digits).

{% include "assets/partials/account_card_create.md" %}

## Transaction results
- `success`: if all credentials are correct and the total purchase amount is less than the `balance`.
- `failure`: if one or more credentials are wrong or if the purchase amount is greater than the `balance`.
- `pending`: if the value of `card_flag` is set to `OTHER`.
