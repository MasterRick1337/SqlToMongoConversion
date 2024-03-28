function getData() {
    const category = document.getElementById('category').value;
    fetch(`http://localhost:5000/api/data/${category}`)
        .then(response => response.json())
        .then(dataString => {
            const data = JSON.parse(dataString);

            const tableHeaders = document.getElementById('tableHeaders');
            const tableBody = document.getElementById('tableBody');
            const filterInput = document.getElementById('filterInput');
            const filterOptions = document.getElementById('filterOptions');

            tableHeaders.innerHTML = '';
            tableBody.innerHTML = '';
            filterOptions.innerHTML = '';

            const headers = Object.keys(data[0]);
            const headerRow = document.createElement('tr');
            headers.forEach(headerText => {
                const header = document.createElement('th');
                header.textContent = headerText;
                headerRow.appendChild(header);

                header.addEventListener('click', () => {
                    sortTable(headerText, data);
                });

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `filter_${headerText}`;
                checkbox.value = headerText;
                const label = document.createElement('label');
                label.textContent = headerText;
                label.htmlFor = `filter_${headerText}`;
                filterOptions.appendChild(checkbox);
                filterOptions.appendChild(label);
                filterOptions.appendChild(document.createElement('br'));
            });
            tableHeaders.appendChild(headerRow);

            renderTable(headers, data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function renderTable(headers, data) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        headers.forEach(header => {
            const cell = document.createElement('td');
            cell.textContent = item[header];
            row.appendChild(cell);
        });
        tableBody.appendChild(row);
    });
}

function sortTable(column, data) {
    data.sort((a, b) => {
        const valueA = a[column];
        const valueB = b[column];
        if (valueA < valueB) {
            return -1;
        }
        if (valueA > valueB) {
            return 1;
        }
        return 0;
    });
    renderTable(Object.keys(data[0]), data);
}

function applyFilter() {
    const filterInput = document.getElementById('filterInput');
    const filterValue = filterInput.value.toLowerCase();
    const filterOptions = document.querySelectorAll('#filterOptions input[type="checkbox"]:checked');
    const headersToFilter = Array.from(filterOptions).map(option => option.value);

    const category = document.getElementById('category').value;
    fetch(`http://localhost:5000/api/data/${category}`)
        .then(response => response.json())
        .then(dataString => {
            const data = JSON.parse(dataString);

            const filteredData = data.filter(item => {
                return headersToFilter.some(header => {
                    return item[header].toString().toLowerCase().includes(filterValue);
                });
            });

            const headers = Object.keys(data[0]);
            renderTable(headers, filteredData);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
