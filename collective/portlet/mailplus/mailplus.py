import random

from AccessControl import getSecurityManager

from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue

from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFCore.utils import getToolByName
from datetime import date
from DateTime import DateTime
import time

from collective.portlet.mailplus import PloneMessageFactory as _

from Acquisition import aq_inner
from collective.portlet.mailplus.interfaces import IMailplus
from z3c.form import form, field, button, group
from plone.app.z3cform.layout import wrap_form
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.utils import getFSVersionTuple

PLONE5 = getFSVersionTuple()[0] >= 5

if PLONE5:
    base_AddForm = base.AddForm
    base_EditForm = base.EditForm
else:
    from plone.app.portlets.browser.z3cformhelper import AddForm as base_AddForm  # noqa
    from plone.app.portlets.browser.z3cformhelper import EditForm as base_EditForm  # noqa
    from z3c.form import field

class IMailplusPortlet(IPortletDataProvider):
    """A portlet that renders Mailplus integration HTML.
    """
    header = = schema.TextLine(
        title=_(u"Title", default=u"Title"),
        description=_(u"portlet_title", default=u"Title of the portlet."),
        required=False

    mailplus_html = schema.Text(
        title=_(u"mailplus_html", default=u"Mailplus HTML"),
        description=_(u"mailplus_html_description", default=u"Paste here the integration HTML provided by Mailplus"),
        required=True)

class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IMailplusPortlet)
    
    header = u''
    mailplus_html = u'' 
    
    def __init__(self, header = u'', mailplus_html = u''):
        self.header = header
        self.mailplus_html = mailplus_html
        
        
    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave or
        static string if title not defined.
        """
        return self.header or _(u'mailplus_header', default=u"Mailplus Portlet")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('mailplus.pt')
    render = _template

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return True
    
    def css_class(self):
        return "portlet-mailplus"
    
    def getTitle(self):
        if self.data.header:
            return self.data.header
        else:
            return _(u"mailplus_title", default=u"Mailplus Portlet")
    
    def render_mailplus(self):
        return self.transformed(self.data.mailplus_html)
        
    def transformed(self, text, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
            ensures that resolve UID links are transformed into real links.
        """
        orig = text
        context = aq_inner(self.context)
        if isinstance(orig, RichTextValue):
            orig = orig.raw

        if not isinstance(orig, unicode):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = unicode(orig, 'utf-8', 'ignore')
            logger.warn("Static portlet at %s has stored non-unicode text. "
                "Assuming utf-8 encoding." % context.absolute_url())

        orig = orig.encode('utf-8')
        result = orig
        
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
        return None

class AddForm(base_AddForm):   
    if PLONE5:
        schema = IMailplusPortlet
    else:
        fields = field.Fields(IMailplusPortlet)

    label = _(u"Add mailplus portlet")
    description = _(u"This portlet renders the integration HTML from Mailplus.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base_EditForm):
    #form_fields = form.Fields(IWeekDayPortlet)

    if PLONE5:
        schema = IMailplusPortlet
    else:
        fields = field.Fields(IMailplusPortlet)

    label = _(u"Add mailplus portlet")
    description = _(u"This portlet renders the integration HTML from Mailplus.")

