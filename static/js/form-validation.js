document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) {
        const phoneError = document.getElementById('phone-error');
        const phonePattern = /^[0-9]{10}$/;
        phoneInput.addEventListener('input', () => {
            if (phonePattern.test(phoneInput.value)) {
                phoneError.textContent = '';
            } else {
                phoneError.textContent = 'Enter a valid 10-digit phone number';
            }
        });
    }

    const outDate = document.querySelector('input[name="outgoing_date"]');
    const outTime = document.querySelector('input[name="outgoing_time"]');
    const inDate = document.querySelector('input[name="ingoing_date"]');
    const inTime = document.querySelector('input[name="ingoing_time"]');
    if (outDate && outTime && inDate && inTime) {
        const dtError = document.getElementById('datetime-error');
        function validateDatetime() {
            if (!outDate.value || !outTime.value || !inDate.value || !inTime.value) {
                dtError.textContent = '';
                return;
            }
            const start = new Date(`${outDate.value}T${outTime.value}`);
            const end = new Date(`${inDate.value}T${inTime.value}`);
            if (start <= end) {
                dtError.textContent = '';
            } else {
                dtError.textContent = 'Ingoing date/time must be after outgoing date/time';
            }
        }
        outDate.addEventListener('change', validateDatetime);
        outTime.addEventListener('change', validateDatetime);
        inDate.addEventListener('change', validateDatetime);
        inTime.addEventListener('change', validateDatetime);
    }
});
