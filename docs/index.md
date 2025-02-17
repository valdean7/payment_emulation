# Inicio

## Descrição

Payment Emulation é uma biblioteca desenvolvida para ser usada em projetos Django 
para emular pagamentos com cartões bancários. Ela é ideal para ser usada em seus 
projetos para implementar um método de pagamento.

## Requisitos
Payment Emulation requer o seguinte:

- Django (>=5.1)
- Python (>=3.10)

## Instalação

{% include "assets/partials/installation_pt.md" %}

## Seeds pré-preparadas

Após executar o comando `migrate`, três registros de seed (*dados iniciais*) serão criados 
nos modelos `Account` (Conta) e `Card` (Cartão) da biblioteca. Esses dados são pré-configurados 
para simular cenários específicos de transações e podem ser recuperados através do método [`get_seeds()`](payment/PaymentSDK.md/#payment_emulation.payment.paymentSDK.PaymentSDK.get_seeds){:target="_blank"}.

Cada chave no dicionário retornado corresponde a um tipo de transação:

- `PROBATUS` → Transação **bem-sucedida** (`success`).

- `REPROBI` → Transação **recusada** (`failure`).

- `PENDENTE` → Transação **pendente** (`pending`).

Veja como obter esses dados.

{% include "assets/partials/seeds.md" %}

## Exemplo

Vamos dar uma olhada em um exemplo rápido de como realizar uma transação bem-sucedida usando a biblioteca Payment Emulation.

{% include "assets/partials/exemple_home.md" %}

{% include "assets/partials/license.md" %}
