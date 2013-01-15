from csv import DictWriter
from cStringIO import StringIO
from DateTime import DateTime

from time import time
from BTrees.IOBTree import IOBTree
from persistent import Persistent
from zope.interface import implements
from zope.interface import Interface

from Products.statusmessages.interfaces import IStatusMessage

from upfront.pagetracker import MessageFactory as _
from upfront.pagetracker.interfaces import IPageTracker

class PageTracker(Persistent):
    """ Utility used to track detailed use of a site
    """
    implements(IPageTracker)
    
    def __init__(self):
        self.pagetracker = IOBTree()

    def log(self, data):
        """ Log a single page request
        """

        key = int(time())
        if not self.pagetracker.has_key(key):
            # init key entry to an empty list if entry does not exist yet.
            self.pagetracker[key] = []

        self.pagetracker[key].append(data)

    def logged_data(self, start_date=False, end_date=False):
        """ Return the logged requests (optionally for a given date range)
        """

        if start_date and end_date:
            if start_date > end_date:
                return
            log_entries = self.pagetracker.items(start_date,end_date)
        else:
            log_entries = self.pagetracker.items()

        return log_entries

    def _clear_log(self):
        """ Remove all entries from the log (use as auxilary for unit tests)
        """
        self.pagetracker.clear()

