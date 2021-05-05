DROP TABLE IF EXISTS songs;

CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bass INTEGER,
    feat INTEGER,
    vocal INTEGER,
    instrument TEXT,
    originality INTEGER,
    isBop INTEGER DEFAULT NULL
)