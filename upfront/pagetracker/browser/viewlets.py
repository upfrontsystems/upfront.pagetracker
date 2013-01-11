from five import grok
from zope.interface import Interface
from zope.component import getUtility

from plone.app.layout.viewlets.interfaces import IPortalFooter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from upfront.pagetracker import MessageFactory as _
from upfront.pagetracker.interfaces import IUpfrontPageTrackerLayer

grok.context(Interface)
grok.layer(IUpfrontPageTrackerLayer)

class PageTrackingViewlet(grok.Viewlet):
    """ A viewlet which will log the request details on each page """

    grok.viewletmanager(IPortalFooter)

    def update(self):
        """ XXX Log  """
        print 'Log to page tracker'
        # log = getUtility(IPageTrackingUtility)
        return

    def render(self):
        """ No-op to keep grok.Viewlet happy
        """
        return ''
