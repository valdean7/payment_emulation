## Resultado das transações

Os possíveis resultados de uma transação são definidos pelas seguintes regras:

- `success` (Sucesso)

    - Todas as credenciais (dados da conta e cartão) são válidas.

    - O valor total da compra é menor ou igual ao saldo disponível (`balance`).

- `failure` (Falha)

    - Pelo menos uma credencial é inválida (ex.: CPF incorreto, CVV errado).

    - O valor da compra é maior que o saldo (`balance`).

- `pending` (Pendente)

    - A bandeira do cartão (`card_flag`) é definida como `OTHER`.

## Como realizar uma transação

Para realizar uma transação utilizando o SDK de pagamento, siga os passos abaixo:

### Paso 1. Preparação dos Dados

1. Escolha uma seed ([ou crie um conta e cartão](account_and_card.md/#como-criar-uma-conta-e-cartao)) de acordo com o tipo de transação desejada.

2. Colete as informações do cartão necessárias para a transação:

    - `cpf`: CPF do titular do cartão (obrigatório se `cnpj` não for informado).

    - `cnpj`: CNPJ do titular do cartão (obrigatório se `cpf` não for informado).

    - `card_number`: Número do cartão (máximo de 16 dígitos).

    - `validity`: Data de validade no formato `MM/AA` (ex: `12/24`).

    - `cvv`: Código de segurança do cartão (3 dígitos).

    - `card_holder_name`: Nome do titular do cartão, conforme registrado.

### Passo 2: Preparação dos Produtos

Antes de chamar o método [`payment()`](payment/PaymentSDK.md/#payment_emulation.payment.paymentSDK.PaymentSDK.payment), é necessário criar uma lista contendo um ou mais dicionários 
com os dados dos produtos. Cada dicionário deve conter as seguintes chaves obrigatórias:

- `quantity`: Quantidade do produto (valor inteiro).

- `unit_price`: Preço unitário do produto (valor float).

Além disso, você pode adicionar outras chaves personalizadas para incluir informações adicionais 
sobre os produtos (ex: product_id, description, ou category).


### Passo 3: Realização da Transação

Utilize o método [`payment()`](payment/PaymentSDK.md/#payment_emulation.payment.paymentSDK.PaymentSDK.payment) da classe [`PaymentSDK`](payment/PaymentSDK.md) para processar a transação. 
O método recebe as credenciais do cartão e retorna uma resposta (`str`) no formato `JSON` contendo o 
resultado da transação e os dados relacionados aos produtos.

Se a transação for bem-sucedida (`transaction: success`), o valor total será debitado do saldo 
(`balance`) da conta (`Account`) vinculada ao cartão.

Veja um exemplo de como realizar uma transação.  

{% include "assets/partials/exemple_transaction.md" %}
