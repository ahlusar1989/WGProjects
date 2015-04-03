# My version for w: monitors events and logs them into a log file.
#
import os.path
from pyinotify import pyinotify

timestamp = datetime.today() #time_record
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events

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
notifier = pyinotify.Notifier(wm, default_proc_fun=handler)

class Watcher(pyinotify.ProcessEvent): #I haave modified the Watcher class to process and read a new file creation or added file

    watchdir = '/tmp/watch'

    def __init__(self):
        pyinotify.ProcessEvent.__init__(self)
        wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(wm, self)
        wdd = wm.add_watch(self.watchdir, pyinotify.EventsCodes.IN_CREATE)
        print "Watching", self.watchdir
        self.notifier.start()

    def process_IN_CREATE(self, event):
        print "Seen:", event
        pathname = os.path.join(event.path, event.name)
        pfile = self._parse(pathname)
        print(pfile)

    def process_IN_MOVED_TO(self, event):
        print "Moved: %s " % os.path.join(event.path, event.name)
        pathname = os.path.join(event.path, event.name)
        pfile = self._parse(pathname)
        print(pfile)

    def _parse(self, filename):
        f = open(filename)
        file = [line.strip() for line in f]
        f.close()
        return file


class Log(pyinotify.ProcessEvent):
    def my_init(self, fileobj):
        """
        Method automatically called from ProcessEvent.__init__(). Additional
        keyworded arguments passed to ProcessEvent.__init__() are then
        delegated to my_init(). This is the case for fileobj.
        """
        self._fileobj = fileobj

    def process_default(self, event):
        self._fileobj.write(str(event) + '\n')
        self._fileobj.flush()

class TrackModifications(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print 'IN_MODIFY'

class Empty(pyinotify.ProcessEvent): #Inherited class to display message  
    def my_init(self, msg):
        self._msg = msg

    def process_default(self, event): #writes decribing the event
        print self._msg


# pyinotify.log.setLevel(10)
filelog = file('/Failure', 'w')

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    # It is important to pass named extra arguments like 'fileobj'
        handler = Empty(TrackModifications(Log(fileobj=filelog)), msg='This is an error message or notificaiton that will be logged  ')
        wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
        notifier.loop()
    except KeyboardInterrupt:
        notifier.stop()
        break
    finally:
        filelog.close()


if __name__ == '__main__':
      Watcher()

