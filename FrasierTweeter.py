import tweepy, json, time, requests, pytz
from datetime import datetime, timedelta
from picamera import PiCamera

class FrasierTweeter(object):

    def __init__():
        self.lat, self.long = 36.1627, -86.7816
        self.date = datetime.strftime(datetime.today(), '%Y-%m-%d')
        self.date_tomorrow = datetime.strftime(datetime.now() + timedelta(days=1), '%Y-%m-%d')
        self.local_tz = pytz.timezone('US/Central')
        self.twitter = self._get_api()

    def _get_api():
        '''Connect to Twitter API, requires `keys.json`'''
        cfg = json.load(open('keys.json'))
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def timelapse():
        camera = PiCamera()
        camera.resolution = (1024,768)
        camera.start_preview()
        time.sleep(2) # let camera warm up / get started
        sunrise_dt, sunset_dt = self._get_suntime()
        for filename in camera.capture_continuous('imgs/img{timestamp:%Y-%m-%d-%H-%M}'.jpg):
            while sunrise_dt < datetime.now().replace(tzinfo=self.local_tz) < sunset_dt:
            print 'Captured {}'.format(filename)
            self._wait()

    def _wait():
        '''Helper fcn to wait 2 min between image captures'''
        next_2min = (datetime.now() + timedelta(minutes=2)).replace(minute=0, second=0, microsecond=0)
        delay = (next_2min - datetime.now()).seconds
        time.sleep(delay)

    def tweet():
        tweet = "Hello, world!"
        status = api.update_status(status=tweet)

    def _get_suntime():
        '''Find sunrise/sunset to know long to take screen captures each day (https://sunrise-sunset.org/api)'''
        APIargs = (self.lat, self.long, self.date)
        response = requests.get('https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'.format(*APIargs)).json()

        sunrise = response['results']['sunrise']
        sunrise_dt = _localize_time(self.date, sunrise)

        sunset = response['results']['sunset']
        if sunset[-2:] == 'AM':
            sunset_dt = _UTC2local(self.date_tomorrow, sunset)
        else:
            sunset_dt = _UTC2local(self.date, sunset)

        print 'Sunrise: {}\nSunset: {}'.format(sunrise_dt, sunset_dt)

    def _UTC2local(date, time):
        '''Helper fcn UTC time to local time'''
        dt_utc = datetime.strptime(' '.join([date, time]), '%Y-%m-%d %I:%M:%S %p')
        dt_local = dt_utc.replace(tzinfo=pytz.utc).astimezone(self.local_tz)
        return dt_local

def main():
    ft = FrasierTweeter()
    ft.timelapse()
    ft.tweet()

if __name__ == '__main__':
    main()
