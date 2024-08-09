<?php

require 'get_access_token.php'; // Ensure this path is correct based on your directory structure

function getDirectCosts($access_token, $company_id, $project_id, $page = 1, $per_page = 100) {
    $endpoint = "https://api.procore.com/rest/v1.1/projects/$project_id/direct_costs";
    $direct_costs = [];
    $n_costs = 1;

    while ($n_costs > 0) {
        $params = [
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
            'Content-Type: application/json',
            'Procore-Company-Id: ' . $company_id
        ]);

        $response = curl_exec($ch);

        if (curl_errno($ch)) {
            echo 'Error:' . curl_error($ch);
            return null;
        }

        $costs_per_page = json_decode($response, true);
        $n_costs = count($costs_per_page);

        $direct_costs = array_merge($direct_costs, $costs_per_page);

        $page++;
        curl_close($ch);
    }

    return $direct_costs;
}

// Main execution
$access_token = getAccessToken($client_id, $client_secret);

$company_id = 8089;
$project_id = 2783683; 
$direct_costs = getDirectCosts($access_token, $company_id, $project_id);
echo "Direct Costs: \n";
print_r($direct_costs);
?>
