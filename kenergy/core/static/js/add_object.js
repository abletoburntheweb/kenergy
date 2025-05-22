// core/static/js/add_object.js
document.addEventListener('DOMContentLoaded', () => {
    const addRegulationButton = document.querySelector('#regulations-table + .add-row-btn');
    const regulationsTable = document.getElementById('regulations-table');

    addRegulationButton.addEventListener('click', () => {
        const newRow = `
            <tr>
                <td><input type="text" name="standard" placeholder="Стандарт" class="full-width-input"></td>
                <td><input type="text" name="requirement" placeholder="Требование" class="full-width-input"></td>
                <td><button type="button" class="remove-row-btn">×</button></td>
            </tr>
        `;
        regulationsTable.querySelector('tbody').insertAdjacentHTML('beforeend', newRow);

        regulationsTable.querySelectorAll('.remove-row-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.target.closest('tr').remove();
            });
        });
    });

    const addDefectButton = document.querySelector('#defects-table + .add-row-btn');
    const defectsTable = document.getElementById('defects-table');

    addDefectButton.addEventListener('click', () => {
        const newRow = `
            <tr>
                <td><input type="text" name="test" placeholder="Испытания" class="full-width-input"></td>
                <td><input type="text" name="recommendation" placeholder="Рекомендуемые действия" class="full-width-input"></td>
                <td><input type="number" name="metric" placeholder="Метрика" class="full-width-input"></td>
                <td><button type="button" class="remove-row-btn">×</button></td>
            </tr>
        `;
        defectsTable.querySelector('tbody').insertAdjacentHTML('beforeend', newRow);

        defectsTable.querySelectorAll('.remove-row-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.target.closest('tr').remove();
            });
        });
    });
});