// core/static/js/add_object.js
document.addEventListener('DOMContentLoaded', () => {
    // Добавление строки в таблицу регламентов
    const regulationsTable = document.getElementById('regulations-table');
    const addRegulationButton = document.querySelector('.section:nth-child(2) .add-row-button');

    addRegulationButton.addEventListener('click', () => {
        const newRow = `
            <tr>
                <td><input type="text" name="standard" placeholder="Стандарт"></td>
                <td><input type="text" name="requirement" placeholder="Требование"></td>
                <td><button type="button" class="remove-button">×</button></td>
            </tr>
        `;
        regulationsTable.querySelector('tbody').insertAdjacentHTML('beforeend', newRow);

        // Добавляем обработчик события для кнопки удаления
        regulationsTable.querySelectorAll('.remove-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.target.closest('tr').remove();
            });
        });
    });

    // Добавление строки в таблицу дефектов
    const defectsTable = document.getElementById('defects-table');
    const addDefectButton = document.querySelector('.section:nth-child(3) .add-row-button');

    addDefectButton.addEventListener('click', () => {
        const newRow = `
            <tr>
                <td><input type="text" name="test" placeholder="Испытания"></td>
                <td><input type="text" name="recommendation" placeholder="Рекомендуемые действия"></td>
                <td><input type="number" name="metric" placeholder="Метрика"></td>
                <td><button type="button" class="remove-button">×</button></td>
            </tr>
        `;
        defectsTable.querySelector('tbody').insertAdjacentHTML('beforeend', newRow);

        // Добавляем обработчик события для кнопки удаления
        defectsTable.querySelectorAll('.remove-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.target.closest('tr').remove();
            });
        });
    });
});