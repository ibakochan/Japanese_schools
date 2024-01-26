$(document).on('submit', '.delete-form', function (e) {
    e.preventDefault();  

    var form = $(this);
    var formData = new FormData(form[0]);

    var url = form.data('url');

    $.ajax({
        type: form.attr('method'),
        url: url,
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data);

            form.closest('.custom-box').remove();
        },
        error: function (data) {
            console.log('Error:', data.responseJSON);
        }
    });
});