## Modal do formulário de pagamento

??? Quote "Source code in "<code>payment_emulation\payment\templates\payment\payment_modal.html</code>"
    ```{.html+jinja linenums="1"}
    {% raw %}
    {% load static %}


    <section id="modal_section" class="fixed w-[100%] h-[100%] top-0 left-0 hidden justify-center items-center bg-gray-900/50">
        <div class="w-[470px] bg-white rounded-md">
            <form method="post" action="{{ action }}" class="flex flex-col gap-4 h-[100%] justify-evenly p-4">
                {% csrf_token %}
                <div class="flex flex-col gap-3">
                    <div class="relative flex flex-col">
                        <label for="id_card_number">Número do cartão</label>
                        <input 
                        autocomplete="one-time-code" 
                        class="border rounded p-2 focus:outline-blue-400" type="text" 
                        name="card_number" 
                        id="id_card_number" 
                        required 
                        placeholder="1234 1234 1234 1234" 
                        pattern="^\d{4}( ?\d{4}){3}$">
                        <img class="w-8 absolute right-1 bottom-[11px]" src="{% static "payment/img/generic.svg" %}" alt="">
                    </div>
                    <div class="flex flex-col">
                        <label for="id_holder">Nome do titular</label>
                        <input 
                        autocomplete="one-time-code" 
                        class="border rounded p-2 focus:outline-blue-400" type="text" 
                        name="holder" 
                        id="id_holder" 
                        required 
                        placeholder="Ex: JHON DOE"
                        pattern="[A-Z ]*">
                    </div>
                    <div class="flex flex-row gap-3">
                        <div class="flex flex-col">
                            <label for="id_validity">Vencimento</label>
                            <input 
                            class="border w-fit rounded p-2 focus:outline-blue-400" 
                            type="text" 
                            name="validity" 
                            id="id_validity" 
                            required 
                            placeholder="MM/AA" 
                            pattern="^(0[1-9]|1[0-2])\/\d{2}$">
                        </div>
                        <div class="relative w-[250px] flex flex-col">
                            <label for="id_cvv">Código de segurança</label>
                            <input 
                            class="border rounded p-2 focus:outline-blue-400"
                            type="text" 
                            name="cvv" 
                            id="id_cvv" 
                            required 
                            placeholder="123"
                            pattern="^\d{3}$">
                            <img class="w-8 absolute right-1 bottom-[11px]" src="{% static "payment/img/code.svg" %}" alt="">
                        </div>
                    </div>
                    <div class="flex flex-row gap-2">
                        <select class="border rounded p-2 focus:outline-blue-400" name="cpfcnpj" id="id_cpfcnpj">
                            <option selected value="CPF">CPF</option>
                            <option value="CNPJ">CNPJ</option>
                        </select>
                        <input 
                        class="inline-block border w-full rounded p-2 focus:outline-blue-400" 
                        type="text" 
                        name="cpf" 
                        id="id_cpf" 
                        placeholder="123.456.789-09" 
                        required
                        pattern="^\d{3}\.\d{3}\.\d{3}-\d{2}$">
                        <input 
                        class="hidden border w-full rounded p-2 focus:outline-blue-400" 
                        type="text" 
                        name="cnpj" 
                        id="id_cnpj" 
                        placeholder="12.345.678/0001-99" 
                        required 
                        disabled
                        pattern="^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$">
                    </div>
                </div>
                <div class="self-end flex flex-row gap-4">
                    <button id="back_btn" class="border px-4 py-2 rounded-md bg-blue-100 text-blue-500 font-semibold hover:bg-blue-200 duration-200 transition-colors">Voltar</button>
                    <button id="pay_btn" class="border px-4 py-2 rounded-md bg-blue-500 text-white font-semibold hover:bg-blue-600 duration-200 transition-colors">Pagar</button>
                </div>
            </form>
        </div>
    </section>

    {% endraw %}
    ```

Uma forma simples de obter as credenciais da conta e do cartão para o processamento do pagamento 
é utilizar o modal do formulário de pagamento. Para integrá-lo ao seu projeto, siga os passos abaixo.

### 1. Incluir o modal em seu template

É importante passar uma URL para a variável de contexto `action`, que define o endpoint onde o pagamento será processado.

```{.jinja .copy}
{% raw %}
{% include "payment/payment_modal.html" with action="/payment/" %}
{% endraw %}
```

### 2. Incluir o script do modal

Certifique-se de incluir o script no mesmo template em que o modal foi inserido ou, alternativamente, 
adicione-o em um template global que seja estendido em suas páginas.

```{.html+jinja .copy}
{% raw %}
<script defer src="{% static "payment/js/paymentModal.js" %}"></script>
{% endraw %}
```

### 3. Criar um botão para a ativar o modal

Para que o botão funcione corretamente, defina o atributo `id` como `modal_activate_btn`.

```{.html .copy}
<input type="button" value="pagar" id="modal_activate_btn">
```
Após seguir todos os passos, ao clicar no botão de ativação, o modal será exibido conforme a imagem abaixo:

![modal](assets/img/payment_modal.png)