CREATE TABLE IF NOT EXISTS prefixes (
    guild_id BIGINT,
    prefix TEXT
);

CREATE TABLE IF NOT EXISTS modlog ( 
    guild_id BIGINT,
    channel_id BIGINT
);

CREATE TABLE IF NOT EXISTS welcome ( 
    guild_id BIGINT,
    welchan BIGINT,
    welcome TEXT
);

CREATE TABLE IF NOT EXISTS goodbye ( 
    guild_id BIGINT,
    goodchan BIGINT,
    goodbye TEXT
);
