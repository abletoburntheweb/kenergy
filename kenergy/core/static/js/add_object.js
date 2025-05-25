document.addEventListener('DOMContentLoaded', () => {
    // Получение элементов DOM
    const mainInventorySelect = document.getElementById('main-inventory-select');
    const mainGroupSelect = document.getElementById('main-group-select');
    const mainObjectSelect = document.getElementById('main-object-select');
    const modalInventorySelect = document.getElementById('modal-inventory-select');
    const modalGroupSelect = document.getElementById('modal-group-select');

    // Проверка существования элементов
    if (!mainInventorySelect) console.error('Элемент с id="main-inventory-select" не найден.');
    if (!mainGroupSelect) console.error('Элемент с id="main-group-select" не найден.');
    if (!mainObjectSelect) console.error('Элемент с id="main-object-select" не найден.');
    if (!modalInventorySelect) console.error('Элемент с id="modal-inventory-select" не найден.');
    if (!modalGroupSelect) console.error('Элемент с id="modal-group-select" не найден.');

    // Инициализация выпадающих списков
    mainGroupSelect.innerHTML = '<option value="">Выберите группу</option>';
    mainObjectSelect.innerHTML = '<option value="">Выберите объект</option>';
    modalGroupSelect.innerHTML = '<option value="">Выберите группу</option>';

    // Функция для заполнения выпадающего списка
    function populateDropdown(selectElement, data) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id_g || item.id_i || item.id_o; // Убедитесь, что передается правильный атрибут
            option.textContent = item.название;
            selectElement.appendChild(option);
        });
        selectElement.disabled = false;
    }

    // Функция для очистки выпадающего списка
    function clearDropdown(selectElement) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        selectElement.disabled = true;
    }

    // Обновление списка групп при выборе инвентаря
    function updateGroups(inventoryId, groupSelect) {
        if (inventoryId) {
            fetch(`/api/groups/?inventory=${inventoryId}`)
                .then(response => {
                    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log('Полученные группы:', data); // Логирование данных
                    populateDropdown(groupSelect, data);
                })
                .catch(error => {
                    console.error('Ошибка при получении групп:', error.message);
                    alert('Не удалось загрузить список групп.');
                });
        } else {
            clearDropdown(groupSelect);
        }
    }

    // Обновление списка объектов при выборе группы
    function updateObjects(groupId, objectSelect) {
        if (groupId) {
            fetch(`/api/objects/?group=${groupId}`)
                .then(response => {
                    if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    console.log('Полученные объекты:', data); // Логирование данных
                    populateDropdown(objectSelect, data);
                })
                .catch(error => {
                    console.error('Ошибка при получении объектов:', error.message);
                    alert('Не удалось загрузить список объектов.');
                });
        } else {
            clearDropdown(objectSelect);
        }
    }

    // Основной интерфейс: выбор инвентаря
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

    // Основной интерфейс: выбор группы
    if (mainGroupSelect && mainObjectSelect) {
        mainGroupSelect.addEventListener('change', () => {
            const groupId = mainGroupSelect.value;
            clearDropdown(mainObjectSelect);
            if (groupId) {
                updateObjects(groupId, mainObjectSelect);
            }
        });
    }

    // Модальное окно "Добавить объект": выбор инвентаря
    if (modalInventorySelect && modalGroupSelect) {
        modalInventorySelect.addEventListener('change', () => {
            const inventoryId = modalInventorySelect.value;
            clearDropdown(modalGroupSelect);
            if (inventoryId) {
                updateGroups(inventoryId, modalGroupSelect);
            }
        });
    }

    // Функция для обработки отправки модальных форм
    function handleModalFormSubmit(modalSelector, selectId, callback) {
        const modal = document.querySelector(modalSelector);
        const form = modal.querySelector('form');
        if (!modal || !form) {
            console.error(`Модальное окно или форма с селектором "${modalSelector}" не найдены.`);
            return;
        }
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(form);
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

    // Обработка отправки формы добавления инвентаря
    handleModalFormSubmit('#add-inventory-modal', 'main-inventory-select', () => {
        updateGroups(mainInventorySelect.value, mainGroupSelect);
    });

    // Обработка отправки формы добавления группы
    handleModalFormSubmit('#add-group-modal', 'main-group-select', () => {
        updateObjects(mainGroupSelect.value, mainObjectSelect);
    });

    // Обработка отправки формы добавления объекта
    handleModalFormSubmit('#add-object-modal', 'main-object-select');

    // Функции для открытия и закрытия модальных окон
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

    // Закрытие модального окна при клике вне его области
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };

    // Добавление строки в таблицу
document.querySelectorAll('.add-row-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tableId = button.getAttribute('data-table-id');
        const table = document.getElementById(tableId);

        // Создаем новую строку
        const newRow = document.createElement('tr');

        // Добавляем ячейки (td) в новую строку
        if (tableId === 'regulations-table') {
            newRow.innerHTML = `
                <td><input type="text" name="standard[]" placeholder="Стандарт"></td>
                <td><input type="text" name="requirement[]" placeholder="Требование"></td>
                <td><button type="button" class="remove-row-btn">×</button></td>
            `;
        } else if (tableId === 'defects-table') {
            newRow.innerHTML = `
                <td><input type="text" name="test[]" placeholder="Испытания"></td>
                <td><input type="text" name="recommendation[]" placeholder="Рекомендуемые действия"></td>
                <td><input type="number" name="metric[]" placeholder="Метрика"></td>
                <td><button type="button" class="remove-row-btn">×</button></td>
            `;
        }

        // Добавляем новую строку в таблицу
        table.querySelector('tbody').appendChild(newRow);
    });
});

