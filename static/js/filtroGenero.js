function filtrarGenero() {
            const input = document.getElementById('myInput');
            const filter = input.value.toUpperCase();
            const items = document.querySelectorAll('.dropdown-item');
            items.forEach(item => {
                const text = item.textContent || item.innerText;
                item.style.display = text.toUpperCase().indexOf(filter) > -1 ? '' : 'none';
            });
        }