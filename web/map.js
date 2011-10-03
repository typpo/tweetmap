var map;
var map_opts;
var lastInfoWindow = null;

function init_map() {
    map_opts = {
      zoom: 10,
      center: new google.maps.LatLng(43.702222, -72.289444),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"),
            map_opts);
}

function resizeMap () {
    $('#map_canvas').height($(window).height()-$('#map_header').height()*2); 
    google.maps.event.trigger(map, 'resize');
}

$(window).resize(function(){resizeMap();});

function markLocation(lat, lon, author, text, valence, youarehere) {
    var myLatLng = new google.maps.LatLng(lat, lon);
    if (record_bounds) {
        bounds.extend(myLatLng);
    }

    var shape = {
        coord: [21,30,10],
        type: 'circle'
    };

    var opts = {
        clickable: !youarehere,
        position: myLatLng,
        map: map,
        icon: image,
        shape: shape,
        //title: markerText.length > 15 ? markerText.substring(0, 12) + "...": markerText,
    }
    if (!youarehere) {
        var image = new google.maps.MarkerImage('fuzzes/' + Math.floor(valence) + '.png',
                new google.maps.Size(49, 59),
                new google.maps.Point(0,0),
                new google.maps.Point(25, 30));

        opts.icon = image;
    }
    var marker = new google.maps.Marker(opts);

    if (!youarehere) {
        var infowindow = new google.maps.InfoWindow({
            content: '<strong>' + author + ': </strong>'+text+' ... '
                + '<div id="traindiv">'
                + '<span class="face" onClick="train(\'positive\', \''+escape(text)+'\');return false;"> :) </span> ... '
                + '<span class="face" onClick="train(\'negative\', \''+escape(text)+'\');return false;"> :( </span>'
                + '</div>'
        });
        $('#keywords_hidden').append(text + '<br>');

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map, marker);
            if (lastInfoWindow != null) {
                lastInfoWindow.close();
            }
            lastInfoWindow = infowindow;
        });
    }

    markersArray.push(marker);
}


// Handling clears/resets
var markersArray = [];
function clearOverlays() {
    if (markersArray) {
        for (i in markersArray) {
            markersArray[i].setMap(null);
        }
    }
}

// For fitting everything in view
var bounds = new google.maps.LatLngBounds();
var record_bounds = false;
function recordBounds() {
    record_bounds = true;
}

function clearBounds() {
    bounds = new google.maps.LatLngBounds(); 
}

function fitBounds() {
    map.fitBounds(bounds);
}
