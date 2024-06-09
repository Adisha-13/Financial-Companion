document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('expense-form');
    const expenseList = document.getElementById('expense-list');
    const expenseCounter = document.getElementById('expense-counter');
    
    let totalExpenses = 0;

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const amountInput = document.getElementById('amount');
        const spentOnInput = document.getElementById('spentOn');
        
        const amount = parseFloat(amountInput.value);
        const spentOn = spentOnInput.value;
        
        if (isNaN(amount) || amount <= 0 || spentOn.trim() === '') {
            alert('Please enter a valid amount and description.');
            return;
        }

        totalExpenses += amount;
        expenseCounter.textContent = totalExpenses.toFixed(2);

        const listItem = document.createElement('li');
        listItem.innerHTML = `<span>${spentOn}</span><span>${amount.toFixed(2)}</span>`;
        expenseList.appendChild(listItem);

        amountInput.value = '';
        spentOnInput.value = '';
    });
});