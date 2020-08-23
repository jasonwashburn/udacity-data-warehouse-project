# Project: Data Warehouse

## Description
The purpose of this project is to create a redshift database of song and user 
activity for Sparkify's new music streaming app.  This will allow them to 
analyze their data which currently resides in a directory of JSON logs and 
JSON metadata.

JSON log and song data files are copied to staging tables in redshift, then 
inserted into analytic tables to allow simple SQL queries for data analysis. 

## Usage

### create_tables.py
This script must be run first. Connects to redshift and drops any existing tables if they exist, then creates `staging_events`, `staging_songs`, `songplay`, `artists`,`songs`, `time`, and `user` tables.

### etl.py
Running this script copies all log and song JSON files into staging tables then inserts the data into analytic tables in the redshift database.

### sql_queries.py
Contains SQL queries used by etl.py to create, drop, and insert data to 
sparkifydb. Does not need to be run by user.

### dwh.cfg
Contains configuration data needed to connect to S3 and redshift database. Syntax as follows:

    [CLUSTER]
    HOST=''
    DB_NAME=''
    DB_USER=''
    DB_PASSWORD=''
    DB_PORT=

    [IAM_ROLE]
    ARN=''

    [S3]
    LOG_DATA=''
    LOG_JSONPATH=''
    SONG_DATA=''

## Database Design
The database design schema consists of the following tables:
    
    staging_events - staging table for raw copy of event data
        artist (text)
        auth (text)
        firstName (text)
        gender (char)
        itemInSession (int)
        lastName (text)
        length (float)
        level (text)
        location (text)
        method (text)
        page (text)
        registration (float)
        sessionId (int)
        song (text)
        status (int)
        ts (bigint)
        userAgent (text)
        userId (text)

    staging_songs - staging table for raw copy of song data
        num_songs (int)
        artist_id (text)
        artist_latitude (float)
        artist_longitude (float)
        artist_location (text)
        artist_name (text)
        song_id (text)
        title (text)
        duration (float)
        year (int)

    songplays - contains a consolidated list of song play activity for analysis
        songplay_id (bigint, IDENTITY(0,1) PRIMARY KEY)
        start_time (timestamp, NOT NULL)
        user_id (int, NOT NULL)
        level (text)
        song_id (text)
        artist_id (text)
        session_id (int)
        location (text)
        user_agent (text)

    users - contains data on sparkify users derived from log files in ./data/log_data
        user_id (int, PRIMARY KEY)
        first_name (text)
        last_name (text)
        gender (char)
        level (text)

    songs - contains details on songs from song files in ./data/song_data
        song_id (text, PRIMARY KEY)
        title (text)
        artist_id (text)
        year (int)
        duration (float)

    artists - contains details on artists from song files in ./data/song_data
        artist_id (text, PRIMARY KEY)
        name (text)
        location (text)
        latitude (float)
        longitude (float)

    time - contains a non-duplicate list of timestamps and converted time data
        start_time (timestamp, PRIMARY KEY)
        hour (int)
        day (int)
        week (int)
        month (int)
        year (int)
        weekday (int)


## Example Queries
The following are some examples of queries that can now be easily performed for 
user and song play analysis.

### Top 5 Most Played Songs
`SELECT songplays.song_id, songs.title, COUNT(*) FROM songplays JOIN songs 
ON songplays.song_id = songs.song_id GROUP BY songplays.song_id, songs.title 
ORDER BY COUNT(*) DESC LIMIT 5`

    song_id	            title                                                   count
    SOBONKR12A58A7A7E0	You're The One	                                        37
    SOUNZHU12A8AE47481	I CAN'T GET STARTED	                                    9
    SOHTKMO12AB01843B0	Catch You Baby (Steve Pitron & Max Sanna Radio Edit)	9
    SOULTKQ12AB018A183	Nothin' On You [feat. Bruno Mars] (Album Version)	    8
    SOLZOBD12AB0185720	Hey Daddy (Daddy's Home)	                            6

### Top 5 Most Used Browsers
`SELECT COUNT(*), user_agent FROM songplays GROUP BY user_agent ORDER BY 
COUNT(*) DESC LIMIT 5`

    count	user_agent
    51	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
    42	    Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0
    34	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
    28	    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
    22	    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"

### Top 5 Busiest Hours of the Day by Song Plays
`SELECT time.hour, COUNT(*) FROM time JOIN songplays ON time.start_time = 
songplays.start_time GROUP BY time.hour ORDER BY COUNT(*) DESC LIMIT 5`

    hour	count
    17      39
    15      25
    18      25
    16      22
     8      18

