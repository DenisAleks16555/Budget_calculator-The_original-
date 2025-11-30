// const users = [
//   { username: "ivan", password: "123", expenses: [] },
//   { username: "maria", password: "abc", expenses: [] },
// ];

// let currentUser = null; // Сейчас никто не вошёл


// let expenses = [
//     // пример данных
//   { description: "Обед", amount: 10, date: "2023-10-01", category: "Еда" },
//   { description: "Такси", amount: 5, date: "2023-10-02", category: "Транспорт" },
//   { description: "Кино", amount: 15, date: "2023-10-01", category: "Развлечения" },
// ];


// function login() {
//   const username = document.getElementById('username').value;
//   const password = document.getElementById('password').value;
  
//   const user = users.find(u => u.username === username && u.password === password);
  
//   if (user) {
//     currentUser = user;
//     document.getElementById('loginSection').style.display = 'none'; // скрыть вход
//     document.getElementById('appSection').style.display = 'block'; // показать расходы
//     displayExpenses(currentUser.expenses);
//   } else {
//     alert('Неверное имя или пароль');
//   }
// }


function displayExpenses(expenses) {
  const tableBody = document.getElementById('expensesBody');
  tableBody.innerHTML = ''; // очистить старое
  expenses.forEach((exp, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${exp.description}</td>
      <td>${exp.amount}</td>
      <td>${exp.date}</td>
      <td contenteditable="true" onblur="updateCategory(${index}, this.innerText)">${exp.category || ''}</td>
      <td>
        <button onclick="deleteExpense(${index})">Удалить</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

function updateCategory(index, newCategory) {
  if (currentUser) {
    currentUser.expenses[index].category = newCategory;
    // тут можно сохранить в localStorage или базу
  }
}

function addExpense(description, amount, date, category) {
  if (currentUser) {
    currentUser.expenses.push({ description, amount, date, category });
    displayExpenses(currentUser.expenses);
  }
}
// function displayExpenses(filteredExpenses) {
//   // эта функция показывает расходы на странице
//   const tableBody = document.getElementById('expensesBody');
//   tableBody.innerHTML = '';
//   filteredExpenses.forEach((exp, index) => {
//     const row = `<tr>
//       <td>${exp.description}</td>
//       <td>${exp.amount}</td>
//       <td>${exp.date}</td>
//       <td contenteditable="true" onblur="updateCategory(${index}, this.innerText)">${exp.category}</td>
//     </tr>`;
//     tableBody.innerHTML += row;
//   });
// }

// Создайте функцию для обновления категории
function updateCategory(index, newCategory) {
  expenses[index].category = newCategory;
  // Можно дополнительно сохранять в localStorage или базу данных
}

// функция для фильтрации по дате
function filterByDate() {
  const dateInput = document.getElementById('filterDate').value;
  const filtered = expenses.filter(exp => exp.date === dateInput);
  displayExpenses(filtered);
}

// функция для сортировки по сумме
function sortBySum() {
  const sorted = [...expenses].sort((a, b) => b.amount - a.amount);
  displayExpenses(sorted);
}

// функция для сортировки по дате
function sortByDate() {
  const sorted = [...expenses].sort((a, b) => new Date(a.date) - new Date(b.date));
  displayExpenses(sorted);
}













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


