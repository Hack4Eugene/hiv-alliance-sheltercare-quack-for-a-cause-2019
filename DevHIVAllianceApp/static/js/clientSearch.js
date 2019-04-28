$(function() {

    // Get the form.
    var form = $('#client-search');

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

            $("#search-results").empty();

            // Set the message text.
            if(!(response && response != "[]")) {
                $(formErrors).text("No clients found").show().delay(5000).fadeOut();
            } else {
                var jsonData = JSON.parse(response);

                jsonData.forEach(element => {
                    $("#search-results").append(
                        ([
                            "<div class='wrap-client'>",
                                "<div class='view-btn-wrapper'>",
                                    ("<button class='edit-btn' onclick=\"location.href='client?client_id=" + element._id + "'\">View</button>"),
                                "</div>",
                                "<div class='content-wrap'>",
                                    "<div id='last_name'>",
                                        "Last Name: ",
                                        element.last_name,
                                    "</div>",
                                    "<div id='city'>",
                                        "City: ",
                                        element.city,
                                    "</div>",
                                    "<div id='birthdate'>",
                                        "Date of Birth: ",
                                        element.birthdate,
                                    "</div>",
                                    "<div id='sex'>",
                                        "Sex: ",
                                        element.sex,
                                    "</div>",
                                    "<div id='gender'>",
                                        "Gender: ",
                                        element.gender,
                                    "</div>",
                                    "<div id='ethnicity'>",
                                        "Ethnicity: ",
                                        element.ethnicity,
                                    "</div>",
                                    "<div id='race'>",
                                        "Race: ",
                                        element.race,
                                    "</div>",
                                    "<div id='zipcode'>",
                                        "Zip Code: ",
                                        element.zipcode,
                                    "</div>",
                                "</div>",
                            "</div>"
                        ]).join('\n')
                        );
                });
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




