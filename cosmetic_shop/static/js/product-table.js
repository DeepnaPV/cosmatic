document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    const table = document.getElementById('products-table');
    const tbody = table.querySelector('tbody');
    const searchInput = document.getElementById('search-input');
    const entriesPerPageSelect = document.getElementById('entries-per-page');
    const paginationContainer = document.getElementById('pagination');
    const showingEntries = document.getElementById('showing-entries');
    const totalProductsSpan = document.getElementById('total-products');
    const noProductsRow = document.getElementById('no-products');

    if (!table || !tbody || !searchInput || !entriesPerPageSelect || !paginationContainer || !showingEntries || !totalProductsSpan) {
        console.error('One or more required elements are missing from the DOM');
        return;
    }

    console.log('All required elements found in the DOM');

    let allRows = Array.from(tbody.querySelectorAll('tr:not(#no-products)'));
    console.log(`Total rows found: ${allRows.length}`);

    let currentPage = 1;
    let entriesPerPage = parseInt(entriesPerPageSelect.value);

    function updateTable() {
        console.log('Updating table');
        const searchTerm = searchInput.value.toLowerCase();
        console.log(`Search term: "${searchTerm}"`);

        const filteredRows = allRows.filter(row => 
            Array.from(row.cells).some(cell => 
                cell.textContent.toLowerCase().includes(searchTerm)
            )
        );
        console.log(`Filtered rows: ${filteredRows.length}`);

        const totalPages = Math.ceil(filteredRows.length / entriesPerPage);
        const startIndex = (currentPage - 1) * entriesPerPage;
        const endIndex = Math.min(startIndex + entriesPerPage, filteredRows.length);
        const visibleRows = filteredRows.slice(startIndex, endIndex);

        console.log(`Displaying rows ${startIndex + 1} to ${endIndex}`);

        tbody.innerHTML = '';
        if (visibleRows.length === 0) {
            console.log('No matching rows, displaying "No products" message');
            noProductsRow.style.display = '';
            tbody.appendChild(noProductsRow);
        } else {
            noProductsRow.style.display = 'none';
            visibleRows.forEach(row => tbody.appendChild(row));
        }

        updatePagination(totalPages);
        updateShowingEntries(startIndex + 1, endIndex, filteredRows.length);
        totalProductsSpan.textContent = filteredRows.length;
    }

    function updatePagination(totalPages) {
        console.log(`Updating pagination. Total pages: ${totalPages}`);
        paginationContainer.innerHTML = '';
        if (totalPages > 1) {
            for (let i = 1; i <= totalPages; i++) {
                const li = document.createElement('li');
                li.classList.add('datatable-pagination-list-item');
                if (i === currentPage) li.classList.add('datatable-active');
                const button = document.createElement('button');
                button.textContent = i;
                button.addEventListener('click', () => {
                    currentPage = i;
                    updateTable();
                });
                li.appendChild(button);
                paginationContainer.appendChild(li);
            }
        }
    }

    function updateShowingEntries(start, end, total) {
        showingEntries.textContent = `Showing ${start} to ${end} of ${total} entries`;
    }

    function sortTable(column, direction) {
        console.log(`Sorting table. Column: ${column}, Direction: ${direction}`);
        allRows.sort((a, b) => {
            const aValue = a.cells[column].textContent;
            const bValue = b.cells[column].textContent;
            return direction === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        });
        updateTable();
    }

    searchInput.addEventListener('input', () => {
        console.log('Search input changed');
        currentPage = 1;
        updateTable();
    });

    entriesPerPageSelect.addEventListener('change', () => {
        console.log('Entries per page changed');
        entriesPerPage = parseInt(entriesPerPageSelect.value);
        currentPage = 1;
        updateTable();
    });

    table.querySelectorAll('th[data-sortable="true"]').forEach(th => {
        th.addEventListener('click', () => {
            const column = Array.from(th.parentNode.children).indexOf(th);
            const currentDirection = th.getAttribute('data-direction') || 'asc';
            const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
            th.setAttribute('data-direction', newDirection);
            sortTable(column, newDirection);
        });
    });

    console.log('Initial table update');
    updateTable();
});