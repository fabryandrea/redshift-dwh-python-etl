# Analyzing Music Streaming: Event Data Modeling with Postgres and ETL Pipeline with Python


## 1.	Motivation

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## 2.  Approach

The solution was to create a Postgres database with tables designed to optimize queries on song play analysis. I created a database schema designed for this particular analytic focus. I defined `songplays` as a fact table and `songs`, `artists`, `users` and `time` as dimension tables for a star schema. I then wrote an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL. The resulting database supports queries about customers, the music they stream, and the time periods when they use the app.

### Schema for Analyzing Songplays

#### Fact Table
**songplays** - records in log data associated with song plays i.e. records with page `NextSong`
* *songplay_id*, *start_time*, *user_id*, *level*, *song_id*, *artist_id*, *session_id*, *location*, *user_agent*

#### Dimension Tables
**users** - users in the app
* *user_id*, *first_name*, *last_name*, *gender*, *level*

**songs** - songs in music database
* *song_id*, *title*, *artist_id*, *year*, *duration*

**artists** - artists in music database
* *artist_id*, *name*, *location*, *lattitude*, *longitude*

**time** - timestamps of records in songplays broken down into specific units
* *start_time*, *hour*, *day*, *week*, *month*, *year*, *weekday*

## 3.  Sample Queries
The database and ETL pipeline was then tested by running queries given to you by the analytics team from Sparkify and compare your results with their expected results. The queries included:
* Find all the paying customers, who are they, what songs they listen to and if they are male or not
* Give me only the following: name of artist, song and user (first and last name) for user ID = 10, session ID = 182
* Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

## Technologies
Project is created with:
* Python version: 3.7.1
* psycopg2 version: 2.7.6.1
* pandas version: 0.23.4

## Setup
To run this project, install all packages with `pip install -r requirements.txt`, then run:
```
$ python create_tables.py
$ python etl.py
```

## Files
* `create_tables.py` drops and creates the tables. Run this file to reset your tables before each time you run your ETL scripts.
* `etl.py` reads and processes files from `song_data` and `log_data` and loads them into the tables.
* `sql_queries.py` contains all sql queries, and is imported into the two files above.
* `requirements.txt`lists all the package requirements.
