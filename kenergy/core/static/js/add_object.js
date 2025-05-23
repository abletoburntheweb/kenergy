document.addEventListener('DOMContentLoaded', () => {
    // Кнопка добавления новой группы
    const addGroupButton = document.getElementById('add-group-button');
    if (addGroupButton) {
        addGroupButton.addEventListener('click', () => {
            alert('Открыть форму для добавления новой группы');
            // Здесь можно добавить логику для открытия модального окна
        });
    }

    // Кнопка добавления новой подгруппы
    const addSubgroupButton = document.getElementById('add-subgroup-button');
    if (addSubgroupButton) {
        addSubgroupButton.addEventListener('click', () => {
            alert('Открыть форму для добавления новой подгруппы');
            // Здесь можно добавить логику для открытия модального окна
        });
    }

    // Кнопка добавления нового объекта
    const addObjectButton = document.getElementById('add-object-button');
    if (addObjectButton) {
        addObjectButton.addEventListener('click', () => {
            alert('Открыть форму для добавления нового объекта');
            // Здесь можно добавить логику для открытия модального окна
        });
    }
});