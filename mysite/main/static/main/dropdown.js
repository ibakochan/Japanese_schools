document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('change', function (event) {
        if (event.target.id === 'category-dropdown') {
            var selectedCategory = event.target.value;
            var categorySections = document.querySelectorAll('.category-section');
            categorySections.forEach(function (section) {
                section.style.display = section.getAttribute('data-category') === selectedCategory ? 'block' : 'none';
            });
        }
    });
});