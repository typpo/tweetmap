<?php
// PHP wrapper for database query

// Debug output
error_reporting(E_ALL);
ini_set('display_errors', true);

$group = isset($_GET['group']) ? $_GET['group'] : null;
$text = isset($_GET['text']) ? $_GET['text'] : null;

if ($group != null && $text != null) {
    $group = escapeshellcmd(urldecode($group));
    $text = escapeshellcmd(urldecode($text));

    $results = array();

    echo "training";
    $cmd = "python /net/tahoe3/ianw/thesis/learner.py train \"$group\" \"$text\"";
    exec($cmd, $results);
    //echo implode('\n', $results);
}

?>
