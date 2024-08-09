<?php

require 'get_access_token.php'; // Ensure this path is correct based on your directory structure

function getCompanies($access_token, $page = 1, $per_page = 100) {
    $endpoint = "https://api.procore.com/rest/v1.0/companies";
    $params = [
        "page" => $page,
        "per_page" => $per_page,
        "include_free_companies" => "true"
    ];

    $query = http_build_query($params);
    $url = $endpoint . '?' . $query;

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $access_token,
        'Content-Type: application/json'
    ]);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        return null;
    }

    $companies = json_decode($response, true);
    curl_close($ch);

    return $companies;
}

// Main execution
$access_token = getAccessToken($client_id, $client_secret);
$companies = getCompanies($access_token);

echo "Companies: \n";
print_r($companies);
