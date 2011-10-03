var radius = 300;
var maxtweets = 100;
var minvalence = 0;
var maxvalence = 10;
var loc = "geolocate";

var lastPage = "settings";
var lastRequest = null;
var mapNeedsInit = true;
var watch = null;

$.dynaCloud.auto = false;

setSettingsVal();

//reset type=date inputs to text
$( document ).bind( "mobileinit", function(){
    $.mobile.page.prototype.options.degradeInputs.date = true;
});   

$('#map_page').live("pagecreate", function() {
    if (mapNeedsInit) {
        init_map();

        mapNeedsInit = false;
    }
});

$('#map_page').live('pageshow',function(){
    if (lastPage == "settings") {
        map.setOptions(map_opts); 
        resizeMap();
        doGetTweets(true);
    }
    lastPage = "map";
});

$('#map_page').live('pagehide',function(){
    if (watch && navigator.geolocation) {
        navigator.geolocation.clearWatch(watch); 
    }
});

function setSettingsVal() {
    $("#radius_slider").val(radius);
    $("#maxtweets_slider").val(maxtweets);
    $("#minvalence_slider").val(minvalence);
    $("#maxvalence_slider").val(maxvalence);
    $("#citypreset_select").val(loc);
}

$('#settings_page').live('pageshow',function(){
    setSettingsVal();

    lastPage = "settings";
    
});

$('#tagcloud_page').live('pageshow',function(){
    lastPage = "tagcloud";

    $('#dynacloud').html('Loading...');
    $('#keywords_hidden').dynaCloud();
});

function doGetTweets(clearall) {
    $("#status_map").html("Loading...");
    $(".setting-slider").attr('disabled', 'disabled')

    if (clearall) {
        lastRequest = null;
        // remove markers
        clearOverlays();
        // reset tag cloud
        $("#keywords_hidden").html('');
    }

    // Main function
    function success(lat, lon) {
        if (clearall) {
            // only recenter if it's the first time, or if we're reloading tweets
            map.setCenter(new google.maps.LatLng(lat, lon), 22);
        }

        // remove old tweets - no longer necessary because we use lastRequest to only get tweets added since last time
        //clearOverlays();

        // mark current location
        markLocation(lat, lon, "", "You are here!", -1, true);

        // mark tweets
        _getTweets(
            lat, lon,
            radius,
            0,
            maxtweets,
            minvalence,
            maxvalence,
            clearall
        );

        // TODO move to gettweet success

        // update last time
        lastRequest = new Date().getTime();

        //setTimeout(doGetTweets, 30*1000);
    }

    if (loc == "geolocate") {
        // Find where user is
        if (navigator.geolocation) {
            watch = navigator.geolocation.watchPosition(
                    function(position) {
                        success(position.coords.latitude,position.coords.longitude);
                    },
                    function(){
                        $("#status_map").html("Geolocation failed");
                        $(".setting-slider").removeAttr('disabled')
                        //setTimeout(doGetTweets, 30*1000);
                    }
            );
        }
        else {
            alert('Your browser doesn\'t have native geolocation capabilities.');
        }
    }
    else {
        s = loc.split(',');
        success(s[0], s[1]);
    }
}


function verifyValence(adjusted) {
    var min = parseInt($("#minvalence_slider").val());
    var max = parseInt($("#maxvalence_slider").val());

    if (adjusted == "min") {
        if (min > max) {
            $("#minvalence_slider").val(max).slider("refresh");
        }
    }
    else {
        if (min > max) {
            $("#maxvalence_slider").val(min).slider("refresh");
        }
    }
    updateVal(adjusted);
}


function updateVal(adjusted) {
    if (adjusted == 'radius') {
        radius = parseInt($("#radius_slider").val());
    }
    else if (adjusted == 'maxtweets') {
        maxtweets = parseInt($("#maxtweets_slider").val());
    }
    else if (adjusted == 'minvalence') {
        minvalence = parseInt($("#minvalence_slider").val());
    }
    else if (adjusted == 'maxvalence') {
        maxvalence = parseInt($("#maxvalence_slider").val());
    }
    else if (adjusted == 'loc') {
        loc = $("#citypreset_select").val();
    }
}
