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
        """ log a page request
        """

        key = int(time())
        if not self.pagetracker.has_key(key):
            # init key entry to an empty list if entry does not exist yet.
            self.pagetracker[key] = []

        self.pagetracker[key].append(data)

    def export_log_csv(self, start_date=False, end_date=False, REQUEST=False):
        """ export the requests for a given date range as CSV file with the
            following columns: time, path, username
            optional start_date and end_date must be in epoch time format
        """

        if start_date and end_date:
            if start_date > end_date:
                return
            log_entries = self.pagetracker.items(start_date,end_date)
        else:
            log_entries = self.pagetracker.items()

        csv_content = None
        log_csv = StringIO()

        if log_entries is not None and len(log_entries) > 0:
            writer = DictWriter(log_csv,
                                fieldnames=['time', 'path', 'username'],
                                restval='',
                                extrasaction='ignore',
                                dialect='excel'
                               )

            # iterate over log entries
            for entry in range(len(log_entries)):
    
                # iterate over entries that happened at the same epoch (if any)
                for item in range(len(log_entries[entry][1])):
    
                    ldict={'time': log_entries[entry][1][item]['time'],
                           'path': log_entries[entry][1][item]['url'],
                           'username': log_entries[entry][1][item]['user'],
                          }
                    writer.writerow(ldict)
            
            csv_content = log_csv.getvalue()
            log_csv.close()

            now = DateTime()
            nice_filename = '%s_%s' % ('requestlog_', now.strftime('%Y%m%d'))

            if REQUEST:
                REQUEST.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.csv" % 
                                             nice_filename)
                REQUEST.response.setHeader("Content-Type", "text/csv")
                REQUEST.response.setHeader("Content-Length", len(csv_content))
                REQUEST.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
                REQUEST.response.setHeader("Cache-Control", "no-store")
                REQUEST.response.setHeader("Pragma", "no-cache")

                REQUEST.response.write(csv_content)

        else:
            msg = _('No log entries exist')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        return csv_content


