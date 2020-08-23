import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events
                                (
                                    artist text,
                                    auth text,
                                    firstName text,
                                    gender char,
                                    itemInSession int,
                                    lastName text,
                                    length float,
                                    level text,
                                    location text,
                                    method text,
                                    page text,
                                    registration float,
                                    sessionId int,
                                    song text,
                                    status int,
                                    ts bigint,
                                    userAgent text,
                                    userId int
                                )
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs
                                (
                                    num_songs int,
                                    artist_id text,
                                    artist_latitude float,
                                    artist_longitude float,
                                    artist_location text,
                                    artist_name text,
                                    song_id text,
                                    title text,
                                    duration float,
                                    year int
                                )
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays 
                            (
                            songplay_id bigint IDENTITY PRIMARY KEY,
                            start_time bigint NOT NULL, 
                            user_id int NOT NULL, 
                            level text, 
                            song_id text,
                            artist_id text, 
                            session_id int, 
                            location text,
                            user_agent text
                            )
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users 
                        (
                            user_id int PRIMARY KEY,
                            first_name text, 
                            last_name text, 
                            gender char, 
                            level text
                        )
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs 
                        (
                            song_id text PRIMARY KEY, 
                            title text,
                            artist_id text, 
                            year int, 
                            duration float
                        )
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists 
                        (
                            artist_id text PRIMARY KEY,
                            name text, 
                            location text, 
                            latitude float, 
                            longitude float
                        )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time 
                        (
                            start_time bigint PRIMARY KEY,
                            hour int, 
                            day int, 
                            week int, 
                            month int, 
                            year int,
                            weekday int
                        )
""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events FROM '{}'
                            iam_role {}
                            format as json 'auto'
""").format('s3://udacity-dend/log-data/2018/11/', config.get("IAM_ROLE", "ARN"))

staging_songs_copy = ("""COPY staging_songs FROM '{}'
                        iam_role {}
                        format as json 'auto'
""").format('s3://udacity-dend/song_data/A/B/C/', config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
