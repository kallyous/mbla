CREATE TABLE player (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
email TEXT NOT NULL,
pass TEXT NOT NULL,
level INT UNSIGNED DEFAULT 0,
exp INT UNSIGNED DEFAULT 0,
class INT UNSIGNED DEFAULT 0,
loc_curr_world INT UNSIGNED,
loc_curr_x INT UNSIGNED,
loc_curr_y INT UNSIGNED,
loc_spawn_world INT UNSIGNED,
loc_spawn_x INT UNSIGNED,
loc_spawn_y INT UNSIGNED
);