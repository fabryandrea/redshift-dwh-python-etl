# Data Infrastructure on the Cloud: Dimensional Modeling of Streaming Event Data with Amazon Redshift

## 1.	Motivation

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## 2.  Approach

To enable the Sparkify analytics team to continue finding insights in what songs their users are listening to, I built an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables. The streaming event data was modeled using a star schema, with `songplays` as a central fact table and `songs`, `artists`, `users` and `time` as dimension tables optimized for queries on song play analysis. I used `boto3` to create a database hosted on Redshift and then wrote an ETL pipeline that uses Python and SQL to extract, stage, and model the event data. The resulting database supports optimized fast queries about customers, the music they stream, and the time periods when they use the app.

## Schema for Song Play Analysis

### Fact Table
1. **songplays** - records in event data associated with song plays i.e. records with page `NextSong` <br>
*songplay_id*, *start_time*, *user_id*, *level*, *song_id*, *artist_id*, *session_id*, *location*, *user_agent*

### Dimension Tables
2. **users** - users in the app <br>
*user_id*, *first_name*, *last_name*, *gender*, *level*
4. **songs** - songs in music database <br>
*song_id*, *title*, *artist_id*, *year*, *duration*
5. **artists** - artists in music database <br>
*artist_id*, *name*, *location*, *latitude*, *longitude*
6. **time** - timestamps of records in songplays broken down into specific units <br>
*start_time*, *hour*, *day*, *week*, *month*, *year*, *weekday*


## Technologies
Project is created with:
* Python version: 3.7.1
* psycopg2 version: 2.7.6.1

## Setup
To run this project, install all packages with `pip install -r requirements.txt`, then run:
```
$ python create_tables.py
$ python etl.py
```

## Files
* `create_tables.py` creates the fact and dimension tables for the star schema in Redshift.
* `etl.py` loads data from S3 into staging tables on Redshift and then processes that data into analytics tables on Redshift.
* `sql_queries.py` defines all SQL statements, which are then imported into the two other files above.
* `dwh.cfg`is a file used by the configparser module to load the appropriate access keys and filepaths to manage AWS credentials. It is provided as an example, the `KEY` and `SECRET KEY` sections have been left blank.
* `requirements.txt`lists all the package requirements.
