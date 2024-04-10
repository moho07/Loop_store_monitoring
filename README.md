# Store Monitoring

## Problem Statement

We monitor several restaurants in the US and need to monitor if the store is online or not. All restaurants are supposed to be online during their business hours. Due to some unknown reasons, a store might go inactive for a few hours. Restaurant owners want to get a report of the how often this happened in the past.

We want to build backend APIs that will help restaurant owners achieve this goal.

## Data Sources

We will have 3 sources of data

1. We poll every store roughly every hour and have data about whether the store was active or not in a CSV. The CSV has 3 columns (`store_id, timestamp_utc, status`) where status is active or inactive. All timestamps are in **UTC**

   a. Data can be found in CSV format [here](https://drive.google.com/file/d/1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025/view?usp=sharing)

2. We have the business hours of all the stores - schema of this data is `store_id, dayOfWeek(0=Monday, 6=Sunday), start_time_local, end_time_local`

   a. These times are in the **local time zone**

   b. If data is missing for a store, assume it is open 24\*7

   c. Data can be found in CSV format [here](https://drive.google.com/file/d/1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg/view?usp=sharing)

3. Timezone for the stores - schema is `store_id, timezone_str`

   a. If data is missing for a store, assume it is America/Chicago

   b. This is used so that data sources 1 and 2 can be compared against each other.

   c. Data can be found in CSV format [here](https://drive.google.com/file/d/101P9quxHoMZMZCVWQ5o-shonk2lgK1-o/view?usp=sharing)

## API Endpoints

There are two API endpoints -

1. /trigger_report endpoint that will trigger report generation from the data provided (stored in DB)-\
   a. No input\
   b. Output - report_id\
   c. report_id will be used for polling the status of report completion

2. /get_report endpoint that will return the status of the report or the csv-\
   a. Input - report_id\
   b. Output
   - if report generation is not complete, return “Running” as the output.
   - if report generation is complete, return “Complete” along with the CSV file with the schema described above.
  
## Logic for last_one_day (uptime and downtime)

1. Initialize a dictionary last_one_day_data with keys "uptime" and "downtime". The values for "uptime" and "downtime" are set to 0.
2. Calculate one_day_ago as the day of the week one day before the current_day. If current_day is 0 (Monday), set one_day_ago to 6 (Sunday), if current_day is 2 (Wednesday), set one_day_ago to 1 (Tuesday) and so on.
3. Check if the store is open during the last one day (one_day_ago to current_day) at the current time (current_time). 
4. This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
5. If the store is not open during the last one day, return the initialized last_one_day_data.
6. If the store is open during the last one day, query the store.status_logs to get all the logs within the last one day (utc_time - 1 day to utc_time) and order them by timestamp.
7. Loop through each log in last_one_day_logs:
8. Check if the log's timestamp falls within the store's business hours on that day (log_in_store_business_hours). This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
9. If the log is not within the store's business hours, skip it and move to the next log.
10. If the log's status is "active", increment the "uptime" value in last_one_day_data by 1 hour.
11. If the log's status is not "active", increment the "downtime" value in last_one_day_data by 1 hour.
12. Same logic has been followed for last one hour and last one week uptime and downtime.


## Environment Setup

1. Make sure you have Python installed on your system. Refer to this [link](https://www.python.org/downloads/) to download latest version of Python.

2. Make sure to have Django installed on your system before running this program. Refer to this [link](https://www.djangoproject.com/download/) to install latest version of Django.

## Running the program

1. Create a virtual environment using the below command -

```
python3 -m venv myenv
```

2. Activate the virtual enviromnent using the command -

```
source myenv/bin/activate
```

3. Clone the repository inside the virtual environment.

```
git clone https://github.com/Apoorvg2000/store_monitoring_loop.git
```

**NOTE**: Make sure to run below commands from the parent directory of manage.py file.

4. Install the required libraries by running the below command -

```
pip install -r requirements.txt
```

5. Setup a Postgresql database, and change the database credentials in the `main/settings.py` file. Refer to this [link](https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb#3-configuring-postgres) to setup a PostgreSQL database.

6. To populate the database with the data in .csv files in `scripts/data` directory, run the below command -

```
python3 manage.py runscript load
```

This will populate the database with all the required data before running the server.

7. After all the above steps are completed, run the below command to launch the server -

```
python3 manage.py runserver
```

Now open your web browser and enter the following address to launch the web app `http://127.0.0.1:8000/`

8. To trigger report generation, click on the `Trigger Report` button on the webpage. This will trigger the `/trigger_report` API endpoint and store the generated report in the database as well as in your local computer. The output will be a `report_id` using which you can view the generated report.

**NOTE**: We are generating report for only the first 100 stores as it will take a lot of time to generate the report for all the stores. We can change that number anytime in the code.

9. To view the generated report, enter the the `report_id` and hit `Get Report` button. This will show the generated report and its url on the local computer, on the webpage if it is completed with its `Status` as "Completed", otherwise its `Status` will be shown as "Running".

## Demo Video

Refer to this [link](https://drive.google.com/file/d/1fgLPQOHqMFRLEEwXjqcU5HHz59YWjuyU/view?usp=share_link) to watch the demo video.


