from crontab import CronTab
from datetime import datetime
import requests, pytz

'''
This script should be scheduled to run at 1am each day.

You can check in Terminal by typing/entering `crontab -l`. If the following does not appear, you can add it in the vim editor (accessed by `crontab -e`):

0 1 * * * python {INSERT_PATH_TO_REPO_HERE}/scheduler.py
'''

def get_sunrise():
    '''Find today's sunrise time for scheduling job (https://sunrise-sunset.org/api)'''
    lat, long = 36.1627, -86.7816
    date = datetime.strftime(datetime.today(), '%Y-%m-%d')
    APIargs = lat, long, date
    response = requests.get('https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'.format(*APIargs)).json()
    sunrise_utc = response['results']['sunrise']
    sunrise_dt_utc = datetime.strptime(' '.join([date, sunrise_utc]), '%Y-%m-%d %I:%M:%S %p')
    sunrise_dt_local = sunrise_dt_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Central'))
    return sunrise_dt_local

# Open up Crontab
cron = CronTab(user='pi')

# Get job to modify. If job does not exist, create it
searchResults = list(cron.find_comment('FrasierTweeter'))
if searchResults:
    job = searchResults[0]

    # there should be only 1 job- delete any extras if they exist
    if len(searchResults) > 1:
        for extraJob in searchResults[1:]:
            extraJob.delete()
else:
    job = cron.new(command='python Frasier/FrasierTweeter.py', comment='FrasierTweeter')

# Schedule job to start at sunrise of the current day
sunrise_dt = get_sunrise()
job.minute.on(sunrise_dt.minute)
job.hour.on(sunrise_dt.hour)
# job.day.every(1)
job.enable()
cron.write()
