from time import time
from zope.component import getUtility

from base import UpfrontPageTrackerTestBase
from upfront.pagetracker.interfaces import IPageTracker

class TestPageTracker(UpfrontPageTrackerTestBase):
    """ Basic methods to test pagetracker methods """
    
    def test_log(self):

        # this tests 'log' and 'logged_data' methods without date range
        data = { "time" : 'time',
                 "url"  : 'http://test',
                 "user" : 'userone' }
        pagetracker = getUtility(IPageTracker)
        pagetracker.log(data)
        result = pagetracker.logged_data()
        self.assertEqual(result[0][1][0]['time'],'time')
        self.assertEqual(result[0][1][0]['url'],'http://test')
        self.assertEqual(result[0][1][0]['user'],'userone')

    def test_logged_data(self):

        # this tests 'log' and 'logged_data' methods with a date range
        data = { "time" : 'time',
                 "url"  : 'http://test',
                 "user" : 'userone' }
        pagetracker = getUtility(IPageTracker)
        pagetracker.log(data)
        # specify wide time range
        start = int(time())-1000
        end = int(time())
        result = pagetracker.logged_data(start,end)
        self.assertEqual(result[0][1][0]['time'],'time')
        self.assertEqual(result[0][1][0]['url'],'http://test')
        self.assertEqual(result[0][1][0]['user'],'userone')
