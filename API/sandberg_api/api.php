<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include_once 'funkcie.php';
include_once 'preteky.php';
include_once 'export_import.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] == 'POST' && preg_match('/\/sks\/api.php\/api\/competitions\/competition/', $_SERVER['REQUEST_URI'])) {
    $data = json_decode(file_get_contents('php://input'), true);

    if (empty($data['competition']) || empty($data['categories'])) {
        echo json_encode(["status" => "error", "message" => "Missing data for race or categories."]);
        exit;
    }

    try {
        $result = ExportImport::spracuj_pretek($data['competition'], $data['categories']);
        echo json_encode($result);
    } catch (Exception $e) {
        echo json_encode(["status" => "error", "message" => $e->getMessage()]);
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] == 'GET' && preg_match('/\/sks\/api.php\/api\/competitions\/(\d+)\/export/', $_SERVER['REQUEST_URI'], $matches)) {
    $id_pret = $matches[1];
    try {
    $result = ExportImport::exportujJSON($id_pret);
    echo json_encode(["status" => "success", "data" => $result]);
} catch (Exception $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
}
