from csv import DictWriter
from cStringIO import StringIO
from DateTime import DateTime

from five import grok
from zope.interface import Interface
from zope.component import getUtility

from Products.statusmessages.interfaces import IStatusMessage

from upfront.pagetracker import MessageFactory as _
from upfront.pagetracker.interfaces import IPageTracker

class ExportLoggedRequestsView(grok.View):
    """ Export the requests for a given date range as CSV file with the
        following columns: time, path, username
        optional start_date and end_date must be in epoch time format
    """
    grok.context(Interface)
    grok.name('export-logged-requests')
    grok.require('zope2.View')

    def __call__(self):
        """ Export the requests for a given date range as CSV file with the
            following columns: time, path, username
            optional start_date and end_date must be in epoch time format
        """

        # get optional parameters off the request
        start_date = self.request.get('start_date', '')
        end_date = self.request.get('end_date', '')

        pagetracker = getUtility(IPageTracker)
        if start_date != '' and end_date != '':
            start = int(start_date)
            end = int(end_date)
            log_entries = pagetracker.logged_data(start, end)
        else:
            log_entries = pagetracker.logged_data()

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

            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.csv" % 
                                             nice_filename)
            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader("Content-Length", len(csv_content))
            self.request.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")

            self.request.response.write(csv_content)

        else:
            msg = _('No log entries exist')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        return csv_content

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
