--
-- File generated with SQLiteStudio v3.1.1 on Пн фев 6 22:25:37 2017
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: cache_rates
DROP TABLE IF EXISTS cache_rates;

CREATE TABLE cache_rates (
    ID                  INTEGER  PRIMARY KEY AUTOINCREMENT
                                 NOT NULL,
    SRC_ID                       REFERENCES rates_sources (ID) ON DELETE CASCADE
                                                               ON UPDATE CASCADE
                                 NOT NULL,
    REQUESTED_RATE_DATE DATE     NOT NULL,
    CACHE_DATETIME      DATETIME NOT NULL
                                 DEFAULT (CURRENT_TIMESTAMP),
    CACHE_DATA          BLOB     NOT NULL
);


-- Table: currency
DROP TABLE IF EXISTS currency;

CREATE TABLE currency (
    ID       VARCHAR (3)  PRIMARY KEY
                          UNIQUE
                          NOT NULL,
    LABEL_ID VARCHAR (15) NOT NULL
);


-- Table: global_variables
DROP TABLE IF EXISTS global_variables;

CREATE TABLE global_variables (
    ID       INTEGER      PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    IDX_TYPE VARCHAR (20) UNIQUE
                          NOT NULL,
    TEXT     VARCHAR (20) NOT NULL
);


-- Table: labels
DROP TABLE IF EXISTS labels;

CREATE TABLE labels (
    ID       INTEGER       PRIMARY KEY AUTOINCREMENT
                           UNIQUE
                           NOT NULL,
    LANG_ID  VARCHAR (3)   REFERENCES lang (ID) ON DELETE RESTRICT
                                                ON UPDATE CASCADE
                           NOT NULL,
    LABEL_ID VARCHAR (15),
    TEXT     VARCHAR (255) NOT NULL
);


-- Table: lang
DROP TABLE IF EXISTS lang;

CREATE TABLE lang (
    ID   VARCHAR (3)   PRIMARY KEY ON CONFLICT ROLLBACK
                       UNIQUE ON CONFLICT ROLLBACK
                       NOT NULL ON CONFLICT ROLLBACK,
    TEXT VARCHAR (255) NOT NULL
)
WITHOUT ROWID;


-- Table: log_bot
DROP TABLE IF EXISTS log_bot;

CREATE TABLE log_bot (
    ID         INTEGER      PRIMARY KEY AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    USER_ID    INTEGER      NOT NULL,
    COMMAND    VARCHAR (20) NOT NULL,
    UPDATES_ID INTEGER      NOT NULL
);


-- Table: log_load
DROP TABLE IF EXISTS log_load;

CREATE TABLE log_load (
    ID            INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    SRC_ID                REFERENCES rates_sources (ID) ON DELETE NO ACTION
                                                        ON UPDATE CASCADE
                          NOT NULL,
    LOAD_DATETIME INTEGER NOT NULL
                          DEFAULT (CURRENT_TIMESTAMP) 
);


-- Table: rates
DROP TABLE IF EXISTS rates;

CREATE TABLE rates (
    ID              INTEGER  PRIMARY KEY AUTOINCREMENT
                             NOT NULL
                             UNIQUE,
    SRC_ID                   REFERENCES rates_sources (ID) ON DELETE RESTRICT
                                                           ON UPDATE CASCADE
                             NOT NULL,
    BUY_VALUE       DECIMAL,
    SELL_VALUE      DECIMAL,
    AVRG_VALUE      DECIMAL,
    RATE_DATETIME   DATETIME NOT NULL,
    CUR_ID_FROM              REFERENCES currency (ID) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                             NOT NULL,
    CUR_ID_TO                REFERENCES currency (ID) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                             NOT NULL,
    QUANT           INT      NOT NULL
                             DEFAULT (1),
    CREATEDDATETIME DATETIME NOT NULL ON CONFLICT ROLLBACK
                             DEFAULT (CURRENT_TIMESTAMP) 
);


-- Table: rates_sources
DROP TABLE IF EXISTS rates_sources;

