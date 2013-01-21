import datetime
from time import time
from zope.component import getUtility
from z3c.form.i18n import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from upfront.pagetracker.interfaces import IPageTracker
from upfront.pagetracker.tests.base import UpfrontPageTrackerTestBase

class TestExportLoggedRequestsView(UpfrontPageTrackerTestBase):
    """ Test ExportLoggedRequestsView view """


    def test_logged_requests_csv(self):

        pagetracker = getUtility(IPageTracker)
        pagetracker._clear_log() # clear potential leftovers from unit tests

        view = self.portal.restrictedTraverse('@@export-logged-requests')
        test_out = view()
        self.assertEqual(test_out,None)

        # create 1 entry in the log
        self.browser.open(self.portal.absolute_url() + '/login_form')
        now = datetime.datetime.now()
        datetime_str = now.strftime('%d/%m/%Y %H:%M:%S')

        view = self.portal.restrictedTraverse('@@export-logged-requests')

        test_out = view()
        csv_ref = datetime_str +\
                  ',http://nohost/plone/login_form,Anonymous User\r\n'

        self.assertEqual(test_out,csv_ref)

        start = str(int(time())-500)
        end = str(int(time()))

        # test with some date paramenters on the request
        self.request.set('start_date',start)
        self.request.set('end_date',end)
        view = self.portal.restrictedTraverse('@@export-logged-requests')
        test_out = view()
        self.assertEqual(test_out,csv_ref)

    def test__call__(self):

        pagetracker = getUtility(IPageTracker)
        pagetracker._clear_log() # clear potential leftovers from unit tests

        view = self.portal.restrictedTraverse('@@export-logged-requests')
        test_out = view()
        self.assertEqual(test_out,None)
        test = IStatusMessage(self.request).show()
        self.assertEqual(test[0].type,'info')
        self.assertEqual(test[0].message,'No log entries exist')

        # create 1 entry in the log
        self.browser.open(self.portal.absolute_url() + '/login_form')
        now = datetime.datetime.now()
        datetime_str = now.strftime('%d/%m/%Y %H:%M:%S')

        view = self.portal.restrictedTraverse('@@export-logged-requests')

        test_out = view()
        csv_ref = datetime_str +\
                  ',http://nohost/plone/login_form,Anonymous User\r\n'

        self.assertEqual(test_out,csv_ref)
        ct = self.request.response.getHeader("Content-Type")
        self.assertEqual(ct,"text/csv")

        start = str(int(time())-500)
        end = str(int(time()))

        # test with some date paramenters on the request
        self.request.set('start_date',start)
        self.request.set('end_date',end)
        view = self.portal.restrictedTraverse('@@export-logged-requests')
        test_out = view()
        self.assertEqual(test_out,csv_ref)
        ct = self.request.response.getHeader("Content-Type")
        self.assertEqual(ct,"text/csv")

