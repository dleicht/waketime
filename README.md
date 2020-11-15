# WakeTime App [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) ![macOS: 11.0.1+](https://img.shields.io/badge/macOS-11.0.1%2B-green) ![Python: 3](https://img.shields.io/badge/Python-3-green)
Tracking uptime and waketime on macOS. Every 60 Seconds. In your statusbar.

![Screen 1](https://raw.githubusercontent.com/dleicht/waketime/master/screen1.png)
![Screen 2](https://raw.githubusercontent.com/dleicht/waketime/master/screen2.png)
![Screen 3](https://raw.githubusercontent.com/dleicht/waketime/master/screen3.png)

### Big Sur ready!
Yeah, you read that right. I took the plunge and updated to Big Sur. All those colors, quite cute. Now guess what: WakeTime App just kept working like a champ.

### Why?
I need to keep track of the time spent working with my macbook. On a mobile device uptime (time since boot) is corrupted by sleeptime (time the device is asleep). I'm actually more interested in waketime (time since last wake from sleep), as it allows me to see how long i've been working in one session.

### How?
This is a simple self-contained python app. Built as a 64bit macOS executable, suitable for macOS 10.14 and above. It utilizes [rumps](https://github.com/jaredks/rumps) to function as a simple macOS statusbar app.
As such it will display uptime and also waketime, if a wake event occured after boot.
If you choose to toggle the app icon the actual uptime or waketime will be displayed directly in your statusbar.

- waketime is calculated by parsing ```pmset -g log```
- uptime is calculated using [uptime](https://github.com/Cairnarvon/uptime)

The format of the displayed time string is: ```D:HH:MM``` Days:Hours:Minutes

I intended to provide backwards compatibility all the way back to Snow Leopard 10.6. But over iterations of macOS all sorts of things changed, including pmset itself, the inner workings of python and how things are written to log files. CBA to sort it all out :) So for now this is macOS 10.14+
It's totally possible that this will no longer work as soon as Apple changes things. Just let me know if that's the case (i prolly wouldn't know as i never use the most recent macOS :)

### Next?
In a next iteration i might sum up all waketimes after boot in order to calculate something like:
- usagetime (time the system was up and i was actually using it)
- sleeptime (time the system was up, but sleeping)
