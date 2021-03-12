CREATE TABLE IF NOT EXISTS aquhx.modlog
(
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    PRIMARY KEY (guild_id, channel_id)
);


CREATE TABLE IF NOT EXISTS aquhx.messages
(
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE IF NOT EXISTS aquhx.welcome
(
    guild_id bigint NOT NULL,
    msg text NOT NULL,
    PRIMARY KEY (guild_id, msg)
);

CREATE TABLE IF NOT EXISTS aquhx.goodbye (
    guild_id bigint NOT NULL,
    msg text NOT NULL,
    PRIMARY KEY (guild_id, msg)
);

CREATE TABLE IF NOT EXISTS aquhx.prefixes (
    guild_id bigint NOT NULL,
    prefix text,
    PRIMARY KEY (guild_id, prefix)
)