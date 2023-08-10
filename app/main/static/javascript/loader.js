$(document).ready(function() {
    $(".container-loader").hide();
    $("#updatePredictionsLink").click(function(e) {
        e.preventDefault();

        // Affichez le loader
        $(".container-loader").show();

        var newUrl = $(this).attr('href');

        $.ajax({
            url: newUrl,
            type: 'GET',
            success: function(response) {
                // Changez l'URL visible dans la barre d'adresse
                history.pushState({}, "", newUrl);

                $(".container-loader").hide();
                $(".contentContainer").empty().html(response.data);
                document.title = "Prédictions - Popularity Corner";
            },
            error: function(error) {
                console.log("Erreur : ", error);
                $(".container-loader").hide();
            }
        });
    });
});


// verify cookie 
$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Est-ce que ce cookie string commence par le nom recherché ?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

