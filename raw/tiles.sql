CREATE TABLE tiles (
    id int unsigned unique not null,
    name text,
    type text,
    tier int unsigned,
    hp int unsigned,
    graphic_asset text,
    asset_x int unsigned,
    asset_y int unsigned,
    script_enter text,
    script_tools text,
    script_break text,
    script_place text,
    fx_walk text,
    fx_run text,
    fx_dash text,
    fx_swim text,
    fx_fly text,
    fx_fly_fast text
);
INSERT INTO tiles VALUES (0, "Empty", "empty", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (1, "Deep Water", "liquid", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (2, "Shallow Water", "liquid", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (3, "Sand", "ground_soft", 0, 10, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (4, "Dirt", "ground_standard", 0, 30, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (5, "Grass", "ground_standard", 0, 20, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (6, "Stone", "ground_hard", 1, 50, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (7, "Snow", "ground_soft", 0, 10, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (8, "Lava", "liquid", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (9, "Oil", "liquid", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
INSERT INTO tiles VALUES (10, "Hole", "empty", 0, 0, "dev-assets.png", 0, 0, "", "", "", "", "", "", "", "", "", "");
