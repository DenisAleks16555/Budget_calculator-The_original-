// Убрал users, currentUser, expenses (локальный массив), login, addExpense и т.д. — теперь данные из Flask.

// Функция для загрузки расходов из Flask
async function loadExpenses() {
    try {
        const response = await fetch('/expenses');
        const expenses = await response.json();
        displayExpenses(expenses);
        updateTotal(expenses);
    } catch (error) {
        console.error('Ошибка загрузки расходов:', error);
    }
}

// Функция для отображения расходов в таблице
function displayExpenses(expenses) {
    const tableBody = document.getElementById('expensesBody');
    tableBody.innerHTML = ''; // Очистить таблицу
    expenses.forEach((exp) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${exp.description}</td>
            <td>${exp.amount}</td>
            <td>${exp.date}</td>
            <td>${exp.category || ''}</td>
            <td>
                <form method="POST" action="/delete/${exp.id}" style="display:inline;">
                    <button type="submit" onclick="return confirm('Удалить?')">Удалить</button>
                </form>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Функция для обновления итоговой суммы
function updateTotal(expenses) {
    const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    document.getElementById('totalAmount').textContent = total.toFixed(2);
}

// Фильтрация по дате
function filterByDate() {
    const dateInput = document.getElementById('filterDate').value;
    if (!dateInput) {
        alert('Введите дату для фильтрации');
        return;
    }
    loadExpenses().then(() => {
        const rows = Array.from(document.querySelectorAll('#expensesBody tr'));
        rows.forEach(row => {
            const dateCell = row.cells[2].textContent;
            row.style.display = dateCell === dateInput ? '' : 'none';
        });
    });
}

// Сортировка по сумме (убывающая)
function sortBySum() {
    loadExpenses().then(() => {
        const rows = Array.from(document.querySelectorAll('#expensesBody tr'));
        rows.sort((a, b) => parseFloat(b.cells[1].textContent) - parseFloat(a.cells[1].textContent));
        const tableBody = document.getElementById('expensesBody');
        tableBody.innerHTML = '';
        rows.forEach(row => tableBody.appendChild(row));
    });
}

// Сортировка по дате (возрастающая)
function sortByDate() {
    loadExpenses().then(() => {
        const rows = Array.from(document.querySelectorAll('#expensesBody tr'));
        rows.sort((a, b) => new Date(a.cells[2].textContent) - new Date(b.cells[2].textContent));
        const tableBody = document.getElementById('expensesBody');
        tableBody.innerHTML = '';
        rows.forEach(row => tableBody.appendChild(row));
    });
}

// Загрузить расходы при загрузке страницы
document.addEventListener('DOMContentLoaded', loadExpenses);











// // Можно добавить простые функции, например, подтверждение удаления
// document.addEventListener('DOMContentLoaded', () => {
//     const forms = document.querySelectorAll('form');
//     forms.forEach(form => {
//         form.addEventListener('submit', (e) => {
//             if(!confirm('Вы уверены, что хотите удалить этот расход?')) {
//                 e.preventDefault();
//             }
//         });
//     });
// });


// // Функция для обновления списка расходов
// function loadExpenses() {
//   fetch('/expenses')  // это URL, по которому сервер отдаст список расходов в JSON
//     .then(response => response.json())
//     .then(data => {
//       const tableBody = document.querySelector('.expenses-table tbody');
//       tableBody.innerHTML = '';  // очищаем текущие данные
//       data.forEach(expense => {
//         const row = document.createElement('tr');

//         row.innerHTML = `
//           <td>${expense.description}</td>
//           <td>${expense.amount}</td>
//           <td>${expense.date}</td>
//           <td>
//             <form method="POST" action="/delete/${expense.id}" style="display:inline;">
//               <button type="submit">Удалить</button>
//             </form>
//           </td>
//         `;
//         tableBody.appendChild(row);
//       });
//     });
// }

// // Вызывать функцию при загрузке страницы
// window.onload = () => {
//   loadExpenses();
// }


