<?php

require 'get_access_token.php';

function getProjects($access_token, $company_id, $per_page = 100) {
    $endpoint = "https://api.procore.com/rest/v1.1/projects";
    $projects = [];
    $n_projects = 1;
    $page = 1;

    while ($n_projects > 0) {
        $params = [
            "company_id" => $company_id,
            "page" => $page,
            "per_page" => $per_page
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

        $projects_per_page = json_decode($response, true);
        $n_projects = count($projects_per_page);

        $projects = array_merge($projects, $projects_per_page);

        $page++;
        curl_close($ch);
    }

    return $projects;
}

// Main execution
$access_token = getAccessToken($client_id, $client_secret);

$company_id = 8089; // Replace with actual company ID
$projects = getProjects($access_token, $company_id);
echo "Projects: \n";
print_r($projects);
