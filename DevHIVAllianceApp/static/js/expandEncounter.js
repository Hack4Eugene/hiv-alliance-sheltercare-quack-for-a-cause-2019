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
                $(formErrors).text("Empty Response");
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
                                    "<div class='last_name'>",
                                        "Last name: ",
                                        element.last_name,
                                    "</div>",
                                    "<div class='city'>",
                                        "City: ",
                                        element.city,
                                    "</div>",
                                    "<div class='birthdate'>",
                                        "Birthdate: ",
                                        element.birthdate,
                                    "</div>",
                                    "<div class='sex'>",
                                        "Sex: ",
                                        element.sex,
                                    "</div>",
                                    "<div class='gender'>",
                                        "Gender: ",
                                        element.gender,
                                    "</div>",
                                    "<div class='ethnicity'>",
                                        "Ethnicity: ",
                                        element.ethnicity,
                                    "</div>",
                                    "<div class='race'>",
                                        "Race: ",
                                        element.race,
                                    "</div>",
                                    "<div class='zipcode'>",
                                        "Zip code: ",
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




