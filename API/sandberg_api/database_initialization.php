<?php
function connect_db() {
    $db = new SQLite3('database.db');
    return $db;
}

function delete_column_api_comp_cat_id() {
    $db = connect_db();
    $createNewTableSQL = <<<SQL
    CREATE TABLE Kategorie_pre_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pret INTEGER NOT NULL,
        id_kat INTEGER NOT NULL
    );
    SQL;
    $db->exec($createNewTableSQL);
    $db->exec("DROP TABLE Kategorie_pre");
    $db->exec("ALTER TABLE Kategorie_pre_new RENAME TO Kategorie_pre");
    $db->close();
    echo "Stĺpec 'api_comp_cat_id' bol úspešne odstránený.\n";
}

function clean_tables() {
    $db = connect_db();
    $db->exec("DELETE FROM Kategorie;");
    $db->exec("DELETE FROM Kategorie_pre;");
    $db->exec("DELETE FROM Preteky;");
    $db->exec("DELETE FROM Prihlaseni;");
    $db->exec("DELETE FROM sqlite_sequence WHERE name='Kategorie';");
    $db->exec("DELETE FROM sqlite_sequence WHERE name='Kategorie_pre';");
    $db->exec("DELETE FROM sqlite_sequence WHERE name='Preteky';");
    $db->exec("DELETE FROM sqlite_sequence WHERE name='Prihlaseni';");
    $db->close();
    echo "Tabuľky boli úspešne vyčistené.\n";
}

function database_initialization() {
    $db = connect_db();
    delete_column_api_comp_cat_id($db);
    clean_tables($db);
    $db->close();
    echo "Inicializácia databázy bola dokončená.\n";
}


database_initialization();
?>