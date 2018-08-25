## FrasierTweeter

This project captures a timelapse of a Fraser fir tree growing and tweets updates.

##### Requirements
+ RaspberryPi w/ camera attachment
+ Python packages: `tweepy`, `picamera`, `time`, `datetime`, `pytz`, `requests`, `json`
<br><br>^Use `pip install requirements.txt` to install these

##### Files
+ `FrasierTweeter.py`
+ `scheduler.py`
<br>This script schedules the daily image captures based on sunrise/sunset times. This should be scheduled to run daily using [CRON](https://www.raspberrypi.org/documentation/linux/usage/cron.md).
<br><br>After installing CRON, open up your Terminal and type `crontab -e` to access the vim editor for adding the task. Type `i` (for **i**nsert), then the following:
```
0 1 * * * python {INSERT_PATH_TO_REPO_HERE}/scheduler.py
```
This tells the machine to run `scheduler.py` every day at 1AM. Press `ESC` to finish editing, then `:wq` (**w**rite, **q**uit) to save your changes.
<br><br>You can check your existing CRON tasks typing `crontab -l` into the terminal.
