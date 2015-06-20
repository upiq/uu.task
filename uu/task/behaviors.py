from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import alsoProvides 


class IUUAssignedTask(model.Schema):
    """Adds due date field"""

    due_on = schema.Datetime(title=u"Due Date")


alsoProvides(IUUAssignedTask, IFormFieldProvider)
