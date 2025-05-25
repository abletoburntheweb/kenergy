document.addEventListener('DOMContentLoaded', () => {
    const mainInventorySelect = document.getElementById('main-inventory-select');
    const mainGroupSelect = document.getElementById('main-group-select');
    const mainObjectSelect = document.getElementById('main-object-select');
    const modalInventorySelect = document.getElementById('modal-inventory-select');
    const modalGroupSelect = document.getElementById('modal-group-select');

    if (!mainInventorySelect) console.error('Элемент с id="main-inventory-select" не найден.');
    if (!mainGroupSelect) console.error('Элемент с id="main-group-select" не найден.');
    if (!mainObjectSelect) console.error('Элемент с id="main-object-select" не найден.');
    if (!modalInventorySelect) console.error('Элемент с id="modal-inventory-select" не найден.');
    if (!modalGroupSelect) console.error('Элемент с id="modal-group-select" не найден.');

    mainGroupSelect.innerHTML = '<option value="">Выберите группу</option>';
    mainObjectSelect.innerHTML = '<option value="">Выберите объект</option>';
    modalGroupSelect.innerHTML = '<option value="">Выберите группу</option>';

    function populateDropdown(selectElement, data) {
    selectElement.innerHTML = '<option value="">Выберите</option>';
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id_g;
        option.textContent = item.название;
        selectElement.appendChild(option);
    });
}

    function clearDropdown(selectElement) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        selectElement.disabled = true;
    }

    function updateGroups(inventoryId, groupSelect) {
        if (inventoryId) {
            fetch(`/api/groups/?inventory=${inventoryId}`)
                .then(response => {
                    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log('Полученные группы:', data);
                    populateDropdown(groupSelect, data);
                    groupSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Ошибка при получении групп:', error.message);
                    alert('Не удалось загрузить список групп.');
                });
        } else {
            clearDropdown(groupSelect);
        }
    }

    function updateObjects(groupId, objectSelect) {
        if (groupId) {
            fetch(`/api/objects/?group=${groupId}`)
                .then(response => {
                    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log('Полученные объекты:', data);
                    populateDropdown(objectSelect, data);
                    objectSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Ошибка при получении объектов:', error.message);
                    alert('Не удалось загрузить список объектов.');
                });
        } else {
            clearDropdown(objectSelect);
        }
    }

    if (mainInventorySelect && mainGroupSelect) {
        mainInventorySelect.addEventListener('change', () => {
            const inventoryId = mainInventorySelect.value;
            clearDropdown(mainGroupSelect);
            clearDropdown(mainObjectSelect);
            if (inventoryId) {
                updateGroups(inventoryId, mainGroupSelect);
            }
        });
    }

    if (mainGroupSelect && mainObjectSelect) {
        mainGroupSelect.addEventListener('change', () => {
            const groupId = mainGroupSelect.value;
            clearDropdown(mainObjectSelect);
            if (groupId) {
                updateObjects(groupId, mainObjectSelect);
            }
        });
    }

    if (modalInventorySelect && modalGroupSelect) {
        modalInventorySelect.addEventListener('change', () => {
            const inventoryId = modalInventorySelect.value;
            clearDropdown(modalGroupSelect);
            if (inventoryId) {
                updateGroups(inventoryId, modalGroupSelect);
            }
        });
    }

    function handleModalFormSubmit(modalSelector, selectId, callback) {
    const modal = document.querySelector(modalSelector);
    const form = modal.querySelector('form');
    if (!modal || !form) {
        console.error(`Модальное окно или форма с селектором "${modalSelector}" не найдены.`);
        return;
    }
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const inventory = document.getElementById('modal-inventory-select').value;
        const group = document.getElementById('modal-group-select').value;
        const name = document.getElementById('modal-object-name').value;

        if (!inventory || !group || !name) {
            alert('Пожалуйста, заполните все обязательные поля.');
            return;
        }

        const formData = new FormData(form);
        console.log('Отправляемые данные:', Object.fromEntries(formData.entries()));

        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]');
        if (!csrfToken) {
            console.error('CSRF-токен не найден.');
            return;
        }

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken.value,
            },
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errors => {
                    throw new Error(JSON.stringify(errors));
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                closeModal(modalSelector.replace('#', ''));

                const objectSelect = document.getElementById('main-object-select');
                clearDropdown(objectSelect);

                const selectElement = document.getElementById(selectId);
                if (selectElement) {
                    const newOption = document.createElement('option');
                    newOption.value = data.id;
                    newOption.textContent = data.name;
                    selectElement.appendChild(newOption);
                    selectElement.value = data.id;
                }

                if (typeof callback === 'function') {
                    callback();
                }
            } else {
                alert('Произошла ошибка при добавлении:\n' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.error('Ошибка при добавлении:', error.message);
            alert('Произошла неожиданная ошибка при сохранении данных.');
        });
    });
}

    handleModalFormSubmit('#add-inventory-modal', 'main-inventory-select', () => {
        updateGroups(mainInventorySelect.value, mainGroupSelect);
    });

    handleModalFormSubmit('#add-group-modal', 'main-group-select', () => {
        updateObjects(mainGroupSelect.value, mainObjectSelect);
    });

    handleModalFormSubmit('#add-object-modal', 'main-object-select');

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
        } else {
            console.error(`Модальное окно с id="${modalId}" не найдено.`);
        }
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        } else {
            console.error(`Модальное окно с id="${modalId}" не найдено.`);
        }
    }

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };
});