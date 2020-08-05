# WakeTime App v1.0 - AUG 2020 by D.Leicht
# https://github.com/dleicht/waketime

import rumps, subprocess
from datetime import datetime

rumps.debug_mode(False)  # turn on command line logging information for development - default is off

def get_datestrings():
    # Get datestrings from bash, decoding bytestream to string
    # Omit the seconds with awk: pmset -g log | grep -w 'Wake from' | tail -1 | awk '{print $1, substr($2, 1, length($2)-3)}'
    LatestWake = subprocess.check_output("pmset -g log | grep -w 'Wake from' | tail -1 | awk '{print $1, $2}'", shell=True).decode("utf-8").strip()
    LatestStart = subprocess.check_output("pmset -g log | grep -w 'Start' | tail -1 | awk '{print $1, $2}'", shell=True).decode("utf-8").strip()
    CurrentTime = subprocess.check_output("date +'%Y-%m-%d %H:%M:%S'", shell=True).decode("utf-8").strip()

    # Convert datestrings to python datetime in order to calculate the timedelta
    dLatestWake = datetime.strptime(LatestWake, '%Y-%m-%d %H:%M:%S')
    dLatestStart = datetime.strptime(LatestStart, '%Y-%m-%d %H:%M:%S')
    dCurrentTime = datetime.strptime(CurrentTime, '%Y-%m-%d %H:%M:%S')
    
    # Put these in a dictionary and return it
    d = {
        "CurrentTime": dCurrentTime,
        "LatestStart": dLatestStart,
        "LatestWake": dLatestWake
    }

    return d

def fake_func():
    pass

class WakeTimeApp(rumps.App):

    def __init__(self, name, *args, **kwargs):
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
    
        def update_datestrings():
            print("Updating datestrings...")
            try:    
                datestrings = get_datestrings()
                if (datestrings['CurrentTime'] - datestrings['LatestStart']) < (datestrings['CurrentTime'] - datestrings['LatestWake']):
                    self.lateststart_menuitem.title = str((datestrings['CurrentTime'] - datestrings['LatestStart']))
                    self.latestwake_menuitem.title = "No wake so far!"
                    if self.icontoggle_menuitem.state != 1:
                        self.title = str((datestrings['CurrentTime'] - datestrings['LatestStart']))
                        self.icon = None
                    else:
                        self.title = None
                        self.icon = 'timer.png'
                else:
                    self.lateststart_menuitem.title = str((datestrings['CurrentTime'] - datestrings['LatestStart']))
                    self.latestwake_menuitem.title = str((datestrings['CurrentTime'] - datestrings['LatestWake']))
                    if self.icontoggle_menuitem.state != 1:
                        self.title = str((datestrings['CurrentTime'] - datestrings['LatestWake']))
                        self.icon = None
                    else:
                        self.title = None
                        self.icon = 'timer.png'
            except Exception as e:
                self.lateststart_menuitem.title = str(e)
                self.latestwake_menuitem.title = str(e)
                self.title = 'Err'
                self.icon = None
    
        update_datestrings()

        @rumps.clicked("Toggle App Icon")
        def toggle_appicon(sender):
            sender.state = not sender.state
            update_datestrings()

        @rumps.clicked("About")
        def about(sender):
            rumps.alert(title='WakeTime App', message='Version 1.0 - AUG 2020 by D. Leicht\nhttps://github.com/dleicht/waketime\n\nTracking uptime and waketime\nlike there is no tomorrow!\n\nLicensed under MIT.\nFramework7 icons licensed under MIT.', ok=None, cancel=None)

        @rumps.timer(60)  # create a new thread that calls the decorated function every 60 seconds
        def a(sender):
            update_datestrings()
        

if __name__ == "__main__":
    WakeTimeApp("").run()
