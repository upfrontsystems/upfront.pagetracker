from time import time
from BTrees.IOBTree import IOBTree
from persistent import Persistent
from zope.interface import implements
from zope.interface import Interface

from upfront.pagetracker.interfaces import IPageTracker

class PageTracker(Persistent):
    """ Utility used to track detailed use of a site
    """
    implements(IPageTracker)
    
    def __init__(self):
        self.pagetracker = IOBTree()

    def log(self, data):
        """ log a page request
        """

        key = int(time())
        if not self.pagetracker.has_key(key):
            # init key entry to an empty list if entry does not exist yet.
            self.pagetracker[key] = []

        self.pagetracker[key].append(data)

    def export_log_csv(self, start_time, end_time):
        """ export the requests for a given time interval to a csv file
        """
        
        # XXX TODO
        # start_time and end_time must be in epoch format before querying Tree

        return self.pagetracker.items(start_time,end_time)      

