from zope.interface import Interface
from upfront.pagetracker import MessageFactory as _

class IUpfrontPageTrackerLayer(Interface):
    """ Marker interface for upfront.pagetracker """

class IPageTracker(Interface):
    """ A utility used to track the detailed use of a site
    """
