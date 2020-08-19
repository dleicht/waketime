# WakeTime App v1.1 - AUG 2020 by D.Leicht
# https://github.com/dleicht/waketime

import rumps, syslog
from uptime import uptime
from subprocess import check_output
from datetime import datetime

class WakeTimeApp(rumps.App):
    rumps.debug_mode(False)  # turn on command line logging information for development - default is off
    syslog.openlog("WakeTime App")    

    def __init__(self, name, *args, **kwargs):
        def fake_func():
            pass
        
        super(WakeTimeApp, self).__init__(name, *args, **kwargs)
        self.title = None
        self.template = True
        self.icon = 'timer.png'
        self.lateststart_menuitem = rumps.MenuItem("", callback=fake_func, icon='power.png', dimensions=(18, 18), template=True)
        self.latestwake_menuitem = rumps.MenuItem("", callback=fake_func, icon='sunrise.png', dimensions=(18, 18), template=True)
        self.icontoggle_menuitem = rumps.MenuItem("Toggle App Icon")
        self.menu.add(self.lateststart_menuitem)
        self.menu.add(self.latestwake_menuitem)
        self.menu.add(self.icontoggle_menuitem)
        self.icontoggle_menuitem.state = 1
        self.menu.add(None)
        self.about_menuitem = rumps.MenuItem("About")
        self.menu.add(self.about_menuitem)

        def logthis(event): # Log to /var/log/system.log
            syslog.syslog(syslog.LOG_ALERT, str(event)) # Make sure event is a string

        def get_uptime(): # Get seconds since latest system start
            try:
                uptime_seconds = uptime()
                return uptime_seconds
            except Exception as e:
                logthis('get_uptime() ERROR: {} {}'.format(type(e), e))
                uptime_seconds = 0
                return uptime_seconds

        def get_waketime(): # Get seconds since latest wake event, or 0 if no wake event was found
            try:
                # Get datestrings from bash, decoding bytestream to string
                LatestWake = check_output("pmset -g log | grep -w 'Wake from' | tail -1 | awk '{print $1, $2}'", shell=True).decode("utf-8").strip()
                CurrentTime = check_output("date +'%Y-%m-%d %H:%M:%S'", shell=True).decode("utf-8").strip()

                # Convert datestrings to python datetime in order to calculate the timedelta
                dLatestWake = datetime.strptime(LatestWake, '%Y-%m-%d %H:%M:%S')
                dCurrentTime = datetime.strptime(CurrentTime, '%Y-%m-%d %H:%M:%S')

                # Get total seconds of waketime from the waketime timedelta
                waketime_seconds = (dCurrentTime - dLatestWake)
                return waketime_seconds.total_seconds()
            except Exception as e:
                logthis('get_waketime() ERROR: {} {}'.format(type(e), e))
                waketime_seconds = 0
                return waketime_seconds
        
        def convert_seconds(seconds): # Calculate days, hours and minutes from total seconds and store them in a tuple
            seconds_day = 60 * 60 * 24
            seconds_hour = 60 * 60
            seconds_minute = 60

            
            days = int(seconds // seconds_day)
            hours = int((seconds - (days * seconds_day))) // seconds_hour
            minutes = int((seconds - (days * seconds_day) - (hours * seconds_hour))) // seconds_minute

            time_tuple = (days, hours, minutes)
            return time_tuple

        def set_timestring(time_tuple): 
            """ The format of the string is important. Space is tight in your statusbar. We want to make sure that the string has a
                consistent look and takes as little space as possible. The desired format is: D:HH:MM. Luckily python makes it super easy
                to format the timestring from the given time_tuple accordingly."""
            timestring = '{}:{:02}:{:02}'.format(time_tuple[0], time_tuple[1], time_tuple[2])
            return timestring

        def update_datestrings():
            uptime_seconds = get_uptime()
            waketime_seconds = get_waketime()
            if uptime_seconds < waketime_seconds:
                waketime_seconds = uptime_seconds
                up_timestring = set_timestring(convert_seconds(uptime_seconds))
                wake_timestring = set_timestring(convert_seconds(waketime_seconds))
                logthis("Uptime: "+up_timestring+" Waketime: "+wake_timestring)
                self.lateststart_menuitem.title = up_timestring
                self.latestwake_menuitem.title = wake_timestring
                self.latestwake_menuitem.set_callback(None)
                if self.icontoggle_menuitem.state != 1:
                    self.title = up_timestring
                    self.icon = None
                else:
                    self.title = None
                    self.icon = 'timer.png'
            else:
                up_timestring = set_timestring(convert_seconds(uptime_seconds))
                wake_timestring = set_timestring(convert_seconds(waketime_seconds))
                logthis("Uptime: "+up_timestring+" Waketime: "+wake_timestring)
                self.lateststart_menuitem.title = up_timestring
                self.latestwake_menuitem.title = wake_timestring
                self.latestwake_menuitem.set_callback(fake_func)
                if self.icontoggle_menuitem.state != 1:
                    self.title = wake_timestring
                    self.icon = None
                else:
                    self.title = None
                    self.icon = 'timer.png'

        @rumps.clicked("Toggle App Icon")
        def toggle_appicon(sender):
            sender.state = not sender.state
            update_datestrings()

        @rumps.clicked("About")
        def about(sender):
            rumps.alert(title='WakeTime App', message='Version 1.1 - AUG 2020 by D. Leicht\nhttps://github.com/dleicht/waketime\n\nTracking uptime and waketime\nlike there is no tomorrow!\n\nLicensed under MIT.\n\nrumps licensed under BSD 3-Clause.\npython-uptime licensed under BSD 2-Clause.\nFramework7 icons licensed under MIT.', ok=None, cancel=None)

        @rumps.timer(60)  # create a new thread that calls the decorated function every 60 seconds
        def a(sender):
            update_datestrings()

if __name__ == "__main__":
    WakeTimeApp("").run()