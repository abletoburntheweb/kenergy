document.addEventListener('DOMContentLoaded', () => {
    const mainInventorySelect = document.getElementById('main-inventory-select');
    const mainGroupSelect = document.getElementById('main-group-select');
    const mainObjectSelect = document.getElementById('main-object-select');

    if (!mainInventorySelect) console.error('Элемент с id="main-inventory-select" не найден.');
    if (!mainGroupSelect) console.error('Элемент с id="main-group-select" не найден.');
    if (!mainObjectSelect) console.error('Элемент с id="main-object-select" не найден.');

    function populateDropdown(selectElement, data) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id_g || item.id_i || item.id_o;
            option.textContent = item.название;
            selectElement.appendChild(option);
        });
        selectElement.disabled = false;
    }

    function clearDropdown(selectElement) {
        selectElement.innerHTML = '<option value="">Выберите</option>';
        selectElement.disabled = true;
    }

    function updateGroups(inventoryId, groupSelect) {
    if (inventoryId) {
        console.log('Запрос групп для инвентаря:', inventoryId);
        fetch(`/api/groups/?inventory=${inventoryId}`)
            .then(response => {
                if (!response.ok) throw new Error(`Ошибка HTTP: ${response.status}`);
                return response.json();
            })
            .then(data => {
                console.log('Полученные группы:', data);
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
                })
                .catch(error => {
                    console.error('Ошибка при получении объектов:', error.message);
                    alert('Не удалось загрузить список объектов.');
                });
        } else {
            clearDropdown(objectSelect);
        }
    }

    function updateUrlParams(params) {
        const url = new URL(window.location.href);
        Object.keys(params).forEach(key => {
            if (params[key]) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        window.history.pushState({}, '', url);
    }

    function initializeFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        const inventoryId = urlParams.get('inventory');
        const groupId = urlParams.get('group');
        const objectId = urlParams.get('object');

        if (inventoryId) {
            mainInventorySelect.value = inventoryId;
            updateGroups(inventoryId, mainGroupSelect);
        }

        if (groupId) {
            mainGroupSelect.value = groupId;
            updateObjects(groupId, mainObjectSelect);
        }

        if (objectId) {
            mainObjectSelect.value = objectId;
            updateRegulationsAndDefects(objectId);
        }
    }

    if (mainInventorySelect && mainGroupSelect) {
        mainInventorySelect.addEventListener('change', () => {
            const inventoryId = mainInventorySelect.value;
            clearDropdown(mainGroupSelect);
            clearDropdown(mainObjectSelect);
            updateUrlParams({ inventory: inventoryId, group: null, object: null });
            if (inventoryId) {
                updateGroups(inventoryId, mainGroupSelect);
            }
        });
    }

    if (mainGroupSelect && mainObjectSelect) {
        mainGroupSelect.addEventListener('change', () => {
            const groupId = mainGroupSelect.value;
            clearDropdown(mainObjectSelect);
            updateUrlParams({ group: groupId, object: null });
            if (groupId) {
                updateObjects(groupId, mainObjectSelect);
            }
        });
    }

    if (mainObjectSelect) {
        mainObjectSelect.addEventListener('change', () => {
            const objectId = mainObjectSelect.value;
            updateUrlParams({ object: objectId });
            if (objectId) {
                updateRegulationsAndDefects(objectId);
            } else {
                document.querySelector('#regulations-table tbody').innerHTML = '';
                document.querySelector('#defects-table tbody').innerHTML = '';
            }
        });
    }

    initializeFromUrl();

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

document.querySelectorAll('.add-row-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tableId = button.getAttribute('data-table-id');
        const table = document.getElementById(tableId);
        const newRow = document.createElement('tr');

        if (tableId === 'regulations-table') {
            newRow.innerHTML = `
                <td><input type="text" name="standard[]" placeholder="Стандарт"></td>
                <td><input type="text" name="requirement[]" placeholder="Требование"></td>
                <td>
                    <button type="button" class="save-new-row-btn">+</button>
                    <button type="button" class="remove-row-btn">×</button>
                </td>
            `;
        } else if (tableId === 'defects-table') {
            newRow.innerHTML = `
                <td><input type="text" name="test[]" placeholder="Испытания"></td>
                <td><input type="text" name="recommendation[]" placeholder="Рекомендуемые действия"></td>
                <td><input type="number" name="metric[]" placeholder="Метрика" min="0"></td>
                <td>
                    <button type="button" class="save-new-row-btn">+</button>
                    <button type="button" class="remove-row-btn">×</button>
                </td>
            `;
        }

        table.querySelector('tbody').appendChild(newRow);

        newRow.querySelector('.save-new-row-btn').addEventListener('click', () => {
            const cells = newRow.querySelectorAll('td');
            const data = {};
            const objectId = document.getElementById('main-object-select').value;

            if (!objectId) {
                alert('Выберите объект перед сохранением.');
                return;
            }

            if (tableId === 'regulations-table') {
                data.standard = cells[0].querySelector('input').value.trim();
                data.requirement = cells[1].querySelector('input').value.trim();
            } else if (tableId === 'defects-table') {
                data.test = cells[0].querySelector('input').value.trim();
                data.recommendation = cells[1].querySelector('input').value.trim();
                data.metric = parseFloat(cells[2].querySelector('input').value.trim());
            }

            fetch('/save-new-row/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                },
                body: JSON.stringify({
                    object_id: objectId,
                    table: tableId,
                    data: data,
                }),
            })
            .then(response => {
                if (!response.ok) throw new Error('Ошибка при сохранении данных.');
                return response.json();
            })
            .then(result => {
                if (result.success) {
                    newRow.dataset.id = result.id;
                    cells[0].textContent = data.standard || data.test || '—';
                    cells[1].textContent = data.requirement || data.recommendation || '—';
                    if (tableId === 'defects-table') {
                        cells[2].textContent = data.metric || '—';
                    }
                    cells[cells.length - 1].innerHTML = `
                        <button type="button" class="edit-row-btn">✎</button>
                        <button type="button" class="remove-row-btn">×</button>
                    `;
                    alert('Строка успешно добавлена.');
                } else {
                    alert('Произошла ошибка при сохранении данных.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Не удалось сохранить строку.');
            });
        });

        newRow.querySelector('.remove-row-btn').addEventListener('click', () => {
            newRow.remove();
        });
    });
});
document.querySelector('.save-button').addEventListener('click', () => {
    const formData = collectFormData();
    if (!formData) return;

    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/save-object/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка при сохранении данных.');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Данные успешно сохранены.');
            updateRegulationsAndDefects(formData.object);
        } else {
            alert('Произошла ошибка при сохранении данных.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось сохранить данные.');
    });
});
    function updateRegulationsAndDefects(objectId) {
    fetch(`/api/regulations/?object=${objectId}`)
        .then(response => response.json())
        .then(data => {
            const regulationsTable = document.querySelector('#regulations-table tbody');
            regulationsTable.innerHTML = '';
            if (data.length === 0) {
                console.warn('Для объекта нет регламентов.');
                return;
            }
            data.forEach(regulation => {
                const row = regulationsTable.insertRow();
                row.dataset.id = regulation.id_s;
                row.insertCell(0).textContent = regulation.стандарт || '—';
                row.insertCell(1).textContent = regulation.требование || '—';
                row.insertCell(2).innerHTML = `
                    <button type="button" class="edit-row-btn">✎</button>
                    <button type="button" class="remove-row-btn">×</button>
                `;
            });
        })
        .catch(error => {
            console.error('Ошибка при получении регламентов:', error.message);
            alert('Не удалось загрузить список регламентов.');
        });

    fetch(`/api/defects/?object=${objectId}`)
        .then(response => response.json())
        .then(data => {
            const defectsTable = document.querySelector('#defects-table tbody');
            defectsTable.innerHTML = '';
            if (data.length === 0) {
                console.warn('Для объекта нет дефектов.');
                return;
            }
            data.forEach(defect => {
                const row = defectsTable.insertRow();
                row.dataset.id = defect.id_def;
                row.insertCell(0).textContent = defect.испытание || '—';
                row.insertCell(1).textContent = defect.рекомендация || '—';
                row.insertCell(2).textContent = defect.метрика || '—';
                row.insertCell(3).innerHTML = `
                    <button type="button" class="edit-row-btn">✎</button>
                    <button type="button" class="remove-row-btn">×</button>
                `;
            });
        })
        .catch(error => {
            console.error('Ошибка при получении дефектов:', error.message);
            alert('Не удалось загрузить список дефектов.');
        });
}

    initializeFromUrl();

