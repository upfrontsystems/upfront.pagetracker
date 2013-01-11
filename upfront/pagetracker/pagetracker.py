from BTrees import IOBTree
from persistent import Persistent
from zope.interface import implements
from zope.interface import Interface

from upfront.pagetracker.interfaces import IPageTracker

class PageTracker(Persistent):
    """ Utility used to track detailed use of a site
    """
    implements(IPageTracker)
    
    def log(self):
            
        return 'nothing here yet'
      

