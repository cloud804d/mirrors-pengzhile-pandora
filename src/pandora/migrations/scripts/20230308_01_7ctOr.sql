-- Init database
-- depends: 

drop table if exists conversation_official;
create table conversation_official
(
    conversation_id char(36)
        primary key,
    title           text    not null,
    create_time     integer not null
);

drop table if exists conversation_info;
create table conversation_info
(
    conversation_id char(36)
        primary key,
    title           varchar(200) not null,
    create_time     integer      not null,
    current_node    char(36)
);

drop table if exists prompt_info;
create table prompt_info
(
    prompt_id       char(36) not null,
    conversation_id char(36) not null,
    model           varchar(64),
    parent_id       char(36),
    role            varchar(20),
    content         longtext,
    create_time     integer  not null,
    constraint prompt_info_pk
        primary key (conversation_id, prompt_id)
);
