<?php

require 'vendor/autoload.php';

$dotenv = Dotenv\Dotenv::createImmutable(dirname(__DIR__)); 
$dotenv->load();

$client_id = getenv('CLIENT_ID');
$client_secret = getenv('CLIENT_SECRET');

function getAccessToken($client_id, $client_secret) {
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, "https://login.procore.com/oauth/token");
    curl_setopt($ch, CURLOPT_POST, 1);

    $postFields = [
        'grant_type' => 'client_credentials',
        'client_id' => $client_id,
        'client_secret' => $client_secret,
        'redirect_uri' => 'urn:ietf:wg:oauth:2.0:oob'
    ];

    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        return null;
    }

    $response_data = json_decode($response, true);
    curl_close($ch);

    return $response_data['access_token'];
}

// Main execution
$access_token = getAccessToken($client_id, $client_secret);

if ($access_token) {
    echo "Successfully obtained access token";
} else {
    echo "Failed to obtain access token.";
}