from zope.interface import Interface
from zope import schema

from collective.portlet.mailplus import PloneMessageFactory as _
from plone.app.textfield import RichText
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Weekday portlet" this interface must be its layer
    """

class IMailplus(Interface):
    """
    This interface defines the mailplus html record on the registry
    """
    
    mailplus_html = schema.Text(
        title=_(u"mailplus_html", default=u"Mailplus HTML"),
        description=_(u"mailplus_html_description", default=u"Paste here the integration HTML provided by Mailplus"),
        required=True)
    

    