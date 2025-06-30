document.addEventListener('DOMContentLoaded', () => {
    const table = document.querySelector('table');
    if (!table) return;
    const tbody = table.querySelector('tbody');
    const headers = table.querySelectorAll('thead th');
    const allRows = Array.from(tbody.querySelectorAll('tr'));
    const sortDir = Array(headers.length).fill('asc');

    headers.forEach((th, idx) => {
        th.classList.add('cursor-pointer');
        th.addEventListener('click', () => sortByColumn(idx));
    });

    function getCellValue(row, index) {
        const text = row.children[index].textContent.trim();
        if (index === 2 || index === 4) {
            return new Date(text);
        }
        if (index === 7) {
            const order = { 'Pending': 0, 'Approved': 1, 'Rejected': 2, 'Expired': 3 };
            return order[text] ?? 99;
        }
        return text.toLowerCase();
    }

    function sortByColumn(index) {
        const dir = sortDir[index] === 'asc' ? 1 : -1;
        const rows = Array.from(tbody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const av = getCellValue(a, index);
            const bv = getCellValue(b, index);
            if (av < bv) return -1 * dir;
            if (av > bv) return 1 * dir;
            return 0;
        });
        sortDir[index] = sortDir[index] === 'asc' ? 'desc' : 'asc';
        rows.forEach(r => tbody.appendChild(r));
    }

    const fromInput = document.getElementById('filter-from');
    const toInput = document.getElementById('filter-to');
    const statusSelect = document.getElementById('status-filter');

    function applyFilters() {
        const from = fromInput && fromInput.value ? new Date(fromInput.value) : null;
        const to = toInput && toInput.value ? new Date(toInput.value) : null;
        const status = statusSelect ? statusSelect.value : 'All';

        allRows.forEach(row => {
            const outDate = new Date(row.children[2].textContent.trim());
            const rowStatus = row.children[7].textContent.trim();
            let show = true;
            if (from && outDate < from) show = false;
            if (show && to && outDate > to) show = false;
            if (show && status !== 'All' && rowStatus !== status) show = false;
            row.style.display = show ? '' : 'none';
        });
    }

    [fromInput, toInput, statusSelect].forEach(el => {
        if (el) el.addEventListener('change', applyFilters);
    });
});
