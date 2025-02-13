<?php
include_once 'preteky.php';

class ExportImport
{
    public static function existuju_prihlaseni($id_pret): bool
    {
        $db = napoj_db();
        $sql = <<<EOF
        SELECT COUNT(*) as count FROM Prihlaseni WHERE id_pret = '$id_pret';
        EOF;
        $ret = $db->query($sql);
        $row = $ret->fetchArray(SQLITE3_ASSOC);
        $db->close();
        return $row['count'] > 0;
    }

    static function existuje_pretek($id): bool
    {
        $db = napoj_db();
        $sql = <<<EOF
        SELECT id FROM Preteky WHERE id = '$id';
        EOF;
        $ret = $db->query($sql);
        $row = $ret->fetchArray(SQLITE3_ASSOC);
        $db->close();
        return (bool)$row;
    }

    public static function exportujJSON($id_pret)
    {
        $db = napoj_db();

        if (!self::existuje_pretek($id_pret)) {
            echo json_encode(["status" => "error", "message" => "Race with ID $id_pret not found."]);
            $db->close();
            exit;
        }

        if (!self::existuju_prihlaseni($id_pret)) {
            echo json_encode(["status" => "error", "message" => "No participants registered for race with ID $id_pret."]);
            $db->close();
            exit;
        }

        $sql = <<<EOF
        SELECT os_i_c, cip, priezvisko, meno, Kategorie_pre.id AS id_kat, Prihlaseni.poznamka
        FROM Prihlaseni
        JOIN (SELECT id, meno, priezvisko, os_i_c, cip FROM Pouzivatelia) AS pouz
        ON Prihlaseni.id_pouz = pouz.id
        JOIN Kategorie_pre
        ON Prihlaseni.id_pret = Kategorie_pre.id_pret
        WHERE Prihlaseni.id_pret = '$id_pret' AND Prihlaseni.id_kat = Kategorie_pre.id_kat
        GROUP BY os_i_c, cip, priezvisko, meno, Prihlaseni.poznamka;
        EOF;

        $ret = $db->query($sql);
        $results = [];
        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
            $results[] = [
                'MENO' => $row['meno'],
                'PRIEZVISKO' => $row['priezvisko'],
                'OS.ČÍSLO' => $row['os_i_c'],
                'ČIP' => $row['cip'],
                'ID_KATÉGORIE' => $row['id_kat'],
                'POZNÁMKA' => $row['poznamka']
            ];
        }

