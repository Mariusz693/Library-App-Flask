const connectHost = async(url, options, callback) => {
    const hostData = await fetch(url, options);
    const hostJson = hostData.json();
    return hostJson;
};


function clearErrors(modalBodyEl) {
    modalBodyEl.querySelectorAll('li').forEach((e) => e.parentElement.remove());
};


function addErrors(errors, formFieldEl) {
    const formEl = formFieldEl[0].parentElement;
    clearErrors(formEl.querySelector('.modal-body'));
    const ulEl = document.createElement('ul');
    const liEl = document.createElement('li');
    for (let key in errors) {
        if (errors[key].length) {
            const divEl = formFieldEl[key].parentElement;
            divEl.appendChild(ulEl.cloneNode());
            for (let i=0; i<errors[key].length; i++) {
                divEl.lastElementChild.appendChild(liEl.cloneNode());
                divEl.lastElementChild.lastElementChild.innerText = errors[key][i];
            };
        };
    };
};


function addFlash(messageText, alertType) {
    document.querySelectorAll('.my-row-alert').forEach((e) => e.remove());
    const divEl = document.createElement('div');
    divEl.classList.add('row', 'my-row-alert');
    const divElChildren = document.createElement('div');
    divElChildren.classList.add('col', 'alert', `alert-${alertType}`);
    divElChildren.role = 'alert';
    divElChildren.innerText = messageText + ' ';
    const buttonEl = document.createElement('button');
    buttonEl.type = 'button';
    buttonEl.classList.add('btn', `btn-${alertType}`);
    buttonEl.dataset.dismiss = 'alert';
    buttonEl.innerText = 'X';
    divElChildren.appendChild(buttonEl);
    divEl.appendChild(divElChildren);
    document.querySelector('.my-row-header').after(divEl);
}


const createAuthor = async (formFieldEl, path) => {
    const url = location.protocol + "//" + location.host + path;
    const obj = {
        csrf_token: formFieldEl['csrf_token'].value,
        name: formFieldEl['name'].value,
        date_of_birth: formFieldEl['date_of_birth'].value,
        date_of_death: formFieldEl['date_of_death'].value
    };
    const options = {
        'method': 'POST',
        'body': JSON.stringify(obj),
    }
    const jsonData = await connectHost(url, options);
    if (jsonData['status'] === 'create') {
        const optionEl = document.querySelectorAll('option')[0].cloneNode();
        optionEl.value = jsonData['author']['id'];
        optionEl.innerText = jsonData['author']['name'];
        optionEl.selected = 'selected';
        document.querySelectorAll('option')[0].after(optionEl);
        addFlash('Profil autora został utworzony', 'success');
        formFieldEl['close'].click();
    }
    else if (jsonData['status'] === 'exist') {
        document.querySelector(`option[value="${jsonData['id']}"]`).selected = 'selected';
        addFlash('Profil autora już istnieje w bazie', 'danger');
        formFieldEl['close'].click();
    }
    else if (jsonData['status'] === 'error') {
        addErrors(jsonData['errors'], formFieldEl);
    };
};


const createCategory = async (formFieldEl, path) => {
    const url = location.protocol + "//" + location.host + path;
    const obj = {
        csrf_token: formFieldEl['csrf_token'].value,
        name: formFieldEl['name'].value
    };
    const options = {
        'method': 'POST',
        'body': JSON.stringify(obj),
    }
    const jsonData = await connectHost(url, options);
    if (jsonData['status'] === 'create') {
        const checkboxAllEl = document.querySelector('#categories');
        const liEl = document.createElement('li');
        const inputEl = document.createElement('input');
        inputEl.id = `categories-${checkboxAllEl.childElementCount}`;
        inputEl.name = 'categories';
        inputEl.type = 'checkbox';
        inputEl.value = jsonData['category']['id'];
        inputEl.checked = true;
        const labelEl = document.createElement('label');
        labelEl.htmlFor = `categories-${checkboxAllEl.childElementCount}`;
        labelEl.innerText = jsonData['category']['name'];
        liEl.appendChild(inputEl);
        liEl.appendChild(labelEl);
        checkboxAllEl.prepend(liEl);
        addFlash('Kategoria została utworzona', 'success');
        formFieldEl['close'].click();
    }
    else if (jsonData['status'] === 'exist') {
        document.querySelector(`input[type="checkbox"][value="${jsonData['id']}"]`).checked = true;
        addFlash('Kategoria już istnieje w bazie', 'danger');
        formFieldEl['close'].click();
    }
    else if (jsonData['status'] === 'error') {
        addErrors(jsonData['errors'], formFieldEl);
    };
};


document.addEventListener("DOMContentLoaded", function() {
    for (let i=0, buttonEl, buttonsEl = document.querySelectorAll('[data-toggle="modal"]'); buttonEl = buttonsEl[i]; i++) {
        buttonEl.onclick = function (e) {
            e.preventDefault();
            if (e.target.id === "button-create-author") {
                const formEl = document.getElementById('form-create-author');
                clearErrors(formEl.querySelector('.modal-body'));
                formEl.addEventListener('submit', function(event) {
                    event.preventDefault();
                    createAuthor(event.target.elements, formEl.dataset.path);
                });
            };
            if (e.target.id === "button-create-category") {
                const formEl = document.getElementById('form-create-category');
                clearErrors(formEl.querySelector('.modal-body'));
                formEl.addEventListener('submit', function(event) {
                    event.preventDefault();
                    createCategory(event.target.elements, formEl.dataset.path);
                });
            };
        };
    };
});