CREATE TABLE rates_sources (
    ID        VARCHAR (15) PRIMARY KEY
                           NOT NULL
                           UNIQUE,
    LABEL_ID  VARCHAR (15) NOT NULL,
    STATE_ID               REFERENCES state (ID) ON DELETE RESTRICT
                                                 ON UPDATE CASCADE
                           NOT NULL,
    ACTIVE    BOOLEAN      NOT NULL
                           DEFAULT True,
    DOMAIN    VARCHAR (50) NOT NULL,
    RATE_TYPE              REFERENCES global_variables (IDX_TYPE) ON DELETE RESTRICT
                                                                  ON UPDATE CASCADE
);


-- Table: ref_cur_user_settings
DROP TABLE IF EXISTS ref_cur_user_settings;

CREATE TABLE ref_cur_user_settings (
    ID          INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE
                        NOT NULL,
    CUR_ID              REFERENCES currency (ID) ON DELETE RESTRICT
                                                 ON UPDATE CASCADE
                        NOT NULL,
    USER_SET_ID         REFERENCES user_settings (ID) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                        NOT NULL
);


-- Table: ref_label_lang
DROP TABLE IF EXISTS ref_label_lang;

CREATE TABLE ref_label_lang (
    ID       INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    LANG_ID          REFERENCES lang (ID) ON DELETE RESTRICT
                                          ON UPDATE CASCADE
                     NOT NULL,
    LABEL_ID         REFERENCES labels (ID) ON DELETE RESTRICT
                                            ON UPDATE CASCADE
                     NOT NULL
);


-- Table: ref_src_cur
DROP TABLE IF EXISTS ref_src_cur;

CREATE TABLE ref_src_cur (
    ID     INTEGER PRIMARY KEY AUTOINCREMENT
                   UNIQUE
                   NOT NULL,
    SRC_ID         REFERENCES rates_sources (ID) ON DELETE RESTRICT
                                                 ON UPDATE CASCADE
                   NOT NULL,
    CUR_ID         REFERENCES currency (ID) ON DELETE RESTRICT
                                            ON UPDATE CASCADE
                   NOT NULL
);


-- Table: ref_src_user_settings
DROP TABLE IF EXISTS ref_src_user_settings;

CREATE TABLE ref_src_user_settings (
    ID          INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE
                        NOT NULL,
    CUR_ID              REFERENCES rates_sources (ID) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                        NOT NULL,
    USER_SET_ID         REFERENCES user_settings (ID) ON DELETE RESTRICT
                                                      ON UPDATE CASCADE
                        NOT NULL
);


-- Table: state
DROP TABLE IF EXISTS state;

CREATE TABLE state (
    ID          VARCHAR (5)   PRIMARY KEY
                              UNIQUE
                              NOT NULL,
    NAME        VARCHAR (255) NOT NULL,
    CUR_ID_FROM               REFERENCES currency (ID) ON DELETE RESTRICT
                                                       ON UPDATE CASCADE
                              NOT NULL
);


-- Table: user_settings
DROP TABLE IF EXISTS user_settings;

CREATE TABLE user_settings (
    ID       INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    USERID   INTEGER UNIQUE
                     NOT NULL,
    LANG_ID          REFERENCES lang (ID) ON DELETE RESTRICT
                                          ON UPDATE CASCADE
                     NOT NULL,
    STATE_ID         REFERENCES state (ID) ON DELETE RESTRICT
                                           ON UPDATE CASCADE
                     NOT NULL
);


-- Index: idx_main
DROP INDEX IF EXISTS idx_main;

CREATE UNIQUE INDEX idx_main ON rates (
    SRC_ID,
    RATE_DATETIME,
    CUR_ID_FROM,
    CUR_ID_TO,
    QUANT
);


-- Index: idx_type
DROP INDEX IF EXISTS idx_type;

CREATE UNIQUE INDEX idx_type ON global_variables (
    IDX_TYPE
);


-- Index: main_idx
DROP INDEX IF EXISTS main_idx;

CREATE UNIQUE INDEX main_idx ON cache_rates (
    SRC_ID,
    REQUESTED_RATE_DATE
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
