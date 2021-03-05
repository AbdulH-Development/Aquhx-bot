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