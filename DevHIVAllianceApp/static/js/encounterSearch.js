$(function() {

    // Get the form.
    var form = $('#encounter-search');

    // Get the messages div.
    var formErrors = $('#form-errors');

    // Set up an event listener for the contact form.
    $(form).submit(function(event) {
        // Stop the browser from submitting the form.
        event.preventDefault();

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
            type: 'GET',
            url: $(form).attr('action'),
            data: formData
        }).done(function(response) {
            // Set the message text.
            if(!(response && response != "[]")) {
                $(formMessages).text("Empty Response");
            } else {
                var encounters = JSON.parse(response);

                var encounterReportTable = $("#encounter-report-table-body");
                encounterReportTable.empty();
                
                tableBodyRowDiv = '<div class="report-table-body-row"></div>'

                encounterLength = encounters.length
                for (var i = 0; i < encounterLength; ++i) {
                    row = $(encounterReportTable).append(tableBodyRowDiv)
                    if (i % 2 == 0) {
                        cell_open_div = '<div class="report-table-body-cell">'
                    } else {
                        cell_open_div = '<div class="highlight-row report-table-body-cell">'
                    }

                    row.append(cell_open_div + encounters[i].today + '</div>');
                    row.append(cell_open_div + encounters[i].staff_initials + '</div>');
                    row.append(cell_open_div + encounters[i].location + '</div>');
                    row.append(cell_open_div + encounters[i].has_used_shared_needles + '</div>');
                    row.append(cell_open_div + encounters[i].syringes_brought_in + '</div>');
                    row.append(cell_open_div + encounters[i].syringes_taken + '</div>');
                    row.append(cell_open_div + encounters[i].is_homeless + '</div>');
                };
            }
            
        }).fail(function(data) {        
            // Set the message text.
            if (data.responseText !== '') {
                $(formErrors).text(data.responseText);
            } else {
                $(formErrors).text('Oops! An error occured and your message could not be sent.');
            }
        });
    });
});




