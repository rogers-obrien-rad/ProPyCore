<?php

require 'get_access_token.php';

function addAttachment($access_token, $company_id, $project_id, $direct_cost_id, $attachments = []) {
    $url = "https://api.procore.com/rest/v1.1/projects/$project_id/direct_costs/$direct_cost_id";

    $headers = [
        "Authorization: Bearer $access_token",
        "Procore-Company-Id: $company_id",
        "Accept: application/json"
    ];

    $postFields = [];
    
    // Create a new finfo resource
    $finfo = finfo_open(FILEINFO_MIME_TYPE);

    // Prepare attachments
    foreach ($attachments as $index => $attachment) {
        $mime_type = finfo_file($finfo, $attachment);
        if ($mime_type === false) {
            $mime_type = 'application/octet-stream';
        }

        $postFields["attachments[$index]"] = new CURLFile($attachment, $mime_type, basename($attachment));
    }

    // Close the finfo resource
    finfo_close($finfo);

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PATCH");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        return null;
    }

    curl_close($ch);

    return json_decode($response, true);
}

// Main execution
$access_token = getAccessToken($client_id, $client_secret);

$company_id = 8089;
$project_id = 2783683;
$direct_cost_id = 95483758;
$attachments = [
    "C:\Users\hfritz\OneDrive - RO\Documents\packages\ProPyCore\php\direct_costs_module.pdf",
];

$response = addAttachment($access_token, $company_id, $project_id, $direct_cost_id, $attachments);
echo "Response from adding attachment: \n";
print_r($response);
