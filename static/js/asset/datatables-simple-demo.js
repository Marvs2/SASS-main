window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple, {
            // Enable pagination
            paging: true,
            
            // Enable length menu
            perPage: 10, // Change this value as needed
            
            // Enable searching
            searchable: true,
            
            // Enable ordering (sorting)
            sortable: true,
            
            // Customize the labels for pagination, searching, and length menu
            labels: {
                placeholder: 'Search...',
                perPage: ' entries',
                noRows: 'No entries found',
                info: 'Showing {start} to {end} of {rows} entries',
                
                // Customize the length menu with "Previous" and "Next" options
                lengthMenu: [
                    ['Previous', 10, 25, 50, 100, -1, 'Next'],
                    ['Previous', 10, 25, 50, 100, 'All', 'Next'],
                ],
            },
     
        });
    }
});
