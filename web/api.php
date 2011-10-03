<?php
// PHP wrapper for database query

// Debug output
error_reporting(E_ALL);
ini_set('display_errors', true);

define("DEFAULT_HOST", "jamuna-prime.cs.dartmouth.edu");
define("DEFAULT_USER", "ianw");
define("DEFAULT_PASS", "uzpM03Eoi");
define("DEFAULT_DB", "ianw");

$valid_params = array(  'lat' => 40.7,
                        'lon' => -73.92,
                        'radius' => 1,
                        'since' => 0,
                        'max' => 15
                    );
$defaults = array(      'lat' => 41.86,
                        'lon' => -72.52,
                        'radius' => 200,
                        'since' => 0,
                        'max' => 15,
                        'valmin' => 0.0,
                        'valmax' => 10.0
                    );


// Connects to db
function connect(   $host = DEFAULT_HOST,
                    $user = DEFAULT_USER,
                    $pass = DEFAULT_PASS,
                    $db = DEFAULT_DB) {

    $ret = new mysqli($host, $user, $pass);
    if (mysqli_connect_errno()) {
        die("Connect failed: ".mysqli_connect_error());
    }
    return $ret;
}

// Returns cleaned request parameters
function param($name, $default) {
    return isset($_GET[$name]) ? floatval($_GET[$name]) : $default;
}


// Populate query params
/*
foreach ($valid_params as $name => $default) {
    $$name = param($name, $default);
}
 */
$lat = isset($_GET['lat']) ? floatval($_GET['lat']) : $defaults['lat'];
$lon = isset($_GET['lon']) ? floatval($_GET['lon']) : $defaults['lon'];
$radius = isset($_GET['radius']) ? floatval($_GET['radius']) : $defaults['radius'];
$since = isset($_GET['since']) ? intval($_GET['since']) : $defaults['since'];
$max = isset($_GET['max']) ? intval($_GET['max']) : $defaults['max'];
$valmax = isset($_GET['valmax']) ? intval($_GET['valmax']) : $defaults['valmax'];
$valmin = isset($_GET['valmin']) ? intval($_GET['valmin']) : $defaults['valmin'];

$handle = connect();

// Build query

// TODO see spatial indices
// http://maisonbisson.com/blog/post/12147/working-with-spatial-data-in-mysql/
// http://dev.mysql.com/doc/refman/5.0/en/using-a-spatial-index.html
// http://stackoverflow.com/questions/2296824/php-mysql-compare-long-and-lat-return-ones-under-10-miles
// They're only with bounding rects, though

// ***
// http://www.movable-type.co.uk/scripts/latlong-db.html
// ***

// Great circle constant for miles
$R = 3959;

// first-cut bounding box (in degrees)
$maxLat = $lat + rad2deg($radius/$R);
$minLat = $lat - rad2deg($radius/$R);

// compensate for degrees longitude getting smaller with increasing latitude
$maxLon = $lon + rad2deg($radius/$R/cos(deg2rad($lat)));
$minLon = $lon - rad2deg($radius/$R/cos(deg2rad($lat)));

// convert origin of filter circle to radians
$lat = deg2rad($lat);
$lon = deg2rad($lon);

$query = "
SELECT *,AsText(location),acos(sin($lat)*sin(radians(X(location))) + cos($lat)*cos(radians(X(Location)))*cos(radians(Y(location))-$lon))*$R As D
FROM (
    SELECT * FROM ianw.tweets
    WHERE X(location)>$minLat And X(location)<$maxLat
        And Y(location)>$minLon And Y(location)<$maxLon
) As FirstCut
WHERE acos(sin($lat)*sin(radians(X(location))) + cos($lat)*cos(radians(X(location)))*cos(radians(Y(location))-$lon))*$R < $radius
AND time >= (FROM_UNIXTIME($since))
AND valence <= $valmax
AND valence >= $valmin
ORDER BY D
LIMIT $max;
";

$final = array();
if ($handle->multi_query($query)) {
    do {
        if ($result = $handle->store_result()) {
            while ($row = $result->fetch_row()) {
                // eg. POINT(42.5, -71.2)
                $latlon = $row[6];
                $latlon = substr($latlon, 6, strlen($latlon)-7);
                $coord_str = explode(' ', $latlon);

                $final[] = array(
                    'author' => $row[1],
                    'text' => $row[2],
                    'date' => $row[3],
                    'valence' => $row[5],
                    'coord' => array('lat'=>floatval($coord_str[0]),'lon'=>floatval($coord_str[1])),
                    'distance' => $row[7]
                );
            }
            $result->free();
        }
        //if ($handle->more_results()) {
        //    echo "-------------------------\n";
        //}
    } while ($handle->next_result());
}

$handle->close();

print json_encode(array('results'=>$final));

?>
