import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR(256),
    auth VARCHAR(256),
    firstName VARCHAR(256),
    gender VARCHAR(256),
    iteminSession INTEGER,
    lastName VARCHAR(256),
    length NUMERIC,
    level VARCHAR(256),
    location VARCHAR(256),
    method VARCHAR(256),
    page VARCHAR(256),
    registration NUMERIC,
    sessionId INTEGER,
    song VARCHAR(256),
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR(256),
    userId VARCHAR(256)
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id VARCHAR(256),
    artist_latitude NUMERIC,
    artist_location VARCHAR(256),
    artist_longitude NUMERIC,
    artist_name VARCHAR(MAX),
    duration NUMERIC,
    num_songs INTEGER,
    song_id VARCHAR(256),
    title VARCHAR(256),
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
  songplay_id      	    bigint identity(0,1)   not null,
  start_time         	timestamp without time zone     	not null sortkey,
  user_id           	varchar(256)     not null,
  level     	        varchar(256)      not null,
  song_id           	varchar(256)     not null distkey,
  artist_id           	varchar(256)     not null,
  session_id     	    integer         not null,
  location          	varchar(256)     not null,
  user_agent      	    varchar(256)     not null
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
  user_id           varchar(256)    not null sortkey,
  first_name        varchar(256)    not null,
  last_name     	varchar(256)    not null,
  gender        	varchar(256)     not null,
  level      	    varchar(256)     not null)
diststyle all;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
  song_id     	varchar(256)     not null	sortkey distkey,
  title        	varchar(256) 	not null,
  artist_id     varchar(256)     not null,
  year        	integer     	not null,
  duration      numeric         not null
);

""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
  artist_id     	varchar(256)    not null    sortkey,
  artist_name       varchar(max)    not null,
  artist_latitude   numeric,
  artist_location   varchar(256),
  artist_longitude  numeric)
diststyle all;
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
  start_time           timestamp without time zone       not null   sortkey,
  hour                 integer  	 not null,
  day                  integer  	 not null,
  week                 integer  	 not null,
  month                integer  	 not null,
  year                 integer       not null,
  dayofweek	           integer       not null)
diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    iam_role '{}'
    json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])


staging_songs_copy = ("""
    copy staging_songs from {}
    iam_role '{}'
    json 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT (TIMESTAMP 'epoch' + "ts" / 1000 * interval '1 second'), userId, level, ss.song_id, ss.artist_id, sessionId, location, userAgent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title
AND se.artist = ss.artist_name
WHERE page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT userId, firstName, lastName, gender, level
FROM staging_events
WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
SELECT song_id, title, artist_id, year, duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
SELECT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, dayofweek)
SELECT start_time, DATE_PART(hr, start_time), DATE_PART(d, start_time),
DATE_PART(w, start_time), DATE_PART(mon, start_time), DATE_PART(yr, start_time), DATE_PART(dow, start_time)
FROM songplays;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
