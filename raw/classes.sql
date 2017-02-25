CREATE TABLE classes (
id INT UNSIGNED PRIMARY KEY NOT NULL,
name_sys TEXT UNIQUE NOT NULL,
name_disp TEXT NOT NULL
);

INSERT INTO classes VALUES (0, "none", "Wanderer");
