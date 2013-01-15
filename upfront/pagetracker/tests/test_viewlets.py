import datetime
from zope.component import getUtility

from upfront.pagetracker.interfaces import IUpfrontPageTrackerLayer
from upfront.pagetracker.interfaces import IPageTracker

from base import UpfrontPageTrackerTestBase

class TestPageTrackingViewlet(UpfrontPageTrackerTestBase):
    """ Basic methods to test page tracking viewlet """

    def test_logrequest(self):

        context = self.portal
        manager_name = 'plone.portalfooter'
        viewlet_name = 'pagetrackingviewlet'
        layer = IUpfrontPageTrackerLayer
        viewlet = self._find_viewlet(context, manager_name, viewlet_name, layer)

        pagetracker = getUtility(IPageTracker)
        pagetracker._clear_log() # clear potential leftovers from unit tests

        viewlet[0].update()
        now = datetime.datetime.now()
        datetime_str = now.strftime('%d/%m/%Y %H:%M:%S')
        
        result = pagetracker.logged_data()
        self.assertEqual(result[0][1][0]['url'],'http://nohost')
        self.assertEqual(result[0][1][0]['user'],'test-user')

        # final assertion test is commented out as it depends on exact time,
        # it works but perhaps it could fail someday due to something taking
        # longer
        # self.assertEqual(result[0][1][0]['time'],datetime_str)