// Удаление строки из таблицы (делегирование событий)
document.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-row-btn')) {
        const row = event.target.closest('tr');
        if (row.parentNode.children.length > 1) {
            row.remove();
        }
    }
});

    // Удаление строки из таблицы (используем делегирование событий)
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-row-btn')) {
            const row = event.target.closest('tr');
            if (row.parentNode.children.length > 1) {
                row.remove();
            }
        }
    });

    // Функция для сохранения данных
    document.querySelector('.save-button').addEventListener('click', () => {
        const inventory = document.getElementById('main-inventory-select').value;
        const group = document.getElementById('main-group-select').value;
        const object = document.getElementById('main-object-select').value;

        if (!inventory || !group || !object) {
            alert('Пожалуйста, выберите инвентарь, группу и объект.');
            return;
        }

        const standards = Array.from(document.querySelectorAll('[name="standard[]"]')).map(input => input.value.trim());
        const requirements = Array.from(document.querySelectorAll('[name="requirement[]"]')).map(input => input.value.trim());
        const tests = Array.from(document.querySelectorAll('[name="test[]"]')).map(input => input.value.trim());
        const recommendations = Array.from(document.querySelectorAll('[name="recommendation[]"]')).map(input => input.value.trim());
        const metrics = Array.from(document.querySelectorAll('[name="metric[]"]')).map(input => input.value.trim());

        // Проверка, что все обязательные поля заполнены
        if (
            standards.some(value => value === '') ||
            requirements.some(value => value === '') ||
            tests.some(value => value === '') ||
            recommendations.some(value => value === '') ||
            metrics.some(value => value === '')
        ) {
            alert('Пожалуйста, заполните все обязательные поля.');
            return;
        }

        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

        // Создаем объект FormData
        const formData = new FormData();
        formData.append('inventory', inventory);
        formData.append('group', group);
        formData.append('object', object);
        standards.forEach((standard, index) => formData.append(`standard[]`, standard));
        requirements.forEach((requirement, index) => formData.append(`requirement[]`, requirement));
        tests.forEach((test, index) => formData.append(`test[]`, test));
        recommendations.forEach((recommendation, index) => formData.append(`recommendation[]`, recommendation));
        metrics.forEach((metric, index) => formData.append(`metric[]`, metric));

        fetch('/save-object/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при сохранении данных.');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Данные успешно сохранены.');
                // Обновление таблиц регламентов и дефектов
                updateRegulationsAndDefects(object);
            } else {
                alert('Произошла ошибка при сохранении данных.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось сохранить данные.');
        });
    });

    // Функция для обновления таблиц регламентов и дефектов
    function updateRegulationsAndDefects(objectId) {
        // Загрузка регламентов
        fetch(`/api/regulations/?object=${objectId}`)
            .then(response => response.json())
            .then(data => {
                const regulationsTable = document.querySelector('#regulations-table tbody');
                regulationsTable.innerHTML = ''; // Очистка таблицы
                if (data.length === 0) {
                    console.warn('Для объекта нет регламентов.');
                    return;
                }
                data.forEach(regulation => {
                    const row = regulationsTable.insertRow();
                    row.insertCell(0).textContent = regulation.стандарт || '—';
                    row.insertCell(1).textContent = regulation.требование || '—';
                    row.insertCell(2).innerHTML = '<button type="button" class="remove-row-btn">×</button>';
                });
            })
            .catch(error => {
                console.error('Ошибка при получении регламентов:', error.message);
                alert('Не удалось загрузить список регламентов.');
            });

        // Загрузка дефектов
        fetch(`/api/defects/?object=${objectId}`)
            .then(response => response.json())
            .then(data => {
                const defectsTable = document.querySelector('#defects-table tbody');
                defectsTable.innerHTML = ''; // Очистка таблицы
                if (data.length === 0) {
                    console.warn('Для объекта нет дефектов.');
                    return;
                }
                data.forEach(defect => {
                    const row = defectsTable.insertRow();
                    row.insertCell(0).textContent = defect.испытание || '—';
                    row.insertCell(1).textContent = defect.рекомендация || '—';
                    row.insertCell(2).textContent = defect.метрика || '—';
                    row.insertCell(3).innerHTML = '<button type="button" class="remove-row-btn">×</button>';
                });
            })
            .catch(error => {
                console.error('Ошибка при получении дефектов:', error.message);
                alert('Не удалось загрузить список дефектов.');
            });
    }

    // Загрузка данных при инициализации страницы
    const selectedObjectId = mainObjectSelect.value;
    if (selectedObjectId) {
        updateRegulationsAndDefects(selectedObjectId);
    }

    // Обновление таблиц при выборе объекта
    mainObjectSelect.addEventListener('change', () => {
        const objectId = mainObjectSelect.value;
        if (objectId) {
            updateRegulationsAndDefects(objectId);
        } else {
            document.querySelector('#regulations-table tbody').innerHTML = '';
            document.querySelector('#defects-table tbody').innerHTML = '';
        }
    });
});