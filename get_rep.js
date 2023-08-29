function getMatchInfo() {
    var matchId = $("#matchIdInput").val();

    $.ajax({
        url: "http://localhost:8000/predict",
        method: "GET",
        data: {
            match_id: matchId
        },
        success: function(response) {
            var jsonResponse = JSON.stringify(response);
            $("#matchInfo").text(jsonResponse);
        },
        error: function(response) {
            var jsonResponse = JSON.stringify(response);
            $("#matchInfo").text(jsonResponse);
        }
    });
}