document.addEventListener('click', (event) => {
    if (event.target.classList.contains('edit-row-btn')) {
        const row = event.target.closest('tr');
        const tableId = row.closest('table').id;
        const cells = row.querySelectorAll('td');
        let isEditing = false;

        cells.forEach((cell, index) => {
            if (index === cells.length - 1) return;
            if (cell.querySelector('input')) {
                isEditing = true;
                return;
            }
        });

        if (!isEditing) {
            cells.forEach((cell, index) => {
                if (index === cells.length - 1) return;
                const content = cell.textContent.trim();
                if (index === 2 && tableId === 'defects-table') {
                    cell.innerHTML = `<input type="number" value="${content}" placeholder="Метрика" min="0">`;
                } else {
                    cell.innerHTML = `<input type="text" value="${content}">`;
                }
            });
        } else {
            const data = {};
            cells.forEach((cell, index) => {
                if (index === cells.length - 1) return;
                const input = cell.querySelector('input');
                if (input) {
                    if (input.type === 'number') {
                        const value = parseFloat(input.value);
                        cell.textContent = isNaN(value) || value < 0 ? '' : value;
                        if (tableId === 'defects-table' && index === 2) {
                            data.metric = cell.textContent;
                        }
                    } else {
                        cell.textContent = input.value.trim();
                        if (tableId === 'regulations-table') {
                            if (index === 0) data.standard = cell.textContent;
                            if (index === 1) data.requirement = cell.textContent;
                        } else if (tableId === 'defects-table') {
                            if (index === 0) data.test = cell.textContent;
                            if (index === 1) data.recommendation = cell.textContent;
                        }
                    }
                }
            });

            saveRowChanges(row, tableId);
        }
    }

    if (event.target.classList.contains('remove-row-btn')) {
        const row = event.target.closest('tr');
        const tableId = row.closest('table').id;
        const cells = row.querySelectorAll('td');
        const data = {};

        if (tableId === 'regulations-table') {
            data.standard = cells[0].textContent.trim();
            data.requirement = cells[1].textContent.trim();
        } else if (tableId === 'defects-table') {
            data.test = cells[0].textContent.trim();
            data.recommendation = cells[1].textContent.trim();
            data.metric = parseFloat(cells[2].textContent.trim());
        }

        const objectId = document.getElementById('main-object-select').value;
        if (!objectId) {
            alert('Выберите объект перед удалением.');
            return;
        }

        fetch('/delete-row/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
            },
            body: JSON.stringify({
                object_id: objectId,
                table: tableId,
                data: data,
            }),
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка при удалении данных.');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Строка успешно удалена.');
                row.remove();
            } else {
                alert('Произошла ошибка при удалении данных.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось удалить строку.');
        });
    }
});
function collectFormData() {
    const inventory = document.getElementById('main-inventory-select').value;
    const group = document.getElementById('main-group-select').value;
    const object = document.getElementById('main-object-select').value;

    if (!inventory || !group || !object) {
        alert('Пожалуйста, выберите инвентарь, группу и объект.');
        return null;
    }

    const regulationsTable = document.querySelector('#regulations-table tbody');
    const regulations = Array.from(regulationsTable.rows).map(row => {
        const cells = row.cells;
        return {
            id_s: row.dataset.id,
            standard: cells[0].textContent.trim(),
            requirement: cells[1].textContent.trim(),
        };
    });

    const defectsTable = document.querySelector('#defects-table tbody');
    const defects = Array.from(defectsTable.rows).map(row => {
        const cells = row.cells;
        return {
            id_def: row.dataset.id,
            test: cells[0].textContent.trim(),
            recommendation: cells[1].textContent.trim(),
            metric: parseFloat(cells[2].textContent.trim()),
        };
    });

    return {
        inventory,
        group,
        object,
        standards: regulations,
        tests: defects,
    };
}
function saveRowChanges(row, tableId) {
    const cells = row.querySelectorAll('td');
    const rowId = row.dataset.id;
    if (!rowId) {
        alert('Ошибка: уникальный идентификатор строки отсутствует.');
        return;
    }

    const data = {};
    if (tableId === 'regulations-table') {
        data.standard = cells[0].textContent.trim();
        data.requirement = cells[1].textContent.trim();
    } else if (tableId === 'defects-table') {
        data.test = cells[0].textContent.trim();
        data.recommendation = cells[1].textContent.trim();
        data.metric = parseFloat(cells[2].textContent.trim());
    }
    data.id = rowId;

    const objectId = document.getElementById('main-object-select').value;
    if (!objectId) {
        alert('Выберите объект перед сохранением изменений.');
        return;
    }

    fetch('/update-row/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
        },
        body: JSON.stringify({
            object_id: objectId,
            table: tableId,
            data: data,
        }),
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка при сохранении данных.');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Изменения успешно сохранены.');
        } else {
            alert('Произошла ошибка при сохранении данных.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось сохранить изменения.');
    });
}

    document.addEventListener('input', (event) => {
        if (event.target.tagName === 'INPUT' && event.target.type === 'number') {
            const value = parseFloat(event.target.value);
            if (isNaN(value) || value < 0) {
                event.target.value = '';
            }
        }
    });
});