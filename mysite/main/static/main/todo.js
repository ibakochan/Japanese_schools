$('#to-do-list-form').submit(function (e) {
    e.preventDefault();

    var form = $(this);
    var formData = new FormData(form[0]);

    formData.delete('csrfmiddlewaretoken');
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    formData.append('csrfmiddlewaretoken', csrfToken);

    var url = form.data('url');

    $.ajax({
        type: form.attr('method'),
        url: url,
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data);

            form.trigger('reset');

            var newItem = '<div class="custom-box card border border-dark mb-3">' +
                '<div class="card-body d-flex align-items-center">' +
                '<span style="color: black; font-weight: bold; margin-right: auto;">' + data.title + '</span>' +
                '<form class="ml-auto delete-form" data-url="{% url "main:to_do_delete" 0 %}" data-pk="' + data.pk + '" method="POST">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrfToken + '">' +
                '<button type="submit" class="btn btn-danger" style="width: 120px;">Erase todo</button>' +
                '</form>' +
                '</div>' +
                '</div>';

            newItem = newItem.replace('{% url "main:to_do_delete" 0 %}', '/todo/' + data.pk + '/delete');

            $('#scroll-target .custom-section').append(newItem);
        },
        error: function (xhr, status, error) {
            console.log('Error:', xhr.responseJSON);

            var errorUrl = form.data('url');
            console.log('Error URL:', errorUrl);

            alert('An error occurred: ' + xhr.statusText);
        }
    });
});
