document.addEventListener('DOMContentLoaded', () => {
    const inventorySelect = document.getElementById('inventory-select');
    const groupSelect = document.getElementById('group-select');
    const objectSelect = document.getElementById('object-select');

    function updateInventoryList() {
        fetch('/api/inventories/')
            .then(response => {
                if (!response.ok) throw new Error('Ошибка при получении инвентаря');
                return response.json();
            })
            .then(data => populateDropdown(inventorySelect, data))
            .catch(error => {
                console.error(error.message);
                alert('Не удалось загрузить список инвентаря.');
            });
    }

    function updateGroups(inventoryId) {
        if (inventoryId) {
            fetch(`/api/groups/?inventory=${inventoryId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка при получении групп');
                    return response.json();
                })
                .then(data => {
                    populateDropdown(groupSelect, data);
                    groupSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Ошибка при получении групп:', error.message);
                    alert('Не удалось загрузить список групп.');
                });
        } else {
            clearDropdown(groupSelect);
            groupSelect.disabled = true;
        }
    }

    function updateObjects(groupId) {
        if (groupId) {
            fetch(`/api/objects/?group=${groupId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Ошибка при получении объектов');
                    return response.json();
                })
                .then(data => {
                    populateDropdown(objectSelect, data);
                    objectSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Ошибка при получении объектов:', error.message);
                    alert('Не удалось загрузить список объектов.');
                });
        } else {
            clearDropdown(objectSelect);
            objectSelect.disabled = true;
        }
    }

    function populateDropdown(selectElement, data) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.название;
            selectElement.appendChild(option);
        });
    }

    function clearDropdown(selectElement) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        selectElement.disabled = true;
    }

    inventorySelect.addEventListener('change', () => {
        const inventoryId = inventorySelect.value;
        clearDropdown(groupSelect);
        clearDropdown(objectSelect);
        updateGroups(inventoryId);
    });

    groupSelect.addEventListener('change', () => {
        const groupId = groupSelect.value;
        clearDropdown(objectSelect);
        updateObjects(groupId);
    });

    function handleModalFormSubmit(modalSelector, callback) {
        const form = document.querySelector(`${modalSelector} form`);
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            if (!form.checkValidity()) {
                alert('Пожалуйста, заполните все обязательные поля.');
                return;
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                },
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка при отправке данных');
                return response.json();
            })
            .then(() => {
                closeModal(modalSelector.replace('#', ''));
                callback();
            })
            .catch(error => {
                console.error(error.message);
                alert('Произошла ошибка при сохранении данных.');
            });
        });
    }

    handleModalFormSubmit('#add-inventory-modal', updateInventoryList);

    handleModalFormSubmit('#add-group-modal', () => {
        const inventoryId = inventorySelect.value;
        updateGroups(inventoryId);
    });

    handleModalFormSubmit('#add-object-modal', () => {
        const groupId = groupSelect.value;
        updateObjects(groupId);
    });

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.style.display = 'block';
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };
});