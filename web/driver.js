
// TODO convert this into argument object
function _getTweets(lat, lon, radius, since, max, valmin, valmax, refreshmap) {
    var params = '';
    params += 'lat=' + lat;
    params += '&lon=' + lon;
    params += '&radius=' + radius;
    params += '&since=' + since;
    params += '&max=' + max;
    params += '&valmax=' + valmax;
    params += '&valmin=' + valmin;

    $.ajax({
        url: 'api.php?' + params,
        success: function(data) {
            if (refreshmap) {
                clearBounds();
                recordBounds();
            }

            if (data.results.length < 1) {
                $("#status_map").html("Map");
                alert('Sorry, no tweets match your query.');
            }

            for (var i=0; i<data.results.length; i++) {
                var tweet = data.results[i];
                var valence = parseFloat(tweet.valence);
                if (valence >= 0) {
                    markLocation(tweet.coord.lat, tweet.coord.lon,
                        tweet.author, tweet.text, tweet.valence
                    );
                }
            }
            if (refreshmap) {
                fitBounds();
            }
            $("#status_map").html("Map");
        },
        dataType: 'json'
    });
}

function train(group, text) {
    var params = '';
    params += 'group=' + group;
    params += '&text=' + text;

    $.ajax({
        url: 'train.php?' + params,
        success: function(data) {
            alert('Thanks for helping to train the system!');
        },
    });
}
