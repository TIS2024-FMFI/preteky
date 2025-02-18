<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
ini_set('log_errors', 1);
ini_set('error_log', '/tmp/php_errors.log');

error_log("Test message");
error_reporting(E_ALL);


include_once 'funkcie.php';
include_once 'preteky.php';
include_once 'export_import.php';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] == 'POST' && preg_match('/\/prihlas\/api.php\/api\/competitions\/competition/', $_SERVER['REQUEST_URI'])) {
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

if ($_SERVER['REQUEST_METHOD'] == 'GET' && preg_match('/\/prihlas\/api.php\/api\/competitions\/(\d+)\/export/', $_SERVER['REQUEST_URI'], $matches)) {
    $id_pret = $matches[1];
    try {
    $result = ExportImport::exportujJSON($id_pret);
    echo json_encode(["status" => "success", "data" => $result]);
} catch (Exception $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
exit;
}
if ($_SERVER['REQUEST_METHOD'] == 'GET' && preg_match('/\/prihlas\/api.php\/api\/competitions\/active/', $_SERVER['REQUEST_URI'])) {
    try {
        $aktivnePretekyId = ExportImport::ziskat_aktivne_preteky_id();
        echo json_encode(["status" => "success", "data" => $aktivnePretekyId]);
    } catch (Exception $e) {
        echo json_encode(["status" => "error", "message" => $e->getMessage()]);
    }
    exit;
}
?>