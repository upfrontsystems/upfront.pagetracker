import datetime
from five import grok
from zope.interface import Interface
from zope.component import getUtility

from plone.app.layout.viewlets.interfaces import IPortalFooter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from upfront.pagetracker import MessageFactory as _
from upfront.pagetracker.interfaces import IUpfrontPageTrackerLayer
from upfront.pagetracker.interfaces import IPageTracker

grok.context(Interface)
grok.layer(IUpfrontPageTrackerLayer)

class PageTrackingViewlet(grok.Viewlet):
    """ A viewlet which will log the request details on each page """

    grok.viewletmanager(IPortalFooter)

    def update(self):
        """ Log data from current request with page tracker
        """

        mt = getToolByName(self.context, 'portal_membership')
        user = mt.getAuthenticatedMember().getUserName()
        now = datetime.datetime.now()
        datetime_str = now.strftime('%d/%m/%Y %H:%M:%S')

        data = { "time" : datetime_str,
                 "url"  : self.request['URL'],
                 "user" : user }

        pagetracker = getUtility(IPageTracker)
        pagetracker.log(data)

    def render(self):
        """ No-op to keep grok.Viewlet happy
        """
        return ''
