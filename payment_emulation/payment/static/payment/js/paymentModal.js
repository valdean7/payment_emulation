const modalSection = document.getElementById('modal_section')
const validity = document.getElementById('id_validity')
const cardNumber = document.getElementById('id_card_number')
const holder = document.getElementById('id_holder')
const cvv = document.getElementById('id_cvv')
const cpfCnpjSelector = document.getElementById('id_cpfcnpj')
const cpf = document.getElementById('id_cpf')
const cnpj = document.getElementById('id_cnpj')
const backBtn = document.getElementById('back_btn')
const payBtn = document.getElementById('pay_btn')
const modalActivateBtn = document.getElementById('modal_activate_btn')

const cleanInputs = () => {
    validity.value = ""
    cardNumber.value = ""
    holder.value = ""
    cvv.value = ""
    cpf.value = ""
    cnpj.value = ""
    cpfCnpjSelector.querySelector('option').selected = true
}

const applyCPFMask = (value) => {
    return value
        .replace(/\D/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1')
}

const applyCNPJMask = (value) => {
    return value
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1/$2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1')
}

cpf.addEventListener('input', function(e) {
    e.target.value = applyCPFMask(e.target.value)
})

cnpj.addEventListener('input', function(e) {
    e.target.value = applyCNPJMask(e.target.value)
})

cpfCnpjSelector.addEventListener('change', function(e) {
    if (e.target.value === 'CNPJ') {
        cnpj.classList.replace('hidden', 'inline-block')
        cnpj.disabled = false
        cnpj.value = ""
        cpf.classList.replace('inline-block', 'hidden')
        cpf.disabled = true
        cpf.value = ""
    }
    if (e.target.value === 'CPF') {
        cpf.classList.replace('hidden','inline-block')
        cpf.disabled = false
        cnpj.classList.replace('inline-block', 'hidden')
        cnpj.disabled = true
    }
})

validity.addEventListener('input', function(e) {
    let value = this.value.replace(/\D/g, '')
    value = value.substring(0, 4)
    if (value.length > 2) {
        value = value.substring(0, 2) + '/' + value.substring(2)
    }
    this.value = value
})

cardNumber.addEventListener('input', function(e) {
    let value = this.value.replace(/\D/g, '')
    value = value.substring(0, 16)
    value = value.replace(/(\d{4})(?=.)/g, '$1 ')
    this.value = value
})


holder.addEventListener('input', function(e) {
    let value = this.value.replace(/[^A-Za-z ]/g, '')
    value = value.toUpperCase()
    this.value = value
})

cvv.addEventListener('input', function(e) {
    let value = this.value.replace(/\D/g, '')
    value = value.substring(0, 3)
    this.value = value
})


modalSection.addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.replace('flex', 'hidden')
        cleanInputs()
    }
})

backBtn.addEventListener('click', function(e) {
    e.preventDefault()
    modalSection.classList.replace('flex', 'hidden')
    cleanInputs()
})

modalActivateBtn.addEventListener('click', function() {
    if (modalSection.classList.contains('hidden')) {
        modalSection.classList.replace('hidden', 'flex')
    }
})
