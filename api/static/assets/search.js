
$(document).ready(function() {
    $("#search-input").on('input', function() {
        let query = $(this).val();
        console.log("User input:", query);

        if (query.length > 2) {
            $.get("{{ url_for('search') }}", { query: query }, function(data) {
                let dropdownHtml = '<ul class="list-group">';
                
                if (data.length === 0) {
                    // If no exams are found
                    dropdownHtml += `<li class="list-group-item"><a href="#" id="request-exam">Request addition of: ${query}</a></li>`;
                } else {
                    for (let i = 0; i < data.length; i++) {
                        let detailUrl = "/" + data[i].url_exam_name ;
                        dropdownHtml += `<li><a href="${detailUrl}">${data[i]['Name of Examination']}</a></li>`;
                    }
                }

                dropdownHtml += '</ul>';
                $("#search-dropdown").html(dropdownHtml).show();
            });
        } else {
            $("#search-dropdown").hide();
        }
    });
    

    $("#search-dropdown").on('click', '#request-exam', function(e) {
    e.preventDefault();
    
    let exam_name = $("#search-input").val(); // Get the value of the input box
    
    $.post("/request-exam", {exam_name: exam_name}, function(response) {
           
      alert('Thank you for your request. We will look into adding this exam soon.');
    });
});

    
});

