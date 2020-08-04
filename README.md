# WakeTime App
Tracking uptime and waketime on macOS.

![Screen 1](https://raw.githubusercontent.com/dleicht/waketime/master/screen1.png)
![Screen 2](https://raw.githubusercontent.com/dleicht/waketime/master/screen2.png)
![Screen 3](https://raw.githubusercontent.com/dleicht/waketime/master/screen3.png)

### Why?
I need to keep track of the time spent working with my macbook. On a mobile device uptime (time since boot) is corrupted by sleeptime (time the device is asleep). I'm actually more interested in waketime (time since last wake from sleep), as it allows me to see how long i've been working in one session.

### How?
This is a simple python app. It utilizes [rumps](https://github.com/jaredks/rumps) to function as a simple macOS statusbar app.
As such it will display uptime and also waketime, if a wake event occured after boot.
If you choose to toggle the app icon the actual uptime or waketime will be displayed directly in your status bar.