        header('Content-Type: application/json');
        echo json_encode($results);
        $db->close();
        exit;
    }

    static function existuje_kategoria($id)
    {
        $db = napoj_db();
        $sql = <<<EOF
        SELECT id FROM Kategorie WHERE id = '$id';
        EOF;

        $ret = $db->query($sql);
        $row = $ret ? $ret->fetchArray(SQLITE3_ASSOC) : null;

        $db->close();

        return $row ? $row['id'] : false;
    }

    static function existuje_kat_preteku($id_pret, $category_id): bool
    {
        $db = napoj_db();
        $sql = <<<EOF
        SELECT * FROM Kategorie_pre WHERE id_pret = '$id_pret' AND id = '$category_id';
        EOF;
        $ret = $db->query($sql);
        $row = $ret->fetchArray(SQLITE3_ASSOC);
        $db->close();
        return (bool)$row;
    }

    public static function pridaj_pretek_s_id($ID, $NAZOV, $DATUM, $DEADLINE, $POZNAMKA)
    {
        $db = napoj_db();

        $NAZOV2 = htmlentities($NAZOV, ENT_QUOTES, 'UTF-8');
        $reg_exUrl = "/(http|https|ftp|ftps):\/\/[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,3}(\/\S*)?/";
        $text = $POZNAMKA;
        if (preg_match($reg_exUrl, $text, $url) && !strpos($text, "</a>") && !strpos($text, "</A>") && !strpos($text, "HREF") && !strpos($text, "href")) {
            $text = preg_replace($reg_exUrl, "<a href=" . $url[0] . ">$url[0]</a> ", $text);
        }
        $POZNAMKA2 = htmlentities($text, ENT_QUOTES, 'UTF-8');

        $sql = <<<EOF
        INSERT INTO Preteky (id, nazov, datum, deadline, aktiv, poznamka)
        VALUES ('$ID', '$NAZOV2', '$DATUM', '$DEADLINE', '1', '$POZNAMKA2');
        EOF;

        $db->exec($sql);

        $db->close();

        return $ID;
    }

    static function pridaj_pretek_s_kontrolou($id, $nazov, $datum, $deadline, $poznamka): bool
    {
        $existujuci_id = self::existuje_pretek($id);
        if ($existujuci_id) {
            return true;
        }
        self::pridaj_pretek_s_id($id, $nazov, $datum, $deadline, $poznamka);
        return false;
    }

    static function pridaj_kategoriu_s_id($id, $nazov)
    {
        $db = napoj_db();
        $sql = <<<EOF
        INSERT INTO Kategorie (id,nazov)
        VALUES ('$id','$nazov');
        EOF;
        $ret = $db->exec($sql);
        if (!$ret) {
            echo $db->lastErrorMsg();
        }
        $db->close();
    }

    static function pridaj_kategoriu_s_kontrolou($id, $nazov)
    {
        $existujuci_id = self::existuje_kategoria($id);
        if ($existujuci_id) {
            return $existujuci_id;
        }

        return self::pridaj_kategoriu_s_id($id, $nazov);
    }

    static function pridaj_kat_preteku_s_id($id_pret, $id, $id_kat)
    {
        $db = napoj_db();
        $sql = <<<EOF
        INSERT INTO Kategorie_pre (id, id_pret, id_kat)
        VALUES ('$id','$id_pret','$id_kat');
        EOF;
        $ret = $db->exec($sql);
        if (!$ret) {
            echo $db->lastErrorMsg();
        }
        $db->close();
    }

    static function pridaj_kat_preteku_s_kontrolou($id_pret, $id, $id_kat)
    {
        if (self::existuje_kat_preteku($id_pret, $id)) {
            return;
        }
        self::pridaj_kat_preteku_s_id($id_pret, $id, $id_kat);
    }

    static function existuje_kat_pre($id_kat): bool
    {
        $db = napoj_db();
        $sql = <<<EOF
        SELECT * FROM Kategorie_pre WHERE id = '$id_kat';
        EOF;
        $ret = $db->query($sql);
        $row = $ret->fetchArray(SQLITE3_ASSOC);
        $db->close();
        return (bool)$row;
    }

    public static function spracuj_pretek($competition, $categories): array
    {
        $existuje = self::pridaj_pretek_s_kontrolou(
            $competition['id'],
            $competition['nazov'],
            $competition['datum'],
            $competition['deadline'],
            $competition['poznamka']
        );
        foreach ($categories as $category) {
            self::pridaj_kategoriu_s_kontrolou(
                $category['category_id'], //globálna kategória
                $category['name']
            );
            if (self::existuje_kat_pre($category['id'])) {
                return ["status" => "error", "message" => "Race with these categories already exists."];
                exit;
            }
            self::pridaj_kat_preteku_s_kontrolou($competition['id'], $category['id'], $category['category_id']);
        }
        if ($existuje) {
            return ["status" => "error", "message" => "Race with ID {$competition['id']} already exists."];
        } else {
            return ["status" => "success", "message" => "Race with ID {$competition['id']} was successfully added."];
        }
        exit;
    }

    public static function ziskat_aktivne_preteky_id()
    {
        $db = napoj_db();
        $sql = <<<EOF
            SELECT id FROM Preteky WHERE datetime(datum) >= datetime('now','-3 days') AND aktiv = 1 ORDER BY deadline DESC;
        EOF;
        $ret = $db->query($sql);
        $activeRaceIds = [];
        while ($row = $ret->fetchArray(SQLITE3_ASSOC)) {
            $activeRaceIds[] = $row['id'];
        }
        header('Content-Type: application/json');
        echo json_encode($activeRaceIds);
        $db->close();
        exit;
    }
}



