#!/usr/bin/env python

# monitors both files and dirs for file creation and whether or not file was moved

import os
import pyinotify
from datetime import datetime
import difflib
import sys
import os


timestamp = datetime.today() #time_record
wm = pyinotify.WatchManager() #Watch Manager
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO #watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Created: %s " % os.path.join(event.path, event.name)
        event_log = open('/Users/sahluwalia/Desktop/', 'a')
        event_log.write(event.name + ' - ' + timestamp.strftime('%c') + '\n')
        event_log.close()

    def process_IN_MOVED_TO(self, event):
        print "Moved: %s " % os.path.join(event.path, event.name)
        event_log = open('/Users/sahluwalia/Desktop/', 'a')
        event_log.write(event.name + ' - ' + timestamp.strftime('%c') + '\n')
        event_log.close()


handler = EventHandler() #instantiated EventHandler Class
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch('/Users/sahluwalia', mask, rec=True)

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:       
        notifier.stop()
        break

notifier.loop() #