document.addEventListener('DOMContentLoaded', () => {
    const inputReg = document.querySelector('input[name="reg"]');

    const textContainer = document.getElementById('days').parentNode;

    inputReg.addEventListener('input', function() {
        let sanitizedValue = this.value.replace(/\D/g, '');
        
        this.value = sanitizedValue; 

        let amount = parseInt(sanitizedValue);

        if (isNaN(amount) || amount === 0) return;

        const truckCapacity = parseInt(this.dataset.capacity);
        
        let deliveriesPerMonth = amount / truckCapacity;
        let daysBetween = 30 / deliveriesPerMonth;

        if (daysBetween >= 1) {
            textContainer.innerHTML = `Буде доставлятись регулярно: по <span class="font-bold text-indigo-600">${truckCapacity}</span> од., кожні <mark id="days" class="bg-indigo-100 text-indigo-800 px-1 rounded font-bold">${Math.round(daysBetween)}</mark> днів.`;
        } else {
            let dailyAmount = Math.ceil(amount / 30); 
            textContainer.innerHTML = `Буде доставлятись <mark id="days" class="bg-indigo-100 text-indigo-600 px-1 rounded font-bold">Щодня</mark>: по <span class="font-bold text-indigo-600">${dailyAmount}</span> од.`;
        }
        
    });

    const inputTerm = document.querySelector('input[name="term"]');
    
    if (inputTerm) {
        inputTerm.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, '');
        });
    }
});